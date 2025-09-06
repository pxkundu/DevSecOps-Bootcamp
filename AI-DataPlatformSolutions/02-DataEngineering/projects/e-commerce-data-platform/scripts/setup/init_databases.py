#!/usr/bin/env python3
"""
Database Initialization Script for E-Commerce Data Platform

This script initializes all required databases, tables, and initial data
for the e-commerce data platform.
"""

import logging
import os
import sys
import time
from pathlib import Path

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import redis

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class DatabaseInitializer:
    """Initialize databases and create required schemas."""
    
    def __init__(self):
        """Initialize database connection parameters."""
        self.postgres_config = {
            'host': os.getenv('POSTGRES_HOST', 'localhost'),
            'port': int(os.getenv('POSTGRES_PORT', 5432)),
            'user': os.getenv('POSTGRES_USER', 'airflow'),
            'password': os.getenv('POSTGRES_PASSWORD', 'airflow'),
            'database': os.getenv('POSTGRES_DB', 'postgres')
        }
        
        self.redis_config = {
            'host': os.getenv('REDIS_HOST', 'localhost'),
            'port': int(os.getenv('REDIS_PORT', 6379)),
            'password': os.getenv('REDIS_PASSWORD', None)
        }
    
    def wait_for_postgres(self, max_retries: int = 30):
        """Wait for PostgreSQL to be ready."""
        for attempt in range(max_retries):
            try:
                conn = psycopg2.connect(**self.postgres_config)
                conn.close()
                logger.info("PostgreSQL is ready!")
                return True
            except psycopg2.OperationalError:
                logger.info(f"Waiting for PostgreSQL... (attempt {attempt + 1}/{max_retries})")
                time.sleep(5)
        
        logger.error("PostgreSQL did not become ready in time")
        return False
    
    def wait_for_redis(self, max_retries: int = 30):
        """Wait for Redis to be ready."""
        for attempt in range(max_retries):
            try:
                r = redis.Redis(**self.redis_config)
                r.ping()
                logger.info("Redis is ready!")
                return True
            except (redis.ConnectionError, redis.TimeoutError):
                logger.info(f"Waiting for Redis... (attempt {attempt + 1}/{max_retries})")
                time.sleep(5)
        
        logger.error("Redis did not become ready in time")
        return False
    
    def create_databases(self):
        """Create required databases."""
        databases_to_create = [
            'warehouse',
            'ecommerce',
            'metadata',
            'feature_store'
        ]
        
        try:
            # Connect to default postgres database
            conn = psycopg2.connect(**self.postgres_config)
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = conn.cursor()
            
            for db_name in databases_to_create:
                try:
                    # Check if database exists
                    cursor.execute(
                        "SELECT 1 FROM pg_database WHERE datname = %s",
                        (db_name,)
                    )
                    
                    if cursor.fetchone():
                        logger.info(f"Database '{db_name}' already exists")
                    else:
                        # Create database
                        cursor.execute(f'CREATE DATABASE "{db_name}"')
                        logger.info(f"Created database '{db_name}'")
                        
                except psycopg2.Error as e:
                    logger.error(f"Error creating database '{db_name}': {e}")
            
            cursor.close()
            conn.close()
            
        except psycopg2.Error as e:
            logger.error(f"Error connecting to PostgreSQL: {e}")
            raise
    
    def create_users(self):
        """Create database users with appropriate permissions."""
        users_to_create = [
            {
                'username': 'dataeng',
                'password': 'dataeng123',
                'databases': ['warehouse', 'ecommerce', 'metadata', 'feature_store']
            },
            {
                'username': 'readonly',
                'password': 'readonly123',
                'databases': ['warehouse', 'ecommerce'],
                'readonly': True
            },
            {
                'username': 'analyst',
                'password': 'analyst123',
                'databases': ['warehouse'],
                'readonly': True
            }
        ]
        
        try:
            conn = psycopg2.connect(**self.postgres_config)
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = conn.cursor()
            
            for user_config in users_to_create:
                username = user_config['username']
                password = user_config['password']
                databases = user_config['databases']
                readonly = user_config.get('readonly', False)
                
                # Check if user exists
                cursor.execute(
                    "SELECT 1 FROM pg_user WHERE usename = %s",
                    (username,)
                )
                
                if cursor.fetchone():
                    logger.info(f"User '{username}' already exists")
                else:
                    # Create user
                    cursor.execute(
                        f"CREATE USER {username} WITH PASSWORD %s",
                        (password,)
                    )
                    logger.info(f"Created user '{username}'")
                
                # Grant permissions
                for db_name in databases:
                    if readonly:
                        cursor.execute(f"GRANT CONNECT ON DATABASE {db_name} TO {username}")
                        # Grant usage on schema and select on tables (done later in create_tables)
                    else:
                        cursor.execute(f"GRANT ALL PRIVILEGES ON DATABASE {db_name} TO {username}")
                    
                    logger.info(f"Granted permissions on '{db_name}' to '{username}'")
            
            cursor.close()
            conn.close()
            
        except psycopg2.Error as e:
            logger.error(f"Error creating users: {e}")
            raise
    
    def create_warehouse_tables(self):
        """Create data warehouse tables."""
        warehouse_config = {**self.postgres_config, 'database': 'warehouse'}
        
        tables_sql = [
            """
            CREATE TABLE IF NOT EXISTS dim_customers (
                customer_id UUID PRIMARY KEY,
                customer_key SERIAL UNIQUE,
                email VARCHAR(255) NOT NULL,
                first_name VARCHAR(100),
                last_name VARCHAR(100),
                full_name VARCHAR(255),
                phone VARCHAR(50),
                date_of_birth DATE,
                gender VARCHAR(10),
                registration_date DATE,
                address_street VARCHAR(255),
                address_city VARCHAR(100),
                address_state VARCHAR(100),
                address_zip VARCHAR(20),
                address_country VARCHAR(10),
                loyalty_tier VARCHAR(20),
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS dim_products (
                product_id UUID PRIMARY KEY,
                product_key SERIAL UNIQUE,
                sku VARCHAR(50) UNIQUE NOT NULL,
                name VARCHAR(255) NOT NULL,
                description TEXT,
                category VARCHAR(100),
                subcategory VARCHAR(100),
                brand VARCHAR(100),
                price DECIMAL(10,2),
                cost DECIMAL(10,2),
                weight DECIMAL(8,2),
                length DECIMAL(8,2),
                width DECIMAL(8,2),
                height DECIMAL(8,2),
                rating DECIMAL(3,2),
                review_count INTEGER,
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS dim_date (
                date_key INTEGER PRIMARY KEY,
                date_value DATE UNIQUE NOT NULL,
                year INTEGER,
                quarter INTEGER,
                month INTEGER,
                month_name VARCHAR(20),
                day INTEGER,
                day_of_week INTEGER,
                day_name VARCHAR(20),
                week_of_year INTEGER,
                is_weekend BOOLEAN,
                is_holiday BOOLEAN DEFAULT FALSE,
                fiscal_year INTEGER,
                fiscal_quarter INTEGER
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS fact_orders (
                order_id UUID PRIMARY KEY,
                customer_key INTEGER REFERENCES dim_customers(customer_key),
                order_date_key INTEGER REFERENCES dim_date(date_key),
                order_date TIMESTAMP,
                order_status VARCHAR(50),
                payment_method VARCHAR(50),
                payment_status VARCHAR(50),
                subtotal DECIMAL(12,2),
                shipping_cost DECIMAL(8,2),
                tax_amount DECIMAL(8,2),
                discount_amount DECIMAL(8,2),
                total_amount DECIMAL(12,2),
                items_count INTEGER,
                currency VARCHAR(3) DEFAULT 'USD',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS fact_order_items (
                order_item_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                order_id UUID REFERENCES fact_orders(order_id),
                product_key INTEGER REFERENCES dim_products(product_key),
                quantity INTEGER,
                unit_price DECIMAL(10,2),
                line_total DECIMAL(12,2),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS fact_events (
                event_id UUID PRIMARY KEY,
                customer_key INTEGER REFERENCES dim_customers(customer_key),
                product_key INTEGER REFERENCES dim_products(product_key),
                event_date_key INTEGER REFERENCES dim_date(date_key),
                event_timestamp TIMESTAMP,
                event_type VARCHAR(50),
                session_id UUID,
                page_url VARCHAR(500),
                referrer VARCHAR(500),
                user_agent VARCHAR(500),
                ip_address INET,
                device_type VARCHAR(20),
                search_query VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS customer_analytics (
                customer_key INTEGER PRIMARY KEY REFERENCES dim_customers(customer_key),
                total_orders INTEGER DEFAULT 0,
                total_spent DECIMAL(12,2) DEFAULT 0,
                avg_order_value DECIMAL(10,2) DEFAULT 0,
                max_order_value DECIMAL(10,2) DEFAULT 0,
                min_order_value DECIMAL(10,2) DEFAULT 0,
                first_order_date DATE,
                last_order_date DATE,
                days_since_last_order INTEGER,
                customer_lifetime_days INTEGER,
                order_frequency DECIMAL(8,4),
                customer_segment VARCHAR(50),
                total_events INTEGER DEFAULT 0,
                last_event_date DATE,
                preferred_category VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS product_analytics (
                product_key INTEGER PRIMARY KEY REFERENCES dim_products(product_key),
                total_orders INTEGER DEFAULT 0,
                total_quantity_sold INTEGER DEFAULT 0,
                total_revenue DECIMAL(12,2) DEFAULT 0,
                avg_selling_price DECIMAL(10,2) DEFAULT 0,
                unique_customers INTEGER DEFAULT 0,
                first_sale_date DATE,
                last_sale_date DATE,
                days_since_last_sale INTEGER,
                sales_velocity DECIMAL(10,4),
                revenue_rank INTEGER,
                performance_tier VARCHAR(30),
                stock_quantity INTEGER DEFAULT 0,
                stock_status VARCHAR(20),
                reorder_point INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS daily_sales_summary (
                date_key INTEGER PRIMARY KEY REFERENCES dim_date(date_key),
                sales_date DATE NOT NULL,
                total_orders INTEGER DEFAULT 0,
                total_revenue DECIMAL(12,2) DEFAULT 0,
                avg_order_value DECIMAL(10,2) DEFAULT 0,
                unique_customers INTEGER DEFAULT 0,
                total_items_sold INTEGER DEFAULT 0,
                top_category VARCHAR(100),
                top_product_id UUID,
                new_customers INTEGER DEFAULT 0,
                returning_customers INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
        ]
        
        try:
            conn = psycopg2.connect(**warehouse_config)
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = conn.cursor()
            
            # Enable UUID extension
            cursor.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")
            
            for table_sql in tables_sql:
                cursor.execute(table_sql)
                logger.info("Created warehouse table")
            
            # Create indexes for better performance
            indexes = [
                "CREATE INDEX IF NOT EXISTS idx_fact_orders_customer_key ON fact_orders(customer_key);",
                "CREATE INDEX IF NOT EXISTS idx_fact_orders_order_date ON fact_orders(order_date);",
                "CREATE INDEX IF NOT EXISTS idx_fact_order_items_order_id ON fact_order_items(order_id);",
                "CREATE INDEX IF NOT EXISTS idx_fact_order_items_product_key ON fact_order_items(product_key);",
                "CREATE INDEX IF NOT EXISTS idx_fact_events_customer_key ON fact_events(customer_key);",
                "CREATE INDEX IF NOT EXISTS idx_fact_events_event_timestamp ON fact_events(event_timestamp);",
                "CREATE INDEX IF NOT EXISTS idx_fact_events_event_type ON fact_events(event_type);",
                "CREATE INDEX IF NOT EXISTS idx_dim_products_category ON dim_products(category);",
                "CREATE INDEX IF NOT EXISTS idx_dim_products_sku ON dim_products(sku);",
                "CREATE INDEX IF NOT EXISTS idx_dim_customers_email ON dim_customers(email);"
            ]
            
            for index_sql in indexes:
                cursor.execute(index_sql)
            
            logger.info("Created warehouse indexes")
            
            # Grant permissions to readonly users
            readonly_users = ['readonly', 'analyst']
            for user in readonly_users:
                cursor.execute(f"GRANT USAGE ON SCHEMA public TO {user};")
                cursor.execute(f"GRANT SELECT ON ALL TABLES IN SCHEMA public TO {user};")
                cursor.execute(f"ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO {user};")
            
            cursor.close()
            conn.close()
            
            logger.info("Created warehouse tables successfully")
            
        except psycopg2.Error as e:
            logger.error(f"Error creating warehouse tables: {e}")
            raise
    
    def populate_dim_date(self):
        """Populate the date dimension table."""
        warehouse_config = {**self.postgres_config, 'database': 'warehouse'}
        
        try:
            conn = psycopg2.connect(**warehouse_config)
            cursor = conn.cursor()
            
            # Check if dim_date is already populated
            cursor.execute("SELECT COUNT(*) FROM dim_date;")
            count = cursor.fetchone()[0]
            
            if count > 0:
                logger.info("Date dimension already populated")
                cursor.close()
                conn.close()
                return
            
            # Populate date dimension for 5 years (2022-2026)
            populate_sql = """
            INSERT INTO dim_date (
                date_key, date_value, year, quarter, month, month_name,
                day, day_of_week, day_name, week_of_year, is_weekend,
                fiscal_year, fiscal_quarter
            )
            SELECT
                TO_CHAR(date_value, 'YYYYMMDD')::INTEGER as date_key,
                date_value,
                EXTRACT(YEAR FROM date_value) as year,
                EXTRACT(QUARTER FROM date_value) as quarter,
                EXTRACT(MONTH FROM date_value) as month,
                TO_CHAR(date_value, 'Month') as month_name,
                EXTRACT(DAY FROM date_value) as day,
                EXTRACT(DOW FROM date_value) as day_of_week,
                TO_CHAR(date_value, 'Day') as day_name,
                EXTRACT(WEEK FROM date_value) as week_of_year,
                CASE WHEN EXTRACT(DOW FROM date_value) IN (0, 6) THEN TRUE ELSE FALSE END as is_weekend,
                CASE 
                    WHEN EXTRACT(MONTH FROM date_value) >= 10 THEN EXTRACT(YEAR FROM date_value) + 1
                    ELSE EXTRACT(YEAR FROM date_value)
                END as fiscal_year,
                CASE 
                    WHEN EXTRACT(MONTH FROM date_value) IN (10, 11, 12) THEN 1
                    WHEN EXTRACT(MONTH FROM date_value) IN (1, 2, 3) THEN 2
                    WHEN EXTRACT(MONTH FROM date_value) IN (4, 5, 6) THEN 3
                    ELSE 4
                END as fiscal_quarter
            FROM generate_series('2022-01-01'::DATE, '2026-12-31'::DATE, '1 day'::interval) as date_value;
            """
            
            cursor.execute(populate_sql)
            conn.commit()
            
            cursor.execute("SELECT COUNT(*) FROM dim_date;")
            count = cursor.fetchone()[0]
            logger.info(f"Populated date dimension with {count} records")
            
            cursor.close()
            conn.close()
            
        except psycopg2.Error as e:
            logger.error(f"Error populating date dimension: {e}")
            raise
    
    def create_ecommerce_tables(self):
        """Create operational database tables."""
        ecommerce_config = {**self.postgres_config, 'database': 'ecommerce'}
        
        tables_sql = [
            """
            CREATE TABLE IF NOT EXISTS customers (
                customer_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                email VARCHAR(255) UNIQUE NOT NULL,
                first_name VARCHAR(100),
                last_name VARCHAR(100),
                phone VARCHAR(50),
                date_of_birth DATE,
                gender VARCHAR(10),
                registration_date DATE DEFAULT CURRENT_DATE,
                address JSONB,
                preferences JSONB,
                loyalty_tier VARCHAR(20) DEFAULT 'Bronze',
                total_spent DECIMAL(10,2) DEFAULT 0,
                last_login TIMESTAMP,
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS products (
                product_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                sku VARCHAR(50) UNIQUE NOT NULL,
                name VARCHAR(255) NOT NULL,
                description TEXT,
                category VARCHAR(100),
                subcategory VARCHAR(100),
                brand VARCHAR(100),
                price DECIMAL(10,2) NOT NULL,
                cost DECIMAL(10,2),
                weight DECIMAL(8,2),
                dimensions JSONB,
                inventory JSONB,
                rating DECIMAL(3,2),
                review_count INTEGER DEFAULT 0,
                tags TEXT[],
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS orders (
                order_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                customer_id UUID REFERENCES customers(customer_id),
                order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                order_status VARCHAR(50) DEFAULT 'pending',
                payment_method VARCHAR(50),
                payment_status VARCHAR(50) DEFAULT 'pending',
                shipping_address JSONB,
                billing_address JSONB,
                items JSONB,
                subtotal DECIMAL(10,2),
                shipping_cost DECIMAL(8,2),
                tax_amount DECIMAL(8,2),
                discount_amount DECIMAL(8,2) DEFAULT 0,
                total_amount DECIMAL(10,2),
                currency VARCHAR(3) DEFAULT 'USD',
                promotion_code VARCHAR(50),
                estimated_delivery TIMESTAMP,
                tracking_number VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS events (
                event_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                customer_id UUID REFERENCES customers(customer_id),
                session_id UUID,
                event_type VARCHAR(50) NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                properties JSONB,
                user_agent VARCHAR(500),
                ip_address INET,
                page_url VARCHAR(500),
                referrer VARCHAR(500),
                device_type VARCHAR(20),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS inventory_updates (
                update_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                product_id UUID REFERENCES products(product_id),
                update_type VARCHAR(50),
                quantity_change INTEGER,
                previous_quantity INTEGER,
                new_quantity INTEGER,
                reason TEXT,
                updated_by VARCHAR(100),
                location VARCHAR(100),
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
        ]
        
        try:
            conn = psycopg2.connect(**ecommerce_config)
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = conn.cursor()
            
            # Enable UUID extension
            cursor.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")
            
            for table_sql in tables_sql:
                cursor.execute(table_sql)
                logger.info("Created ecommerce table")
            
            # Create indexes
            indexes = [
                "CREATE INDEX IF NOT EXISTS idx_customers_email ON customers(email);",
                "CREATE INDEX IF NOT EXISTS idx_products_sku ON products(sku);",
                "CREATE INDEX IF NOT EXISTS idx_products_category ON products(category);",
                "CREATE INDEX IF NOT EXISTS idx_orders_customer_id ON orders(customer_id);",
                "CREATE INDEX IF NOT EXISTS idx_orders_order_date ON orders(order_date);",
                "CREATE INDEX IF NOT EXISTS idx_events_customer_id ON events(customer_id);",
                "CREATE INDEX IF NOT EXISTS idx_events_timestamp ON events(timestamp);",
                "CREATE INDEX IF NOT EXISTS idx_events_event_type ON events(event_type);",
                "CREATE INDEX IF NOT EXISTS idx_inventory_product_id ON inventory_updates(product_id);",
                "CREATE INDEX IF NOT EXISTS idx_inventory_timestamp ON inventory_updates(timestamp);"
            ]
            
            for index_sql in indexes:
                cursor.execute(index_sql)
            
            logger.info("Created ecommerce indexes")
            
            cursor.close()
            conn.close()
            
            logger.info("Created ecommerce tables successfully")
            
        except psycopg2.Error as e:
            logger.error(f"Error creating ecommerce tables: {e}")
            raise
    
    def setup_redis(self):
        """Setup Redis with initial configuration."""
        try:
            r = redis.Redis(**self.redis_config)
            
            # Test connection
            r.ping()
            
            # Set some initial configuration
            r.config_set('maxmemory-policy', 'allkeys-lru')
            r.config_set('save', '900 1 300 10 60 10000')  # RDB snapshots
            
            # Create some sample cache keys
            r.hset('platform:config', mapping={
                'version': '1.0.0',
                'environment': 'development',
                'initialized_at': str(time.time())
            })
            
            logger.info("Redis setup completed successfully")
            
        except Exception as e:
            logger.error(f"Error setting up Redis: {e}")
            raise
    
    def run_initialization(self):
        """Run the complete database initialization process."""
        logger.info("Starting database initialization...")
        
        try:
            # Wait for services to be ready
            if not self.wait_for_postgres():
                raise Exception("PostgreSQL not ready")
            
            if not self.wait_for_redis():
                raise Exception("Redis not ready")
            
            # Initialize PostgreSQL
            self.create_databases()
            self.create_users()
            self.create_warehouse_tables()
            self.populate_dim_date()
            self.create_ecommerce_tables()
            
            # Initialize Redis
            self.setup_redis()
            
            logger.info("Database initialization completed successfully!")
            
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            sys.exit(1)


if __name__ == "__main__":
    initializer = DatabaseInitializer()
    initializer.run_initialization()
