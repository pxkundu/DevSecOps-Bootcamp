"""
E-Commerce Sample Data Generator

This script generates realistic sample data for the e-commerce data platform
including customers, products, orders, and behavioral events.
"""

import json
import random
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List

import pandas as pd
from faker import Faker

# Initialize Faker for generating realistic data
fake = Faker()


class ECommerceDataGenerator:
    """Generates sample e-commerce data for the data platform."""
    
    def __init__(self, output_dir: str = "data-sources/sample-data"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Product categories and their properties
        self.categories = {
            "Electronics": ["Smartphone", "Laptop", "Tablet", "Headphones", "Smart Watch"],
            "Clothing": ["T-Shirt", "Jeans", "Dress", "Jacket", "Shoes"],
            "Home & Garden": ["Furniture", "Appliances", "Decor", "Tools", "Plants"],
            "Books": ["Fiction", "Non-Fiction", "Textbook", "Children", "Self-Help"],
            "Sports": ["Equipment", "Apparel", "Accessories", "Fitness", "Outdoor"]
        }
        
        self.price_ranges = {
            "Electronics": (50, 2000),
            "Clothing": (15, 300),
            "Home & Garden": (25, 1500),
            "Books": (10, 80),
            "Sports": (20, 500)
        }
        
        # Generate base data first
        self.customers = []
        self.products = []
        self.generated_data = {}

    def generate_customers(self, num_customers: int = 10000) -> List[Dict]:
        """Generate customer data."""
        print(f"Generating {num_customers} customers...")
        
        customers = []
        for i in range(num_customers):
            customer_id = str(uuid.uuid4())
            registration_date = fake.date_between(start_date='-2y', end_date='today')
            
            customer = {
                "customer_id": customer_id,
                "email": fake.email(),
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
                "phone": fake.phone_number(),
                "date_of_birth": fake.date_of_birth(minimum_age=18, maximum_age=80).isoformat(),
                "gender": random.choice(["M", "F", "Other"]),
                "registration_date": registration_date.isoformat(),
                "address": {
                    "street": fake.street_address(),
                    "city": fake.city(),
                    "state": fake.state(),
                    "zip_code": fake.zipcode(),
                    "country": fake.country_code()
                },
                "preferences": {
                    "newsletter": random.choice([True, False]),
                    "sms_notifications": random.choice([True, False]),
                    "preferred_categories": random.sample(list(self.categories.keys()), 
                                                        random.randint(1, 3))
                },
                "loyalty_tier": random.choice(["Bronze", "Silver", "Gold", "Platinum"]),
                "total_spent": round(random.uniform(0, 10000), 2),
                "last_login": fake.date_time_between(start_date=registration_date, 
                                                   end_date='now').isoformat()
            }
            customers.append(customer)
        
        self.customers = customers
        return customers

    def generate_products(self, num_products: int = 5000) -> List[Dict]:
        """Generate product catalog data."""
        print(f"Generating {num_products} products...")
        
        products = []
        for i in range(num_products):
            category = random.choice(list(self.categories.keys()))
            subcategory = random.choice(self.categories[category])
            price_min, price_max = self.price_ranges[category]
            
            product_id = str(uuid.uuid4())
            created_date = fake.date_between(start_date='-1y', end_date='today')
            
            product = {
                "product_id": product_id,
                "sku": f"SKU-{random.randint(100000, 999999)}",
                "name": f"{fake.word().title()} {subcategory}",
                "description": fake.text(max_nb_chars=500),
                "category": category,
                "subcategory": subcategory,
                "brand": fake.company(),
                "price": round(random.uniform(price_min, price_max), 2),
                "cost": round(random.uniform(price_min * 0.3, price_min * 0.7), 2),
                "weight": round(random.uniform(0.1, 10.0), 2),
                "dimensions": {
                    "length": round(random.uniform(5, 50), 1),
                    "width": round(random.uniform(5, 50), 1),
                    "height": round(random.uniform(1, 30), 1)
                },
                "inventory": {
                    "stock_quantity": random.randint(0, 1000),
                    "reserved_quantity": random.randint(0, 50),
                    "reorder_point": random.randint(10, 100),
                    "supplier_id": str(uuid.uuid4())
                },
                "rating": round(random.uniform(1.0, 5.0), 1),
                "review_count": random.randint(0, 1000),
                "tags": random.sample(["popular", "new", "sale", "featured", "limited"], 
                                    random.randint(0, 3)),
                "is_active": random.choice([True, True, True, False]),  # 75% active
                "created_date": created_date.isoformat(),
                "updated_date": fake.date_time_between(start_date=created_date, 
                                                     end_date='now').isoformat()
            }
            products.append(product)
        
        self.products = products
        return products

    def generate_orders(self, num_orders: int = 50000) -> List[Dict]:
        """Generate order transaction data."""
        print(f"Generating {num_orders} orders...")
        
        if not self.customers or not self.products:
            raise ValueError("Must generate customers and products before orders")
        
        orders = []
        for i in range(num_orders):
            customer = random.choice(self.customers)
            order_date = fake.date_time_between(start_date='-1y', end_date='now')
            
            # Generate order items (1-5 items per order)
            num_items = random.randint(1, 5)
            order_items = []
            total_amount = 0
            
            for _ in range(num_items):
                product = random.choice(self.products)
                quantity = random.randint(1, 3)
                unit_price = product["price"]
                line_total = quantity * unit_price
                total_amount += line_total
                
                order_items.append({
                    "product_id": product["product_id"],
                    "sku": product["sku"],
                    "product_name": product["name"],
                    "quantity": quantity,
                    "unit_price": unit_price,
                    "line_total": round(line_total, 2)
                })
            
            # Calculate shipping and tax
            shipping_cost = round(random.uniform(0, 25), 2) if total_amount < 100 else 0
            tax_amount = round(total_amount * 0.08, 2)  # 8% tax
            final_total = round(total_amount + shipping_cost + tax_amount, 2)
            
            order = {
                "order_id": str(uuid.uuid4()),
                "customer_id": customer["customer_id"],
                "order_date": order_date.isoformat(),
                "order_status": random.choice(["pending", "processing", "shipped", 
                                             "delivered", "cancelled", "returned"]),
                "payment_method": random.choice(["credit_card", "debit_card", "paypal", 
                                               "apple_pay", "google_pay"]),
                "payment_status": random.choice(["pending", "completed", "failed", "refunded"]),
                "shipping_address": customer["address"],
                "billing_address": customer["address"],
                "items": order_items,
                "subtotal": round(total_amount, 2),
                "shipping_cost": shipping_cost,
                "tax_amount": tax_amount,
                "total_amount": final_total,
                "currency": "USD",
                "promotion_code": fake.word() if random.random() < 0.2 else None,
                "discount_amount": round(random.uniform(0, total_amount * 0.2), 2) 
                                 if random.random() < 0.2 else 0,
                "estimated_delivery": (order_date + timedelta(days=random.randint(2, 14))).isoformat(),
                "tracking_number": f"TRACK{random.randint(1000000000, 9999999999)}" 
                                 if random.random() < 0.8 else None
            }
            orders.append(order)
        
        return orders

    def generate_events(self, num_events: int = 200000) -> List[Dict]:
        """Generate user behavioral events."""
        print(f"Generating {num_events} behavioral events...")
        
        if not self.customers or not self.products:
            raise ValueError("Must generate customers and products before events")
        
        events = []
        event_types = [
            "page_view", "product_view", "add_to_cart", "remove_from_cart",
            "search", "login", "logout", "checkout_start", "checkout_complete",
            "wishlist_add", "review_submit", "share_product"
        ]
        
        for i in range(num_events):
            customer = random.choice(self.customers)
            event_type = random.choice(event_types)
            timestamp = fake.date_time_between(start_date='-6m', end_date='now')
            
            # Base event properties
            event = {
                "event_id": str(uuid.uuid4()),
                "customer_id": customer["customer_id"],
                "session_id": str(uuid.uuid4()),
                "event_type": event_type,
                "timestamp": timestamp.isoformat(),
                "user_agent": fake.user_agent(),
                "ip_address": fake.ipv4(),
                "referrer": fake.url() if random.random() < 0.5 else None,
                "page_url": f"https://techmart.com/{fake.uri_path()}"
            }
            
            # Add event-specific properties
            if event_type in ["product_view", "add_to_cart", "remove_from_cart", 
                            "wishlist_add", "share_product"]:
                product = random.choice(self.products)
                event["product_id"] = product["product_id"]
                event["product_name"] = product["name"]
                event["product_category"] = product["category"]
                event["product_price"] = product["price"]
            
            elif event_type == "search":
                event["search_query"] = fake.word()
                event["search_results_count"] = random.randint(0, 100)
            
            elif event_type == "review_submit":
                product = random.choice(self.products)
                event["product_id"] = product["product_id"]
                event["rating"] = random.randint(1, 5)
                event["review_text"] = fake.text(max_nb_chars=200)
            
            elif event_type in ["checkout_start", "checkout_complete"]:
                event["cart_value"] = round(random.uniform(10, 500), 2)
                event["cart_items_count"] = random.randint(1, 10)
            
            events.append(event)
        
        return events

    def generate_inventory_updates(self, num_updates: int = 25000) -> List[Dict]:
        """Generate inventory update events."""
        print(f"Generating {num_updates} inventory updates...")
        
        if not self.products:
            raise ValueError("Must generate products before inventory updates")
        
        updates = []
        update_types = ["restock", "sale", "adjustment", "return", "damaged"]
        
        for i in range(num_updates):
            product = random.choice(self.products)
            update_type = random.choice(update_types)
            timestamp = fake.date_time_between(start_date='-6m', end_date='now')
            
            # Determine quantity change based on update type
            if update_type == "restock":
                quantity_change = random.randint(10, 500)
            elif update_type == "sale":
                quantity_change = -random.randint(1, 10)
            elif update_type == "return":
                quantity_change = random.randint(1, 5)
            elif update_type == "damaged":
                quantity_change = -random.randint(1, 20)
            else:  # adjustment
                quantity_change = random.randint(-50, 50)
            
            update = {
                "update_id": str(uuid.uuid4()),
                "product_id": product["product_id"],
                "sku": product["sku"],
                "update_type": update_type,
                "quantity_change": quantity_change,
                "previous_quantity": random.randint(0, 1000),
                "new_quantity": max(0, random.randint(0, 1000) + quantity_change),
                "reason": fake.sentence(),
                "updated_by": fake.user_name(),
                "timestamp": timestamp.isoformat(),
                "location": random.choice(["Warehouse-A", "Warehouse-B", "Store-NYC", 
                                         "Store-LA", "Store-Chicago"])
            }
            updates.append(update)
        
        return updates

    def save_data_to_files(self, data_dict: Dict[str, List[Dict]]):
        """Save generated data to various file formats."""
        print("Saving data to files...")
        
        for data_type, data_list in data_dict.items():
            if not data_list:
                continue
                
            # Save as JSON
            json_file = self.output_dir / f"{data_type}.json"
            with open(json_file, 'w') as f:
                json.dump(data_list, f, indent=2, default=str)
            
            # Save as CSV
            csv_file = self.output_dir / f"{data_type}.csv"
            df = pd.json_normalize(data_list)
            df.to_csv(csv_file, index=False)
            
            # Save as Parquet (more efficient for large datasets)
            parquet_file = self.output_dir / f"{data_type}.parquet"
            df.to_parquet(parquet_file, index=False)
            
            print(f"Saved {len(data_list)} {data_type} records")

    def generate_all_data(self, 
                         num_customers: int = 10000,
                         num_products: int = 5000,
                         num_orders: int = 50000,
                         num_events: int = 200000,
                         num_inventory_updates: int = 25000):
        """Generate all sample data."""
        print("Starting data generation...")
        
        # Generate data in order (dependencies matter)
        customers = self.generate_customers(num_customers)
        products = self.generate_products(num_products)
        orders = self.generate_orders(num_orders)
        events = self.generate_events(num_events)
        inventory_updates = self.generate_inventory_updates(num_inventory_updates)
        
        # Compile all data
        all_data = {
            "customers": customers,
            "products": products,
            "orders": orders,
            "events": events,
            "inventory_updates": inventory_updates
        }
        
        # Save to files
        self.save_data_to_files(all_data)
        
        print("Data generation completed!")
        print(f"Files saved to: {self.output_dir}")
        
        return all_data


def main():
    """Main function to run data generation."""
    generator = ECommerceDataGenerator()
    
    # Generate sample data
    generator.generate_all_data(
        num_customers=1000,      # Reduced for development
        num_products=500,        # Reduced for development
        num_orders=5000,         # Reduced for development
        num_events=20000,        # Reduced for development
        num_inventory_updates=2500  # Reduced for development
    )


if __name__ == "__main__":
    main()
