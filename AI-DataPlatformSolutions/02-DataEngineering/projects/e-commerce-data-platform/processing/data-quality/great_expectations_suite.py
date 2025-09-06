"""
Great Expectations Data Quality Suite for E-Commerce Data Platform

This module implements comprehensive data quality monitoring and validation
using Great Expectations framework for all data sources in the platform.
"""

import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

import great_expectations as ge
from great_expectations.core.batch import RuntimeBatchRequest
from great_expectations.data_context import BaseDataContext
from great_expectations.data_context.types.base import DataContextConfig
from great_expectations.checkpoint import SimpleCheckpoint
from great_expectations.exceptions import DataContextError
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class ECommerceDataQualityValidator:
    """Comprehensive data quality validation for e-commerce data."""
    
    def __init__(self, data_context_root: str = "/opt/airflow/processing/data-quality"):
        """Initialize Great Expectations data context."""
        self.data_context_root = Path(data_context_root)
        self.data_context_root.mkdir(parents=True, exist_ok=True)
        
        # Initialize Great Expectations context
        self.context = self._initialize_context()
        
        # Data quality rules and thresholds
        self.quality_thresholds = {
            'completeness_threshold': 0.95,  # 95% completeness required
            'uniqueness_threshold': 0.99,    # 99% uniqueness for IDs
            'validity_threshold': 0.98,      # 98% valid values
            'consistency_threshold': 0.97,   # 97% consistency
            'freshness_threshold_hours': 24, # Data should be < 24 hours old
            'volume_change_threshold': 0.2   # Max 20% volume change
        }
        
        # Critical fields that must pass validation
        self.critical_fields = {
            'customers': ['customer_id', 'email'],
            'products': ['product_id', 'sku', 'price'],
            'orders': ['order_id', 'customer_id', 'total_amount'],
            'events': ['event_id', 'event_type', 'timestamp']
        }
    
    def _initialize_context(self) -> BaseDataContext:
        """Initialize Great Expectations data context."""
        try:
            # Check if context already exists
            context_path = self.data_context_root / "great_expectations"
            if context_path.exists():
                context = ge.data_context.DataContext(context_root_dir=str(context_path))
                logger.info("Loaded existing Great Expectations context")
            else:
                # Create new context
                context = ge.data_context.DataContext.create(str(context_path))
                logger.info("Created new Great Expectations context")
            
            return context
        except Exception as e:
            logger.error(f"Failed to initialize Great Expectations context: {str(e)}")
            raise
    
    def create_customer_expectations(self) -> str:
        """Create expectations for customer data."""
        suite_name = "customer_data_quality_suite"
        
        try:
            # Create or get expectation suite
            suite = self.context.create_expectation_suite(
                expectation_suite_name=suite_name,
                overwrite_existing=True
            )
            
            # Add expectations for customer data
            expectations = [
                # Table-level expectations
                {
                    "expectation_type": "expect_table_columns_to_match_ordered_list",
                    "kwargs": {
                        "column_list": [
                            "customer_id", "email", "first_name", "last_name", 
                            "phone", "date_of_birth", "gender", "registration_date",
                            "loyalty_tier", "total_spent", "last_login"
                        ]
                    }
                },
                {
                    "expectation_type": "expect_table_row_count_to_be_between",
                    "kwargs": {
                        "min_value": 100,
                        "max_value": 1000000
                    }
                },
                
                # Customer ID expectations
                {
                    "expectation_type": "expect_column_to_exist",
                    "kwargs": {"column": "customer_id"}
                },
                {
                    "expectation_type": "expect_column_values_to_not_be_null",
                    "kwargs": {"column": "customer_id"}
                },
                {
                    "expectation_type": "expect_column_values_to_be_unique",
                    "kwargs": {"column": "customer_id"}
                },
                {
                    "expectation_type": "expect_column_values_to_match_regex",
                    "kwargs": {
                        "column": "customer_id",
                        "regex": r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"
                    }
                },
                
                # Email expectations
                {
                    "expectation_type": "expect_column_values_to_not_be_null",
                    "kwargs": {"column": "email"}
                },
                {
                    "expectation_type": "expect_column_values_to_be_unique",
                    "kwargs": {"column": "email"}
                },
                {
                    "expectation_type": "expect_column_values_to_match_regex",
                    "kwargs": {
                        "column": "email",
                        "regex": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
                    }
                },
                
                # Name expectations
                {
                    "expectation_type": "expect_column_values_to_not_be_null",
                    "kwargs": {"column": "first_name"}
                },
                {
                    "expectation_type": "expect_column_value_lengths_to_be_between",
                    "kwargs": {
                        "column": "first_name",
                        "min_value": 1,
                        "max_value": 50
                    }
                },
                {
                    "expectation_type": "expect_column_values_to_not_be_null",
                    "kwargs": {"column": "last_name"}
                },
                
                # Gender expectations
                {
                    "expectation_type": "expect_column_values_to_be_in_set",
                    "kwargs": {
                        "column": "gender",
                        "value_set": ["M", "F", "Other"]
                    }
                },
                
                # Loyalty tier expectations
                {
                    "expectation_type": "expect_column_values_to_be_in_set",
                    "kwargs": {
                        "column": "loyalty_tier",
                        "value_set": ["Bronze", "Silver", "Gold", "Platinum"]
                    }
                },
                
                # Financial expectations
                {
                    "expectation_type": "expect_column_values_to_be_between",
                    "kwargs": {
                        "column": "total_spent",
                        "min_value": 0,
                        "max_value": 100000
                    }
                },
                
                # Date expectations
                {
                    "expectation_type": "expect_column_values_to_be_dateutil_parseable",
                    "kwargs": {"column": "registration_date"}
                },
                {
                    "expectation_type": "expect_column_values_to_be_dateutil_parseable",
                    "kwargs": {"column": "last_login"}
                }
            ]
            
            # Add expectations to suite
            for expectation in expectations:
                suite.add_expectation(**expectation)
            
            # Save suite
            self.context.save_expectation_suite(suite)
            logger.info(f"Created customer expectations suite: {suite_name}")
            
            return suite_name
            
        except Exception as e:
            logger.error(f"Failed to create customer expectations: {str(e)}")
            raise
    
    def create_product_expectations(self) -> str:
        """Create expectations for product data."""
        suite_name = "product_data_quality_suite"
        
        try:
            suite = self.context.create_expectation_suite(
                expectation_suite_name=suite_name,
                overwrite_existing=True
            )
            
            expectations = [
                # Table-level expectations
                {
                    "expectation_type": "expect_table_row_count_to_be_between",
                    "kwargs": {
                        "min_value": 50,
                        "max_value": 100000
                    }
                },
                
                # Product ID expectations
                {
                    "expectation_type": "expect_column_values_to_not_be_null",
                    "kwargs": {"column": "product_id"}
                },
                {
                    "expectation_type": "expect_column_values_to_be_unique",
                    "kwargs": {"column": "product_id"}
                },
                
                # SKU expectations
                {
                    "expectation_type": "expect_column_values_to_not_be_null",
                    "kwargs": {"column": "sku"}
                },
                {
                    "expectation_type": "expect_column_values_to_be_unique",
                    "kwargs": {"column": "sku"}
                },
                {
                    "expectation_type": "expect_column_values_to_match_regex",
                    "kwargs": {
                        "column": "sku",
                        "regex": r"^SKU-[0-9]{6}$"
                    }
                },
                
                # Product name expectations
                {
                    "expectation_type": "expect_column_values_to_not_be_null",
                    "kwargs": {"column": "name"}
                },
                {
                    "expectation_type": "expect_column_value_lengths_to_be_between",
                    "kwargs": {
                        "column": "name",
                        "min_value": 1,
                        "max_value": 255
                    }
                },
                
                # Category expectations
                {
                    "expectation_type": "expect_column_values_to_be_in_set",
                    "kwargs": {
                        "column": "category",
                        "value_set": ["Electronics", "Clothing", "Home & Garden", "Books", "Sports"]
                    }
                },
                
                # Price expectations
                {
                    "expectation_type": "expect_column_values_to_not_be_null",
                    "kwargs": {"column": "price"}
                },
                {
                    "expectation_type": "expect_column_values_to_be_between",
                    "kwargs": {
                        "column": "price",
                        "min_value": 0.01,
                        "max_value": 10000
                    }
                },
                
                # Cost expectations
                {
                    "expectation_type": "expect_column_values_to_be_between",
                    "kwargs": {
                        "column": "cost",
                        "min_value": 0,
                        "max_value": 5000
                    }
                },
                
                # Inventory expectations
                {
                    "expectation_type": "expect_column_values_to_be_between",
                    "kwargs": {
                        "column": "inventory.stock_quantity",
                        "min_value": 0,
                        "max_value": 10000
                    }
                },
                
                # Rating expectations
                {
                    "expectation_type": "expect_column_values_to_be_between",
                    "kwargs": {
                        "column": "rating",
                        "min_value": 1.0,
                        "max_value": 5.0
                    }
                },
                
                # Boolean expectations
                {
                    "expectation_type": "expect_column_values_to_be_in_set",
                    "kwargs": {
                        "column": "is_active",
                        "value_set": [True, False]
                    }
                }
            ]
            
            for expectation in expectations:
                suite.add_expectation(**expectation)
            
            self.context.save_expectation_suite(suite)
            logger.info(f"Created product expectations suite: {suite_name}")
            
            return suite_name
            
        except Exception as e:
            logger.error(f"Failed to create product expectations: {str(e)}")
            raise
    
    def create_order_expectations(self) -> str:
        """Create expectations for order data."""
        suite_name = "order_data_quality_suite"
        
        try:
            suite = self.context.create_expectation_suite(
                expectation_suite_name=suite_name,
                overwrite_existing=True
            )
            
            expectations = [
                # Order ID expectations
                {
                    "expectation_type": "expect_column_values_to_not_be_null",
                    "kwargs": {"column": "order_id"}
                },
                {
                    "expectation_type": "expect_column_values_to_be_unique",
                    "kwargs": {"column": "order_id"}
                },
                
                # Customer ID expectations
                {
                    "expectation_type": "expect_column_values_to_not_be_null",
                    "kwargs": {"column": "customer_id"}
                },
                
                # Amount expectations
                {
                    "expectation_type": "expect_column_values_to_not_be_null",
                    "kwargs": {"column": "total_amount"}
                },
                {
                    "expectation_type": "expect_column_values_to_be_between",
                    "kwargs": {
                        "column": "total_amount",
                        "min_value": 0.01,
                        "max_value": 50000
                    }
                },
                {
                    "expectation_type": "expect_column_values_to_be_between",
                    "kwargs": {
                        "column": "subtotal",
                        "min_value": 0.01,
                        "max_value": 50000
                    }
                },
                
                # Status expectations
                {
                    "expectation_type": "expect_column_values_to_be_in_set",
                    "kwargs": {
                        "column": "order_status",
                        "value_set": ["pending", "processing", "shipped", "delivered", "cancelled", "returned"]
                    }
                },
                {
                    "expectation_type": "expect_column_values_to_be_in_set",
                    "kwargs": {
                        "column": "payment_status",
                        "value_set": ["pending", "completed", "failed", "refunded"]
                    }
                },
                
                # Payment method expectations
                {
                    "expectation_type": "expect_column_values_to_be_in_set",
                    "kwargs": {
                        "column": "payment_method",
                        "value_set": ["credit_card", "debit_card", "paypal", "apple_pay", "google_pay"]
                    }
                },
                
                # Date expectations
                {
                    "expectation_type": "expect_column_values_to_be_dateutil_parseable",
                    "kwargs": {"column": "order_date"}
                },
                
                # Items expectations
                {
                    "expectation_type": "expect_column_values_to_not_be_null",
                    "kwargs": {"column": "items"}
                }
            ]
            
            for expectation in expectations:
                suite.add_expectation(**expectation)
            
            self.context.save_expectation_suite(suite)
            logger.info(f"Created order expectations suite: {suite_name}")
            
            return suite_name
            
        except Exception as e:
            logger.error(f"Failed to create order expectations: {str(e)}")
            raise
    
    def create_event_expectations(self) -> str:
        """Create expectations for event data."""
        suite_name = "event_data_quality_suite"
        
        try:
            suite = self.context.create_expectation_suite(
                expectation_suite_name=suite_name,
                overwrite_existing=True
            )
            
            expectations = [
                # Event ID expectations
                {
                    "expectation_type": "expect_column_values_to_not_be_null",
                    "kwargs": {"column": "event_id"}
                },
                {
                    "expectation_type": "expect_column_values_to_be_unique",
                    "kwargs": {"column": "event_id"}
                },
                
                # Event type expectations
                {
                    "expectation_type": "expect_column_values_to_not_be_null",
                    "kwargs": {"column": "event_type"}
                },
                {
                    "expectation_type": "expect_column_values_to_be_in_set",
                    "kwargs": {
                        "column": "event_type",
                        "value_set": [
                            "page_view", "product_view", "add_to_cart", "remove_from_cart",
                            "search", "login", "logout", "checkout_start", "checkout_complete",
                            "wishlist_add", "review_submit", "share_product"
                        ]
                    }
                },
                
                # Customer ID expectations
                {
                    "expectation_type": "expect_column_values_to_not_be_null",
                    "kwargs": {"column": "customer_id"}
                },
                
                # Session ID expectations
                {
                    "expectation_type": "expect_column_values_to_not_be_null",
                    "kwargs": {"column": "session_id"}
                },
                
                # Timestamp expectations
                {
                    "expectation_type": "expect_column_values_to_not_be_null",
                    "kwargs": {"column": "timestamp"}
                },
                {
                    "expectation_type": "expect_column_values_to_be_dateutil_parseable",
                    "kwargs": {"column": "timestamp"}
                },
                
                # IP address expectations
                {
                    "expectation_type": "expect_column_values_to_match_regex",
                    "kwargs": {
                        "column": "ip_address",
                        "regex": r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
                    }
                }
            ]
            
            for expectation in expectations:
                suite.add_expectation(**expectation)
            
            self.context.save_expectation_suite(suite)
            logger.info(f"Created event expectations suite: {suite_name}")
            
            return suite_name
            
        except Exception as e:
            logger.error(f"Failed to create event expectations: {str(e)}")
            raise
    
    def validate_data(self, data_path: str, data_type: str, file_format: str = "parquet") -> Dict[str, Any]:
        """Validate data against expectations."""
        try:
            # Determine suite name based on data type
            suite_mapping = {
                'customers': 'customer_data_quality_suite',
                'products': 'product_data_quality_suite',
                'orders': 'order_data_quality_suite',
                'events': 'event_data_quality_suite'
            }
            
            suite_name = suite_mapping.get(data_type)
            if not suite_name:
                raise ValueError(f"Unknown data type: {data_type}")
            
            # Create datasource
            datasource_name = f"{data_type}_datasource"
            try:
                datasource = self.context.get_datasource(datasource_name)
            except DataContextError:
                datasource_config = {
                    "name": datasource_name,
                    "class_name": "Datasource",
                    "module_name": "great_expectations.datasource",
                    "execution_engine": {
                        "module_name": "great_expectations.execution_engine",
                        "class_name": "PandasExecutionEngine"
                    },
                    "data_connectors": {
                        "default_inferred_data_connector": {
                            "class_name": "InferredAssetFilesystemDataConnector",
                            "base_directory": str(Path(data_path).parent),
                            "default_regex": {
                                "group_names": ["data_asset_name"],
                                "pattern": f"({Path(data_path).name})"
                            }
                        }
                    }
                }
                datasource = self.context.add_datasource(**datasource_config)
            
            # Create batch request
            batch_request = RuntimeBatchRequest(
                datasource_name=datasource_name,
                data_connector_name="default_inferred_data_connector",
                data_asset_name=Path(data_path).name.split('.')[0],
                runtime_parameters={"path": data_path},
                batch_identifiers={"default_identifier_name": "default_identifier"}
            )
            
            # Create checkpoint
            checkpoint_name = f"{data_type}_checkpoint"
            checkpoint_config = {
                "name": checkpoint_name,
                "config_version": 1.0,
                "template_name": None,
                "module_name": "great_expectations.checkpoint",
                "class_name": "SimpleCheckpoint",
                "run_name_template": f"{data_type}_validation_%Y%m%d_%H%M%S",
                "expectation_suite_name": suite_name,
                "batch_request": batch_request,
                "action_list": [
                    {
                        "name": "store_validation_result",
                        "action": {"class_name": "StoreValidationResultAction"},
                    }
                ]
            }
            
            checkpoint = SimpleCheckpoint(
                f"{data_type}_checkpoint",
                self.context,
                **checkpoint_config
            )
            
            # Run validation
            results = checkpoint.run()
            
            # Extract validation results
            validation_result = results.list_validation_results()[0]
            
            # Process results
            success = validation_result.success
            statistics = validation_result.statistics
            
            # Calculate quality metrics
            total_expectations = statistics.get('evaluated_expectations', 0)
            successful_expectations = statistics.get('successful_expectations', 0)
            success_rate = (successful_expectations / total_expectations * 100) if total_expectations > 0 else 0
            
            # Extract failed expectations
            failed_expectations = []
            for result in validation_result.results:
                if not result.success:
                    failed_expectations.append({
                        'expectation_type': result.expectation_config.expectation_type,
                        'column': result.expectation_config.kwargs.get('column', 'N/A'),
                        'result': result.result
                    })
            
            validation_summary = {
                'data_type': data_type,
                'data_path': data_path,
                'validation_time': datetime.utcnow().isoformat(),
                'overall_success': success,
                'success_rate': round(success_rate, 2),
                'total_expectations': total_expectations,
                'successful_expectations': successful_expectations,
                'failed_expectations_count': len(failed_expectations),
                'failed_expectations': failed_expectations[:10],  # Limit to first 10
                'statistics': statistics,
                'quality_score': self._calculate_quality_score(validation_result)
            }
            
            logger.info(f"Validation completed for {data_type}: {success_rate:.1f}% success rate")
            
            return validation_summary
            
        except Exception as e:
            logger.error(f"Validation failed for {data_type}: {str(e)}")
            raise
    
    def _calculate_quality_score(self, validation_result) -> float:
        """Calculate overall data quality score."""
        try:
            stats = validation_result.statistics
            total = stats.get('evaluated_expectations', 0)
            successful = stats.get('successful_expectations', 0)
            
            if total == 0:
                return 0.0
            
            # Base score from success rate
            base_score = (successful / total) * 100
            
            # Apply penalties for critical field failures
            critical_penalty = 0
            for result in validation_result.results:
                if not result.success:
                    column = result.expectation_config.kwargs.get('column', '')
                    expectation_type = result.expectation_config.expectation_type
                    
                    # Heavy penalty for critical field failures
                    if any(critical in column for critical in ['_id', 'email', 'price', 'amount']):
                        critical_penalty += 10
                    
                    # Penalty for null values in important columns
                    if 'not_be_null' in expectation_type:
                        critical_penalty += 5
                    
                    # Penalty for uniqueness violations
                    if 'unique' in expectation_type:
                        critical_penalty += 8
            
            final_score = max(0, base_score - critical_penalty)
            return round(final_score, 2)
            
        except Exception as e:
            logger.error(f"Failed to calculate quality score: {str(e)}")
            return 0.0
    
    def run_full_validation_suite(self, data_directory: str) -> Dict[str, Any]:
        """Run validation on all data types."""
        logger.info("Starting full data quality validation suite...")
        
        # Create all expectation suites
        self.create_customer_expectations()
        self.create_product_expectations()
        self.create_order_expectations()
        self.create_event_expectations()
        
        # Run validations
        validation_results = {}
        data_files = {
            'customers': f"{data_directory}/customers.parquet",
            'products': f"{data_directory}/products.parquet",
            'orders': f"{data_directory}/orders.parquet",
            'events': f"{data_directory}/events.parquet"
        }
        
        overall_success = True
        total_quality_score = 0
        
        for data_type, file_path in data_files.items():
            if Path(file_path).exists():
                try:
                    result = self.validate_data(file_path, data_type)
                    validation_results[data_type] = result
                    
                    if not result['overall_success']:
                        overall_success = False
                    
                    total_quality_score += result['quality_score']
                    
                except Exception as e:
                    logger.error(f"Validation failed for {data_type}: {str(e)}")
                    validation_results[data_type] = {
                        'error': str(e),
                        'overall_success': False,
                        'quality_score': 0
                    }
                    overall_success = False
            else:
                logger.warning(f"Data file not found: {file_path}")
                validation_results[data_type] = {
                    'error': 'File not found',
                    'overall_success': False,
                    'quality_score': 0
                }
                overall_success = False
        
        # Calculate overall metrics
        avg_quality_score = total_quality_score / len(data_files) if data_files else 0
        
        summary = {
            'validation_time': datetime.utcnow().isoformat(),
            'overall_success': overall_success,
            'average_quality_score': round(avg_quality_score, 2),
            'data_validation_results': validation_results,
            'recommendations': self._generate_recommendations(validation_results)
        }
        
        logger.info(f"Full validation suite completed. Overall success: {overall_success}")
        logger.info(f"Average quality score: {avg_quality_score:.1f}")
        
        return summary
    
    def _generate_recommendations(self, validation_results: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on validation results."""
        recommendations = []
        
        for data_type, result in validation_results.items():
            if isinstance(result, dict) and 'quality_score' in result:
                score = result['quality_score']
                
                if score < 80:
                    recommendations.append(f"CRITICAL: {data_type} data quality is poor (score: {score}). Immediate attention required.")
                elif score < 90:
                    recommendations.append(f"WARNING: {data_type} data quality needs improvement (score: {score}).")
                
                if 'failed_expectations' in result and result['failed_expectations']:
                    failed_count = result['failed_expectations_count']
                    recommendations.append(f"Review {failed_count} failed expectations for {data_type} data.")
        
        if not recommendations:
            recommendations.append("All data quality checks passed. Data is ready for processing.")
        
        return recommendations


def main():
    """Main function to run data quality validation."""
    validator = ECommerceDataQualityValidator()
    
    # Run validation on sample data
    data_directory = "/opt/airflow/data-sources/sample-data"
    results = validator.run_full_validation_suite(data_directory)
    
    # Print summary
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
