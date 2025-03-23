const express = require('express');
const app = express();
app.use(express.static('public'));
app.use(express.urlencoded({ extended: true }));
app.get('/', (req, res) => {
  res.send(`
    <h1>Message Encoder/Decoder</h1>
    <form action="/encode" method="POST">
      <label>English Message: <input type="text" name="message"></label>
      <button type="submit">Encode to Binary</button>
    </form>
    <form action="/decode" method="POST">
      <label>Binary Message: <input type="text" name="binary"></label>
      <button type="submit">Decode to English</button>
    </form>
    <div id="result"></div>
    <script>
      document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', async (e) => {
          e.preventDefault();
          const formData = new FormData(form);
          const response = await fetch(form.action, {
            method: 'POST',
            body: formData
          });
          const data = await response.json();
          document.getElementById('result').innerHTML = '<p>Result: ' + data.result + '</p>';
        });
      });
    </script>
  `);
});
app.post('/encode', async (req, res) => {
  const message = req.body.message;
  const response = await fetch('http://blog-backend-service:4000/encode', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message })
  });
  const data = await response.json();
  res.json({ result: data.binary });
});
app.post('/decode', async (req, res) => {
  const binary = req.body.binary;
  const response = await fetch('http://blog-backend-service:4000/decode', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ binary })
  });
  const data = await response.json();
  res.json({ result: data.message });
});
app.listen(3000, () => console.log('Frontend running on port 3000'));
