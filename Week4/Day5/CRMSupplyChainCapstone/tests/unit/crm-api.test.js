const request = require('supertest');
const app = require('../services/crm-api/app');

describe('CRM API', () => {
  it('POST /orders creates an order with valid API key', async () => {
    const res = await request(app)
      .post('/orders')
      .set('X-API-Key', 'default-key')
      .send({ customerId: 1, productId: 'prod-001', quantity: 5 });
    expect(res.status).toBe(201);
    expect(res.body.orderId).toBeDefined();
  });

  it('POST /orders fails without API key', async () => {
    const res = await request(app)
      .post('/orders')
      .send({ customerId: 1, productId: 'prod-001', quantity: 5 });
    expect(res.status).toBe(401);
  });
});
