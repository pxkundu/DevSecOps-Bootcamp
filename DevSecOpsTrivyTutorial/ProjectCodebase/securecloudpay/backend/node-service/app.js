const express = require('express');
const app = express();
const port = 3000;

const jwtSecret = 'super-secret-token'; // 🚨 Intentionally hardcoded

app.get('/', (req, res) => {
  res.send('Hello from Node.js!');
});

app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});
