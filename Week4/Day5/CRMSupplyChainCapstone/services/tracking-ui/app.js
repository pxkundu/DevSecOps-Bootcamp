const express = require('express');
const axios = require('axios');
const path = require('path');
const app = express();

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));
app.use(express.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, 'public')));

// API endpoint configuration
const logisticsServiceUrl = process.env.LOGISTICS_SERVICE_URL || 'http://localhost:5000';
const apiKey = process.env.API_KEY || 'default-key';

// Home page - Tracking search
app.get('/', (req, res) => {
  res.render('index', { shipment: null, error: null });
});

// Track shipment
app.get('/shipments/:id', async (req, res) => {
  const { id } = req.params;
  try {
    const shipmentRes = await axios.get(`${logisticsServiceUrl}/shipments/${id}`, { headers: { 'X-API-Key': apiKey } });
    res.render('index', { shipment: shipmentRes.data, error: null });
  } catch (err) {
    res.render('index', { shipment: null, error: 'Shipment not found or service unavailable' });
  }
});

app.listen(8000, () => console.log('tracking-ui running on port 8000'));
