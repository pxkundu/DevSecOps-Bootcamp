const request = require('supertest');
const app = require('../services/order-service/app');

describe('Order Service', () => {
  it('POST /supply-orders processes order with valid API key', async () => {
    const res = await request(app)
      .post('/supply-orders')
      .set('X-API-Key', 'default-key')
      .send({ orderId: 1, customerId: 1, productId: 'prod-001', quantity: 5 });
    expect(res.status).toBe(200);
    expect(res.body.shipmentId).toBeDefined();
  });

  it('POST /supply-orders fails without API key', async () => {
    const res = await request(app)
      .post('/supply-orders')
      .send({ orderId: 1, customerId: 1, productId: 'prod-001', quantity: 5 });
    expect(res.status).toBe(401);
  });
});
