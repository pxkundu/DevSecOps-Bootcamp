"""
MLOps Model Serving API

FastAPI application for serving ML models with comprehensive monitoring,
logging, and production-ready features.
"""

import logging
import time
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any

import mlflow
import mlflow.sklearn
import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from prometheus_client import Counter, Histogram, Gauge, generate_latest
from starlette.responses import Response
import redis
import psycopg2
from sqlalchemy import create_engine
import joblib
import pickle

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Prometheus metrics
PREDICTION_REQUESTS = Counter('model_prediction_requests_total', 'Total prediction requests', ['model_name', 'version'])
PREDICTION_LATENCY = Histogram('model_prediction_duration_seconds', 'Prediction latency', ['model_name', 'version'])
PREDICTION_ERRORS = Counter('model_prediction_errors_total', 'Total prediction errors', ['model_name', 'version', 'error_type'])
ACTIVE_MODELS = Gauge('active_models_count', 'Number of active models')
MODEL_ACCURACY = Gauge('model_accuracy', 'Model accuracy', ['model_name', 'version'])

# FastAPI app
app = FastAPI(
    title="MLOps Model Serving API",
    description="Production-ready ML model serving with monitoring and observability",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for model management
loaded_models = {}
model_metadata = {}


class PredictionRequest(BaseModel):
    """Request model for predictions."""
    features: Dict[str, Any] = Field(..., description="Feature values for prediction")
    model_name: Optional[str] = Field("churn-prediction", description="Model name to use")
    model_version: Optional[str] = Field("latest", description="Model version to use")
    request_id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique request ID")


class PredictionResponse(BaseModel):
    """Response model for predictions."""
    prediction: float = Field(..., description="Model prediction")
    prediction_proba: List[float] = Field(..., description="Prediction probabilities")
    confidence: float = Field(..., description="Prediction confidence")
    model_name: str = Field(..., description="Model name used")
    model_version: str = Field(..., description="Model version used")
    request_id: str = Field(..., description="Request ID")
    timestamp: str = Field(..., description="Prediction timestamp")
    latency_ms: float = Field(..., description="Prediction latency in milliseconds")


class BatchPredictionRequest(BaseModel):
    """Request model for batch predictions."""
    features: List[Dict[str, Any]] = Field(..., description="List of feature dictionaries")
    model_name: Optional[str] = Field("churn-prediction", description="Model name to use")
    model_version: Optional[str] = Field("latest", description="Model version to use")


class BatchPredictionResponse(BaseModel):
    """Response model for batch predictions."""
    predictions: List[PredictionResponse] = Field(..., description="List of predictions")
    batch_size: int = Field(..., description="Number of predictions in batch")
    total_latency_ms: float = Field(..., description="Total batch processing time")


class HealthResponse(BaseModel):
    """Health check response model."""
    status: str = Field(..., description="Service status")
    timestamp: str = Field(..., description="Health check timestamp")
    version: str = Field(..., description="API version")
    models_loaded: int = Field(..., description="Number of loaded models")
    uptime_seconds: float = Field(..., description="Service uptime in seconds")


class ModelInfo(BaseModel):
    """Model information response model."""
    model_name: str = Field(..., description="Model name")
    version: str = Field(..., description="Model version")
    loaded_at: str = Field(..., description="Model load timestamp")
    metrics: Dict[str, float] = Field(..., description="Model performance metrics")
    status: str = Field(..., description="Model status")


# Startup time for uptime calculation
startup_time = time.time()


class ModelManager:
    """Manages model loading, caching, and metadata."""
    
    def __init__(self):
        self.mlflow_client = mlflow.tracking.MlflowClient()
        self.redis_client = self._get_redis_client()
        self.db_engine = self._get_db_engine()
    
    def _get_redis_client(self) -> Optional[redis.Redis]:
        """Get Redis client for caching."""
        try:
            return redis.Redis(host='redis', port=6379, decode_responses=True)
        except Exception as e:
            logger.warning(f"Could not connect to Redis: {e}")
            return None
    
    def _get_db_engine(self):
        """Get database engine for logging."""
        try:
            return create_engine('postgresql://mlops:mlops123@postgres:5432/mlops')
        except Exception as e:
            logger.warning(f"Could not connect to database: {e}")
            return None
    
    def load_model(self, model_name: str, version: str = "latest") -> Dict[str, Any]:
        """Load model from MLflow registry."""
        try:
            # Get model from MLflow
            if version == "latest":
                model_version = self.mlflow_client.get_latest_versions(model_name, stages=["Production"])
                if not model_version:
                    model_version = self.mlflow_client.get_latest_versions(model_name, stages=["Staging"])
                if not model_version:
                    model_version = self.mlflow_client.get_latest_versions(model_name)
                
                if model_version:
                    version = model_version[0].version
                else:
                    raise ValueError(f"No versions found for model {model_name}")
            
            model_uri = f"models:/{model_name}/{version}"
            model = mlflow.sklearn.load_model(model_uri)
            
            # Load preprocessing artifacts if available
            try:
                run_id = self.mlflow_client.get_model_version(model_name, version).run_id
                preprocessing_path = f"runs:/{run_id}/preprocessing.pkl"
                # In a real scenario, you'd download and load the preprocessing artifacts
                preprocessing = None
            except:
                preprocessing = None
            
            # Get model metadata
            model_version_info = self.mlflow_client.get_model_version(model_name, version)
            
            model_info = {
                'model': model,
                'preprocessing': preprocessing,
                'metadata': {
                    'name': model_name,
                    'version': version,
                    'stage': model_version_info.current_stage,
                    'loaded_at': datetime.now().isoformat(),
                    'run_id': model_version_info.run_id
                }
            }
            
            # Cache model info
            model_key = f"{model_name}:{version}"
            loaded_models[model_key] = model_info
            model_metadata[model_key] = model_info['metadata']
            
            logger.info(f"Loaded model {model_name} version {version}")
            ACTIVE_MODELS.set(len(loaded_models))
            
            return model_info
            
        except Exception as e:
            logger.error(f"Error loading model {model_name} version {version}: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to load model: {str(e)}")
    
    def get_model(self, model_name: str, version: str = "latest") -> Dict[str, Any]:
        """Get model, loading if necessary."""
        model_key = f"{model_name}:{version}"
        
        if model_key not in loaded_models:
            return self.load_model(model_name, version)
        
        return loaded_models[model_key]
    
    def log_prediction(self, request: PredictionRequest, response: PredictionResponse):
        """Log prediction for monitoring and retraining."""
        if self.db_engine is None:
            return
        
        try:
            log_data = {
                'request_id': response.request_id,
                'model_name': response.model_name,
                'model_version': response.model_version,
                'features': str(request.features),
                'prediction': response.prediction,
                'confidence': response.confidence,
                'timestamp': response.timestamp,
                'latency_ms': response.latency_ms
            }
            
            # In a real implementation, you'd insert this into a proper table
            logger.info(f"Logged prediction: {log_data}")
            
        except Exception as e:
            logger.error(f"Error logging prediction: {e}")


# Initialize model manager
model_manager = ModelManager()


def get_model_manager() -> ModelManager:
    """Dependency to get model manager."""
    return model_manager


@app.on_event("startup")
async def startup_event():
    """Load default models on startup."""
    try:
        # Load default churn prediction model
        model_manager.load_model("churn-prediction-model-random_forest", "latest")
        logger.info("Default models loaded successfully")
    except Exception as e:
        logger.warning(f"Could not load default models: {e}")


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        version="1.0.0",
        models_loaded=len(loaded_models),
        uptime_seconds=time.time() - startup_time
    )


@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint."""
    return Response(generate_latest(), media_type="text/plain")


@app.get("/models", response_model=List[ModelInfo])
async def list_models():
    """List all loaded models."""
    return [
        ModelInfo(
            model_name=metadata['name'],
            version=metadata['version'],
            loaded_at=metadata['loaded_at'],
            metrics={},  # Would load actual metrics from MLflow
            status="active"
        )
        for metadata in model_metadata.values()
    ]


@app.post("/models/{model_name}/load")
async def load_model_endpoint(model_name: str, version: str = "latest"):
    """Load a specific model version."""
    try:
        model_info = model_manager.load_model(model_name, version)
        return {
            "message": f"Model {model_name} version {version} loaded successfully",
            "metadata": model_info['metadata']
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/predict", response_model=PredictionResponse)
async def predict(
    request: PredictionRequest,
    background_tasks: BackgroundTasks,
    manager: ModelManager = Depends(get_model_manager)
):
    """Make a single prediction."""
    start_time = time.time()
    
    try:
        # Get model
        model_info = manager.get_model(request.model_name, request.model_version)
        model = model_info['model']
        metadata = model_info['metadata']
        
        # Increment request counter
        PREDICTION_REQUESTS.labels(
            model_name=metadata['name'],
            version=metadata['version']
        ).inc()
        
        # Prepare features
        # In a real implementation, you'd apply the same preprocessing as training
        features_df = pd.DataFrame([request.features])
        
        # Make prediction
        prediction = model.predict(features_df)[0]
        prediction_proba = model.predict_proba(features_df)[0].tolist()
        confidence = max(prediction_proba)
        
        # Calculate latency
        latency_ms = (time.time() - start_time) * 1000
        
        # Record latency
        PREDICTION_LATENCY.labels(
            model_name=metadata['name'],
            version=metadata['version']
        ).observe(latency_ms / 1000)
        
        # Create response
        response = PredictionResponse(
            prediction=float(prediction),
            prediction_proba=prediction_proba,
            confidence=confidence,
            model_name=metadata['name'],
            model_version=metadata['version'],
            request_id=request.request_id,
            timestamp=datetime.now().isoformat(),
            latency_ms=latency_ms
        )
        
        # Log prediction in background
        background_tasks.add_task(manager.log_prediction, request, response)
        
        return response
        
    except Exception as e:
        # Record error
        PREDICTION_ERRORS.labels(
            model_name=request.model_name,
            version=request.model_version,
            error_type=type(e).__name__
        ).inc()
        
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@app.post("/predict/batch", response_model=BatchPredictionResponse)
async def predict_batch(
    request: BatchPredictionRequest,
    background_tasks: BackgroundTasks,
    manager: ModelManager = Depends(get_model_manager)
):
    """Make batch predictions."""
    start_time = time.time()
    
    try:
        # Get model
        model_info = manager.get_model(request.model_name, request.model_version)
        model = model_info['model']
        metadata = model_info['metadata']
        
        # Prepare features
        features_df = pd.DataFrame(request.features)
        
        # Make predictions
        predictions = model.predict(features_df)
        predictions_proba = model.predict_proba(features_df)
        
        # Create individual responses
        prediction_responses = []
        for i, (pred, proba) in enumerate(zip(predictions, predictions_proba)):
            pred_response = PredictionResponse(
                prediction=float(pred),
                prediction_proba=proba.tolist(),
                confidence=max(proba),
                model_name=metadata['name'],
                model_version=metadata['version'],
                request_id=str(uuid.uuid4()),
                timestamp=datetime.now().isoformat(),
                latency_ms=(time.time() - start_time) * 1000
            )
            prediction_responses.append(pred_response)
        
        total_latency_ms = (time.time() - start_time) * 1000
        
        # Record metrics
        PREDICTION_REQUESTS.labels(
            model_name=metadata['name'],
            version=metadata['version']
        ).inc(len(request.features))
        
        return BatchPredictionResponse(
            predictions=prediction_responses,
            batch_size=len(request.features),
            total_latency_ms=total_latency_ms
        )
        
    except Exception as e:
        logger.error(f"Batch prediction error: {e}")
        raise HTTPException(status_code=500, detail=f"Batch prediction failed: {str(e)}")


@app.get("/models/{model_name}/info")
async def get_model_info(model_name: str, version: str = "latest"):
    """Get detailed information about a specific model."""
    try:
        model_key = f"{model_name}:{version}"
        if model_key not in model_metadata:
            raise HTTPException(status_code=404, detail="Model not found")
        
        metadata = model_metadata[model_key]
        
        # Get additional info from MLflow
        try:
            run_info = model_manager.mlflow_client.get_run(metadata['run_id'])
            metrics = run_info.data.metrics
        except:
            metrics = {}
        
        return {
            "model_name": metadata['name'],
            "version": metadata['version'],
            "stage": metadata['stage'],
            "loaded_at": metadata['loaded_at'],
            "run_id": metadata['run_id'],
            "metrics": metrics,
            "status": "active"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/models/{model_name}/feedback")
async def submit_feedback(
    model_name: str,
    feedback_data: Dict[str, Any],
    version: str = "latest"
):
    """Submit feedback for model improvement."""
    try:
        # Log feedback for model monitoring and retraining
        feedback_log = {
            "model_name": model_name,
            "version": version,
            "feedback": feedback_data,
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info(f"Received feedback: {feedback_log}")
        
        # In a real implementation, you'd store this in a database
        # and use it for model retraining triggers
        
        return {"message": "Feedback received successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to submit feedback: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
