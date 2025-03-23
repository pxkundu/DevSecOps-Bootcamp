const request = require('supertest');
const app = require('../services/inventory-service/app');

describe('Inventory Service', () => {
  it('GET /inventory/:productId returns stock with valid API key', async () => {
    const res = await request(app)
      .get('/inventory/prod-001')
      .set('X-API-Key', 'default-key');
    expect(res.status).toBe(200);
    expect(res.body.quantity).toBeDefined();
  });

  it('GET /inventory/:productId fails without API key', async () => {
    const res = await request(app).get('/inventory/prod-001');
    expect(res.status).toBe(401);
  });
});
