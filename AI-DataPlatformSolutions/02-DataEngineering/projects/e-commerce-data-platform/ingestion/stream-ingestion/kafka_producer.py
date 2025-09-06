"""
Kafka Producer for E-Commerce Real-Time Events

This module simulates real-time e-commerce events and publishes them to Kafka topics
for stream processing. Events include user behavior, transactions, and system events.
"""

import json
import logging
import random
import time
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from concurrent.futures import ThreadPoolExecutor
import threading

from kafka import KafkaProducer
from kafka.errors import KafkaError
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class ECommerceEventProducer:
    """Produces real-time e-commerce events to Kafka topics."""
    
    def __init__(self, bootstrap_servers: List[str] = ['localhost:9092']):
        """Initialize Kafka producer and load reference data."""
        self.bootstrap_servers = bootstrap_servers
        self.producer = None
        self.is_running = False
        
        # Kafka topics
        self.topics = {
            'user_events': 'ecommerce.user.events',
            'order_events': 'ecommerce.order.events',
            'inventory_events': 'ecommerce.inventory.events',
            'payment_events': 'ecommerce.payment.events',
            'system_events': 'ecommerce.system.events'
        }
        
        # Load reference data for realistic events
        self.customers = []
        self.products = []
        self.active_sessions = {}
        
        # Event probabilities and configurations
        self.event_config = {
            'user_events': {
                'page_view': 0.4,
                'product_view': 0.25,
                'search': 0.15,
                'add_to_cart': 0.1,
                'remove_from_cart': 0.05,
                'checkout_start': 0.03,
                'login': 0.015,
                'logout': 0.005
            },
            'order_events': {
                'order_created': 0.4,
                'payment_initiated': 0.25,
                'payment_completed': 0.2,
                'order_shipped': 0.1,
                'order_delivered': 0.05
            },
            'inventory_events': {
                'stock_update': 0.6,
                'low_stock_alert': 0.25,
                'out_of_stock': 0.1,
                'restock': 0.05
            },
            'payment_events': {
                'payment_started': 0.35,
                'payment_completed': 0.3,
                'payment_failed': 0.2,
                'refund_initiated': 0.1,
                'refund_completed': 0.05
            },
            'system_events': {
                'user_session_start': 0.3,
                'user_session_end': 0.25,
                'api_call': 0.2,
                'error_occurred': 0.15,
                'system_health_check': 0.1
            }
        }
        
        self._initialize_producer()
        self._load_reference_data()
    
    def _initialize_producer(self):
        """Initialize Kafka producer with optimized settings."""
        try:
            self.producer = KafkaProducer(
                bootstrap_servers=self.bootstrap_servers,
                value_serializer=lambda v: json.dumps(v, default=str).encode('utf-8'),
                key_serializer=lambda k: str(k).encode('utf-8') if k else None,
                # Performance settings
                batch_size=16384,
                linger_ms=10,
                compression_type='snappy',
                # Reliability settings
                acks='1',
                retries=3,
                retry_backoff_ms=100,
                # Error handling
                api_version_auto_timeout_ms=30000
            )
            logger.info("Kafka producer initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Kafka producer: {str(e)}")
            raise
    
    def _load_reference_data(self):
        """Load customer and product data for generating realistic events."""
        try:
            # Load customers (in production, this would come from a database)
            self.customers = [
                {
                    'customer_id': str(uuid.uuid4()),
                    'email': f'user{i}@example.com',
                    'segment': random.choice(['VIP', 'High Value', 'Regular', 'New'])
                }
                for i in range(1000)
            ]
            
            # Load products
            categories = ['Electronics', 'Clothing', 'Home & Garden', 'Books', 'Sports']
            self.products = [
                {
                    'product_id': str(uuid.uuid4()),
                    'sku': f'SKU-{random.randint(100000, 999999)}',
                    'name': f'Product {i}',
                    'category': random.choice(categories),
                    'price': round(random.uniform(10, 1000), 2)
                }
                for i in range(500)
            ]
            
            logger.info(f"Loaded {len(self.customers)} customers and {len(self.products)} products")
        except Exception as e:
            logger.error(f"Failed to load reference data: {str(e)}")
            # Use minimal data for demonstration
            self.customers = [{'customer_id': str(uuid.uuid4()), 'email': 'demo@example.com', 'segment': 'Regular'}]
            self.products = [{'product_id': str(uuid.uuid4()), 'sku': 'SKU-123456', 'name': 'Demo Product', 'category': 'Electronics', 'price': 99.99}]
    
    def generate_user_event(self) -> Dict:
        """Generate a user behavior event."""
        customer = random.choice(self.customers)
        event_types = list(self.event_config['user_events'].keys())
        event_weights = list(self.event_config['user_events'].values())
        event_type = random.choices(event_types, weights=event_weights)[0]
        
        base_event = {
            'event_id': str(uuid.uuid4()),
            'event_type': event_type,
            'customer_id': customer['customer_id'],
            'session_id': self._get_or_create_session(customer['customer_id']),
            'timestamp': datetime.utcnow().isoformat(),
            'user_agent': random.choice([
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15'
            ]),
            'ip_address': f'{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}',
            'device_type': random.choice(['desktop', 'mobile', 'tablet'])
        }
        
        # Add event-specific data
        if event_type in ['product_view', 'add_to_cart', 'remove_from_cart']:
            product = random.choice(self.products)
            base_event.update({
                'product_id': product['product_id'],
                'product_name': product['name'],
                'product_category': product['category'],
                'product_price': product['price']
            })
        
        elif event_type == 'search':
            base_event.update({
                'search_query': random.choice(['laptop', 'shoes', 'phone', 'book', 'watch']),
                'search_results_count': random.randint(0, 100)
            })
        
        elif event_type == 'page_view':
            base_event.update({
                'page_url': f'/category/{random.choice(["electronics", "clothing", "books"])}',
                'referrer': random.choice([None, 'google.com', 'facebook.com', 'direct'])
            })
        
        elif event_type == 'checkout_start':
            base_event.update({
                'cart_value': round(random.uniform(50, 500), 2),
                'cart_items_count': random.randint(1, 5)
            })
        
        return base_event
    
    def generate_order_event(self) -> Dict:
        """Generate an order-related event."""
        customer = random.choice(self.customers)
        event_types = list(self.event_config['order_events'].keys())
        event_weights = list(self.event_config['order_events'].values())
        event_type = random.choices(event_types, weights=event_weights)[0]
        
        order_id = str(uuid.uuid4())
        
        event = {
            'event_id': str(uuid.uuid4()),
            'event_type': event_type,
            'order_id': order_id,
            'customer_id': customer['customer_id'],
            'timestamp': datetime.utcnow().isoformat(),
            'order_value': round(random.uniform(25, 1000), 2),
            'currency': 'USD'
        }
        
        if event_type == 'order_created':
            event.update({
                'items_count': random.randint(1, 5),
                'payment_method': random.choice(['credit_card', 'debit_card', 'paypal', 'apple_pay']),
                'shipping_method': random.choice(['standard', 'express', 'overnight'])
            })
        
        elif event_type in ['payment_initiated', 'payment_completed']:
            event.update({
                'payment_id': str(uuid.uuid4()),
                'payment_method': random.choice(['credit_card', 'debit_card', 'paypal', 'apple_pay']),
                'payment_processor': random.choice(['stripe', 'paypal', 'square'])
            })
        
        elif event_type in ['order_shipped', 'order_delivered']:
            event.update({
                'tracking_number': f'TRACK{random.randint(1000000000, 9999999999)}',
                'carrier': random.choice(['UPS', 'FedEx', 'USPS', 'DHL'])
            })
        
        return event
    
    def generate_inventory_event(self) -> Dict:
        """Generate an inventory-related event."""
        product = random.choice(self.products)
        event_types = list(self.event_config['inventory_events'].keys())
        event_weights = list(self.event_config['inventory_events'].values())
        event_type = random.choices(event_types, weights=event_weights)[0]
        
        event = {
            'event_id': str(uuid.uuid4()),
            'event_type': event_type,
            'product_id': product['product_id'],
            'sku': product['sku'],
            'timestamp': datetime.utcnow().isoformat(),
            'warehouse_location': random.choice(['NYC', 'LA', 'Chicago', 'Dallas'])
        }
        
        if event_type == 'stock_update':
            event.update({
                'previous_quantity': random.randint(0, 1000),
                'new_quantity': random.randint(0, 1000),
                'change_type': random.choice(['sale', 'restock', 'adjustment', 'return'])
            })
        
        elif event_type in ['low_stock_alert', 'out_of_stock']:
            event.update({
                'current_quantity': random.randint(0, 10) if event_type == 'low_stock_alert' else 0,
                'reorder_point': random.randint(10, 50),
                'alert_level': 'critical' if event_type == 'out_of_stock' else 'warning'
            })
        
        elif event_type == 'restock':
            event.update({
                'quantity_added': random.randint(50, 500),
                'supplier_id': str(uuid.uuid4()),
                'expected_delivery': (datetime.utcnow() + timedelta(days=random.randint(1, 7))).isoformat()
            })
        
        return event
    
    def generate_payment_event(self) -> Dict:
        """Generate a payment-related event."""
        customer = random.choice(self.customers)
        event_types = list(self.event_config['payment_events'].keys())
        event_weights = list(self.event_config['payment_events'].values())
        event_type = random.choices(event_types, weights=event_weights)[0]
        
        event = {
            'event_id': str(uuid.uuid4()),
            'event_type': event_type,
            'payment_id': str(uuid.uuid4()),
            'customer_id': customer['customer_id'],
            'order_id': str(uuid.uuid4()),
            'timestamp': datetime.utcnow().isoformat(),
            'amount': round(random.uniform(10, 1000), 2),
            'currency': 'USD',
            'payment_method': random.choice(['credit_card', 'debit_card', 'paypal', 'apple_pay', 'google_pay']),
            'payment_processor': random.choice(['stripe', 'paypal', 'square', 'adyen'])
        }
        
        if event_type == 'payment_failed':
            event.update({
                'failure_reason': random.choice([
                    'insufficient_funds',
                    'card_declined',
                    'expired_card',
                    'fraud_detected',
                    'network_error'
                ]),
                'retry_attempt': random.randint(1, 3)
            })
        
        elif event_type in ['refund_initiated', 'refund_completed']:
            event.update({
                'refund_reason': random.choice(['customer_request', 'defective_product', 'wrong_item', 'damaged_shipping']),
                'refund_amount': event['amount'] * random.uniform(0.5, 1.0)
            })
        
        return event
    
    def generate_system_event(self) -> Dict:
        """Generate a system-related event."""
        event_types = list(self.event_config['system_events'].keys())
        event_weights = list(self.event_config['system_events'].values())
        event_type = random.choices(event_types, weights=event_weights)[0]
        
        event = {
            'event_id': str(uuid.uuid4()),
            'event_type': event_type,
            'timestamp': datetime.utcnow().isoformat(),
            'service_name': random.choice(['web-app', 'api-gateway', 'payment-service', 'inventory-service', 'order-service']),
            'environment': random.choice(['production', 'staging', 'development'])
        }
        
        if event_type in ['user_session_start', 'user_session_end']:
            customer = random.choice(self.customers)
            event.update({
                'customer_id': customer['customer_id'],
                'session_id': str(uuid.uuid4()),
                'device_type': random.choice(['desktop', 'mobile', 'tablet'])
            })
        
        elif event_type == 'api_call':
            event.update({
                'endpoint': random.choice(['/api/products', '/api/orders', '/api/customers', '/api/payments']),
                'method': random.choice(['GET', 'POST', 'PUT', 'DELETE']),
                'response_code': random.choices([200, 201, 400, 401, 404, 500], weights=[0.7, 0.1, 0.05, 0.05, 0.05, 0.05])[0],
                'response_time_ms': random.randint(50, 2000)
            })
        
        elif event_type == 'error_occurred':
            event.update({
                'error_type': random.choice(['database_error', 'network_timeout', 'validation_error', 'authentication_error']),
                'error_message': 'Sample error message',
                'stack_trace': 'Sample stack trace',
                'severity': random.choice(['low', 'medium', 'high', 'critical'])
            })
        
        elif event_type == 'system_health_check':
            event.update({
                'cpu_usage': random.uniform(10, 90),
                'memory_usage': random.uniform(30, 85),
                'disk_usage': random.uniform(20, 80),
                'status': random.choices(['healthy', 'warning', 'critical'], weights=[0.8, 0.15, 0.05])[0]
            })
        
        return event
    
    def _get_or_create_session(self, customer_id: str) -> str:
        """Get existing session or create new one for customer."""
        if customer_id not in self.active_sessions:
            self.active_sessions[customer_id] = {
                'session_id': str(uuid.uuid4()),
                'created_at': datetime.utcnow(),
                'last_activity': datetime.utcnow()
            }
        else:
            # Update last activity
            self.active_sessions[customer_id]['last_activity'] = datetime.utcnow()
            
            # Create new session if current one is older than 30 minutes
            if datetime.utcnow() - self.active_sessions[customer_id]['last_activity'] > timedelta(minutes=30):
                self.active_sessions[customer_id] = {
                    'session_id': str(uuid.uuid4()),
                    'created_at': datetime.utcnow(),
                    'last_activity': datetime.utcnow()
                }
        
        return self.active_sessions[customer_id]['session_id']
    
    def send_event(self, topic: str, event: Dict, key: Optional[str] = None):
        """Send an event to a Kafka topic."""
        try:
            future = self.producer.send(topic, value=event, key=key)
            # Don't wait for acknowledgment to maintain high throughput
            # future.get(timeout=1)  # Uncomment for guaranteed delivery
            return True
        except KafkaError as e:
            logger.error(f"Failed to send event to {topic}: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error sending event: {str(e)}")
            return False
    
    def start_event_stream(self, events_per_second: int = 10, duration_seconds: Optional[int] = None):
        """Start generating and sending events continuously."""
        self.is_running = True
        start_time = datetime.utcnow()
        event_count = 0
        
        logger.info(f"Starting event stream: {events_per_second} events/second")
        
        try:
            while self.is_running:
                if duration_seconds and (datetime.utcnow() - start_time).seconds >= duration_seconds:
                    break
                
                # Generate different types of events
                event_generators = [
                    (self.generate_user_event, self.topics['user_events']),
                    (self.generate_order_event, self.topics['order_events']),
                    (self.generate_inventory_event, self.topics['inventory_events']),
                    (self.generate_payment_event, self.topics['payment_events']),
                    (self.generate_system_event, self.topics['system_events'])
                ]
                
                for _ in range(events_per_second):
                    if not self.is_running:
                        break
                    
                    # Randomly select event type with weighted distribution
                    generator, topic = random.choices(
                        event_generators,
                        weights=[0.4, 0.2, 0.15, 0.15, 0.1]  # User events most frequent
                    )[0]
                    
                    event = generator()
                    key = event.get('customer_id') or event.get('product_id') or event.get('order_id')
                    
                    if self.send_event(topic, event, key):
                        event_count += 1
                
                # Log progress
                if event_count % 100 == 0:
                    logger.info(f"Sent {event_count} events")
                
                # Sleep to maintain desired rate
                time.sleep(1)
                
        except KeyboardInterrupt:
            logger.info("Event stream interrupted by user")
        except Exception as e:
            logger.error(f"Error in event stream: {str(e)}")
        finally:
            self.stop()
            logger.info(f"Event stream stopped. Total events sent: {event_count}")
    
    def start_parallel_streams(self, num_producers: int = 3, events_per_second_per_producer: int = 10, duration_seconds: Optional[int] = None):
        """Start multiple parallel event streams for higher throughput."""
        logger.info(f"Starting {num_producers} parallel event streams")
        
        with ThreadPoolExecutor(max_workers=num_producers) as executor:
            futures = []
            for i in range(num_producers):
                future = executor.submit(self.start_event_stream, events_per_second_per_producer, duration_seconds)
                futures.append(future)
            
            # Wait for all producers to complete
            for future in futures:
                try:
                    future.result()
                except Exception as e:
                    logger.error(f"Producer thread failed: {str(e)}")
    
    def stop(self):
        """Stop event generation and close producer."""
        self.is_running = False
        if self.producer:
            self.producer.flush()
            self.producer.close()
            logger.info("Kafka producer closed")


def main():
    """Main function to run the event producer."""
    producer = ECommerceEventProducer()
    
    try:
        # Start event stream
        producer.start_event_stream(
            events_per_second=20,
            duration_seconds=3600  # Run for 1 hour
        )
    except KeyboardInterrupt:
        logger.info("Producer stopped by user")
    finally:
        producer.stop()


if __name__ == "__main__":
    main()
