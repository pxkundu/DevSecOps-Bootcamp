const express = require('express');
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
app.get('/health', (req, res) => {
  res.json({ status: 'healthy' });
});

// In-memory shipment store (stateless, for demo)
const shipments = {};

// POST /shipments - Create shipment for an order
app.post('/shipments', (req, res) => {
  const { orderId } = req.body;
  const shipmentId = `ship-${Date.now()}`;
  shipments[shipmentId] = { orderId, status: 'in transit', createdAt: new Date() };
  logger.info('Shipment created', { shipmentId, orderId });
  res.status(201).json({ shipmentId, status: 'in transit' });
});

// GET /shipments/:id - Get shipment status
app.get('/shipments/:id', (req, res) => {
  const { id } = req.params;
  const shipment = shipments[id];
  if (!shipment) return res.status(404).json({ error: 'Shipment not found' });
  res.json(shipment);
});

app.listen(5000, () => logger.info('logistics-service running', { port: 5000 }));
