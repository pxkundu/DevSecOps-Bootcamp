const express = require('express');
const { Pool } = require('pg');
const axios = require('axios');
const winston = require('winston');
const app = express();
app.use(express.json());

// Structured logging with winston
const logger = winston.createLogger({
  level: 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  transports: [new winston.transports.Console()]
});

// PostgreSQL connection
const pool = new Pool({
  user: process.env.DB_USER || 'admin',
  host: process.env.DB_HOST || 'localhost',
  database: process.env.DB_NAME || 'crm_supply_db',
  password: process.env.DB_PASSWORD || 'securepassword',
  port: process.env.DB_PORT || 5432,
});

// Basic authentication middleware
const apiKey = process.env.API_KEY || 'default-key';
app.use((req, res, next) => {
  if (req.headers['x-api-key'] !== apiKey) {
    logger.warn('Unauthorized access attempt', { path: req.path });
    return res.status(401).json({ error: 'Unauthorized' });
  }
  next();
});

// Health check endpoint
app.get('/health', async (req, res) => {
  try {
    await pool.query('SELECT 1');
    res.json({ status: 'healthy', db: 'connected' });
  } catch (err) {
    logger.error('Health check failed', { error: err.message });
    res.status(503).json({ status: 'unhealthy', db: 'disconnected' });
  }
});

// POST /orders - Create a customer order
app.post('/orders', async (req, res) => {
  const { customerId, productId, quantity } = req.body;
  try {
    const result = await pool.query(
      'INSERT INTO orders (customer_id, product_id, quantity, status) VALUES ($1, $2, $3, $4) RETURNING id',
      [customerId, productId, quantity, 'pending']
    );
    const orderId = result.rows[0].id;
    await axios.post('http://order-service:6000/supply-orders', { orderId, customerId, productId, quantity }, {
      headers: { 'X-API-Key': apiKey }
    });
    logger.info('Order created and sent to supply chain', { orderId });
    res.status(201).json({ orderId, message: 'Order created and sent to supply chain' });
  } catch (err) {
    logger.error('Error creating order', { error: err.message });
    res.status(500).json({ error: 'Internal server error' });
  }
});

// GET /orders/:id - Retrieve order details
app.get('/orders/:id', async (req, res) => {
  const { id } = req.params;
  try {
    const result = await pool.query('SELECT * FROM orders WHERE id = $1', [id]);
    if (result.rows.length === 0) return res.status(404).json({ error: 'Order not found' });
    res.json(result.rows[0]);
  } catch (err) {
    logger.error('Error fetching order', { error: err.message });
    res.status(500).json({ error: 'Internal server error' });
  }
});

// GET /customers/:id - Fetch customer data
app.get('/customers/:id', async (req, res) => {
  const { id } = req.params;
  try {
    const result = await pool.query('SELECT * FROM customers WHERE id = $1', [id]);
    if (result.rows.length === 0) return res.status(404).json({ error: 'Customer not found' });
    res.json(result.rows[0]);
  } catch (err) {
    logger.error('Error fetching customer', { error: err.message });
    res.status(500).json({ error: 'Internal server error' });
  }
});

app.listen(3000, () => logger.info('crm-api running', { port: 3000 }));
