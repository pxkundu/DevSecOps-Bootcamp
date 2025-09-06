"""
Apache Flink Stream Processing for E-Commerce Data Platform

This module implements real-time stream processing using PyFlink to process
Kafka events and generate real-time analytics and alerts.
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

from pyflink.datastream import StreamExecutionEnvironment, TimeCharacteristic
from pyflink.table import StreamTableEnvironment, EnvironmentSettings
from pyflink.datastream.connectors.kafka import FlinkKafkaConsumer, FlinkKafkaProducer
from pyflink.common.serialization import SimpleStringSchema
from pyflink.common.typeinfo import Types
from pyflink.datastream.functions import MapFunction, FilterFunction, ProcessFunction
from pyflink.datastream.window import TumblingProcessingTimeWindows, SlidingProcessingTimeWindows
from pyflink.common.time import Time
from pyflink.datastream.state import ValueStateDescriptor
from pyflink.table.expressions import col, lit
from pyflink.table.window import Tumble, Slide

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class EventDeserializer(MapFunction):
    """Deserialize JSON events from Kafka."""
    
    def map(self, value):
        try:
            return json.loads(value)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON: {e}")
            return None


class EventFilter(FilterFunction):
    """Filter out invalid or incomplete events."""
    
    def filter(self, event):
        if event is None:
            return False
        
        required_fields = ['event_id', 'event_type', 'timestamp']
        return all(field in event for field in required_fields)


class RealTimeAnalyticsProcessor:
    """Real-time analytics processor using Apache Flink."""
    
    def __init__(self, kafka_bootstrap_servers: str = "localhost:9092"):
        """Initialize Flink environment and configurations."""
        self.kafka_servers = kafka_bootstrap_servers
        
        # Set up Flink environment
        self.env = StreamExecutionEnvironment.get_execution_environment()
        self.env.set_stream_time_characteristic(TimeCharacteristic.ProcessingTime)
        self.env.set_parallelism(2)
        
        # Set up Table environment for SQL operations
        self.t_env = StreamTableEnvironment.create(
            self.env,
            environment_settings=EnvironmentSettings.new_instance()
            .in_streaming_mode()
            .use_blink_planner()
            .build()
        )
        
        # Kafka connection properties
        self.kafka_properties = {
            'bootstrap.servers': self.kafka_servers,
            'group.id': 'flink-analytics-processor',
            'auto.offset.reset': 'latest',
            'enable.auto.commit': 'true'
        }
        
        # Topics to consume
        self.input_topics = {
            'user_events': 'ecommerce.user.events',
            'order_events': 'ecommerce.order.events',
            'inventory_events': 'ecommerce.inventory.events',
            'payment_events': 'ecommerce.payment.events',
            'system_events': 'ecommerce.system.events'
        }
        
        # Output topics for processed data
        self.output_topics = {
            'real_time_metrics': 'ecommerce.analytics.metrics',
            'alerts': 'ecommerce.analytics.alerts',
            'user_sessions': 'ecommerce.analytics.sessions',
            'product_recommendations': 'ecommerce.analytics.recommendations'
        }
    
    def create_kafka_source(self, topic: str):
        """Create Kafka source for a specific topic."""
        return FlinkKafkaConsumer(
            topic,
            SimpleStringSchema(),
            self.kafka_properties
        )
    
    def create_kafka_sink(self, topic: str):
        """Create Kafka sink for a specific topic."""
        return FlinkKafkaProducer(
            topic,
            SimpleStringSchema(),
            self.kafka_servers
        )
    
    def process_user_events(self):
        """Process user behavior events for real-time insights."""
        # Create data stream from Kafka
        user_events_stream = self.env.add_source(
            self.create_kafka_source(self.input_topics['user_events'])
        )
        
        # Parse and filter events
        parsed_events = user_events_stream \
            .map(EventDeserializer()) \
            .filter(EventFilter())
        
        # Real-time user activity metrics (5-minute windows)
        user_activity_metrics = parsed_events \
            .key_by(lambda event: event.get('customer_id', 'unknown')) \
            .window(TumblingProcessingTimeWindows.of(Time.minutes(5))) \
            .process(UserActivityProcessor())
        
        # Page view analytics (1-minute sliding windows)
        page_view_analytics = parsed_events \
            .filter(lambda event: event.get('event_type') == 'page_view') \
            .window(SlidingProcessingTimeWindows.of(Time.minutes(5), Time.minutes(1))) \
            .process(PageViewProcessor())
        
        # Product popularity tracking
        product_popularity = parsed_events \
            .filter(lambda event: event.get('event_type') == 'product_view') \
            .key_by(lambda event: event.get('product_id', 'unknown')) \
            .window(TumblingProcessingTimeWindows.of(Time.minutes(10))) \
            .process(ProductPopularityProcessor())
        
        # Send metrics to output topics
        user_activity_metrics.add_sink(
            self.create_kafka_sink(self.output_topics['real_time_metrics'])
        )
        
        page_view_analytics.add_sink(
            self.create_kafka_sink(self.output_topics['real_time_metrics'])
        )
        
        product_popularity.add_sink(
            self.create_kafka_sink(self.output_topics['real_time_metrics'])
        )
    
    def process_order_events(self):
        """Process order events for real-time sales analytics."""
        order_events_stream = self.env.add_source(
            self.create_kafka_source(self.input_topics['order_events'])
        )
        
        parsed_events = order_events_stream \
            .map(EventDeserializer()) \
            .filter(EventFilter())
        
        # Real-time sales metrics
        sales_metrics = parsed_events \
            .filter(lambda event: event.get('event_type') == 'order_created') \
            .window(TumblingProcessingTimeWindows.of(Time.minutes(5))) \
            .process(SalesMetricsProcessor())
        
        # Order status tracking
        order_status_tracking = parsed_events \
            .key_by(lambda event: event.get('order_id', 'unknown')) \
            .process(OrderStatusProcessor())
        
        # Fraud detection (simplified)
        fraud_alerts = parsed_events \
            .key_by(lambda event: event.get('customer_id', 'unknown')) \
            .process(FraudDetectionProcessor())
        
        # Send results to output topics
        sales_metrics.add_sink(
            self.create_kafka_sink(self.output_topics['real_time_metrics'])
        )
        
        fraud_alerts.add_sink(
            self.create_kafka_sink(self.output_topics['alerts'])
        )
    
    def process_inventory_events(self):
        """Process inventory events for stock monitoring."""
        inventory_events_stream = self.env.add_source(
            self.create_kafka_source(self.input_topics['inventory_events'])
        )
        
        parsed_events = inventory_events_stream \
            .map(EventDeserializer()) \
            .filter(EventFilter())
        
        # Low stock alerts
        low_stock_alerts = parsed_events \
            .filter(lambda event: event.get('event_type') in ['low_stock_alert', 'out_of_stock']) \
            .map(InventoryAlertProcessor())
        
        # Stock level tracking
        stock_tracking = parsed_events \
            .key_by(lambda event: event.get('product_id', 'unknown')) \
            .process(StockLevelProcessor())
        
        # Send alerts
        low_stock_alerts.add_sink(
            self.create_kafka_sink(self.output_topics['alerts'])
        )
    
    def process_payment_events(self):
        """Process payment events for transaction monitoring."""
        payment_events_stream = self.env.add_source(
            self.create_kafka_source(self.input_topics['payment_events'])
        )
        
        parsed_events = payment_events_stream \
            .map(EventDeserializer()) \
            .filter(EventFilter())
        
        # Payment failure monitoring
        payment_failures = parsed_events \
            .filter(lambda event: event.get('event_type') == 'payment_failed') \
            .window(TumblingProcessingTimeWindows.of(Time.minutes(5))) \
            .process(PaymentFailureProcessor())
        
        # Transaction volume monitoring
        transaction_volume = parsed_events \
            .filter(lambda event: event.get('event_type') == 'payment_completed') \
            .window(SlidingProcessingTimeWindows.of(Time.minutes(15), Time.minutes(5))) \
            .process(TransactionVolumeProcessor())
        
        # Send metrics and alerts
        payment_failures.add_sink(
            self.create_kafka_sink(self.output_topics['alerts'])
        )
        
        transaction_volume.add_sink(
            self.create_kafka_sink(self.output_topics['real_time_metrics'])
        )
    
    def create_real_time_dashboard_data(self):
        """Create aggregated data for real-time dashboards."""
        # Use Table API for complex analytics
        self.t_env.execute_sql("""
            CREATE TABLE user_events (
                event_id STRING,
                event_type STRING,
                customer_id STRING,
                timestamp TIMESTAMP(3),
                product_id STRING,
                product_category STRING,
                session_id STRING,
                WATERMARK FOR timestamp AS timestamp - INTERVAL '5' SECOND
            ) WITH (
                'connector' = 'kafka',
                'topic' = 'ecommerce.user.events',
                'properties.bootstrap.servers' = 'localhost:9092',
                'properties.group.id' = 'flink-table-processor',
                'format' = 'json'
            )
        """)
        
        # Real-time dashboard metrics
        dashboard_metrics = self.t_env.sql_query("""
            SELECT 
                TUMBLE_START(timestamp, INTERVAL '1' MINUTE) as window_start,
                event_type,
                product_category,
                COUNT(*) as event_count,
                COUNT(DISTINCT customer_id) as unique_users,
                COUNT(DISTINCT session_id) as unique_sessions
            FROM user_events
            WHERE timestamp > CURRENT_TIMESTAMP - INTERVAL '1' HOUR
            GROUP BY 
                TUMBLE(timestamp, INTERVAL '1' MINUTE),
                event_type,
                product_category
        """)
        
        # Convert to data stream and send to output
        dashboard_stream = self.t_env.to_append_stream(dashboard_metrics, Types.ROW_NAMED(
            ['window_start', 'event_type', 'product_category', 'event_count', 'unique_users', 'unique_sessions'],
            [Types.SQL_TIMESTAMP(), Types.STRING(), Types.STRING(), Types.LONG(), Types.LONG(), Types.LONG()]
        ))
        
        dashboard_stream.map(lambda row: json.dumps({
            'window_start': str(row[0]),
            'event_type': row[1],
            'product_category': row[2],
            'event_count': row[3],
            'unique_users': row[4],
            'unique_sessions': row[5],
            'metric_type': 'dashboard_data'
        })).add_sink(self.create_kafka_sink(self.output_topics['real_time_metrics']))
    
    def run_stream_processing(self):
        """Start all stream processing jobs."""
        logger.info("Starting Flink stream processing jobs...")
        
        try:
            # Set up all processing pipelines
            self.process_user_events()
            self.process_order_events()
            self.process_inventory_events()
            self.process_payment_events()
            self.create_real_time_dashboard_data()
            
            # Execute the job
            self.env.execute("E-Commerce Real-Time Analytics")
            
        except Exception as e:
            logger.error(f"Stream processing failed: {str(e)}")
            raise


# Custom processors for different event types
class UserActivityProcessor(ProcessFunction):
    """Process user activity events."""
    
    def process_element(self, value, ctx, out):
        # Aggregate user activity metrics
        activity_summary = {
            'metric_type': 'user_activity',
            'window_start': ctx.window().start,
            'window_end': ctx.window().end,
            'customer_id': value.get('customer_id'),
            'event_count': 1,
            'timestamp': datetime.utcnow().isoformat()
        }
        out.collect(json.dumps(activity_summary))


class PageViewProcessor(ProcessFunction):
    """Process page view events."""
    
    def process_element(self, value, ctx, out):
        page_metrics = {
            'metric_type': 'page_views',
            'window_start': ctx.window().start,
            'window_end': ctx.window().end,
            'page_url': value.get('page_url', 'unknown'),
            'view_count': 1,
            'timestamp': datetime.utcnow().isoformat()
        }
        out.collect(json.dumps(page_metrics))


class ProductPopularityProcessor(ProcessFunction):
    """Track product popularity."""
    
    def process_element(self, value, ctx, out):
        popularity_metrics = {
            'metric_type': 'product_popularity',
            'window_start': ctx.window().start,
            'window_end': ctx.window().end,
            'product_id': value.get('product_id'),
            'view_count': 1,
            'timestamp': datetime.utcnow().isoformat()
        }
        out.collect(json.dumps(popularity_metrics))


class SalesMetricsProcessor(ProcessFunction):
    """Process sales metrics."""
    
    def process_element(self, value, ctx, out):
        sales_data = {
            'metric_type': 'sales_metrics',
            'window_start': ctx.window().start,
            'window_end': ctx.window().end,
            'order_count': 1,
            'revenue': value.get('order_value', 0),
            'timestamp': datetime.utcnow().isoformat()
        }
        out.collect(json.dumps(sales_data))


class OrderStatusProcessor(ProcessFunction):
    """Track order status changes."""
    
    def process_element(self, value, ctx, out):
        status_update = {
            'metric_type': 'order_status',
            'order_id': value.get('order_id'),
            'event_type': value.get('event_type'),
            'customer_id': value.get('customer_id'),
            'timestamp': value.get('timestamp')
        }
        out.collect(json.dumps(status_update))


class FraudDetectionProcessor(ProcessFunction):
    """Simple fraud detection processor."""
    
    def __init__(self):
        self.order_count_state = None
    
    def open(self, runtime_context):
        self.order_count_state = runtime_context.get_state(
            ValueStateDescriptor("order_count", Types.INT())
        )
    
    def process_element(self, value, ctx, out):
        if value.get('event_type') == 'order_created':
            current_count = self.order_count_state.value() or 0
            current_count += 1
            self.order_count_state.update(current_count)
            
            # Simple fraud rule: more than 5 orders in short time
            if current_count > 5:
                fraud_alert = {
                    'alert_type': 'fraud_detection',
                    'customer_id': value.get('customer_id'),
                    'order_count': current_count,
                    'severity': 'high',
                    'message': f'Customer placed {current_count} orders in short time',
                    'timestamp': datetime.utcnow().isoformat()
                }
                out.collect(json.dumps(fraud_alert))


class InventoryAlertProcessor(MapFunction):
    """Process inventory alerts."""
    
    def map(self, value):
        alert = {
            'alert_type': 'inventory',
            'product_id': value.get('product_id'),
            'sku': value.get('sku'),
            'event_type': value.get('event_type'),
            'current_quantity': value.get('current_quantity', 0),
            'warehouse_location': value.get('warehouse_location'),
            'severity': 'critical' if value.get('event_type') == 'out_of_stock' else 'warning',
            'timestamp': datetime.utcnow().isoformat()
        }
        return json.dumps(alert)


class StockLevelProcessor(ProcessFunction):
    """Track stock levels."""
    
    def process_element(self, value, ctx, out):
        stock_update = {
            'metric_type': 'stock_level',
            'product_id': value.get('product_id'),
            'event_type': value.get('event_type'),
            'quantity_change': value.get('new_quantity', 0) - value.get('previous_quantity', 0),
            'current_quantity': value.get('new_quantity', 0),
            'timestamp': value.get('timestamp')
        }
        out.collect(json.dumps(stock_update))


class PaymentFailureProcessor(ProcessFunction):
    """Monitor payment failures."""
    
    def process_element(self, value, ctx, out):
        failure_metrics = {
            'metric_type': 'payment_failures',
            'window_start': ctx.window().start,
            'window_end': ctx.window().end,
            'failure_count': 1,
            'failure_reason': value.get('failure_reason'),
            'payment_method': value.get('payment_method'),
            'timestamp': datetime.utcnow().isoformat()
        }
        out.collect(json.dumps(failure_metrics))


class TransactionVolumeProcessor(ProcessFunction):
    """Monitor transaction volume."""
    
    def process_element(self, value, ctx, out):
        volume_metrics = {
            'metric_type': 'transaction_volume',
            'window_start': ctx.window().start,
            'window_end': ctx.window().end,
            'transaction_count': 1,
            'total_amount': value.get('amount', 0),
            'payment_method': value.get('payment_method'),
            'timestamp': datetime.utcnow().isoformat()
        }
        out.collect(json.dumps(volume_metrics))


def main():
    """Main function to run the stream processor."""
    processor = RealTimeAnalyticsProcessor()
    processor.run_stream_processing()


if __name__ == "__main__":
    main()
