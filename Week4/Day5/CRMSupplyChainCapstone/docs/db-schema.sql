-- PostgreSQL schema for crm_supply_db

-- Customers table (CRM data)
CREATE TABLE customers (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Inventory table (Supply chain data)
CREATE TABLE inventory (
  product_id VARCHAR(50) PRIMARY KEY,
  quantity INT NOT NULL CHECK (quantity >= 0),
  last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Orders table (Links CRM and supply chain)
CREATE TABLE orders (
  id SERIAL PRIMARY KEY,
  customer_id INT REFERENCES customers(id),
  product_id VARCHAR(50) REFERENCES inventory(product_id),
  quantity INT NOT NULL CHECK (quantity > 0),
  status VARCHAR(50) NOT NULL DEFAULT 'pending', -- pending, out_of_stock, shipped, failed
  shipment_id VARCHAR(50),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Sample data
INSERT INTO customers (name, email) VALUES
  ('John Doe', 'john.doe@example.com'),
  ('Jane Smith', 'jane.smith@example.com');

INSERT INTO inventory (product_id, quantity) VALUES
  ('prod-001', 100),
  ('prod-002', 50);

INSERT INTO orders (customer_id, product_id, quantity) VALUES
  (1, 'prod-001', 10);
