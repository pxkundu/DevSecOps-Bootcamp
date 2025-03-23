const request = require('supertest');
const app = require('../services/logistics-service/app');

describe('Logistics Service', () => {
  it('POST /shipments creates a shipment with valid API key', async () => {
    const res = await request(app)
      .post('/shipments')
      .set('X-API-Key', 'default-key')
      .send({ orderId: 1 });
    expect(res.status).toBe(201);
    expect(res.body.shipmentId).toBeDefined();
  });

  it('POST /shipments fails without API key', async () => {
    const res = await request(app)
      .post('/shipments')
      .send({ orderId: 1 });
    expect(res.status).toBe(401);
  });
});
