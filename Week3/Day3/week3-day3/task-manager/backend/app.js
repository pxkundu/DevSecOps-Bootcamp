const express = require('express');
const app = express();
app.use(express.json());
let tasks = [];

app.post('/tasks', (req, res) => {
  const task = req.body;
  tasks.push(task);
  res.status(201).send(task);
});

app.get('/tasks', (req, res) => {
  res.send(tasks);
});

app.listen(3000, () => console.log('Backend running on port 3000'));
