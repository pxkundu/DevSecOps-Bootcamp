const express = require('express');
const { Pool } = require('pg');
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

// GET /inventory/:productId - Check stock availability
app.get('/inventory/:productId', async (req, res) => {
  const { productId } = req.params;
  try {
    const result = await pool.query('SELECT quantity FROM inventory WHERE product_id = $1', [productId]);
    if (result.rows.length === 0) return res.status(404).json({ error: 'Product not found' });
    res.json({ productId, quantity: result.rows[0].quantity });
  } catch (err) {
    logger.error('Error fetching inventory', { error: err.message });
    res.status(500).json({ error: 'Internal server error' });
  }
});

// PUT /inventory/:productId - Update stock levels
app.put('/inventory/:productId', async (req, res) => {
  const { productId } = req.params;
  const { quantity } = req.body;
  try {
    const result = await pool.query(
      'UPDATE inventory SET quantity = $1 WHERE product_id = $2 RETURNING quantity',
      [quantity, productId]
    );
    if (result.rows.length === 0) return res.status(404).json({ error: 'Product not found' });
    logger.info('Inventory updated', { productId, quantity });
    res.json({ productId, quantity: result.rows[0].quantity });
  } catch (err) {
    logger.error('Error updating inventory', { error: err.message });
    res.status(500).json({ error: 'Internal server error' });
  }
});

app.listen(4000, () => logger.info('inventory-service running', { port: 4000 }));
