"""
Apache Spark ETL Pipeline for E-Commerce Data Platform

This module implements batch ETL processes for transforming raw e-commerce data
into business-ready analytics datasets.
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import (
    col, count, sum as spark_sum, avg, max as spark_max, min as spark_min,
    when, lit, current_timestamp, date_format, year, month, dayofmonth,
    regexp_replace, trim, lower, upper, split, explode, collect_list,
    window, lag, rank, dense_rank, row_number, coalesce, isnan, isnull
)
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, BooleanType, TimestampType
from pyspark.sql.window import Window

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ECommerceSparkETL:
    """Spark ETL pipeline for e-commerce data processing."""
    
    def __init__(self, app_name: str = "ECommerceETL"):
        """Initialize Spark session and configurations."""
        self.spark = SparkSession.builder \
            .appName(app_name) \
            .config("spark.sql.adaptive.enabled", "true") \
            .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
            .config("spark.sql.adaptive.skewJoin.enabled", "true") \
            .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \
            .getOrCreate()
        
        self.spark.sparkContext.setLogLevel("WARN")
        logger.info(f"Spark session initialized: {app_name}")
    
    def read_data(self, file_path: str, file_format: str = "parquet") -> DataFrame:
        """Read data from various file formats."""
        try:
            if file_format.lower() == "parquet":
                df = self.spark.read.parquet(file_path)
            elif file_format.lower() == "csv":
                df = self.spark.read.option("header", "true").option("inferSchema", "true").csv(file_path)
            elif file_format.lower() == "json":
                df = self.spark.read.json(file_path)
            else:
                raise ValueError(f"Unsupported file format: {file_format}")
            
            logger.info(f"Successfully read {df.count()} records from {file_path}")
            return df
        except Exception as e:
            logger.error(f"Error reading data from {file_path}: {str(e)}")
            raise
    
    def clean_customer_data(self, customers_df: DataFrame) -> DataFrame:
        """Clean and standardize customer data."""
        logger.info("Cleaning customer data...")
        
        cleaned_df = customers_df \
            .filter(col("customer_id").isNotNull()) \
            .filter(col("email").isNotNull()) \
            .withColumn("email", lower(trim(col("email")))) \
            .withColumn("first_name", trim(col("first_name"))) \
            .withColumn("last_name", trim(col("last_name"))) \
            .withColumn("phone", regexp_replace(col("phone"), "[^0-9]", "")) \
            .withColumn("full_name", 
                       when(col("first_name").isNotNull() & col("last_name").isNotNull(),
                            concat(col("first_name"), lit(" "), col("last_name")))
                       .otherwise(coalesce(col("first_name"), col("last_name")))) \
            .withColumn("registration_year", year(col("registration_date"))) \
            .withColumn("registration_month", month(col("registration_date"))) \
            .withColumn("days_since_registration", 
                       datediff(current_date(), col("registration_date"))) \
            .withColumn("is_active", 
                       when(col("last_login").isNotNull() & 
                            datediff(current_date(), col("last_login")) <= 90, True)
                       .otherwise(False))
        
        logger.info(f"Customer data cleaned: {cleaned_df.count()} records")
        return cleaned_df
    
    def clean_product_data(self, products_df: DataFrame) -> DataFrame:
        """Clean and enrich product data."""
        logger.info("Cleaning product data...")
        
        cleaned_df = products_df \
            .filter(col("product_id").isNotNull()) \
            .filter(col("price") > 0) \
            .withColumn("name", trim(col("name"))) \
            .withColumn("description", trim(col("description"))) \
            .withColumn("brand", trim(col("brand"))) \
            .withColumn("category", upper(trim(col("category")))) \
            .withColumn("subcategory", trim(col("subcategory"))) \
            .withColumn("profit_margin", 
                       when(col("cost") > 0, (col("price") - col("cost")) / col("price"))
                       .otherwise(0)) \
            .withColumn("price_tier",
                       when(col("price") < 50, "Budget")
                       .when(col("price") < 200, "Mid-Range")
                       .when(col("price") < 500, "Premium")
                       .otherwise("Luxury")) \
            .withColumn("stock_status",
                       when(col("inventory.stock_quantity") == 0, "Out of Stock")
                       .when(col("inventory.stock_quantity") <= col("inventory.reorder_point"), "Low Stock")
                       .otherwise("In Stock")) \
            .withColumn("days_since_created", 
                       datediff(current_date(), col("created_date")))
        
        logger.info(f"Product data cleaned: {cleaned_df.count()} records")
        return cleaned_df
    
    def clean_order_data(self, orders_df: DataFrame) -> DataFrame:
        """Clean and enrich order data."""
        logger.info("Cleaning order data...")
        
        cleaned_df = orders_df \
            .filter(col("order_id").isNotNull()) \
            .filter(col("customer_id").isNotNull()) \
            .filter(col("total_amount") > 0) \
            .withColumn("order_year", year(col("order_date"))) \
            .withColumn("order_month", month(col("order_date"))) \
            .withColumn("order_day", dayofmonth(col("order_date"))) \
            .withColumn("order_hour", hour(col("order_date"))) \
            .withColumn("day_of_week", date_format(col("order_date"), "EEEE")) \
            .withColumn("is_weekend", 
                       when(date_format(col("order_date"), "u").isin("6", "7"), True)
                       .otherwise(False)) \
            .withColumn("items_count", size(col("items"))) \
            .withColumn("avg_item_price", col("subtotal") / col("items_count")) \
            .withColumn("has_discount", 
                       when(col("discount_amount") > 0, True).otherwise(False)) \
            .withColumn("discount_percentage", 
                       when(col("subtotal") > 0, col("discount_amount") / col("subtotal") * 100)
                       .otherwise(0)) \
            .withColumn("order_value_tier",
                       when(col("total_amount") < 50, "Small")
                       .when(col("total_amount") < 200, "Medium")
                       .when(col("total_amount") < 500, "Large")
                       .otherwise("Premium"))
        
        logger.info(f"Order data cleaned: {cleaned_df.count()} records")
        return cleaned_df
    
    def create_customer_analytics(self, customers_df: DataFrame, orders_df: DataFrame) -> DataFrame:
        """Create customer analytics aggregations."""
        logger.info("Creating customer analytics...")
        
        # Customer order statistics
        customer_stats = orders_df \
            .filter(col("order_status").isin(["delivered", "shipped"])) \
            .groupBy("customer_id") \
            .agg(
                count("order_id").alias("total_orders"),
                spark_sum("total_amount").alias("total_spent"),
                avg("total_amount").alias("avg_order_value"),
                spark_max("total_amount").alias("max_order_value"),
                spark_min("total_amount").alias("min_order_value"),
                spark_max("order_date").alias("last_order_date"),
                spark_min("order_date").alias("first_order_date"),
                countDistinct("payment_method").alias("payment_methods_used"),
                spark_sum("items_count").alias("total_items_purchased")
            ) \
            .withColumn("days_since_last_order", 
                       datediff(current_date(), col("last_order_date"))) \
            .withColumn("customer_tenure_days", 
                       datediff(col("last_order_date"), col("first_order_date"))) \
            .withColumn("order_frequency", 
                       when(col("customer_tenure_days") > 0, 
                            col("total_orders") / col("customer_tenure_days") * 30)
                       .otherwise(0)) \
            .withColumn("customer_segment",
                       when((col("total_spent") >= 1000) & (col("total_orders") >= 10), "VIP")
                       .when((col("total_spent") >= 500) & (col("total_orders") >= 5), "High Value")
                       .when((col("total_spent") >= 100) & (col("total_orders") >= 2), "Regular")
                       .otherwise("New/Low Value"))
        
        # Join with customer master data
        customer_analytics = customers_df \
            .join(customer_stats, "customer_id", "left") \
            .fillna(0, ["total_orders", "total_spent", "avg_order_value", 
                       "total_items_purchased", "payment_methods_used"]) \
            .withColumn("customer_segment", 
                       coalesce(col("customer_segment"), lit("New/Low Value")))
        
        logger.info(f"Customer analytics created: {customer_analytics.count()} records")
        return customer_analytics
    
    def create_product_analytics(self, products_df: DataFrame, orders_df: DataFrame) -> DataFrame:
        """Create product performance analytics."""
        logger.info("Creating product analytics...")
        
        # Explode order items to get individual product sales
        order_items = orders_df \
            .select("order_id", "order_date", "order_status", explode("items").alias("item")) \
            .select("order_id", "order_date", "order_status",
                   col("item.product_id").alias("product_id"),
                   col("item.quantity").alias("quantity"),
                   col("item.unit_price").alias("unit_price"),
                   col("item.line_total").alias("line_total"))
        
        # Product sales statistics
        product_stats = order_items \
            .filter(col("order_status").isin(["delivered", "shipped"])) \
            .groupBy("product_id") \
            .agg(
                count("order_id").alias("total_orders"),
                spark_sum("quantity").alias("total_quantity_sold"),
                spark_sum("line_total").alias("total_revenue"),
                avg("unit_price").alias("avg_selling_price"),
                countDistinct("order_id").alias("unique_customers"),
                spark_max("order_date").alias("last_sale_date"),
                spark_min("order_date").alias("first_sale_date")
            ) \
            .withColumn("days_since_last_sale", 
                       datediff(current_date(), col("last_sale_date"))) \
            .withColumn("sales_velocity", 
                       col("total_quantity_sold") / 
                       greatest(datediff(current_date(), col("first_sale_date")), lit(1)))
        
        # Product ranking by revenue
        revenue_window = Window.orderBy(col("total_revenue").desc())
        product_stats = product_stats \
            .withColumn("revenue_rank", rank().over(revenue_window)) \
            .withColumn("performance_tier",
                       when(col("revenue_rank") <= 100, "Top Performer")
                       .when(col("revenue_rank") <= 500, "Good Performer")
                       .when(col("revenue_rank") <= 1000, "Average Performer")
                       .otherwise("Low Performer"))
        
        # Join with product master data
        product_analytics = products_df \
            .join(product_stats, "product_id", "left") \
            .fillna(0, ["total_orders", "total_quantity_sold", "total_revenue", 
                       "unique_customers", "revenue_rank"]) \
            .withColumn("performance_tier", 
                       coalesce(col("performance_tier"), lit("New Product")))
        
        logger.info(f"Product analytics created: {product_analytics.count()} records")
        return product_analytics
    
    def create_sales_analytics(self, orders_df: DataFrame) -> DataFrame:
        """Create sales analytics by time periods."""
        logger.info("Creating sales analytics...")
        
        # Daily sales summary
        daily_sales = orders_df \
            .filter(col("order_status").isin(["delivered", "shipped"])) \
            .groupBy("order_date") \
            .agg(
                count("order_id").alias("daily_orders"),
                spark_sum("total_amount").alias("daily_revenue"),
                avg("total_amount").alias("daily_avg_order_value"),
                countDistinct("customer_id").alias("daily_unique_customers"),
                spark_sum("items_count").alias("daily_items_sold")
            ) \
            .withColumn("day_of_week", date_format(col("order_date"), "EEEE")) \
            .withColumn("is_weekend", 
                       when(date_format(col("order_date"), "u").isin("6", "7"), True)
                       .otherwise(False))
        
        # Monthly sales summary
        monthly_sales = orders_df \
            .filter(col("order_status").isin(["delivered", "shipped"])) \
            .withColumn("year_month", date_format(col("order_date"), "yyyy-MM")) \
            .groupBy("year_month") \
            .agg(
                count("order_id").alias("monthly_orders"),
                spark_sum("total_amount").alias("monthly_revenue"),
                avg("total_amount").alias("monthly_avg_order_value"),
                countDistinct("customer_id").alias("monthly_unique_customers"),
                countDistinct("order_date").alias("active_days")
            ) \
            .withColumn("revenue_per_day", col("monthly_revenue") / col("active_days"))
        
        # Add trend analysis
        monthly_window = Window.orderBy("year_month")
        monthly_sales = monthly_sales \
            .withColumn("prev_month_revenue", 
                       lag("monthly_revenue", 1).over(monthly_window)) \
            .withColumn("revenue_growth", 
                       when(col("prev_month_revenue") > 0, 
                            (col("monthly_revenue") - col("prev_month_revenue")) / 
                            col("prev_month_revenue") * 100)
                       .otherwise(0))
        
        logger.info("Sales analytics created")
        return {"daily": daily_sales, "monthly": monthly_sales}
    
    def write_data(self, df: DataFrame, output_path: str, 
                   file_format: str = "parquet", mode: str = "overwrite",
                   partition_by: Optional[list] = None):
        """Write DataFrame to storage."""
        try:
            writer = df.write.mode(mode)
            
            if partition_by:
                writer = writer.partitionBy(*partition_by)
            
            if file_format.lower() == "parquet":
                writer.parquet(output_path)
            elif file_format.lower() == "csv":
                writer.option("header", "true").csv(output_path)
            elif file_format.lower() == "json":
                writer.json(output_path)
            else:
                raise ValueError(f"Unsupported file format: {file_format}")
            
            logger.info(f"Successfully wrote data to {output_path}")
        except Exception as e:
            logger.error(f"Error writing data to {output_path}: {str(e)}")
            raise
    
    def run_full_etl(self, input_dir: str, output_dir: str):
        """Run the complete ETL pipeline."""
        logger.info("Starting full ETL pipeline...")
        
        try:
            # Read raw data
            customers_raw = self.read_data(f"{input_dir}/customers.parquet")
            products_raw = self.read_data(f"{input_dir}/products.parquet")
            orders_raw = self.read_data(f"{input_dir}/orders.parquet")
            
            # Clean data
            customers_clean = self.clean_customer_data(customers_raw)
            products_clean = self.clean_product_data(products_raw)
            orders_clean = self.clean_order_data(orders_raw)
            
            # Create analytics
            customer_analytics = self.create_customer_analytics(customers_clean, orders_clean)
            product_analytics = self.create_product_analytics(products_clean, orders_clean)
            sales_analytics = self.create_sales_analytics(orders_clean)
            
            # Write clean data
            self.write_data(customers_clean, f"{output_dir}/customers_clean", 
                          partition_by=["registration_year"])
            self.write_data(products_clean, f"{output_dir}/products_clean", 
                          partition_by=["category"])
            self.write_data(orders_clean, f"{output_dir}/orders_clean", 
                          partition_by=["order_year", "order_month"])
            
            # Write analytics
            self.write_data(customer_analytics, f"{output_dir}/customer_analytics", 
                          partition_by=["customer_segment"])
            self.write_data(product_analytics, f"{output_dir}/product_analytics", 
                          partition_by=["category", "performance_tier"])
            self.write_data(sales_analytics["daily"], f"{output_dir}/daily_sales")
            self.write_data(sales_analytics["monthly"], f"{output_dir}/monthly_sales")
            
            logger.info("ETL pipeline completed successfully!")
            
        except Exception as e:
            logger.error(f"ETL pipeline failed: {str(e)}")
            raise
        finally:
            self.spark.stop()


def main():
    """Main function to run the ETL pipeline."""
    etl = ECommerceSparkETL()
    
    # Configure paths
    input_dir = "/opt/airflow/data-sources/sample-data"
    output_dir = "/opt/airflow/storage/data-warehouse"
    
    # Run ETL
    etl.run_full_etl(input_dir, output_dir)


if __name__ == "__main__":
    main()
