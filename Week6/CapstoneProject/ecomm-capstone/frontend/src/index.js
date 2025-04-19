import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import express from 'express'; // For health endpoints

const app = express();
app.get('/health', (req, res) => res.status(200).send('OK'));
app.get('/ready', (req, res) => res.status(200).send('Ready'));
app.listen(80, () => console.log('Health server on port 80'));

ReactDOM.render(<App />, document.getElementById('root'));
