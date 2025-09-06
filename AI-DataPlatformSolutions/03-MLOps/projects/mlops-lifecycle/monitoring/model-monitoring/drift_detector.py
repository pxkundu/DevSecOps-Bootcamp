"""
Model and Data Drift Detection System

This module implements comprehensive monitoring for ML models including:
- Data drift detection using statistical tests
- Model performance drift monitoring
- Concept drift detection
- Automated alerting and reporting
"""

import logging
import json
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from abc import ABC, abstractmethod

from scipy import stats
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from evidently import ColumnMapping
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset, TargetDriftPreset
from evidently.test_suite import TestSuite
from evidently.tests import TestNumberOfDriftedColumns, TestShareOfDriftedColumns
import mlflow
import psycopg2
from prometheus_client import Gauge, Counter, Histogram
import redis

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Prometheus metrics for monitoring
DATA_DRIFT_SCORE = Gauge('model_data_drift_score', 'Data drift score', ['model_name', 'feature'])
PERFORMANCE_DRIFT_SCORE = Gauge('model_performance_drift_score', 'Performance drift score', ['model_name', 'metric'])
CONCEPT_DRIFT_DETECTED = Counter('model_concept_drift_detected_total', 'Concept drift detection events', ['model_name'])
DRIFT_ALERTS_SENT = Counter('model_drift_alerts_sent_total', 'Number of drift alerts sent', ['model_name', 'drift_type'])


@dataclass
class DriftResult:
    """Container for drift detection results."""
    drift_detected: bool
    drift_score: float
    p_value: float
    test_statistic: float
    drift_type: str
    timestamp: str
    feature_name: Optional[str] = None
    details: Optional[Dict[str, Any]] = None


@dataclass
class PerformanceMetrics:
    """Container for model performance metrics."""
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    roc_auc: Optional[float] = None
    timestamp: str = None


class DriftDetector(ABC):
    """Abstract base class for drift detectors."""
    
    @abstractmethod
    def detect_drift(self, reference_data: pd.DataFrame, current_data: pd.DataFrame) -> DriftResult:
        """Detect drift between reference and current data."""
        pass


class KolmogorovSmirnovDriftDetector(DriftDetector):
    """Kolmogorov-Smirnov test for numerical feature drift."""
    
    def __init__(self, threshold: float = 0.05):
        self.threshold = threshold
    
    def detect_drift(self, reference_data: pd.Series, current_data: pd.Series, 
                    feature_name: str = None) -> DriftResult:
        """Detect drift using KS test."""
        try:
            # Remove NaN values
            ref_clean = reference_data.dropna()
            curr_clean = current_data.dropna()
            
            if len(ref_clean) == 0 or len(curr_clean) == 0:
                return DriftResult(
                    drift_detected=False,
                    drift_score=0.0,
                    p_value=1.0,
                    test_statistic=0.0,
                    drift_type="ks_test",
                    timestamp=datetime.now().isoformat(),
                    feature_name=feature_name,
                    details={"error": "Insufficient data"}
                )
            
            # Perform KS test
            ks_statistic, p_value = stats.ks_2samp(ref_clean, curr_clean)
            drift_detected = p_value < self.threshold
            
            return DriftResult(
                drift_detected=drift_detected,
                drift_score=ks_statistic,
                p_value=p_value,
                test_statistic=ks_statistic,
                drift_type="ks_test",
                timestamp=datetime.now().isoformat(),
                feature_name=feature_name,
                details={
                    "threshold": self.threshold,
                    "ref_mean": float(ref_clean.mean()),
                    "curr_mean": float(curr_clean.mean()),
                    "ref_std": float(ref_clean.std()),
                    "curr_std": float(curr_clean.std())
                }
            )
            
        except Exception as e:
            logger.error(f"Error in KS drift detection: {e}")
            return DriftResult(
                drift_detected=False,
                drift_score=0.0,
                p_value=1.0,
                test_statistic=0.0,
                drift_type="ks_test",
                timestamp=datetime.now().isoformat(),
                feature_name=feature_name,
                details={"error": str(e)}
            )


class ChiSquareDriftDetector(DriftDetector):
    """Chi-square test for categorical feature drift."""
    
    def __init__(self, threshold: float = 0.05):
        self.threshold = threshold
    
    def detect_drift(self, reference_data: pd.Series, current_data: pd.Series,
                    feature_name: str = None) -> DriftResult:
        """Detect drift using Chi-square test."""
        try:
            # Get value counts
            ref_counts = reference_data.value_counts()
            curr_counts = current_data.value_counts()
            
            # Align categories
            all_categories = set(ref_counts.index) | set(curr_counts.index)
            ref_aligned = ref_counts.reindex(all_categories, fill_value=0)
            curr_aligned = curr_counts.reindex(all_categories, fill_value=0)
            
            # Perform chi-square test
            chi2_statistic, p_value = stats.chisquare(curr_aligned, ref_aligned)
            drift_detected = p_value < self.threshold
            
            return DriftResult(
                drift_detected=drift_detected,
                drift_score=chi2_statistic,
                p_value=p_value,
                test_statistic=chi2_statistic,
                drift_type="chi_square_test",
                timestamp=datetime.now().isoformat(),
                feature_name=feature_name,
                details={
                    "threshold": self.threshold,
                    "ref_categories": len(ref_counts),
                    "curr_categories": len(curr_counts),
                    "new_categories": list(set(curr_counts.index) - set(ref_counts.index)),
                    "missing_categories": list(set(ref_counts.index) - set(curr_counts.index))
                }
            )
            
        except Exception as e:
            logger.error(f"Error in Chi-square drift detection: {e}")
            return DriftResult(
                drift_detected=False,
                drift_score=0.0,
                p_value=1.0,
                test_statistic=0.0,
                drift_type="chi_square_test",
                timestamp=datetime.now().isoformat(),
                feature_name=feature_name,
                details={"error": str(e)}
            )


class PSIDriftDetector(DriftDetector):
    """Population Stability Index (PSI) for drift detection."""
    
    def __init__(self, threshold: float = 0.2):
        self.threshold = threshold
    
    def detect_drift(self, reference_data: pd.Series, current_data: pd.Series,
                    feature_name: str = None, bins: int = 10) -> DriftResult:
        """Detect drift using PSI."""
        try:
            # Create bins based on reference data
            if reference_data.dtype in ['object', 'category']:
                # Categorical data
                ref_counts = reference_data.value_counts(normalize=True)
                curr_counts = current_data.value_counts(normalize=True)
                
                # Align categories
                all_categories = set(ref_counts.index) | set(curr_counts.index)
                ref_pct = ref_counts.reindex(all_categories, fill_value=0.001)  # Small value to avoid log(0)
                curr_pct = curr_counts.reindex(all_categories, fill_value=0.001)
            else:
                # Numerical data
                bin_edges = pd.qcut(reference_data.dropna(), q=bins, retbins=True, duplicates='drop')[1]
                ref_pct = pd.cut(reference_data, bins=bin_edges, include_lowest=True).value_counts(normalize=True)
                curr_pct = pd.cut(current_data, bins=bin_edges, include_lowest=True).value_counts(normalize=True)
                
                # Handle missing bins
                ref_pct = ref_pct.fillna(0.001)
                curr_pct = curr_pct.reindex(ref_pct.index, fill_value=0.001)
            
            # Calculate PSI
            psi = np.sum((curr_pct - ref_pct) * np.log(curr_pct / ref_pct))
            drift_detected = psi > self.threshold
            
            return DriftResult(
                drift_detected=drift_detected,
                drift_score=psi,
                p_value=None,  # PSI doesn't have p-value
                test_statistic=psi,
                drift_type="psi",
                timestamp=datetime.now().isoformat(),
                feature_name=feature_name,
                details={
                    "threshold": self.threshold,
                    "interpretation": self._interpret_psi(psi)
                }
            )
            
        except Exception as e:
            logger.error(f"Error in PSI drift detection: {e}")
            return DriftResult(
                drift_detected=False,
                drift_score=0.0,
                p_value=None,
                test_statistic=0.0,
                drift_type="psi",
                timestamp=datetime.now().isoformat(),
                feature_name=feature_name,
                details={"error": str(e)}
            )
    
    def _interpret_psi(self, psi_value: float) -> str:
        """Interpret PSI value."""
        if psi_value < 0.1:
            return "No significant change"
        elif psi_value < 0.2:
            return "Minor change"
        else:
            return "Major change"


class ModelMonitoringSystem:
    """Comprehensive model monitoring system."""
    
    def __init__(self, model_name: str, mlflow_tracking_uri: str = "http://localhost:5000"):
        self.model_name = model_name
        self.mlflow_tracking_uri = mlflow_tracking_uri
        mlflow.set_tracking_uri(mlflow_tracking_uri)
        
        # Initialize drift detectors
        self.ks_detector = KolmogorovSmirnovDriftDetector()
        self.chi2_detector = ChiSquareDriftDetector()
        self.psi_detector = PSIDriftDetector()
        
        # Initialize storage connections
        self.redis_client = self._get_redis_client()
        self.db_engine = self._get_db_connection()
        
        # Reference data storage
        self.reference_data = None
        self.reference_performance = None
        
        # Drift detection thresholds
        self.drift_thresholds = {
            'data_drift': 0.05,
            'performance_drift': 0.1,
            'concept_drift': 0.15
        }
    
    def _get_redis_client(self) -> Optional[redis.Redis]:
        """Get Redis client for caching."""
        try:
            return redis.Redis(host='redis', port=6379, decode_responses=True)
        except Exception as e:
            logger.warning(f"Could not connect to Redis: {e}")
            return None
    
    def _get_db_connection(self):
        """Get database connection for storing results."""
        try:
            return psycopg2.connect(
                host="postgres",
                port=5432,
                database="monitoring",
                user="mlops",
                password="mlops123"
            )
        except Exception as e:
            logger.warning(f"Could not connect to database: {e}")
            return None
    
    def set_reference_data(self, reference_data: pd.DataFrame, 
                          reference_performance: PerformanceMetrics = None):
        """Set reference data for drift detection."""
        self.reference_data = reference_data.copy()
        self.reference_performance = reference_performance
        
        # Cache in Redis if available
        if self.redis_client:
            try:
                self.redis_client.set(
                    f"{self.model_name}:reference_data_shape",
                    json.dumps(list(reference_data.shape))
                )
                self.redis_client.set(
                    f"{self.model_name}:reference_timestamp",
                    datetime.now().isoformat()
                )
            except Exception as e:
                logger.warning(f"Could not cache reference data: {e}")
        
        logger.info(f"Set reference data with shape {reference_data.shape}")
    
    def detect_data_drift(self, current_data: pd.DataFrame) -> Dict[str, DriftResult]:
        """Detect data drift across all features."""
        if self.reference_data is None:
            raise ValueError("Reference data not set. Call set_reference_data() first.")
        
        drift_results = {}
        
        for column in current_data.columns:
            if column not in self.reference_data.columns:
                logger.warning(f"Column {column} not in reference data, skipping")
                continue
            
            ref_series = self.reference_data[column]
            curr_series = current_data[column]
            
            # Choose appropriate test based on data type
            if pd.api.types.is_numeric_dtype(ref_series):
                # Use KS test for numerical data
                result = self.ks_detector.detect_drift(ref_series, curr_series, column)
            else:
                # Use Chi-square test for categorical data
                result = self.chi2_detector.detect_drift(ref_series, curr_series, column)
            
            drift_results[column] = result
            
            # Record metrics
            DATA_DRIFT_SCORE.labels(model_name=self.model_name, feature=column).set(result.drift_score)
            
            if result.drift_detected:
                logger.warning(f"Data drift detected in feature {column}: {result.drift_score:.4f}")
        
        return drift_results
    
    def detect_performance_drift(self, current_performance: PerformanceMetrics) -> Dict[str, DriftResult]:
        """Detect performance drift."""
        if self.reference_performance is None:
            logger.warning("Reference performance not set, cannot detect performance drift")
            return {}
        
        drift_results = {}
        
        # Check each performance metric
        ref_metrics = {
            'accuracy': self.reference_performance.accuracy,
            'precision': self.reference_performance.precision,
            'recall': self.reference_performance.recall,
            'f1_score': self.reference_performance.f1_score
        }
        
        curr_metrics = {
            'accuracy': current_performance.accuracy,
            'precision': current_performance.precision,
            'recall': current_performance.recall,
            'f1_score': current_performance.f1_score
        }
        
        if self.reference_performance.roc_auc and current_performance.roc_auc:
            ref_metrics['roc_auc'] = self.reference_performance.roc_auc
            curr_metrics['roc_auc'] = current_performance.roc_auc
        
        for metric_name, ref_value in ref_metrics.items():
            curr_value = curr_metrics[metric_name]
            
            # Calculate relative change
            relative_change = abs(curr_value - ref_value) / ref_value if ref_value > 0 else 0
            drift_detected = relative_change > self.drift_thresholds['performance_drift']
            
            result = DriftResult(
                drift_detected=drift_detected,
                drift_score=relative_change,
                p_value=None,
                test_statistic=relative_change,
                drift_type="performance_drift",
                timestamp=datetime.now().isoformat(),
                feature_name=metric_name,
                details={
                    "reference_value": ref_value,
                    "current_value": curr_value,
                    "absolute_change": curr_value - ref_value,
                    "relative_change": relative_change
                }
            )
            
            drift_results[metric_name] = result
            
            # Record metrics
            PERFORMANCE_DRIFT_SCORE.labels(model_name=self.model_name, metric=metric_name).set(relative_change)
            
            if drift_detected:
                logger.warning(f"Performance drift detected in {metric_name}: {relative_change:.4f}")
        
        return drift_results
    
    def detect_concept_drift(self, predictions: np.ndarray, actuals: np.ndarray = None) -> DriftResult:
        """Detect concept drift using prediction distribution."""
        # Simple concept drift detection based on prediction distribution
        if self.redis_client:
            try:
                # Get historical predictions from cache
                historical_key = f"{self.model_name}:historical_predictions"
                historical_predictions = self.redis_client.get(historical_key)
                
                if historical_predictions:
                    historical_predictions = json.loads(historical_predictions)
                    historical_array = np.array(historical_predictions)
                    
                    # Use KS test on prediction distributions
                    ks_statistic, p_value = stats.ks_2samp(historical_array, predictions)
                    drift_detected = p_value < self.drift_thresholds['concept_drift']
                    
                    result = DriftResult(
                        drift_detected=drift_detected,
                        drift_score=ks_statistic,
                        p_value=p_value,
                        test_statistic=ks_statistic,
                        drift_type="concept_drift",
                        timestamp=datetime.now().isoformat(),
                        details={
                            "historical_mean": float(historical_array.mean()),
                            "current_mean": float(predictions.mean()),
                            "historical_std": float(historical_array.std()),
                            "current_std": float(predictions.std())
                        }
                    )
                    
                    if drift_detected:
                        CONCEPT_DRIFT_DETECTED.labels(model_name=self.model_name).inc()
                    
                    # Update historical predictions (keep last 1000)
                    updated_predictions = list(historical_array[-900:]) + list(predictions)
                    self.redis_client.set(historical_key, json.dumps(updated_predictions))
                    
                    return result
                else:
                    # Initialize historical predictions
                    self.redis_client.set(historical_key, json.dumps(list(predictions)))
                    
            except Exception as e:
                logger.error(f"Error in concept drift detection: {e}")
        
        # Return no drift if can't detect
        return DriftResult(
            drift_detected=False,
            drift_score=0.0,
            p_value=1.0,
            test_statistic=0.0,
            drift_type="concept_drift",
            timestamp=datetime.now().isoformat(),
            details={"error": "Could not detect concept drift"}
        )
    
    def run_comprehensive_monitoring(self, current_data: pd.DataFrame,
                                   current_performance: PerformanceMetrics = None,
                                   predictions: np.ndarray = None) -> Dict[str, Any]:
        """Run comprehensive monitoring including all drift types."""
        monitoring_results = {
            'timestamp': datetime.now().isoformat(),
            'model_name': self.model_name,
            'data_drift': {},
            'performance_drift': {},
            'concept_drift': {},
            'summary': {}
        }
        
        # Data drift detection
        try:
            data_drift_results = self.detect_data_drift(current_data)
            monitoring_results['data_drift'] = {
                col: {
                    'drift_detected': result.drift_detected,
                    'drift_score': result.drift_score,
                    'p_value': result.p_value,
                    'details': result.details
                }
                for col, result in data_drift_results.items()
            }
            
            # Count drifted features
            drifted_features = sum(1 for result in data_drift_results.values() if result.drift_detected)
            monitoring_results['summary']['drifted_features'] = drifted_features
            monitoring_results['summary']['total_features'] = len(data_drift_results)
            
        except Exception as e:
            logger.error(f"Error in data drift detection: {e}")
            monitoring_results['data_drift']['error'] = str(e)
        
        # Performance drift detection
        if current_performance:
            try:
                perf_drift_results = self.detect_performance_drift(current_performance)
                monitoring_results['performance_drift'] = {
                    metric: {
                        'drift_detected': result.drift_detected,
                        'drift_score': result.drift_score,
                        'details': result.details
                    }
                    for metric, result in perf_drift_results.items()
                }
                
                drifted_metrics = sum(1 for result in perf_drift_results.values() if result.drift_detected)
                monitoring_results['summary']['drifted_metrics'] = drifted_metrics
                
            except Exception as e:
                logger.error(f"Error in performance drift detection: {e}")
                monitoring_results['performance_drift']['error'] = str(e)
        
        # Concept drift detection
        if predictions is not None:
            try:
                concept_drift_result = self.detect_concept_drift(predictions)
                monitoring_results['concept_drift'] = {
                    'drift_detected': concept_drift_result.drift_detected,
                    'drift_score': concept_drift_result.drift_score,
                    'p_value': concept_drift_result.p_value,
                    'details': concept_drift_result.details
                }
                
            except Exception as e:
                logger.error(f"Error in concept drift detection: {e}")
                monitoring_results['concept_drift']['error'] = str(e)
        
        # Overall summary
        total_drifts = (
            monitoring_results['summary'].get('drifted_features', 0) +
            monitoring_results['summary'].get('drifted_metrics', 0) +
            (1 if monitoring_results['concept_drift'].get('drift_detected', False) else 0)
        )
        
        monitoring_results['summary']['total_drifts'] = total_drifts
        monitoring_results['summary']['overall_health'] = 'healthy' if total_drifts == 0 else 'warning' if total_drifts < 3 else 'critical'
        
        # Store results
        self._store_monitoring_results(monitoring_results)
        
        return monitoring_results
    
    def _store_monitoring_results(self, results: Dict[str, Any]):
        """Store monitoring results in database and cache."""
        # Store in database
        if self.db_engine:
            try:
                cursor = self.db_engine.cursor()
                
                # Insert monitoring record
                insert_query = """
                INSERT INTO model_monitoring_results (
                    model_name, timestamp, data_drift_count, performance_drift_count,
                    concept_drift_detected, overall_health, results_json
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                
                cursor.execute(insert_query, (
                    self.model_name,
                    results['timestamp'],
                    results['summary'].get('drifted_features', 0),
                    results['summary'].get('drifted_metrics', 0),
                    results['concept_drift'].get('drift_detected', False),
                    results['summary']['overall_health'],
                    json.dumps(results)
                ))
                
                self.db_engine.commit()
                cursor.close()
                
            except Exception as e:
                logger.error(f"Error storing monitoring results: {e}")
        
        # Cache latest results in Redis
        if self.redis_client:
            try:
                self.redis_client.set(
                    f"{self.model_name}:latest_monitoring",
                    json.dumps(results),
                    ex=86400  # Expire after 24 hours
                )
            except Exception as e:
                logger.error(f"Error caching monitoring results: {e}")
    
    def generate_monitoring_report(self) -> str:
        """Generate a human-readable monitoring report."""
        if self.redis_client:
            try:
                latest_results = self.redis_client.get(f"{self.model_name}:latest_monitoring")
                if latest_results:
                    results = json.loads(latest_results)
                    
                    report = f"""
# Model Monitoring Report - {self.model_name}

**Timestamp**: {results['timestamp']}
**Overall Health**: {results['summary']['overall_health'].upper()}

## Data Drift Summary
- **Total Features Checked**: {results['summary'].get('total_features', 0)}
- **Features with Drift**: {results['summary'].get('drifted_features', 0)}

## Performance Drift Summary
- **Metrics with Drift**: {results['summary'].get('drifted_metrics', 0)}

## Concept Drift
- **Detected**: {results['concept_drift'].get('drift_detected', False)}

## Recommendations
"""
                    
                    # Add recommendations based on results
                    total_drifts = results['summary']['total_drifts']
                    if total_drifts == 0:
                        report += "✅ No significant drift detected. Model is performing well.\n"
                    elif total_drifts < 3:
                        report += "⚠️  Minor drift detected. Consider monitoring more closely.\n"
                    else:
                        report += "🚨 Significant drift detected. Consider retraining the model.\n"
                    
                    return report
            except Exception as e:
                logger.error(f"Error generating monitoring report: {e}")
        
        return "No monitoring data available."


def main():
    """Example usage of the monitoring system."""
    # Initialize monitoring system
    monitor = ModelMonitoringSystem("churn-prediction-model")
    
    # Generate sample data
    np.random.seed(42)
    
    # Reference data
    reference_data = pd.DataFrame({
        'feature1': np.random.normal(0, 1, 1000),
        'feature2': np.random.normal(5, 2, 1000),
        'feature3': np.random.choice(['A', 'B', 'C'], 1000)
    })
    
    # Current data with some drift
    current_data = pd.DataFrame({
        'feature1': np.random.normal(0.5, 1.2, 500),  # Mean shift and variance change
        'feature2': np.random.normal(5, 2, 500),      # No drift
        'feature3': np.random.choice(['A', 'B', 'C', 'D'], 500)  # New category
    })
    
    # Set reference data
    reference_performance = PerformanceMetrics(
        accuracy=0.85,
        precision=0.82,
        recall=0.88,
        f1_score=0.85,
        timestamp=datetime.now().isoformat()
    )
    
    monitor.set_reference_data(reference_data, reference_performance)
    
    # Current performance (with some degradation)
    current_performance = PerformanceMetrics(
        accuracy=0.78,  # Degradation
        precision=0.80,
        recall=0.75,    # Degradation
        f1_score=0.77,  # Degradation
        timestamp=datetime.now().isoformat()
    )
    
    # Run monitoring
    results = monitor.run_comprehensive_monitoring(
        current_data=current_data,
        current_performance=current_performance,
        predictions=np.random.beta(0.3, 0.7, 500)  # Simulated predictions
    )
    
    # Print results
    print("Monitoring Results:")
    print(json.dumps(results, indent=2))
    
    # Generate report
    report = monitor.generate_monitoring_report()
    print("\nMonitoring Report:")
    print(report)


if __name__ == "__main__":
    main()
