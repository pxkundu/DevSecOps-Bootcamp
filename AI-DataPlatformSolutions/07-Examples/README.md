# Implementation Examples

## Overview
This section provides practical implementation examples through real-world case studies, comprehensive code samples, and deployment scripts for enterprise AI platforms.

## 1. **Real-World Case Studies**

### 1. **E-commerce Recommendation System**
```mermaid
graph TB
    subgraph "E-commerce Recommendation System"
        A[User Behavior Data] --> B[Data Processing Pipeline]
        B --> C[Feature Engineering]
        C --> D[ML Model Training]
        D --> E[Model Deployment]
        E --> F[Real-time Recommendations]
        
        G[User Interactions] --> A
        H[Product Catalog] --> C
        I[Performance Monitoring] --> F
    end
```

### 2. **Financial Fraud Detection System**
```mermaid
graph LR
    subgraph "Fraud Detection System"
        A[Transaction Data] --> B[Real-time Processing]
        B --> C[Feature Extraction]
        C --> D[ML Model Inference]
        D --> E[Fraud Alert System]
        
        F[Historical Data] --> G[Model Training]
        G --> H[Model Updates]
        H --> D
    end
```

## 2. **Complete ML Training Pipeline**

### **Scikit-learn ML Training Pipeline**
```python
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
import joblib
import mlflow
import logging
from datetime import datetime
import os

class MLTrainingPipeline:
    def __init__(self, config):
        self.config = config
        self.model = None
        self.scaler = StandardScaler()
        self.logger = self._setup_logging()
        
        # Set MLflow experiment
        mlflow.set_experiment(config.get('experiment_name', 'default'))
    
    def _setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        return logging.getLogger(__name__)
    
    def load_data(self, data_path):
        """Load data from various sources"""
        self.logger.info(f"Loading data from: {data_path}")
        
        if data_path.endswith('.csv'):
            data = pd.read_csv(data_path)
        elif data_path.endswith('.parquet'):
            data = pd.read_parquet(data_path)
        elif data_path.endswith('.json'):
            data = pd.read_json(data_path)
        else:
            raise ValueError(f"Unsupported file format: {data_path}")
        
        self.logger.info(f"Loaded {len(data)} rows and {len(data.columns)} columns")
        return data
    
    def preprocess_data(self, data):
        """Preprocess data for ML training"""
        self.logger.info("Starting data preprocessing")
        
        # Handle missing values
        data = self._handle_missing_values(data)
        
        # Handle categorical variables
        data = self._encode_categorical_variables(data)
        
        # Feature scaling
        if self.config.get('scale_features', True):
            numeric_columns = data.select_dtypes(include=[np.number]).columns
            data[numeric_columns] = self.scaler.fit_transform(data[numeric_columns])
        
        self.logger.info("Data preprocessing completed")
        return data
    
    def _handle_missing_values(self, data):
        """Handle missing values in the dataset"""
        missing_counts = data.isnull().sum()
        
        if missing_counts.sum() > 0:
            self.logger.info(f"Missing values found: {missing_counts[missing_counts > 0]}")
            
            # Strategy: fill numeric with median, categorical with mode
            for column in data.columns:
                if data[column].dtype in ['int64', 'float64']:
                    data[column].fillna(data[column].median(), inplace=True)
                else:
                    data[column].fillna(data[column].mode()[0], inplace=True)
        
        return data
    
    def _encode_categorical_variables(self, data):
        """Encode categorical variables"""
        categorical_columns = data.select_dtypes(include=['object']).columns
        
        for column in categorical_columns:
            if data[column].nunique() < 10:  # Low cardinality
                data[column] = data[column].astype('category').cat.codes
            else:  # High cardinality - use one-hot encoding
                data = pd.get_dummies(data, columns=[column], prefix=column)
        
        return data
    
    def split_data(self, data, target_column, test_size=0.2, random_state=42):
        """Split data into training and testing sets"""
        self.logger.info(f"Splitting data with test size: {test_size}")
        
        X = data.drop(columns=[target_column])
        y = data[target_column]
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
        
        self.logger.info(f"Training set: {X_train.shape}, Test set: {X_test.shape}")
        
        return X_train, X_test, y_train, y_test
    
    def train_model(self, X_train, y_train):
        """Train the ML model"""
        self.logger.info("Starting model training")
        
        # Initialize model
        model_params = self.config.get('model_params', {})
        self.model = RandomForestClassifier(**model_params)
        
        # Cross-validation
        cv_scores = cross_val_score(self.model, X_train, y_train, cv=5)
        self.logger.info(f"Cross-validation scores: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
        
        # Train final model
        self.model.fit(X_train, y_train)
        
        self.logger.info("Model training completed")
        return self.model
    
    def evaluate_model(self, X_test, y_test):
        """Evaluate model performance"""
        if self.model is None:
            raise ValueError("Model not trained yet")
        
        self.logger.info("Evaluating model performance")
        
        # Make predictions
        y_pred = self.model.predict(X_test)
        y_pred_proba = self.model.predict_proba(X_test)
        
        # Calculate metrics
        from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
        
        metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred, average='weighted'),
            'recall': recall_score(y_test, y_pred, average='weighted'),
            'f1_score': f1_score(y_test, y_pred, average='weighted'),
            'roc_auc': roc_auc_score(y_test, y_pred_proba[:, 1]) if len(np.unique(y_test)) == 2 else None
        }
        
        # Log metrics
        for metric_name, metric_value in metrics.items():
            if metric_value is not None:
                self.logger.info(f"{metric_name}: {metric_value:.4f}")
        
        # Generate detailed report
        report = classification_report(y_test, y_pred, output_dict=True)
        
        return {
            'metrics': metrics,
            'classification_report': report,
            'predictions': y_pred,
            'probabilities': y_pred_proba
        }
    
    def save_model(self, output_path):
        """Save the trained model and artifacts"""
        if self.model is None:
            raise ValueError("Model not trained yet")
        
        self.logger.info(f"Saving model to: {output_path}")
        
        # Create output directory
        os.makedirs(output_path, exist_ok=True)
        
        # Save model
        model_path = os.path.join(output_path, 'model.pkl')
        joblib.dump(self.model, model_path)
        
        # Save scaler
        scaler_path = os.path.join(output_path, 'scaler.pkl')
        joblib.dump(self.scaler, scaler_path)
        
        # Save model metadata
        metadata = {
            'model_type': type(self.model).__name__,
            'training_date': datetime.now().isoformat(),
            'config': self.config,
            'feature_names': list(self.model.feature_names_in_) if hasattr(self.model, 'feature_names_in_') else None
        }
        
        metadata_path = os.path.join(output_path, 'metadata.json')
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        self.logger.info(f"Model saved successfully to {output_path}")
        
        return {
            'model_path': model_path,
            'scaler_path': scaler_path,
            'metadata_path': metadata_path
        }
    
    def run_pipeline(self, data_path, target_column, output_path):
        """Run the complete ML training pipeline"""
        self.logger.info("Starting ML training pipeline")
        
        try:
            # Load data
            data = self.load_data(data_path)
            
            # Preprocess data
            processed_data = self.preprocess_data(data)
            
            # Split data
            X_train, X_test, y_train, y_test = self.split_data(
                processed_data, target_column
            )
            
            # Train model
            self.train_model(X_train, y_train)
            
            # Evaluate model
            evaluation_results = self.evaluate_model(X_test, y_test)
            
            # Save model
            model_artifacts = self.save_model(output_path)
            
            # Log to MLflow
            with mlflow.start_run():
                mlflow.log_params(self.config.get('model_params', {}))
                mlflow.log_metrics(evaluation_results['metrics'])
                mlflow.sklearn.log_model(self.model, "model")
                mlflow.log_artifact(output_path)
            
            self.logger.info("ML training pipeline completed successfully")
            
            return {
                'model': self.model,
                'evaluation_results': evaluation_results,
                'model_artifacts': model_artifacts
            }
            
        except Exception as e:
            self.logger.error(f"Pipeline failed: {str(e)}")
            raise

# Configuration
config = {
    'experiment_name': 'customer_churn_prediction',
    'scale_features': True,
    'model_params': {
        'n_estimators': 100,
        'max_depth': 10,
        'random_state': 42,
        'n_jobs': -1
    }
}

# Initialize and run pipeline
pipeline = MLTrainingPipeline(config)

results = pipeline.run_pipeline(
    data_path='data/customer_data.csv',
    target_column='churn',
    output_path='models/churn_model'
)

print(f"Model accuracy: {results['evaluation_results']['metrics']['accuracy']:.4f}")
```

## 3. **FastAPI ML Model Service**

### **Complete FastAPI Service for ML Model Serving**
```python
from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from pydantic import BaseModel, Field, validator
import joblib
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import logging
import json
import os
from typing import List, Optional, Dict, Any
import uvicorn
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import redis
import asyncio

# Pydantic models for request/response
class PredictionRequest(BaseModel):
    features: List[float] = Field(..., description="Model features")
    request_id: Optional[str] = Field(None, description="Unique request identifier")
    
    @validator('features')
    def validate_features(cls, v):
        if len(v) == 0:
            raise ValueError('Features list cannot be empty')
        return v

class PredictionResponse(BaseModel):
    prediction: float
    probability: Optional[float] = None
    request_id: str
    timestamp: str
    model_version: str
    processing_time_ms: float

class BatchPredictionRequest(BaseModel):
    requests: List[PredictionRequest] = Field(..., max_items=1000)
    
    @validator('requests')
    def validate_batch_size(cls, v):
        if len(v) > 1000:
            raise ValueError('Batch size cannot exceed 1000 requests')
        return v

class BatchPredictionResponse(BaseModel):
    predictions: List[Dict[str, Any]]
    total_requests: int
    successful_requests: int
    failed_requests: int
    processing_time_ms: float

class ModelHealthResponse(BaseModel):
    status: str
    model_version: str
    last_updated: str
    uptime_seconds: float
    total_predictions: int
    average_response_time_ms: float

# Prometheus metrics
PREDICTION_COUNTER = Counter('ml_predictions_total', 'Total predictions made')
PREDICTION_ERROR_COUNTER = Counter('ml_prediction_errors_total', 'Total prediction errors')
PREDICTION_LATENCY = Histogram('ml_prediction_latency_seconds', 'Prediction latency in seconds')
BATCH_PREDICTION_COUNTER = Counter('ml_batch_predictions_total', 'Total batch predictions made')

class MLModelService:
    def __init__(self, model_path: str, scaler_path: str, metadata_path: str):
        self.model_path = model_path
        self.scaler_path = scaler_path
        self.metadata_path = metadata_path
        
        self.model = None
        self.scaler = None
        self.metadata = {}
        self.start_time = datetime.now()
        self.total_predictions = 0
        self.response_times = []
        
        self.logger = self._setup_logging()
        self.redis_client = self._setup_redis()
        
        # Load model
        self.load_model()
    
    def _setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        return logging.getLogger(__name__)
    
    def _setup_redis(self):
        """Setup Redis connection for caching"""
        try:
            redis_client = redis.Redis(
                host=os.getenv('REDIS_HOST', 'localhost'),
                port=int(os.getenv('REDIS_PORT', 6379)),
                db=int(os.getenv('REDIS_DB', 0)),
                decode_responses=True
            )
            redis_client.ping()
            self.logger.info("Redis connection established")
            return redis_client
        except Exception as e:
            self.logger.warning(f"Redis connection failed: {e}")
            return None
    
    def load_model(self):
        """Load the trained ML model and artifacts"""
        try:
            self.logger.info("Loading ML model and artifacts")
            
            # Load model
            self.model = joblib.load(self.model_path)
            
            # Load scaler
            if os.path.exists(self.scaler_path):
                self.scaler = joblib.load(self.scaler_path)
            
            # Load metadata
            if os.path.exists(self.metadata_path):
                with open(self.metadata_path, 'r') as f:
                    self.metadata = json.load(f)
            
            self.logger.info("Model loaded successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to load model: {e}")
            raise
    
    def preprocess_features(self, features: List[float]) -> np.ndarray:
        """Preprocess input features"""
        # Convert to numpy array
        features_array = np.array(features).reshape(1, -1)
        
        # Apply scaling if scaler is available
        if self.scaler is not None:
            features_array = self.scaler.transform(features_array)
        
        return features_array
    
    def predict(self, features: List[float]) -> Dict[str, Any]:
        """Make a single prediction"""
        start_time = datetime.now()
        
        try:
            # Preprocess features
            processed_features = self.preprocess_features(features)
            
            # Make prediction
            prediction = self.model.predict(processed_features)[0]
            
            # Get probability if available
            probability = None
            if hasattr(self.model, 'predict_proba'):
                proba = self.model.predict_proba(processed_features)[0]
                probability = float(np.max(proba))
            
            # Calculate processing time
            processing_time = (datetime.now() - start_time).total_seconds() * 1000
            
            # Update metrics
            self.total_predictions += 1
            self.response_times.append(processing_time)
            
            # Update Prometheus metrics
            PREDICTION_COUNTER.inc()
            PREDICTION_LATENCY.observe(processing_time / 1000)
            
            return {
                'prediction': float(prediction),
                'probability': probability,
                'processing_time_ms': processing_time
            }
            
        except Exception as e:
            self.logger.error(f"Prediction failed: {e}")
            PREDICTION_ERROR_COUNTER.inc()
            raise
    
    def predict_batch(self, requests: List[PredictionRequest]) -> List[Dict[str, Any]]:
        """Make batch predictions"""
        start_time = datetime.now()
        
        try:
            results = []
            
            for request in requests:
                try:
                    # Check cache first
                    cache_key = f"prediction:{hash(tuple(request.features))}"
                    cached_result = None
                    
                    if self.redis_client:
                        cached_result = self.redis_client.get(cache_key)
                        if cached_result:
                            cached_result = json.loads(cached_result)
                            results.append(cached_result)
                            continue
                    
                    # Make prediction
                    prediction_result = self.predict(request.features)
                    
                    # Add request metadata
                    result = {
                        'request_id': request.request_id or f"req_{len(results)}",
                        'prediction': prediction_result['prediction'],
                        'probability': prediction_result['probability'],
                        'processing_time_ms': prediction_result['processing_time_ms'],
                        'status': 'success'
                    }
                    
                    # Cache result
                    if self.redis_client:
                        self.redis_client.setex(
                            cache_key, 
                            3600,  # 1 hour TTL
                            json.dumps(result)
                        )
                    
                    results.append(result)
                    
                except Exception as e:
                    # Handle individual request failure
                    result = {
                        'request_id': request.request_id or f"req_{len(results)}",
                        'error': str(e),
                        'status': 'failed'
                    }
                    results.append(result)
            
            # Update batch metrics
            BATCH_PREDICTION_COUNTER.inc()
            
            return results
            
        except Exception as e:
            self.logger.error(f"Batch prediction failed: {e}")
            raise
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get service health status"""
        uptime = (datetime.now() - self.start_time).total_seconds()
        
        avg_response_time = np.mean(self.response_times) if self.response_times else 0
        
        return {
            'status': 'healthy' if self.model is not None else 'unhealthy',
            'model_version': self.metadata.get('model_type', 'unknown'),
            'last_updated': self.metadata.get('training_date', 'unknown'),
            'uptime_seconds': uptime,
            'total_predictions': self.total_predictions,
            'average_response_time_ms': avg_response_time
        }

# Initialize FastAPI app
app = FastAPI(
    title="ML Model API",
    description="API for serving machine learning models",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]
)

# Initialize model service
model_service = MLModelService(
    model_path="models/model.pkl",
    scaler_path="models/scaler.pkl",
    metadata_path="models/metadata.json"
)

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    logging.info("Starting ML Model API")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logging.info("Shutting down ML Model API")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "ML Model API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    health_status = model_service.get_health_status()
    return ModelHealthResponse(**health_status)

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """Make a single prediction"""
    try:
        # Generate request ID if not provided
        if not request.request_id:
            request.request_id = f"req_{datetime.now().timestamp()}"
        
        # Make prediction
        prediction_result = model_service.predict(request.features)
        
        return PredictionResponse(
            prediction=prediction_result['prediction'],
            probability=prediction_result['probability'],
            request_id=request.request_id,
            timestamp=datetime.now().isoformat(),
            model_version=model_service.metadata.get('model_type', 'unknown'),
            processing_time_ms=prediction_result['processing_time_ms']
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict/batch", response_model=BatchPredictionResponse)
async def predict_batch(request: BatchPredictionRequest):
    """Make batch predictions"""
    try:
        start_time = datetime.now()
        
        # Make batch predictions
        predictions = model_service.predict_batch(request.requests)
        
        # Calculate processing time
        processing_time = (datetime.now() - start_time).total_seconds() * 1000
        
        # Count successful and failed requests
        successful = sum(1 for p in predictions if p['status'] == 'success')
        failed = len(predictions) - successful
        
        return BatchPredictionResponse(
            predictions=predictions,
            total_requests=len(predictions),
            successful_requests=successful,
            failed_requests=failed,
            processing_time_ms=processing_time
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    return generate_latest()

@app.get("/model/info")
async def model_info():
    """Get model information"""
    return {
        'model_type': model_service.metadata.get('model_type', 'unknown'),
        'training_date': model_service.metadata.get('training_date', 'unknown'),
        'config': model_service.metadata.get('config', {}),
        'feature_names': model_service.metadata.get('feature_names', [])
    }

@app.post("/model/reload")
async def reload_model():
    """Reload the model from disk"""
    try:
        model_service.load_model()
        return {"message": "Model reloaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to reload model: {e}")

# Background task for model monitoring
async def monitor_model_performance():
    """Background task to monitor model performance"""
    while True:
        try:
            health_status = model_service.get_health_status()
            
            # Log performance metrics
            logging.info(f"Model performance - Total predictions: {health_status['total_predictions']}, "
                        f"Avg response time: {health_status['average_response_time_ms']:.2f}ms")
            
            # Check for performance degradation
            if health_status['average_response_time_ms'] > 1000:  # 1 second threshold
                logging.warning("Model performance degradation detected")
            
            await asyncio.sleep(60)  # Check every minute
            
        except Exception as e:
            logging.error(f"Model monitoring failed: {e}")
            await asyncio.sleep(60)

# Start monitoring task
@app.on_event("startup")
async def start_monitoring():
    """Start background monitoring task"""
    asyncio.create_task(monitor_model_performance())

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
```

## 4. **Kubernetes Deployment for ML Platform**

### **Complete Kubernetes Deployment Configuration**
```yaml
# ml-platform-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ml-platform
  labels:
    app: ml-platform
    version: v1.0.0
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: ml-platform
  template:
    metadata:
      labels:
        app: ml-platform
        version: v1.0.0
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "8000"
        prometheus.io/path: "/metrics"
    spec:
      serviceAccountName: ml-platform-sa
      containers:
      - name: ml-platform
        image: ml-platform:latest
        imagePullPolicy: Always
        ports:
        - containerPort: 8000
          name: http
        - containerPort: 8001
          name: metrics
        env:
        - name: MODEL_PATH
          value: "/app/models"
        - name: LOG_LEVEL
          value: "INFO"
        - name: REDIS_HOST
          value: "redis-service"
        - name: REDIS_PORT
          value: "6379"
        - name: REDIS_DB
          value: "0"
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
        volumeMounts:
        - name: model-storage
          mountPath: /app/models
          readOnly: true
        - name: config-volume
          mountPath: /app/config
          readOnly: true
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 3
        securityContext:
          runAsNonRoot: true
          runAsUser: 1000
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          capabilities:
            drop:
            - ALL
      volumes:
      - name: model-storage
        persistentVolumeClaim:
          claimName: ml-models-pvc
      - name: config-volume
        configMap:
          name: ml-platform-config
      - name: tmp-volume
        emptyDir: {}
      initContainers:
      - name: model-downloader
        image: busybox:1.35
        command: ['sh', '-c']
        args:
        - |
          echo "Downloading model artifacts..."
          # Download model from S3 or other storage
          # This is a placeholder for actual download logic
          echo "Model download completed"
        volumeMounts:
        - name: model-storage
          mountPath: /models
        - name: tmp-volume
          mountPath: /tmp
      securityContext:
        fsGroup: 1000
        runAsNonRoot: true
        runAsUser: 1000
---
apiVersion: v1
kind: Service
metadata:
  name: ml-platform-service
  labels:
    app: ml-platform
spec:
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 8000
    protocol: TCP
    name: http
  - port: 8001
    targetPort: 8001
    protocol: TCP
    name: metrics
  selector:
    app: ml-platform
  sessionAffinity: ClientIP
  sessionAffinityConfig:
    clientIP:
      timeoutSeconds: 10800
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: ml-models-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
  storageClassName: gp2
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: ml-platform-config
data:
  app.conf: |
    [app]
    name = ML Platform
    version = 1.0.0
    
    [model]
    path = /app/models
    cache_ttl = 3600
    
    [redis]
    host = redis-service
    port = 6379
    db = 0
    
    [monitoring]
    metrics_port = 8001
    health_check_interval = 30
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: ml-platform-sa
  labels:
    app: ml-platform
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: ml-platform-role
rules:
- apiGroups: [""]
  resources: ["pods", "services", "endpoints"]
  verbs: ["get", "list", "watch"]
- apiGroups: [""]
  resources: ["configmaps"]
  verbs: ["get"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: ml-platform-rolebinding
subjects:
- kind: ServiceAccount
  name: ml-platform-sa
  namespace: default
roleRef:
  kind: Role
  name: ml-platform-role
  apiGroup: rbac.authorization.k8s.io
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: ml-platform-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: ml-platform
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
      - type: Percent
        value: 100
        periodSeconds: 15
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 10
        periodSeconds: 60
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ml-platform-ingress
  annotations:
    kubernetes.io/ingress.class: "nginx"
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/force-ssl-redirect: "true"
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
spec:
  tls:
  - hosts:
    - ml-api.example.com
    secretName: ml-platform-tls
  rules:
  - host: ml-api.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: ml-platform-service
            port:
              number: 80
---
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: ml-platform-monitor
  labels:
    release: prometheus
spec:
  selector:
    matchLabels:
      app: ml-platform
  endpoints:
  - port: metrics
    interval: 15s
    path: /metrics
---
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: ml-platform-pdb
spec:
  minAvailable: 2
  selector:
    matchLabels:
      app: ml-platform
---
apiVersion: batch/v1
kind: CronJob
metadata:
  name: ml-model-updater
spec:
  schedule: "0 2 * * *"  # Daily at 2 AM
  jobTemplate:
    spec:
      template:
        spec:
          serviceAccountName: ml-platform-sa
          containers:
          - name: model-updater
            image: ml-model-updater:latest
            command: ["python", "/app/update_model.py"]
            env:
            - name: MODEL_SOURCE
              value: "s3://ml-models-bucket/latest/"
            - name: MODEL_DESTINATION
              value: "/models"
            volumeMounts:
            - name: model-storage
              mountPath: /models
          volumes:
          - name: model-storage
            persistentVolumeClaim:
              claimName: ml-models-pvc
          restartPolicy: OnFailure
```

## 5. **Docker Compose for Local Development**

### **Complete Docker Compose Setup**
```yaml
# docker-compose.yml
version: '3.8'

services:
  # ML Platform Service
  ml-platform:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
      - "8001:8001"
    environment:
      - MODEL_PATH=/app/models
      - LOG_LEVEL=DEBUG
      - REDIS_HOST=redis
      - REDIS_PORT=6379
      - REDIS_DB=0
    volumes:
      - ./models:/app/models:ro
      - ./config:/app/config:ro
      - ./logs:/app/logs
    depends_on:
      - redis
      - postgres
    networks:
      - ml-network
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: '1.0'
        reservations:
          memory: 1G
          cpus: '0.5'
    healthcheck:
      test: ["CMD", "curl", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  # Redis Cache
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
      - ./redis/redis.conf:/usr/local/etc/redis/redis.conf:ro
    command: redis-server /usr/local/etc/redis/redis.conf
    networks:
      - ml-network
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 3

  # PostgreSQL Database
  postgres:
    image: postgres:15-alpine
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_DB=ml_platform
      - POSTGRES_USER=ml_user
      - POSTGRES_PASSWORD=ml_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./postgres/init.sql:/docker-entrypoint-initdb.d/init.sql:ro
    networks:
      - ml-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ml_user -d ml_platform"]
      interval: 10s
      timeout: 5s
      retries: 3

  # MLflow Tracking Server
  mlflow:
    image: python:3.9-slim
    ports:
      - "5000:5000"
    environment:
      - MLFLOW_TRACKING_URI=http://localhost:5000
      - MLFLOW_S3_ENDPOINT_URL=http://minio:9000
      - AWS_ACCESS_KEY_ID=minioadmin
      - AWS_SECRET_ACCESS_KEY=minioadmin
    volumes:
      - ./mlflow:/mlflow
      - ./mlflow/start_server.sh:/start_server.sh:ro
    command: ["/start_server.sh"]
    depends_on:
      - postgres
      - minio
    networks:
      - ml-network

  # MinIO Object Storage
  minio:
    image: minio/minio:latest
    ports:
      - "9000:9000"
      - "9001:9001"
    environment:
      - MINIO_ROOT_USER=minioadmin
      - MINIO_ROOT_PASSWORD=minioadmin
    volumes:
      - minio_data:/data
    command: server /data --console-address ":9001"
    networks:
      - ml-network
    healthcheck:
      test: ["CMD", "curl", "http://localhost:9000/minio/health/live"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Prometheus Monitoring
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'
      - '--storage.tsdb.retention.time=200h'
      - '--web.enable-lifecycle'
    networks:
      - ml-network

  # Grafana Dashboard
  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
      - GF_USERS_ALLOW_SIGN_UP=false
    volumes:
      - grafana_data:/var/lib/grafana
      - ./grafana/provisioning:/etc/grafana/provisioning:ro
      - ./grafana/dashboards:/var/lib/grafana/dashboards:ro
    depends_on:
      - prometheus
    networks:
      - ml-network

  # Jupyter Notebook
  jupyter:
    image: jupyter/datascience-notebook:latest
    ports:
      - "8888:8888"
    environment:
      - JUPYTER_ENABLE_LAB=yes
      - JUPYTER_TOKEN=mlplatform
    volumes:
      - ./notebooks:/home/jovyan/work
      - ./data:/home/jovyan/data:ro
    networks:
      - ml-network
    command: start.sh jupyter lab --LabApp.token='mlplatform'

  # Airflow for Data Pipelines
  airflow-webserver:
    image: apache/airflow:2.7.1
    ports:
      - "8080:8080"
    environment:
      - AIRFLOW__CORE__EXECUTOR=LocalExecutor
      - AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgresql+psycopg2://ml_user:ml_password@postgres:5432/airflow
      - AIRFLOW__CORE__FERNET_KEY=your-fernet-key-here
      - AIRFLOW__CORE__DAGS_ARE_PAUSED_AT_CREATION=True
      - AIRFLOW__CORE__LOAD_EXAMPLES=False
    volumes:
      - ./airflow/dags:/opt/airflow/dags
      - ./airflow/logs:/opt/airflow/logs
      - ./airflow/plugins:/opt/airflow/plugins
    depends_on:
      - postgres
    networks:
      - ml-network
    command: webserver
    healthcheck:
      test: ["CMD", "curl", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Airflow Scheduler
  airflow-scheduler:
    image: apache/airflow:2.7.1
    environment:
      - AIRFLOW__CORE__EXECUTOR=LocalExecutor
      - AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgresql+psycopg2://ml_user:ml_password@postgres:5432/airflow
      - AIRFLOW__CORE__FERNET_KEY=your-fernet-key-here
    volumes:
      - ./airflow/dags:/opt/airflow/dags
      - ./airflow/logs:/opt/airflow/logs
      - ./airflow/plugins:/opt/airflow/plugins
    depends_on:
      - postgres
      - airflow-webserver
    networks:
      - ml-network
    command: scheduler

volumes:
  redis_data:
  postgres_data:
  minio_data:
  prometheus_data:
  grafana_data:

networks:
  ml-network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16
```

## 6. **Best Practices**

### **Implementation Guidelines**
1. **Modular Design**: Break down complex systems into manageable components
2. **Error Handling**: Implement comprehensive error handling and logging
3. **Monitoring**: Add monitoring and observability from the start
4. **Testing**: Include unit tests and integration tests
5. **Documentation**: Document code, APIs, and deployment procedures

### **Performance Optimization**
1. **Caching**: Implement caching strategies for frequently accessed data
2. **Batch Processing**: Use batch processing for large datasets
3. **Resource Management**: Optimize resource allocation and usage
4. **Scaling**: Design for horizontal scaling from the beginning

### **Security Considerations**
1. **Input Validation**: Validate all inputs and sanitize data
2. **Authentication**: Implement proper authentication and authorization
3. **Encryption**: Use encryption for data at rest and in transit
4. **Access Control**: Implement least privilege access controls

---

**Next Section**: [Best Practices & Standards](../08-BestPractices/README.md)
