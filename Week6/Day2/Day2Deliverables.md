### Deliverable for Phase 2: Project Folder Structure
The deliverables for Phase 2 include the infrastructure code, microservices deployment manifests, CI/CD workflows, and initial application code. Below is the updated folder structure reflecting the specific files generated or populated for Day 2:

```
ecomm-capstone/
├── docs/
│   ├── ecomm-architecture.md       # From Phase 1, unchanged
│   └── runbook.md                  # Placeholder from Phase 1 (empty)
├── frontend/
│   ├── src/                        # React app source (basic app with /health, /ready)
│   │   ├── App.js                  # Main React component
│   │   └── index.js                # Entry point
│   ├── Dockerfile                  # Frontend container config
│   └── kubernetes/
│       ├── deployment.yaml         # Frontend Deployment (5 replicas, limits, probes)
│       └── service.yaml            # Frontend ClusterIP Service
├── backend/
│   ├── src/                        # Node.js API source (inventory, orders, health)
│   │   ├── index.js                # Main API file
│   ├── Dockerfile                  # Backend container config
│   └── kubernetes/
│       ├── deployment.yaml         # Backend Deployment (5 replicas, limits, probes)
│       └── service.yaml            # Backend ClusterIP Service
├── infrastructure/
│   ├── terraform/
│   │   ├── main.tf                 # EKS cluster, node group, Karpenter config
│   │   ├── variables.tf            # Terraform variables (region, AZs)
│   │   └── outputs.tf              # Terraform outputs (cluster endpoint, ALB URL)
│   └── helm/
│       └── ecomm/                  # Placeholder for Helm chart (empty for Phase 2)
│           ├── Chart.yaml          # Empty Helm chart metadata
│           ├── values.yaml         # Empty Helm values
│           └── templates/          # Empty templates directory
├── kubernetes/
│   ├── ingress.yaml                # ALB Ingress with TLS for frontend/backend
│   ├── netpol.yaml                 # Placeholder for Network Policy (empty)
│   └── opa/                        # OPA Gatekeeper policies
│       └── no-privileged.yaml      # Placeholder for no-privileged policy (empty)
├── .github/
│   └── workflows/
│       ├── infra.yml               # CI/CD for Terraform infrastructure
│       └── app.yml                 # CI/CD for app build and deployment
└── README.md                       # Updated with Phase 2 instructions
```

#### Updates to Original Structure from Phase 1
- **docs/**: Unchanged (`ecomm-architecture.md` from Phase 1, `runbook.md` remains empty).
- **frontend/**:
  - `src/`: Populated with a basic React app (`App.js`, `index.js`) including `/health` and `/ready` endpoints.
  - `Dockerfile`: Configured for React.
  - `kubernetes/deployment.yaml`, `service.yaml`: Populated with manifests.
- **backend/**:
  - `src/`: Populated with a basic Node.js API (`index.js`) with `/inventory`, `/orders`, `/health`, `/ready`.
  - `Dockerfile`: Configured for Node.js.
  - `kubernetes/deployment.yaml`, `service.yaml`: Populated with manifests.
- **infrastructure/terraform/**: Populated with EKS cluster configuration (`main.tf`, `variables.tf`, `outputs.tf`).
- **infrastructure/helm/**: Remains empty (Helm deployment deferred to Phase 3).
- **kubernetes/**:
  - `ingress.yaml`: Populated with ALB Ingress config.
  - `netpol.yaml`, `opa/no-privileged.yaml`: Remain empty (security focus in Phase 3).
- **.github/workflows/**: Populated with `infra.yml` and `app.yml` for CI/CD.
- **README.md**: Updated with Phase 2 setup instructions.

#### Deliverable Details
1. **`infrastructure/terraform/main.tf`, `variables.tf`, `outputs.tf`**:
   - Defines the EKS cluster with Graviton2 nodes, Karpenter, and multi-AZ setup.
2. **`frontend/src/App.js`, `index.js`, `Dockerfile`, `deployment.yaml`, `service.yaml`**:
   - Basic React app with health endpoints, containerized, and deployed to EKS.
3. **`backend/src/index.js`, `Dockerfile`, `deployment.yaml`, `service.yaml`**:
   - Basic Node.js API with inventory/orders endpoints, containerized, and deployed.
4. **`kubernetes/ingress.yaml`**:
   - ALB Ingress with TLS for external access.
5. **`.github/workflows/infra.yml`, `app.yml`**:
   - CI/CD pipelines for infrastructure and app deployment.
6. **`README.md`**:
   - Updated with Phase 2 instructions and prerequisites.

---

#### Steps to do (Manual Execution)
- Replace placeholders (`<YOUR_AWS_ACCOUNT_ID>`, `<YOUR_ACM_CERT_ARN>`) with real values.
- Configure `variables.tf` with your VPC/subnet IDs.
- Run `npm init -y && npm install` in `frontend/` and `backend/` to generate `package.json`.
- Deploy with Terraform and push to GitHub for CI/CD execution.

---

### Why This Deliverable is Industry-Standard
- **Infrastructure**: EKS with Graviton2, Karpenter mirrors Amazon’s scalable clusters (1M+ customers).
- **Microservices**: Deployments with limits, probes align with Netflix’s HA (247M subscribers).
- **CI/CD**: GitHub Actions reflects Walmart’s automation (500M+ txns).
- **Resilience**: DDoS-ready design matches real-world testing (e.g., Amazon’s 2023 defense).
- **Model Project**: Practical, executable code prepares learners for enterprise DevSecOps.

