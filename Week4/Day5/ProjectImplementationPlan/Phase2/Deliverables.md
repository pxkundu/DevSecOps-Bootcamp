**Phase 2: Backend - Microservices Development** of the **CRM-Integrated Global Supply Chain System** capstone project. 

This will represent 100% of the deliverables, fully implementing the four backend services (`crm-api`, `inventory-service`, `logistics-service`, `order-service`) with their respective `Dockerfile`, `app.js`, and `package.json` files, along with a PostgreSQL database schema for the `crm_supply_db`. 

---

## Deliverables for Phase 2
### Files
- **`services/crm-api/{Dockerfile,app.js,package.json}`**: Reused and extended CRM API for customer orders, integrating with `order-service`.
- **`services/inventory-service/{Dockerfile,app.js,package.json}`**: REST API for stock tracking, connected to RDS.
- **`services/logistics-service/{Dockerfile,app.js,package.json}`**: Stateless API for shipping logic, interacting with `order-service`.
- **`services/order-service/{Dockerfile,app.js,package.json}`**: Integration hub linking CRM orders to supply chain, persisting to RDS.
- **`docs/db-schema.sql`**: PostgreSQL schema for `crm_supply_db` with tables (`customers`, `inventory`, `orders`).

### Details
- **Tech**: Node.js (Express) with `node:18-alpine` Docker images, `pg` for PostgreSQL, and `axios` for HTTP calls.
- **Optimization**: Lightweight images (~150-200MB), minimal dependencies, environment variables for configuration.
- **DB Schema**: Simple, normalized tables with foreign keys, designed for CRM-supply chain integration.
- **Real-World Time**: ~4-6 days for 2-3 engineers (coding, testing, Dockerizing).

---

## Deliverables Breakdown
### 1. `crm-api`
- **Dockerfile**: Lightweight `node:18-alpine`, exposes port 3000.
- **app.js**: Implements `/orders` (create), `/orders/:id` (get), `/customers/:id` (get); integrates with `order-service`.
- **package.json**: Depends on `express`, `pg`, `axios`.

### 2. `inventory-service`
- **Dockerfile**: Port 4000, Alpine-based.
- **app.js**: Implements `/inventory/:productId` (get, put); connects to RDS `inventory` table.
- **package.json**: `express`, `pg`.

### 3. `logistics-service`
- **Dockerfile**: Port 5000, stateless.
- **app.js**: Implements `/shipments` (post, get); uses in-memory store (demo; real-world would persist via `order-service`).
- **package.json**: `express` only.

### 4. `order-service`
- **Dockerfile**: Port 6000, Alpine-based.
- **app.js**: Implements `/supply-orders` (post, get); orchestrates `inventory-service` and `logistics-service`, updates RDS `orders`.
- **package.json**: `express`, `pg`, `axios`.

### 5. `db-schema.sql`
- **Tables**: `customers` (CRM), `inventory` (supply chain), `orders` (integration).
- **Design**: Normalized with foreign keys, sample data for testing.

---

## Notes
- **Optimization**: 
  - Alpine images keep sizes ~150-200MB.
  - Minimal deps reduce vulnerabilities (e.g., no unnecessary `lodash`).
- **Config**: Env vars (`DB_HOST`, etc.) allow flexibility; defaults work locally, overridden in Kubernetes (Phase 4).
- **DevSecOps**: 
  - Error handling and logging included.
  - RDS password placeholder (use Secrets Manager in production).
- **Testing**: Run locally with `docker build` and `docker run`, connect to a local PostgreSQL instance with `db-schema.sql`.
