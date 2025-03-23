Let’s define the **Deliverables for Phase 3: Frontend - User Interfaces** of the **CRM-Integrated Global Supply Chain System** capstone project. 

This phase focuses on creating two frontend services—`crm-ui` (reused and enhanced customer dashboard) and `tracking-ui` (new shipment tracking UI)—as Dockerized single-page applications (SPAs) using Node.js, Express, and EJS templates. 

---

## Deliverables for Phase 3
The deliverables are the files needed to build Docker images for the two frontend services:
- **`services/crm-ui/{Dockerfile,app.js,package.json,views/}`**: Enhanced customer dashboard for order management, integrating with `crm-api` and `order-service`.
- **`services/tracking-ui/{Dockerfile,app.js,package.json,views/}`**: New UI for tracking shipment statuses, fetching from `logistics-service`.

### Details
- **Tech**: Node.js (Express), EJS for server-side rendering, vanilla JS/CSS for dynamic behavior, minimal dependencies.
- **Optimization**: Lightweight `node:18-alpine` images (~150-200MB), reusable EJS partials, no heavy frameworks.
- **Output**: Docker images (`crm-ui:latest`, `tracking-ui:latest`) built locally, no extra infra cost.
- **Real-World Time**: ~5-6 days for 2-3 engineers (design, coding, Dockerizing, testing).

---

## Deliverables Breakdown
### 1. `crm-ui`
- **Dockerfile**: Uses `node:18-alpine`, exposes port 7000.
- **app.js**: Serves dashboard (`/`), handles order submission (`/orders`), and order details (`/orders/:id`).
- **package.json**: Minimal deps (`express`, `ejs`, `axios`).
- **views/index.ejs**: Dashboard with order table and form.
- **views/order-details.ejs**: Order details page with supply chain status.
- **views/partials/order-table.ejs**: Reusable table component.
- **public/**: Basic CSS (`styles.css`) and JS (`script.js`) for styling and client-side logic.

### 2. `tracking-ui`
- **Dockerfile**: Uses `node:18-alpine`, exposes port 8000.
- **app.js**: Serves tracking page (`/`), fetches shipment details (`/shipments/:id`).
- **package.json**: Minimal deps (`express`, `ejs`, `axios`).
- **views/index.ejs**: Tracking page with search and shipment display.
- **views/partials/shipment-card.ejs**: Reusable shipment card component.
- **public/**: Basic CSS (`styles.css`) for styling.

---

## Notes on Deliverables
- **Clean & Optimized**:
  - **Dockerfiles**: Lightweight images (~150-200MB), efficient `npm install`.
  - **EJS**: Server-side rendering keeps client JS minimal.
  - **CSS**: Simple, responsive styling without frameworks (e.g., Tailwind optional).
- **Original Structure**: Only `services/crm-ui` and `services/tracking-ui` populated; other dirs remain placeholders.
- **DevSecOps**:
  - Env vars (`CRM_API_URL`, etc.) for flexibility, defaults for local use.
  - API key headers for secure backend calls (from Phase 2).
  - Error handling in UI for resilience.
- **Local Registry**: Build with `docker build -t crm-ui:latest .` and `docker build -t tracking-ui:latest .`.

---

## Real-World Alignment
- **Time**: ~5-6 days reflects lightweight SPA development, typical for a sprint.
- **Standards**: SSR, reusable components, and minimal deps align with cost-efficient enterprise UIs (e.g., DHL tracking).
- **Next Steps**: Phase 4 will deploy these to Kubernetes, integrating with backend services.

These deliverables provide a professional frontend foundation for Phase 3, ready for local testing and Docker builds.