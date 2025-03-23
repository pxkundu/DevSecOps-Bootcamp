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

// POST /supply-orders - Process CRM order into supply chain
app.post('/supply-orders', async (req, res) => {
  const { orderId, customerId, productId, quantity } = req.body;
  try {
    const inventoryRes = await axios.get(`http://inventory-service:4000/inventory/${productId}`, {
      headers: { 'X-API-Key': apiKey }
    });
    if (inventoryRes.data.quantity < quantity) {
      await pool.query('UPDATE orders SET status = $1 WHERE id = $2', ['out_of_stock', orderId]);
      logger.warn('Insufficient inventory', { orderId, productId });
      return res.status(400).json({ error: 'Insufficient inventory' });
    }

    await axios.put(`http://inventory-service:4000/inventory/${productId}`, { quantity: inventoryRes.data.quantity - quantity }, {
      headers: { 'X-API-Key': apiKey }
    });

    const shipmentRes = await axios.post('http://logistics-service:5000/shipments', { orderId }, {
      headers: { 'X-API-Key': apiKey }
    });
    const shipmentId = shipmentRes.data.shipmentId;

    await pool.query('UPDATE orders SET status = $1, shipment_id = $2 WHERE id = $3', ['shipped', shipmentId, orderId]);
    logger.info('Order processed and shipped', { orderId, shipmentId });
    res.status(200).json({ orderId, shipmentId, status: 'shipped' });
  } catch (err) {
    logger.error('Error processing supply order', { error: err.message });
    await pool.query('UPDATE orders SET status = $1 WHERE id = $2', ['failed', orderId]);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// GET /supply-orders/:id - Retrieve order status
app.get('/supply-orders/:id', async (req, res) => {
  const { id } = req.params;
  try {
    const orderResult = await pool.query('SELECT * FROM orders WHERE id = $1', [id]);
    if (orderResult.rows.length === 0) return res.status(404).json({ error: 'Order not found' });
    const order = orderResult.rows[0];

    if (order.shipment_id) {
      const shipmentRes = await axios.get(`http://logistics-service:5000/shipments/${order.shipment_id}`, {
        headers: { 'X-API-Key': apiKey }
      });
      order.shipment_status = shipmentRes.data.status;
    }

    res.json(order);
  } catch (err) {
    logger.error('Error fetching supply order', { error: err.message });
    res.status(500).json({ error: 'Internal server error' });
  }
});

app.listen(6000, () => logger.info('order-service running', { port: 6000 }));
