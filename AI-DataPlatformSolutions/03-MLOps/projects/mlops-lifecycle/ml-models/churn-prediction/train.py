"""
Customer Churn Prediction Model Training Pipeline

This script implements a comprehensive ML pipeline for predicting customer churn
with experiment tracking, model registration, and automated hyperparameter optimization.
"""

import logging
import os
import pickle
from datetime import datetime
from pathlib import Path
from typing import Dict, Tuple, Any, Optional

import mlflow
import mlflow.sklearn
import numpy as np
import pandas as pd
import optuna
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report
)
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
import xgboost as xgb
import lightgbm as lgb

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class ChurnPredictionTrainer:
    """Customer churn prediction model trainer with MLOps best practices."""
    
    def __init__(self, mlflow_tracking_uri: str = "http://localhost:5000"):
        """Initialize the trainer with MLflow configuration."""
        mlflow.set_tracking_uri(mlflow_tracking_uri)
        self.experiment_name = "customer-churn-prediction"
        self.model_name = "churn-prediction-model"
        
        # Set up MLflow experiment
        try:
            experiment = mlflow.get_experiment_by_name(self.experiment_name)
            if experiment is None:
                mlflow.create_experiment(self.experiment_name)
                logger.info(f"Created MLflow experiment: {self.experiment_name}")
            else:
                logger.info(f"Using existing MLflow experiment: {self.experiment_name}")
        except Exception as e:
            logger.error(f"Error setting up MLflow experiment: {e}")
            raise
        
        mlflow.set_experiment(self.experiment_name)
        
        # Initialize preprocessing components
        self.scaler = StandardScaler()
        self.label_encoders = {}
        
        # Model configurations
        self.model_configs = {
            'logistic_regression': {
                'model_class': LogisticRegression,
                'params': {
                    'random_state': 42,
                    'max_iter': 1000
                },
                'param_distributions': {
                    'C': [0.001, 0.01, 0.1, 1, 10, 100],
                    'penalty': ['l1', 'l2'],
                    'solver': ['liblinear', 'saga']
                }
            },
            'random_forest': {
                'model_class': RandomForestClassifier,
                'params': {
                    'random_state': 42,
                    'n_jobs': -1
                },
                'param_distributions': {
                    'n_estimators': [50, 100, 200, 300],
                    'max_depth': [3, 5, 7, 10, None],
                    'min_samples_split': [2, 5, 10],
                    'min_samples_leaf': [1, 2, 4],
                    'max_features': ['sqrt', 'log2', None]
                }
            },
            'gradient_boosting': {
                'model_class': GradientBoostingClassifier,
                'params': {
                    'random_state': 42
                },
                'param_distributions': {
                    'n_estimators': [50, 100, 200],
                    'learning_rate': [0.01, 0.1, 0.2],
                    'max_depth': [3, 5, 7],
                    'subsample': [0.8, 0.9, 1.0],
                    'max_features': ['sqrt', 'log2', None]
                }
            },
            'xgboost': {
                'model_class': xgb.XGBClassifier,
                'params': {
                    'random_state': 42,
                    'eval_metric': 'logloss'
                },
                'param_distributions': {
                    'n_estimators': [50, 100, 200],
                    'learning_rate': [0.01, 0.1, 0.2],
                    'max_depth': [3, 5, 7],
                    'subsample': [0.8, 0.9, 1.0],
                    'colsample_bytree': [0.8, 0.9, 1.0]
                }
            },
            'lightgbm': {
                'model_class': lgb.LGBMClassifier,
                'params': {
                    'random_state': 42,
                    'verbose': -1
                },
                'param_distributions': {
                    'n_estimators': [50, 100, 200],
                    'learning_rate': [0.01, 0.1, 0.2],
                    'max_depth': [3, 5, 7, -1],
                    'num_leaves': [31, 50, 100],
                    'subsample': [0.8, 0.9, 1.0],
                    'colsample_bytree': [0.8, 0.9, 1.0]
                }
            }
        }
    
    def generate_synthetic_data(self, n_samples: int = 10000) -> pd.DataFrame:
        """Generate synthetic customer churn data for demonstration."""
        np.random.seed(42)
        
        data = {
            'customer_id': [f'CUST_{i:06d}' for i in range(n_samples)],
            'tenure_months': np.random.randint(1, 73, n_samples),
            'monthly_charges': np.random.normal(65, 20, n_samples).clip(20, 150),
            'total_charges': np.random.normal(2500, 1500, n_samples).clip(100, 8000),
            'contract_type': np.random.choice(['Month-to-month', 'One year', 'Two year'], 
                                            n_samples, p=[0.5, 0.3, 0.2]),
            'payment_method': np.random.choice(['Electronic check', 'Mailed check', 
                                              'Bank transfer', 'Credit card'], 
                                            n_samples, p=[0.35, 0.15, 0.25, 0.25]),
            'internet_service': np.random.choice(['DSL', 'Fiber optic', 'No'], 
                                               n_samples, p=[0.4, 0.4, 0.2]),
            'online_security': np.random.choice(['Yes', 'No'], n_samples, p=[0.3, 0.7]),
            'tech_support': np.random.choice(['Yes', 'No'], n_samples, p=[0.3, 0.7]),
            'streaming_tv': np.random.choice(['Yes', 'No'], n_samples, p=[0.4, 0.6]),
            'streaming_movies': np.random.choice(['Yes', 'No'], n_samples, p=[0.4, 0.6]),
            'paperless_billing': np.random.choice(['Yes', 'No'], n_samples, p=[0.6, 0.4]),
            'senior_citizen': np.random.choice([0, 1], n_samples, p=[0.85, 0.15]),
            'partner': np.random.choice(['Yes', 'No'], n_samples, p=[0.5, 0.5]),
            'dependents': np.random.choice(['Yes', 'No'], n_samples, p=[0.3, 0.7]),
            'phone_service': np.random.choice(['Yes', 'No'], n_samples, p=[0.9, 0.1]),
            'multiple_lines': np.random.choice(['Yes', 'No'], n_samples, p=[0.4, 0.6])
        }
        
        df = pd.DataFrame(data)
        
        # Create churn labels based on realistic business rules
        churn_probability = (
            0.1 +  # Base probability
            0.3 * (df['contract_type'] == 'Month-to-month') +
            0.2 * (df['tenure_months'] < 12) +
            0.15 * (df['monthly_charges'] > 80) +
            0.1 * (df['payment_method'] == 'Electronic check') +
            0.1 * (df['tech_support'] == 'No') +
            0.05 * (df['senior_citizen'] == 1) +
            -0.1 * (df['partner'] == 'Yes') +
            -0.1 * (df['dependents'] == 'Yes')
        ).clip(0, 1)
        
        df['churn'] = np.random.binomial(1, churn_probability, n_samples)
        
        logger.info(f"Generated {n_samples} synthetic customer records")
        logger.info(f"Churn rate: {df['churn'].mean():.2%}")
        
        return df
    
    def preprocess_data(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
        """Preprocess the data for training."""
        logger.info("Starting data preprocessing...")
        
        # Separate features and target
        X = df.drop(['customer_id', 'churn'], axis=1)
        y = df['churn']
        
        # Handle categorical variables
        categorical_columns = X.select_dtypes(include=['object']).columns
        for col in categorical_columns:
            if col not in self.label_encoders:
                self.label_encoders[col] = LabelEncoder()
            X[col] = self.label_encoders[col].fit_transform(X[col])
        
        # Feature engineering
        X['charges_per_month'] = X['total_charges'] / (X['tenure_months'] + 1)
        X['avg_monthly_usage'] = X['total_charges'] / X['monthly_charges']
        X['tenure_years'] = X['tenure_months'] / 12
        
        # Create interaction features
        X['high_charges_short_tenure'] = ((X['monthly_charges'] > X['monthly_charges'].quantile(0.75)) & 
                                         (X['tenure_months'] < 12)).astype(int)
        
        # Scale numerical features
        numerical_columns = X.select_dtypes(include=[np.number]).columns
        X[numerical_columns] = self.scaler.fit_transform(X[numerical_columns])
        
        logger.info(f"Preprocessing completed. Features: {X.shape[1]}, Samples: {X.shape[0]}")
        
        return X, y
    
    def objective(self, trial, X_train, X_val, y_train, y_val, model_name: str):
        """Optuna objective function for hyperparameter optimization."""
        config = self.model_configs[model_name]
        
        # Suggest hyperparameters
        params = config['params'].copy()
        param_dist = config['param_distributions']
        
        for param, values in param_dist.items():
            if isinstance(values, list):
                if all(isinstance(v, (int, float)) for v in values):
                    if all(isinstance(v, int) for v in values):
                        params[param] = trial.suggest_int(param, min(values), max(values))
                    else:
                        params[param] = trial.suggest_float(param, min(values), max(values))
                else:
                    params[param] = trial.suggest_categorical(param, values)
        
        # Train model
        model = config['model_class'](**params)
        model.fit(X_train, y_train)
        
        # Predict and evaluate
        y_pred = model.predict(X_val)
        y_pred_proba = model.predict_proba(X_val)[:, 1]
        
        # Return F1 score as the objective to maximize
        f1 = f1_score(y_val, y_pred)
        
        return f1
    
    def train_model(self, model_name: str, X_train, X_val, y_train, y_val, 
                   optimize_hyperparams: bool = True, n_trials: int = 50) -> Dict[str, Any]:
        """Train a specific model with optional hyperparameter optimization."""
        logger.info(f"Training {model_name} model...")
        
        config = self.model_configs[model_name]
        
        with mlflow.start_run(run_name=f"{model_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"):
            # Log model type
            mlflow.set_tag("model_type", model_name)
            mlflow.set_tag("optimization", "enabled" if optimize_hyperparams else "disabled")
            
            if optimize_hyperparams:
                # Hyperparameter optimization with Optuna
                logger.info(f"Optimizing hyperparameters for {model_name} with {n_trials} trials...")
                
                study = optuna.create_study(direction='maximize')
                study.optimize(
                    lambda trial: self.objective(trial, X_train, X_val, y_train, y_val, model_name),
                    n_trials=n_trials
                )
                
                best_params = {**config['params'], **study.best_params}
                mlflow.log_params(best_params)
                mlflow.log_metric("best_f1_score", study.best_value)
                
                logger.info(f"Best F1 score: {study.best_value:.4f}")
                logger.info(f"Best parameters: {study.best_params}")
            else:
                best_params = config['params']
                mlflow.log_params(best_params)
            
            # Train final model with best parameters
            model = config['model_class'](**best_params)
            model.fit(X_train, y_train)
            
            # Evaluate on validation set
            y_pred = model.predict(X_val)
            y_pred_proba = model.predict_proba(X_val)[:, 1]
            
            # Calculate metrics
            metrics = {
                'accuracy': accuracy_score(y_val, y_pred),
                'precision': precision_score(y_val, y_pred),
                'recall': recall_score(y_val, y_pred),
                'f1_score': f1_score(y_val, y_pred),
                'roc_auc': roc_auc_score(y_val, y_pred_proba)
            }
            
            # Log metrics
            for metric_name, metric_value in metrics.items():
                mlflow.log_metric(metric_name, metric_value)
            
            # Log confusion matrix and classification report
            cm = confusion_matrix(y_val, y_pred)
            mlflow.log_text(str(cm), "confusion_matrix.txt")
            
            report = classification_report(y_val, y_pred)
            mlflow.log_text(report, "classification_report.txt")
            
            # Cross-validation score
            cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='f1')
            mlflow.log_metric("cv_f1_mean", cv_scores.mean())
            mlflow.log_metric("cv_f1_std", cv_scores.std())
            
            # Feature importance (if available)
            if hasattr(model, 'feature_importances_'):
                feature_importance = pd.DataFrame({
                    'feature': X_train.columns,
                    'importance': model.feature_importances_
                }).sort_values('importance', ascending=False)
                
                mlflow.log_text(feature_importance.to_string(), "feature_importance.txt")
            
            # Log model
            mlflow.sklearn.log_model(
                model,
                "model",
                registered_model_name=f"{self.model_name}-{model_name}",
                signature=mlflow.models.infer_signature(X_train, y_pred_proba)
            )
            
            # Log preprocessing objects
            mlflow.log_dict({"scaler": "StandardScaler"}, "preprocessing_info.json")
            
            run_id = mlflow.active_run().info.run_id
            logger.info(f"Model training completed. Run ID: {run_id}")
            
            return {
                'model': model,
                'metrics': metrics,
                'run_id': run_id,
                'best_params': best_params
            }
    
    def train_all_models(self, df: pd.DataFrame, test_size: float = 0.2, 
                        optimize_hyperparams: bool = True) -> Dict[str, Any]:
        """Train all models and compare performance."""
        logger.info("Starting comprehensive model training...")
        
        # Preprocess data
        X, y = self.preprocess_data(df)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, stratify=y, random_state=42
        )
        
        # Further split training data for validation
        X_train, X_val, y_train, y_val = train_test_split(
            X_train, y_train, test_size=0.2, stratify=y_train, random_state=42
        )
        
        logger.info(f"Data split - Train: {X_train.shape[0]}, Val: {X_val.shape[0]}, Test: {X_test.shape[0]}")
        
        # Train all models
        results = {}
        for model_name in self.model_configs.keys():
            try:
                result = self.train_model(
                    model_name, X_train, X_val, y_train, y_val, optimize_hyperparams
                )
                results[model_name] = result
            except Exception as e:
                logger.error(f"Error training {model_name}: {e}")
                continue
        
        # Find best model
        best_model_name = max(results.keys(), key=lambda k: results[k]['metrics']['f1_score'])
        best_model_info = results[best_model_name]
        
        logger.info(f"Best model: {best_model_name} with F1 score: {best_model_info['metrics']['f1_score']:.4f}")
        
        # Evaluate best model on test set
        best_model = best_model_info['model']
        y_test_pred = best_model.predict(X_test)
        y_test_pred_proba = best_model.predict_proba(X_test)[:, 1]
        
        test_metrics = {
            'test_accuracy': accuracy_score(y_test, y_test_pred),
            'test_precision': precision_score(y_test, y_test_pred),
            'test_recall': recall_score(y_test, y_test_pred),
            'test_f1_score': f1_score(y_test, y_test_pred),
            'test_roc_auc': roc_auc_score(y_test, y_test_pred_proba)
        }
        
        logger.info("Test set performance:")
        for metric, value in test_metrics.items():
            logger.info(f"{metric}: {value:.4f}")
        
        # Save preprocessing objects
        preprocessing_artifacts = {
            'scaler': self.scaler,
            'label_encoders': self.label_encoders
        }
        
        return {
            'best_model_name': best_model_name,
            'best_model': best_model,
            'all_results': results,
            'test_metrics': test_metrics,
            'preprocessing': preprocessing_artifacts,
            'data_splits': {
                'X_train': X_train, 'X_val': X_val, 'X_test': X_test,
                'y_train': y_train, 'y_val': y_val, 'y_test': y_test
            }
        }
    
    def save_artifacts(self, results: Dict[str, Any], output_dir: str = "artifacts"):
        """Save model artifacts and preprocessing objects."""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Save best model
        best_model = results['best_model']
        model_path = output_path / "best_model.pkl"
        with open(model_path, 'wb') as f:
            pickle.dump(best_model, f)
        
        # Save preprocessing objects
        preprocessing_path = output_path / "preprocessing.pkl"
        with open(preprocessing_path, 'wb') as f:
            pickle.dump(results['preprocessing'], f)
        
        # Save model metadata
        metadata = {
            'best_model_name': results['best_model_name'],
            'test_metrics': results['test_metrics'],
            'training_timestamp': datetime.now().isoformat(),
            'model_version': '1.0.0'
        }
        
        metadata_path = output_path / "model_metadata.json"
        import json
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        logger.info(f"Artifacts saved to {output_path}")


def main():
    """Main function to run the training pipeline."""
    # Initialize trainer
    trainer = ChurnPredictionTrainer()
    
    # Generate synthetic data (in production, load from data source)
    df = trainer.generate_synthetic_data(n_samples=10000)
    
    # Train all models
    results = trainer.train_all_models(df, optimize_hyperparams=True)
    
    # Save artifacts
    trainer.save_artifacts(results)
    
    logger.info("Training pipeline completed successfully!")


if __name__ == "__main__":
    main()
