# Environment Configuration for Phase 2 Backend Services

This document describes the environment variables used by the Phase 2 backend services (`crm-api`, `inventory-service`, `logistics-service`, `order-service`).

## Common Variables
- **DB_HOST**: PostgreSQL host (default: `localhost` locally, RDS endpoint in production).
- **DB_USER**: DB username (default: `admin`).
- **DB_PASSWORD**: DB password (set securely in production, e.g., via AWS Secrets Manager).
- **DB_NAME**: Database name (default: `crm_supply_db`).
- **DB_PORT**: DB port (default: `5432`).
- **API_KEY**: API key for authentication (default: `default-key` locally, unique per service in production).

## Service-Specific Variables
- **crm-api**:
  - **ORDER_SERVICE_URL**: Order service endpoint (default: `http://localhost:6000`).
- **order-service**:
  - **INVENTORY_SERVICE_URL**: Inventory service endpoint (default: `http://localhost:4000`).
  - **LOGISTICS_SERVICE_URL**: Logistics service endpoint (default: `http://localhost:5000`).

## Usage
- Copy `.env.example` to `.env` in each service directory and adjust values as needed.
- Locally: Set manually or use Docker `-e` flags.
- Production: Use Kubernetes ConfigMaps/Secrets (Phase 4).
