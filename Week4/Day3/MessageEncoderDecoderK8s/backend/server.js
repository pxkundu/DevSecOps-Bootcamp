const express = require('express');
const app = express();
app.use(express.json());
app.post('/encode', (req, res) => {
  const message = req.body.message || '';
  const binary = message.split('').map(char => char.charCodeAt(0).toString(2).padStart(8, '0')).join(' ');
  res.json({ binary });
});
app.post('/decode', (req, res) => {
  const binary = req.body.binary || '';
  const message = binary.split(' ').map(bin => String.fromCharCode(parseInt(bin, 2))).join('');
  res.json({ message });
});
app.listen(4000, () => console.log('Backend running on port 4000'));
