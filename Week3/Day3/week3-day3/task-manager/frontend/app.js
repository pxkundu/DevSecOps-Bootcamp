const express = require('express');
const axios = require('axios');
const app = express();

app.get('/tasks', async (req, res) => {
  try {
    const response = await axios.get('http://localhost:3000/tasks');
    res.send(response.data);
  } catch (error) {
    res.status(500).send('Error fetching tasks');
  }
});

app.listen(8080, () => console.log('Frontend running on port 8080'));
