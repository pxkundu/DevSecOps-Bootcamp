#!/usr/bin/env python3
"""
MLOps Platform Initialization Script

This script initializes the MLOps platform by setting up databases,
creating necessary tables, initializing services, and preparing sample data.
"""

import os
import sys
import time
import logging
import json
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional

import psycopg2
import redis
import mlflow
import requests
from sqlalchemy import create_engine, text
import pandas as pd
import numpy as np

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MLOpsPlatformInitializer:
    """Initialize and configure the MLOps platform."""
    
    def __init__(self):
        """Initialize the platform initializer."""
        self.config = self._load_config()
        self.db_engine = None
        self.redis_client = None
        
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from environment variables."""
        return {
            # Database configuration
            'postgres': {
                'host': os.getenv('POSTGRES_HOST', 'localhost'),
                'port': int(os.getenv('POSTGRES_PORT', 5432)),
                'user': os.getenv('POSTGRES_USER', 'mlops'),
                'password': os.getenv('POSTGRES_PASSWORD', 'mlops123'),
                'database': os.getenv('POSTGRES_DB', 'mlops')
            },
            
            # Redis configuration
            'redis': {
                'host': os.getenv('REDIS_HOST', 'localhost'),
                'port': int(os.getenv('REDIS_PORT', 6379))
            },
            
            # MLflow configuration
            'mlflow': {
                'tracking_uri': os.getenv('MLFLOW_TRACKING_URI', 'http://localhost:5000'),
                's3_endpoint': os.getenv('MLFLOW_S3_ENDPOINT_URL', 'http://localhost:9000')
            },
            
            # Service URLs
            'services': {
                'model_api': os.getenv('MODEL_API_URL', 'http://localhost:8000'),
                'prometheus': os.getenv('PROMETHEUS_URL', 'http://localhost:9090'),
                'grafana': os.getenv('GRAFANA_URL', 'http://localhost:3000')
            }
        }
    
    def wait_for_service(self, url: str, timeout: int = 300, interval: int = 10) -> bool:
        """Wait for a service to become available."""
        logger.info(f"Waiting for service at {url}...")
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                response = requests.get(f"{url}/health", timeout=5)
                if response.status_code == 200:
                    logger.info(f"✅ Service at {url} is ready")
                    return True
            except requests.exceptions.RequestException:
                pass
            
            logger.info(f"⏳ Service not ready yet, waiting {interval} seconds...")
            time.sleep(interval)
        
        logger.error(f"❌ Service at {url} did not become ready within {timeout} seconds")
        return False
    
    def initialize_postgresql(self) -> bool:
        """Initialize PostgreSQL databases and tables."""
        logger.info("🗄️ Initializing PostgreSQL...")
        
        try:
            # Connect to PostgreSQL
            connection_string = (
                f"postgresql://{self.config['postgres']['user']}:"
                f"{self.config['postgres']['password']}@"
                f"{self.config['postgres']['host']}:"
                f"{self.config['postgres']['port']}"
            )
            
            # Connect to default database first
            engine = create_engine(f"{connection_string}/postgres")
            
            # Create databases if they don't exist
            databases = ['mlops', 'mlflow', 'feast', 'monitoring']
            
            with engine.connect() as conn:
                conn.execute(text("COMMIT"))  # End any existing transaction
                
                for db_name in databases:
                    try:
                        # Check if database exists
                        result = conn.execute(
                            text("SELECT 1 FROM pg_database WHERE datname = :db_name"),
                            {"db_name": db_name}
                        )
                        
                        if not result.fetchone():
                            conn.execute(text(f"CREATE DATABASE {db_name}"))
                            logger.info(f"✅ Created database: {db_name}")
                        else:
                            logger.info(f"ℹ️ Database {db_name} already exists")
                    except Exception as e:
                        logger.warning(f"⚠️ Could not create database {db_name}: {e}")
            
            # Connect to mlops database and create tables
            self.db_engine = create_engine(f"{connection_string}/mlops")
            
            # Create monitoring tables
            self._create_monitoring_tables()
            
            logger.info("✅ PostgreSQL initialization completed")
            return True
            
        except Exception as e:
            logger.error(f"❌ PostgreSQL initialization failed: {e}")
            return False
    
    def _create_monitoring_tables(self):
        """Create monitoring and governance tables."""
        logger.info("📊 Creating monitoring tables...")
        
        monitoring_schema = """
        -- Model monitoring results table
        CREATE TABLE IF NOT EXISTS model_monitoring_results (
            id SERIAL PRIMARY KEY,
            model_name VARCHAR(100) NOT NULL,
            timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            data_drift_count INTEGER DEFAULT 0,
            performance_drift_count INTEGER DEFAULT 0,
            concept_drift_detected BOOLEAN DEFAULT FALSE,
            overall_health VARCHAR(20) DEFAULT 'unknown',
            results_json JSONB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Model performance metrics table
        CREATE TABLE IF NOT EXISTS model_performance_metrics (
            id SERIAL PRIMARY KEY,
            model_name VARCHAR(100) NOT NULL,
            version VARCHAR(50) NOT NULL,
            metric_name VARCHAR(50) NOT NULL,
            metric_value FLOAT NOT NULL,
            timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            environment VARCHAR(20) DEFAULT 'production'
        );
        
        -- Model governance table
        CREATE TABLE IF NOT EXISTS model_governance (
            id SERIAL PRIMARY KEY,
            model_name VARCHAR(100) NOT NULL,
            version VARCHAR(50) NOT NULL,
            stage VARCHAR(20) NOT NULL DEFAULT 'development',
            approval_status VARCHAR(20) DEFAULT 'pending',
            approved_by VARCHAR(100),
            approval_timestamp TIMESTAMP,
            deployment_timestamp TIMESTAMP,
            retirement_timestamp TIMESTAMP,
            governance_metadata JSONB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Prediction logs table
        CREATE TABLE IF NOT EXISTS prediction_logs (
            id SERIAL PRIMARY KEY,
            request_id VARCHAR(100) NOT NULL,
            model_name VARCHAR(100) NOT NULL,
            version VARCHAR(50) NOT NULL,
            features JSONB NOT NULL,
            prediction FLOAT,
            confidence FLOAT,
            latency_ms FLOAT,
            timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            user_feedback JSONB
        );
        
        -- Create indexes for better performance
        CREATE INDEX IF NOT EXISTS idx_monitoring_model_timestamp 
            ON model_monitoring_results(model_name, timestamp);
        
        CREATE INDEX IF NOT EXISTS idx_performance_model_metric 
            ON model_performance_metrics(model_name, metric_name, timestamp);
        
        CREATE INDEX IF NOT EXISTS idx_governance_model_stage 
            ON model_governance(model_name, stage);
        
        CREATE INDEX IF NOT EXISTS idx_predictions_model_timestamp 
            ON prediction_logs(model_name, timestamp);
        """
        
        try:
            with self.db_engine.connect() as conn:
                conn.execute(text(monitoring_schema))
                conn.commit()
            logger.info("✅ Monitoring tables created successfully")
        except Exception as e:
            logger.error(f"❌ Failed to create monitoring tables: {e}")
    
    def initialize_redis(self) -> bool:
        """Initialize Redis and set up basic configuration."""
        logger.info("🔄 Initializing Redis...")
        
        try:
            self.redis_client = redis.Redis(
                host=self.config['redis']['host'],
                port=self.config['redis']['port'],
                decode_responses=True
            )
            
            # Test connection
            self.redis_client.ping()
            
            # Set up basic configuration
            self.redis_client.config_set('maxmemory-policy', 'allkeys-lru')
            
            # Initialize feature store cache
            self._initialize_feature_store_cache()
            
            logger.info("✅ Redis initialization completed")
            return True
            
        except Exception as e:
            logger.error(f"❌ Redis initialization failed: {e}")
            return False
    
    def _initialize_feature_store_cache(self):
        """Initialize feature store cache with sample data."""
        logger.info("🏪 Initializing feature store cache...")
        
        # Sample customer features
        sample_customers = {
            'CUST_000001': {
                'age': 35,
                'income_level': 'medium',
                'customer_since_days': 365,
                'total_transactions_30d': 12,
                'avg_transaction_amount_30d': 67.5
            },
            'CUST_000002': {
                'age': 28,
                'income_level': 'high', 
                'customer_since_days': 180,
                'total_transactions_30d': 8,
                'avg_transaction_amount_30d': 95.0
            }
        }
        
        for customer_id, features in sample_customers.items():
            cache_key = f"customer_features:{customer_id}"
            self.redis_client.hmset(cache_key, features)
            self.redis_client.expire(cache_key, 86400)  # 24 hours
        
        logger.info(f"✅ Cached features for {len(sample_customers)} customers")
    
    def initialize_mlflow(self) -> bool:
        """Initialize MLflow tracking server and create experiments."""
        logger.info("🧪 Initializing MLflow...")
        
        try:
            # Set MLflow tracking URI
            mlflow.set_tracking_uri(self.config['mlflow']['tracking_uri'])
            
            # Wait for MLflow server to be ready
            if not self.wait_for_service(self.config['mlflow']['tracking_uri']):
                return False
            
            # Create default experiments
            experiments = [
                'customer-churn-prediction',
                'product-recommendation',
                'fraud-detection',
                'demand-forecasting',
                'model-benchmarking'
            ]
            
            for exp_name in experiments:
                try:
                    experiment = mlflow.get_experiment_by_name(exp_name)
                    if experiment is None:
                        mlflow.create_experiment(exp_name)
                        logger.info(f"✅ Created experiment: {exp_name}")
                    else:
                        logger.info(f"ℹ️ Experiment {exp_name} already exists")
                except Exception as e:
                    logger.warning(f"⚠️ Could not create experiment {exp_name}: {e}")
            
            # Create sample model registry entries
            self._create_sample_model_registry()
            
            logger.info("✅ MLflow initialization completed")
            return True
            
        except Exception as e:
            logger.error(f"❌ MLflow initialization failed: {e}")
            return False
    
    def _create_sample_model_registry(self):
        """Create sample model registry entries for demonstration."""
        logger.info("📋 Creating sample model registry...")
        
        try:
            client = mlflow.tracking.MlflowClient()
            
            # Sample models to register
            models = [
                'churn-prediction-model',
                'recommendation-model',
                'fraud-detection-model',
                'demand-forecasting-model'
            ]
            
            for model_name in models:
                try:
                    # Check if model exists
                    try:
                        client.get_registered_model(model_name)
                        logger.info(f"ℹ️ Model {model_name} already exists")
                    except mlflow.exceptions.RestException:
                        # Model doesn't exist, create it
                        client.create_registered_model(
                            model_name,
                            description=f"Production model for {model_name.replace('-', ' ')}"
                        )
                        logger.info(f"✅ Created registered model: {model_name}")
                        
                except Exception as e:
                    logger.warning(f"⚠️ Could not create model {model_name}: {e}")
                    
        except Exception as e:
            logger.warning(f"⚠️ Could not create sample model registry: {e}")
    
    def initialize_feast(self) -> bool:
        """Initialize Feast feature store."""
        logger.info("🍽️ Initializing Feast feature store...")
        
        try:
            # Navigate to feature store directory
            feature_store_dir = Path(__file__).parent.parent.parent / "feature-engineering" / "feature-store"
            
            if not feature_store_dir.exists():
                logger.warning(f"⚠️ Feature store directory not found: {feature_store_dir}")
                return False
            
            # Change to feature store directory
            original_dir = os.getcwd()
            os.chdir(feature_store_dir)
            
            try:
                # Apply feature definitions
                result = subprocess.run(['feast', 'apply'], 
                                      capture_output=True, text=True, timeout=60)
                
                if result.returncode == 0:
                    logger.info("✅ Feast feature definitions applied")
                else:
                    logger.warning(f"⚠️ Feast apply output: {result.stderr}")
                
                # Try to materialize features (may fail if no data source)
                try:
                    subprocess.run(['feast', 'materialize-incremental', '2023-01-01T00:00:00'], 
                                 capture_output=True, text=True, timeout=30)
                    logger.info("✅ Initial feature materialization completed")
                except subprocess.TimeoutExpired:
                    logger.info("ℹ️ Feature materialization skipped (no data sources)")
                
            finally:
                os.chdir(original_dir)
            
            logger.info("✅ Feast initialization completed")
            return True
            
        except Exception as e:
            logger.error(f"❌ Feast initialization failed: {e}")
            return False
    
    def create_sample_data(self) -> bool:
        """Create sample data for demonstration."""
        logger.info("📊 Creating sample data...")
        
        try:
            # Generate customer data
            np.random.seed(42)
            
            customers_data = []
            for i in range(1000):
                customer = {
                    'customer_id': f'CUST_{i:06d}',
                    'age': np.random.randint(18, 80),
                    'tenure_months': np.random.randint(1, 72),
                    'monthly_charges': round(np.random.normal(65, 20), 2),
                    'total_charges': round(np.random.normal(2500, 1500), 2),
                    'contract_type': np.random.choice(['Month-to-month', 'One year', 'Two year']),
                    'churn': np.random.choice([0, 1], p=[0.75, 0.25])
                }
                customers_data.append(customer)
            
            # Save to database
            df = pd.DataFrame(customers_data)
            df.to_sql('sample_customers', self.db_engine, if_exists='replace', index=False)
            
            logger.info(f"✅ Created {len(customers_data)} sample customer records")
            
            # Create sample predictions for monitoring
            self._create_sample_predictions()
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Sample data creation failed: {e}")
            return False
    
    def _create_sample_predictions(self):
        """Create sample prediction logs for monitoring demo."""
        logger.info("🔮 Creating sample prediction logs...")
        
        try:
            predictions_data = []
            for i in range(100):
                prediction = {
                    'request_id': f'REQ_{i:06d}',
                    'model_name': 'churn-prediction-model',
                    'version': '1.0.0',
                    'features': json.dumps({
                        'tenure_months': np.random.randint(1, 72),
                        'monthly_charges': round(np.random.normal(65, 20), 2)
                    }),
                    'prediction': round(np.random.random(), 3),
                    'confidence': round(np.random.uniform(0.6, 0.95), 3),
                    'latency_ms': round(np.random.uniform(50, 150), 2)
                }
                predictions_data.append(prediction)
            
            df = pd.DataFrame(predictions_data)
            df.to_sql('prediction_logs', self.db_engine, if_exists='append', index=False)
            
            logger.info(f"✅ Created {len(predictions_data)} sample prediction logs")
            
        except Exception as e:
            logger.warning(f"⚠️ Could not create sample predictions: {e}")
    
    def verify_setup(self) -> bool:
        """Verify that all components are working correctly."""
        logger.info("🔍 Verifying platform setup...")
        
        all_checks_passed = True
        
        # Check PostgreSQL
        try:
            with self.db_engine.connect() as conn:
                result = conn.execute(text("SELECT COUNT(*) FROM sample_customers"))
                count = result.fetchone()[0]
                logger.info(f"✅ PostgreSQL: {count} sample customers found")
        except Exception as e:
            logger.error(f"❌ PostgreSQL check failed: {e}")
            all_checks_passed = False
        
        # Check Redis
        try:
            info = self.redis_client.info()
            logger.info(f"✅ Redis: {info['connected_clients']} clients connected")
        except Exception as e:
            logger.error(f"❌ Redis check failed: {e}")
            all_checks_passed = False
        
        # Check MLflow
        try:
            experiments = mlflow.search_experiments()
            logger.info(f"✅ MLflow: {len(experiments)} experiments found")
        except Exception as e:
            logger.error(f"❌ MLflow check failed: {e}")
            all_checks_passed = False
        
        # Check Model API
        try:
            response = requests.get(f"{self.config['services']['model_api']}/health", timeout=10)
            if response.status_code == 200:
                logger.info("✅ Model API: Health check passed")
            else:
                logger.warning(f"⚠️ Model API: Health check returned {response.status_code}")
        except Exception as e:
            logger.warning(f"⚠️ Model API check failed: {e}")
        
        return all_checks_passed
    
    def run_initialization(self) -> bool:
        """Run the complete initialization process."""
        logger.info("🚀 Starting MLOps platform initialization...")
        
        steps = [
            ("PostgreSQL", self.initialize_postgresql),
            ("Redis", self.initialize_redis),
            ("MLflow", self.initialize_mlflow),
            ("Feast", self.initialize_feast),
            ("Sample Data", self.create_sample_data),
        ]
        
        for step_name, step_func in steps:
            logger.info(f"\n{'='*50}")
            logger.info(f"Initializing {step_name}...")
            logger.info(f"{'='*50}")
            
            if not step_func():
                logger.error(f"❌ {step_name} initialization failed")
                return False
        
        # Final verification
        logger.info(f"\n{'='*50}")
        logger.info("Running final verification...")
        logger.info(f"{'='*50}")
        
        if self.verify_setup():
            logger.info("\n🎉 MLOps platform initialization completed successfully!")
            logger.info("You can now access the following services:")
            logger.info("• MLflow UI: http://localhost:5000")
            logger.info("• Grafana: http://localhost:3000")
            logger.info("• Model API: http://localhost:8000")
            logger.info("• Jupyter Lab: http://localhost:8888")
            return True
        else:
            logger.error("\n❌ Platform initialization completed with some issues")
            return False


def main():
    """Main function."""
    initializer = MLOpsPlatformInitializer()
    
    try:
        success = initializer.run_initialization()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        logger.info("\n⏹️ Initialization interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"\n💥 Unexpected error during initialization: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
