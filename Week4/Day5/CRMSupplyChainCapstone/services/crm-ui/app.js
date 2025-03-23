const express = require('express');
const axios = require('axios');
const path = require('path');
const app = express();

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));
app.use(express.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, 'public')));

// API endpoints configuration
const crmApiUrl = process.env.CRM_API_URL || 'http://localhost:3000';
const orderServiceUrl = process.env.ORDER_SERVICE_URL || 'http://localhost:6000';
const apiKey = process.env.API_KEY || 'default-key';

// Home page - Customer dashboard
app.get('/', async (req, res) => {
  try {
    const ordersRes = await axios.get(`${crmApiUrl}/orders`, { headers: { 'X-API-Key': apiKey } });
    res.render('index', { orders: ordersRes.data || [], error: null });
  } catch (err) {
    res.render('index', { orders: [], error: 'Failed to fetch orders' });
  }
});

// Submit new order
app.post('/orders', async (req, res) => {
  const { productId, quantity } = req.body;
  try {
    await axios.post(`${crmApiUrl}/orders`, { customerId: 1, productId, quantity }, { headers: { 'X-API-Key': apiKey } });
    res.redirect('/');
  } catch (err) {
    res.render('index', { orders: [], error: 'Failed to create order' });
  }
});

// Order details
app.get('/orders/:id', async (req, res) => {
  const { id } = req.params;
  try {
    const orderRes = await axios.get(`${orderServiceUrl}/supply-orders/${id}`, { headers: { 'X-API-Key': apiKey } });
    res.render('order-details', { order: orderRes.data });
  } catch (err) {
    res.render('order-details', { order: null, error: 'Failed to fetch order details' });
  }
});

app.listen(7000, () => console.log('crm-ui running on port 7000'));
