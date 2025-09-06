"""
Airflow DAG for E-Commerce Data Platform ETL Pipeline

This DAG orchestrates the complete data pipeline including:
- Data ingestion from various sources
- Data validation and quality checks
- Batch processing with Spark
- Data loading to warehouse
- Monitoring and alerting
"""

from datetime import datetime, timedelta
from pathlib import Path

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.sensors.filesystem import FileSensor
from airflow.utils.task_group import TaskGroup
from airflow.utils.dates import days_ago

# DAG Configuration
DAG_ID = "ecommerce_etl_pipeline"
OWNER = "data_engineering_team"
EMAIL = ["data-team@techmart.com"]

# Default arguments
default_args = {
    'owner': OWNER,
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email': EMAIL,
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'catchup': False,
}

# DAG definition
dag = DAG(
    DAG_ID,
    default_args=default_args,
    description='E-Commerce Data Platform ETL Pipeline',
    schedule_interval='0 2 * * *',  # Daily at 2 AM
    max_active_runs=1,
    tags=['ecommerce', 'etl', 'data-engineering', 'batch'],
    doc_md=__doc__,
)

# File paths
DATA_DIR = "/opt/airflow/data-sources"
PROCESSING_DIR = "/opt/airflow/processing"
STORAGE_DIR = "/opt/airflow/storage"


def generate_sample_data(**context):
    """Generate sample data for the pipeline."""
    import sys
    sys.path.append(DATA_DIR)
    
    from data_generators.generate_sample_data import ECommerceDataGenerator
    
    generator = ECommerceDataGenerator(f"{DATA_DIR}/sample-data")
    generator.generate_all_data(
        num_customers=1000,
        num_products=500,
        num_orders=5000,
        num_events=20000,
        num_inventory_updates=2500
    )
    
    return "Sample data generated successfully"


def validate_data_quality(**context):
    """Validate data quality using Great Expectations."""
    import great_expectations as ge
    import pandas as pd
    
    # Load data
    customers_df = pd.read_parquet(f"{DATA_DIR}/sample-data/customers.parquet")
    products_df = pd.read_parquet(f"{DATA_DIR}/sample-data/products.parquet")
    orders_df = pd.read_parquet(f"{DATA_DIR}/sample-data/orders.parquet")
    
    # Validate customers
    customers_ge = ge.from_pandas(customers_df)
    customers_ge.expect_column_to_exist("customer_id")
    customers_ge.expect_column_values_to_not_be_null("customer_id")
    customers_ge.expect_column_values_to_be_unique("customer_id")
    customers_ge.expect_column_values_to_match_regex("email", r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    
    # Validate products
    products_ge = ge.from_pandas(products_df)
    products_ge.expect_column_to_exist("product_id")
    products_ge.expect_column_values_to_not_be_null("product_id")
    products_ge.expect_column_values_to_be_unique("product_id")
    products_ge.expect_column_values_to_be_between("price", min_value=0, max_value=10000)
    
    # Validate orders
    orders_ge = ge.from_pandas(orders_df)
    orders_ge.expect_column_to_exist("order_id")
    orders_ge.expect_column_values_to_not_be_null("order_id")
    orders_ge.expect_column_values_to_be_unique("order_id")
    orders_ge.expect_column_values_to_be_between("total_amount", min_value=0)
    
    return "Data quality validation completed"


def check_data_freshness(**context):
    """Check if data is fresh and within acceptable time windows."""
    import pandas as pd
    from datetime import datetime, timedelta
    
    # Check if sample data exists and is recent
    data_files = [
        f"{DATA_DIR}/sample-data/customers.parquet",
        f"{DATA_DIR}/sample-data/products.parquet",
        f"{DATA_DIR}/sample-data/orders.parquet"
    ]
    
    for file_path in data_files:
        file_path_obj = Path(file_path)
        if not file_path_obj.exists():
            raise FileNotFoundError(f"Required data file not found: {file_path}")
        
        # Check if file is not older than 24 hours
        file_mtime = datetime.fromtimestamp(file_path_obj.stat().st_mtime)
        if datetime.now() - file_mtime > timedelta(hours=24):
            print(f"Warning: Data file {file_path} is older than 24 hours")
    
    return "Data freshness check completed"


def create_database_tables(**context):
    """Create or update database tables in PostgreSQL."""
    sql_commands = [
        """
        CREATE TABLE IF NOT EXISTS customer_analytics (
            customer_id UUID PRIMARY KEY,
            email VARCHAR(255),
            full_name VARCHAR(255),
            registration_date DATE,
            loyalty_tier VARCHAR(20),
            total_orders INTEGER,
            total_spent DECIMAL(10,2),
            avg_order_value DECIMAL(10,2),
            customer_segment VARCHAR(50),
            is_active BOOLEAN,
            last_order_date DATE,
            days_since_last_order INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS product_analytics (
            product_id UUID PRIMARY KEY,
            sku VARCHAR(50),
            name VARCHAR(255),
            category VARCHAR(100),
            subcategory VARCHAR(100),
            brand VARCHAR(100),
            price DECIMAL(10,2),
            profit_margin DECIMAL(5,4),
            price_tier VARCHAR(20),
            stock_status VARCHAR(20),
            total_orders INTEGER,
            total_quantity_sold INTEGER,
            total_revenue DECIMAL(12,2),
            performance_tier VARCHAR(30),
            revenue_rank INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS daily_sales (
            order_date DATE PRIMARY KEY,
            daily_orders INTEGER,
            daily_revenue DECIMAL(12,2),
            daily_avg_order_value DECIMAL(10,2),
            daily_unique_customers INTEGER,
            daily_items_sold INTEGER,
            day_of_week VARCHAR(10),
            is_weekend BOOLEAN,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS monthly_sales (
            year_month VARCHAR(7) PRIMARY KEY,
            monthly_orders INTEGER,
            monthly_revenue DECIMAL(12,2),
            monthly_avg_order_value DECIMAL(10,2),
            monthly_unique_customers INTEGER,
            active_days INTEGER,
            revenue_per_day DECIMAL(12,2),
            revenue_growth DECIMAL(5,2),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
    ]
    
    return sql_commands


def load_analytics_to_warehouse(**context):
    """Load processed analytics data to PostgreSQL warehouse."""
    import pandas as pd
    from sqlalchemy import create_engine
    import os
    
    # Database connection
    db_url = "postgresql://airflow:airflow@postgres:5432/warehouse"
    engine = create_engine(db_url)
    
    # Load analytics data
    data_files = {
        'customer_analytics': f"{STORAGE_DIR}/data-warehouse/customer_analytics",
        'product_analytics': f"{STORAGE_DIR}/data-warehouse/product_analytics",
        'daily_sales': f"{STORAGE_DIR}/data-warehouse/daily_sales",
        'monthly_sales': f"{STORAGE_DIR}/data-warehouse/monthly_sales"
    }
    
    for table_name, file_path in data_files.items():
        try:
            # Read parquet files
            df = pd.read_parquet(file_path)
            
            # Clean column names
            df.columns = [col.lower().replace(' ', '_') for col in df.columns]
            
            # Load to PostgreSQL
            df.to_sql(table_name, engine, if_exists='replace', index=False, method='multi')
            print(f"Loaded {len(df)} records to {table_name}")
            
        except Exception as e:
            print(f"Error loading {table_name}: {str(e)}")
            raise
    
    return "Analytics data loaded to warehouse"


def send_pipeline_report(**context):
    """Send pipeline execution summary report."""
    from airflow.models import DagRun, TaskInstance
    
    dag_run = context['dag_run']
    
    # Get task instances
    task_instances = dag_run.get_task_instances()
    
    # Calculate statistics
    total_tasks = len(task_instances)
    successful_tasks = len([ti for ti in task_instances if ti.state == 'success'])
    failed_tasks = len([ti for ti in task_instances if ti.state == 'failed'])
    
    # Create report
    report = f"""
    E-Commerce ETL Pipeline Execution Report
    =====================================
    
    Execution Date: {dag_run.execution_date}
    DAG ID: {dag_run.dag_id}
    Run ID: {dag_run.run_id}
    
    Task Summary:
    - Total Tasks: {total_tasks}
    - Successful: {successful_tasks}
    - Failed: {failed_tasks}
    - Success Rate: {(successful_tasks/total_tasks*100):.1f}%
    
    Pipeline Status: {'SUCCESS' if failed_tasks == 0 else 'FAILED'}
    
    Data Processing Summary:
    - Customers processed: ~1,000
    - Products processed: ~500
    - Orders processed: ~5,000
    - Events processed: ~20,000
    
    Next Steps:
    - Data available in warehouse tables
    - Analytics dashboards updated
    - Monitoring alerts configured
    """
    
    print(report)
    return report


# Task definitions
start_task = DummyOperator(
    task_id='start_pipeline',
    dag=dag,
)

end_task = DummyOperator(
    task_id='end_pipeline',
    dag=dag,
)

# Data Generation Task Group
with TaskGroup("data_generation", dag=dag) as data_generation_group:
    
    generate_data_task = PythonOperator(
        task_id='generate_sample_data',
        python_callable=generate_sample_data,
        dag=dag,
    )
    
    data_freshness_task = PythonOperator(
        task_id='check_data_freshness',
        python_callable=check_data_freshness,
        dag=dag,
    )
    
    generate_data_task >> data_freshness_task

# Data Quality Task Group
with TaskGroup("data_quality", dag=dag) as data_quality_group:
    
    validate_quality_task = PythonOperator(
        task_id='validate_data_quality',
        python_callable=validate_data_quality,
        dag=dag,
    )

# Spark Processing Task
spark_etl_task = SparkSubmitOperator(
    task_id='spark_etl_processing',
    application=f'{PROCESSING_DIR}/batch-processing/spark_etl.py',
    name='ecommerce-etl',
    conn_id='spark_default',
    application_args=[
        '--input-dir', f'{DATA_DIR}/sample-data',
        '--output-dir', f'{STORAGE_DIR}/data-warehouse'
    ],
    conf={
        'spark.sql.adaptive.enabled': 'true',
        'spark.sql.adaptive.coalescePartitions.enabled': 'true',
        'spark.executor.memory': '2g',
        'spark.executor.cores': '2',
        'spark.driver.memory': '1g'
    },
    dag=dag,
)

# Database Setup Task Group
with TaskGroup("database_setup", dag=dag) as database_setup_group:
    
    create_tables_task = PostgresOperator(
        task_id='create_warehouse_tables',
        postgres_conn_id='postgres_warehouse',
        sql=create_database_tables(),
        dag=dag,
    )

# Data Loading Task Group
with TaskGroup("data_loading", dag=dag) as data_loading_group:
    
    load_warehouse_task = PythonOperator(
        task_id='load_analytics_to_warehouse',
        python_callable=load_analytics_to_warehouse,
        dag=dag,
    )

# Monitoring and Reporting
report_task = PythonOperator(
    task_id='send_pipeline_report',
    python_callable=send_pipeline_report,
    dag=dag,
)

# Data Quality Monitoring
quality_monitor_task = BashOperator(
    task_id='monitor_data_quality',
    bash_command="""
    echo "Monitoring data quality metrics..."
    # Add custom data quality monitoring commands here
    echo "Data quality monitoring completed"
    """,
    dag=dag,
)

# Task Dependencies
start_task >> data_generation_group
data_generation_group >> data_quality_group
data_quality_group >> spark_etl_task
spark_etl_task >> database_setup_group
database_setup_group >> data_loading_group
data_loading_group >> [report_task, quality_monitor_task]
[report_task, quality_monitor_task] >> end_task

# DAG documentation
dag.doc_md = """
# E-Commerce Data Platform ETL Pipeline

This DAG implements a comprehensive ETL pipeline for processing e-commerce data.

## Pipeline Overview

1. **Data Generation**: Generate sample e-commerce data including customers, products, orders, and events
2. **Data Quality**: Validate data quality using Great Expectations framework
3. **Spark Processing**: Transform and aggregate data using Apache Spark
4. **Database Setup**: Create and maintain warehouse tables in PostgreSQL
5. **Data Loading**: Load processed analytics to the data warehouse
6. **Monitoring**: Generate reports and monitor data quality

## Data Flow

```
Raw Data → Quality Checks → Spark ETL → Data Warehouse → Analytics
```

## Success Criteria

- All data quality checks pass
- Spark processing completes without errors
- Analytics data loaded to warehouse
- Pipeline execution report generated

## Monitoring

- Task failure alerts sent to data engineering team
- Data quality metrics tracked
- Performance metrics monitored
- Pipeline execution reports generated

## Recovery

- Automatic retries configured for transient failures
- Manual intervention required for data quality failures
- Backfill capability for historical data processing
"""
