## Phase 3: Frontend - User Interfaces

### Objective
- Develop and Dockerize two frontend services:
  - **`crm-ui`**: Reused and extended customer dashboard for order management.
  - **`tracking-ui`**: New UI for tracking shipment statuses.
- Deliver Docker images for both services in a local registry, ready for Kubernetes deployment in Phase 4.

### Real-World Time Estimate
- **Design & Coding**: ~3-4 days (UI design, Node.js/Express coding for 2-3 engineers).
- **Dockerization**: ~1 day (building/testing images).
- **Validation**: ~1 day (local testing, integration with backend).
- **Total**: ~5-6 days, reflecting a realistic sprint for lightweight frontend development.

---

### Thought Process
- **Minimalist Approach**: Use Node.js with Express to serve SPAs, leveraging server-side rendering (SSR) with EJS templates instead of client-heavy frameworks. This keeps the frontend lightweight, cost-effective, and quick to build—ideal for a capstone scope while mimicking enterprise dashboards (e.g., DHL’s tracking portals).
- **Reuse & Extend**: Build on `crm-ui` from Day 2’s CRM project, adding supply chain integration, to save time and maintain consistency.
- **Dynamic & Reusable**: Design UI components (e.g., tables, buttons) as modular EJS partials for reuse across both UIs, ensuring maintainability and scalability.
- **User-Centric**: Prioritize simplicity and functionality—customers manage orders in `crm-ui`, while supply chain visibility shines in `tracking-ui`—mirroring real-world retail UIs.
- **DevSecOps**: Embed security (e.g., input sanitization), observability (logging prep), and automation (Dockerized builds) from the start.

---

### UI Components and Design

#### 1. `crm-ui` (Reused Customer Dashboard)
- **What**: A dashboard for customers to view and place orders, extended to show supply chain status.
- **How**:
  - **Tech**: Node.js (Express), EJS templates, vanilla JS for dynamic updates, CSS (e.g., Tailwind or custom).
  - **Endpoints**:
    - `GET /`: Renders dashboard with order list and “Place Order” form.
    - `POST /orders`: Submits new order to `crm-api`.
    - `GET /orders/:id`: Fetches order details with supply chain status (via `order-service`).
  - **Layout**:
    - **Header**: Logo, user greeting (e.g., “Welcome, John”).
    - **Sidebar**: Navigation (Orders, Profile).
    - **Main Content**:
      - **Order Table**: Lists orders (ID, Product, Quantity, Status), reusable component.
      - **Order Form**: Input fields (Product ID, Quantity), submit button.
      - **Order Details Modal**: Pops up with status (e.g., “Shipped”, shipment ID).
- **Why**:
  - **Reuse**: Extends Day 2’s `crm-ui`, saving ~1-2 days of dev time, akin to Amazon’s iterative UI updates.
  - **Customer Focus**: Simplifies order management, a core CRM need (e.g., Walmart’s customer portal).
  - **Lightweight**: SSR with EJS avoids heavy JS bundles, optimizing load times for cost-conscious retailers.
- **Diagram**:
  ```
  +----------------------------------------+
  | Header (Logo, User)                    |
  +----------------------------------------+
  | Sidebar    | Main                      |
  | - Orders   | - Order Table (Reusable)  |
  | - Profile  | - Order Form              |
  |            | - Modal (Order Details)   |
  +----------------------------------------+
  ```

#### 2. `tracking-ui` (Shipment Tracking Interface)
- **What**: A public-facing UI to display shipment statuses, fetching data from `logistics-service`.
- **How**:
  - **Tech**: Node.js (Express), EJS, vanilla JS, CSS.
  - **Endpoints**:
    - `GET /`: Renders tracking page with search form.
    - `GET /shipments/:id`: Fetches shipment details from `logistics-service`.
  - **Layout**:
    - **Header**: Branding (e.g., “Supply Chain Tracker”).
    - **Main Content**:
      - **Search Bar**: Input for shipment ID, submit button.
      - **Shipment Card**: Displays status (e.g., “In Transit”), order ID, timestamp—reusable component.
      - **Status Timeline**: Visual steps (e.g., “Pending → In Transit → Delivered”).
- **Why**:
  - **Visibility**: Provides real-time shipment tracking, a key supply chain feature (e.g., DHL’s tracking portal).
  - **Simplicity**: Single-purpose UI reduces complexity, aligning with cost/time goals.
  - **Dynamic**: Fetches live data, enhancing user trust, a retailer standard.
- **Diagram**:
  ```
  +----------------------------+
  | Header (Branding)          |
  +----------------------------+
  | Main                       |
  | - Search Bar               |
  | - Shipment Card (Reusable) |
  | - Status Timeline          |
  +----------------------------+
  ```

---

### Dynamic and Reusable Components
- **Order Table (crm-ui)**:
  - **Design**: EJS partial (`views/partials/order-table.ejs`) with `<table>` dynamically populated via JS fetching `/orders`.
  - **Reuse**: Could be adapted for admin UIs in future phases.
  - **Why**: Reduces code duplication, a maintainability win (Walmart’s reusable widgets).
- **Shipment Card (tracking-ui)**:
  - **Design**: EJS partial (`views/partials/shipment-card.ejs`) with `<div>` showing status, order ID, etc.
  - **Reuse**: Applicable to `crm-ui` for shipment details or analytics UIs later.
  - **Why**: Modular design speeds up development and updates (Amazon’s component library approach).
- **Buttons and Forms**:
  - **Design**: EJS partials (`views/partials/button.ejs`, `form.ejs`) with consistent styling (e.g., Tailwind classes).
  - **Reuse**: Shared across both UIs for submits, navigation.
  - **Why**: Ensures UI consistency, a professional standard (DHL’s uniform UX).

---

### Overall Frontend Architecture
- **Diagram**:
  ```
  +-------------+       +----------------+
  | crm-ui      |<----->| crm-api        |
  | (Port 7000) |       +----------------+
  |             |<----->| order-service  |
  +-------------+       +----------------+
                               |
  +-------------+       +-------------------+
  | tracking-ui |<----->| logistics-service |
  | (Port 8000) |       +-------------------+
  +-------------+
  ```
- **Flow**:
  1. `crm-ui` fetches orders from `crm-api`, supply chain status from `order-service`.
  2. `tracking-ui` queries `logistics-service` for shipment details.

---

### Why This Design?
1. **Minimalist SPA**:
   - SSR with EJS and vanilla JS keeps it lightweight (~100-200KB images), avoiding React’s build overhead—a cost/time saver for a capstone (unlike Amazon’s client-heavy UIs).
2. **Reuse**:
   - Extending `crm-ui` leverages prior work, mirroring enterprise efficiency (e.g., Walmart’s iterative dashboards).
3. **Dynamic**:
   - Real-time data via backend calls ensures UX reflects live state, a retailer must-have (DHL’s tracking).
4. **Modularity**:
   - Reusable components reduce future dev effort, a professional practice (Amazon’s design systems).
5. **User Experience**:
   - Simple, focused layouts meet customer/supply chain needs without overcomplication, aligning with real-world UIs.

---

### Industry Standards & DevSecOps Best Practices

#### Industry Standards
- **Lightweight UIs**: SSR over heavy frameworks matches cost-efficient enterprise portals (e.g., DHL’s tracking pages).
- **Responsive Design**: Use CSS (e.g., Tailwind) for mobile-friendly layouts, a retail norm (Walmart’s customer UIs).
- **API-Driven**: Fetching data from backend services mirrors microservice UIs (Amazon’s modular frontends).
- **Consistency**: Reusable components ensure uniform look/feel, a UX standard (DHL’s branding).

#### DevSecOps Best Practices
1. **Security**:
   - Sanitize inputs in forms (e.g., `escape-html`) to prevent XSS, a must for public UIs.
   - Use API keys (from Phase 2) for secure backend calls, extendable to JWT later.
2. **Resilience**:
   - Graceful error handling in JS (e.g., “Service unavailable” messages) improves UX during backend downtime.
   - Health checks from Phase 2 ensure UI reflects service status.
3. **Observability**:
   - Prep logging in Express (e.g., `winston` from Phase 2) for request tracking, integrating with ELK later.
   - Client-side JS logs errors to console (future: send to backend).
4. **Automation**:
   - Dockerized builds enable CI/CD (Phase 5), a DHL automation staple.
   - Minimal deps reduce build time and vulnerabilities.
5. **Cost Efficiency**:
   - No frameworks or extra infra keep dev costs low, aligning with budget goals.

---

### Implementation Notes
- **Deliverables**:
  - `services/crm-ui/{Dockerfile,app.js,package.json,views/}` (with `index.ejs`, partials).
  - `services/tracking-ui/{Dockerfile,app.js,package.json,views/}` (with `index.ejs`, partials).
- **Local Registry**: Images (`crm-ui:latest`, `tracking-ui:latest`) built locally, no AWS spend.
- **Views Directory**: EJS templates in `services/*/views/` (e.g., `views/partials/order-table.ejs`).
- **Ports**: `crm-ui` on 7000, `tracking-ui` on 8000 to avoid conflicts.

---

### Why This Phase Matters
Phase 3 is the project’s face—where users interact with CRM and supply chain features. A professional, lightweight frontend:
- Enhances user trust with intuitive order and tracking UIs (retailer priority).
- Sets up scalable components for future admin/analytics UIs (enterprise foresight).
- Delivers a polished capstone demo without overengineering, balancing cost and quality.

This detailed plan ensures Phase 3 is dynamic, reusable, and industry-grade. 