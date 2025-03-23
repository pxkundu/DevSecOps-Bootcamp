## Backend - Microservices Development

### Objective
- Build and Dockerize backend services for CRM (`crm-api`) and supply chain (`inventory-service`, `logistics-service`, `order-service`) to handle customer orders, inventory tracking, shipping logic, and order integration.
- Deliver Docker images for these four services in a local registry, setting the stage for Kubernetes deployment in Phase 4.

### Real-World Time Estimate
- **Design & Coding**: ~2-3 days (API design, Node.js implementation for 2-3 engineers).
- **Dockerization**: ~1-2 days (writing Dockerfiles, building/testing images).
- **Validation**: ~1 day (local testing, integration checks).
- **Total**: ~4-6 days for a small team, reflecting industry-standard microservice development cycles.

---

### Thought Process
- **Microservices Architecture**: Adopt a decoupled, service-oriented design to ensure scalability, maintainability, and independent deployment—hallmarks of modern enterprise systems.
- **Reuse Existing Work**: Leverage the `crm-api` from Day 2’s CRM project to save time and maintain continuity, extending it for supply chain integration.
- **Lightweight & Efficient**: Use Node.js with an Alpine base in Docker to minimize resource usage and speed up builds, optimizing for cost and performance.
- **Stateless vs. Stateful**: Differentiate services (e.g., stateless `logistics-service` vs. stateful `inventory-service`) to align with real-world use cases and Kubernetes deployment needs.
- **DevSecOps Focus**: Embed security (e.g., input validation), observability (logging prep), and automation (Dockerized builds) from the start.
- **Real-World Use Case**: Simulate a retailer like Walmart integrating CRM orders with supply chain ops, ensuring practical relevance.

---

### Backend Components and Design

#### 1. CRM-API (Reused)
- **What**: A RESTful API managing customer orders, reused from Day 2’s CRM project.
- **How**:
  - Endpoints: 
    - `POST /orders`: Create a customer order.
    - `GET /orders/:id`: Retrieve order details.
    - `GET /customers/:id`: Fetch customer data.
  - Tech: Node.js (Express), stateless, connects to RDS (`crm_supply_db`) for persistence.
  - Integration: Extended to call `order-service` for supply chain linkage.
- **Why**:
  - **Reuse**: Avoids redundant development, leveraging Day 2’s proven functionality, akin to Amazon’s service reuse strategy.
  - **Core CRM**: Handles customer-facing operations, a critical piece for order initiation, mirroring Walmart’s customer-order workflows.
  - **Stateless**: Simplifies scaling in Kubernetes, a common enterprise choice.
- **DevSecOps**:
  - Input validation to prevent injection attacks.
  - Basic logging (e.g., request/response) for observability prep.
- **Diagram**:
  ```
  +-------------------------+
  | crm-api                 |
  | - POST /orders          |
  | - GET /orders/:id       |
  | - GET /customers/:id    |
  | -> RDS (crm_supply_db)  |
  | -> order-service        |
  +-------------------------+
  ```

#### 2. Inventory-Service (New)
- **What**: A RESTful API tracking stock levels, integrated with PostgreSQL.
- **How**:
  - Endpoints:
    - `GET /inventory/:productId`: Check stock availability.
    - `PUT /inventory/:productId`: Update stock (e.g., after order fulfillment).
  - Tech: Node.js (Express), stateful, uses RDS (`crm_supply_db`, `inventory` table).
  - Docker: Alpine-based Node.js image for lightweight deployment.
- **Why**:
  - **Supply Chain Core**: Real-time inventory tracking is essential for retailers (e.g., DHL’s logistics precision), ensuring orders align with stock.
  - **Stateful**: Persists data in RDS for durability, a standard for inventory systems needing consistency.
  - **Lightweight**: Alpine base reduces image size (~50MB vs. 900MB full Node), optimizing build and deploy times.
- **DevSecOps**:
  - DB connection encrypted (SSL to RDS).
  - Rate limiting to prevent abuse, a security best practice.
- **Diagram**:
  ```
  +---------------------------+
  | inventory-service         |
  | - GET /inventory/:id      |
  | - PUT /inventory/:id      |
  | -> RDS (inventory table)  |
  +---------------------------+
  ```

#### 3. Logistics-Service (New)
- **What**: A stateless API handling shipping logic and status updates.
- **How**:
  - Endpoints:
    - `POST /shipments`: Create a shipment for an order.
    - `GET /shipments/:id`: Get shipment status (e.g., “in transit”).
  - Tech: Node.js (Express), stateless, no direct DB (relies on `order-service` for persistence).
  - Docker: Alpine-based, minimal dependencies (Express only).
- **Why**:
  - **Shipping Logic**: Encapsulates logistics (e.g., route optimization simulation), a key supply chain function for DHL-like systems.
  - **Stateless**: Enables easy scaling and resilience in Kubernetes, reducing complexity.
  - **Decoupled**: Separates shipping from order state, improving maintainability, a Walmart-style microservice split.
- **DevSecOps**:
  - API key or token auth planned for secure calls (implemented in Phase 4).
  - Structured logging for shipment events.
- **Diagram**:
  ```
  +-----------------------+
  | logistics-service     |
  | - POST /shipments     |
  | - GET /shipments/:id  |
  | -> order-service      |
  +-----------------------+
  ```

#### 4. Order-Service (New)
- **What**: A RESTful API linking CRM orders to supply chain operations.
- **How**:
  - Endpoints:
    - `POST /supply-orders`: Process a CRM order (calls `inventory-service`, `logistics-service`).
    - `GET /supply-orders/:id`: Retrieve order status across CRM/supply chain.
  - Tech: Node.js (Express), stateless, connects to RDS (`orders` table) for state.
  - Docker: Alpine-based, integrates with other services via HTTP.
- **Why**:
  - **Integration Hub**: Bridges CRM (`crm-api`) and supply chain (`inventory-service`, `logistics-service`), ensuring seamless order flow, a critical retailer need (e.g., Amazon’s order fulfillment).
  - **Stateless Logic**: Keeps business logic lightweight, with state in RDS for reliability.
  - **Centralized Coordination**: Simplifies tracking across domains, reducing complexity for frontend UIs.
- **DevSecOps**:
  - Retry logic for service calls to handle failures (resilience).
  - Audit logging for order events (compliance prep).
- **Diagram**:
  ```
  +---------------------------+
  | order-service             |
  | - POST /supply-orders     |
  | - GET /supply-orders/:id  |
  | -> crm-api                |
  | -> inventory-service      |
  | -> logistics-service      |
  | -> RDS (orders table)     |
  +---------------------------+
  ```

---

### Overall Backend Architecture
- **Diagram**:
  ```
  +----------------+        +-----------------+
  | crm-api        |<------>| order-service   |
  | (Reused)       |        | (Integration)   |
  +----------------+        +-----------------+
          |                        |
          v                        v
  +-------------------+    +-------------------+
  | inventory-service |    | logistics-service |
  | (Stateful, RDS)   |    | (Stateless)       |
  +-------------------+    +-------------------+
          |
  +--------------------+
  | RDS: crm_supply_db |
  | - customers        |
  | - inventory        |
  | - orders           |
  +--------------------+
  ```

- **Flow**: 
  1. Customer places order via `crm-api`.
  2. `order-service` processes it, checking `inventory-service` for stock and triggering `logistics-service` for shipping.
  3. Data persists in RDS, with services interacting via REST APIs.

---

### Why This Design?
1. **Microservices**:
   - Independent services allow separate scaling (e.g., `logistics-service` during peak shipping), a Walmart/Amazon norm.
2. **Reuse**:
   - Extending `crm-api` saves ~1-2 days of dev time, mirroring enterprise efficiency.
3. **Lightweight**:
   - Node.js + Alpine reduces image sizes (e.g., ~50MB vs. 200MB with full Node), cutting build/deploy costs—key for DHL’s logistics apps.
4. **Stateless/Stateful Mix**:
   - Stateless services (`logistics-service`, `order-service`) scale easily, while stateful `inventory-service` ensures data integrity, a balanced enterprise approach.
5. **Integration**:
   - `order-service` as a hub simplifies CRM-supply chain linkage, reducing frontend complexity, a practical retailer choice.

---

### Industry Standards & DevSecOps Best Practices

#### Industry Standards
- **Service Isolation**: Each microservice has a single responsibility (e.g., `inventory-service` for stock), matching Amazon’s microservice design.
- **RESTful APIs**: Standardized endpoints (e.g., `GET /inventory/:id`) ensure interoperability, a Walmart/DHL practice.
- **Dockerization**: Alpine-based images align with lightweight container trends, optimizing CI/CD pipelines (e.g., Jenkins in Phase 5).
- **Database Sharing**: Single RDS instance (`crm_supply_db`) mimics centralized data stores in retail (e.g., Walmart’s inventory DB), balancing cost and simplicity.

#### DevSecOps Best Practices
1. **Security**:
   - Input validation in APIs prevents injection (e.g., SQL, XSS).
   - RDS SSL connections (planned in Docker env vars) secure data in transit.
   - API auth (e.g., tokens) prepped for Phase 4, ensuring secure service calls.
2. **Resilience**:
   - Retry logic in `order-service` handles transient failures (e.g., `inventory-service` downtime).
   - Stateless design enables Kubernetes self-healing (Phase 4).
3. **Observability**:
   - Basic logging (e.g., request IDs, timestamps) in each service preps for Prometheus/ELK integration.
   - Audit trails in `order-service` support compliance (e.g., GDPR, SOX).
4. **Automation**:
   - Dockerized services automate builds/tests in CI/CD (Phase 5), a DHL automation staple.
   - Minimal dependencies reduce vulnerability surface and build time.
5. **Cost Efficiency**:
   - Lightweight images and stateless logic minimize compute needs, aligning with budget goals.

---

### Implementation Notes
- **Deliverables**: 
  - `services/crm-api/{Dockerfile,app.js,package.json}` (extended from Day 2).
  - `services/inventory-service/{Dockerfile,app.js,package.json}`.
  - `services/logistics-service/{Dockerfile,app.js,package.json}`.
  - `services/order-service/{Dockerfile,app.js,package.json}`.
- **Local Registry**: Images built locally (e.g., `docker build -t crm-api .`), pushed to ECR in Phase 5.
- **No AWS Spend**: Development occurs locally, leveraging Phase 1’s infra prep without provisioning yet.

---

### Why This Phase Matters
Phase 2 is the backbone of the project—without these services, CRM and supply chain features can’t function. By designing them as modular, secure, and efficient microservices, we:
- Enable scalability for millions of orders (Fortune 100 scale).
- Ensure professional-grade code ready for Kubernetes (Phase 4).
- Lay a DevSecOps foundation that matures in later phases (e.g., CI/CD, testing).

This detailed plan ensures Phase 2 delivers robust building blocks, setting us up for success.