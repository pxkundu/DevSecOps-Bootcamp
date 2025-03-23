const express = require('express');
const app = express();
app.get('/api/customers', (req, res) => {
  res.json({ message: "CRM API - Customer Data" });
});
app.listen(3000, () => console.log('CRM API running on port 3000'));
