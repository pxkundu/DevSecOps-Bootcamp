Let’s define the **Deliverables for Phase 4: Core Features - Integration and Functionality** of the **CRM-Integrated Global Supply Chain System** capstone project and provide a single, optimized script to generate them within the existing `CRMSupplyChainCapstone/` folder structure. 

This phase focuses on Kubernetes manifests to deploy all services (`crm-ui`, `crm-api`, `order-service`, `inventory-service`, `logistics-service`, `tracking-ui`, `crm-analytics`, `analytics-service`) across regional namespaces (`crm-us`, `crm-eu`, `supply-us`, `supply-eu`), integrate core features (order placement, inventory check, shipment tracking, analytics), and set up an NGINX Ingress API Gateway. 

---

## Deliverables for Phase 4
The deliverables are Kubernetes manifests that define deployments, services, HPA, and Ingress for the system:
- **`kubernetes/crm/`**: Manifests for CRM services (`crm-ui`, `crm-api`, `order-service`, `crm-analytics`) in `crm-us` and `crm-eu` namespaces.
- **`kubernetes/supply-chain/`**: Manifests for supply chain services (`inventory-service`, `logistics-service`, `tracking-ui`, `analytics-service`) in `supply-us` and `supply-eu` namespaces, including HPA for `analytics-service`.
- **`kubernetes/ingress/`**: NGINX Ingress configuration for `supplychain-crm.globalretail.com`.
- **New Files**: 
  - Separate deployment and service files per service for clarity (e.g., `crm-ui-deployment.yaml`, `crm-ui-service.yaml`).
  - HPA file (`analytics-service-hpa.yaml`) for `analytics-service`.
- **Budget**: EKS compute (~$0.32/hr for 4 nodes), minimal Ingress cost.

### Updated Project Folder Structure
```
CRMSupplyChainCapstone/
├── kubernetes/                 # Kubernetes manifests
│   ├── crm/                   # CRM K8s resources
│   │   ├── crm-ui-deployment.yaml
│   │   ├── crm-ui-service.yaml
│   │   ├── crm-api-deployment.yaml
│   │   ├── crm-api-service.yaml
│   │   ├── order-service-deployment.yaml
│   │   ├── order-service-service.yaml
│   │   ├── crm-analytics-deployment.yaml
│   │   └── crm-analytics-service.yaml
│   ├── supply-chain/          # Supply chain K8s resources
│   │   ├── inventory-service-deployment.yaml
│   │   ├── inventory-service-service.yaml
│   │   ├── logistics-service-deployment.yaml
│   │   ├── logistics-service-service.yaml
│   │   ├── tracking-ui-deployment.yaml
│   │   ├── tracking-ui-service.yaml
│   │   ├── analytics-service-deployment.yaml
│   │   ├── analytics-service-service.yaml
│   │   └── analytics-service-hpa.yaml
│   └── ingress/               # Ingress configuration
│       └── ingress.yaml
```
- **Changes**: Replaced generic `deployment.yaml` and `service.yaml` with specific files per service for better organization and readability.

---

## How to Use the Script
1. **Precondition**: Ensure Phases 2-3 deliverables exist (Docker images in ECR).
2. **Save the Script**:
   ```bash
   cat << 'EOF' > generate-phase4-deliverables.sh
   # [Paste script content here]
   EOF
   ```
3. **Make it Executable**:
   ```bash
   chmod +x generate-phase4-deliverables.sh
   ```
4. **Run the Script**:
   ```bash
   ./generate-phase4-deliverables.sh
   ```
   - Populates `kubernetes/crm/`, `kubernetes/supply-chain/`, and `kubernetes/ingress/`.
5. **Verify**:
   ```bash
   ls -R CRMSupplyChainCapstone/kubernetes
   ```

---

## Deliverables Breakdown
### 1. `kubernetes/crm/`
- **Files**: Deployment and Service manifests for `crm-ui`, `crm-api`, `order-service`, `crm-analytics`.
- **Details**: 2 replicas each, `crm-us` namespace, LoadBalancer for `crm-ui`, ClusterIP for APIs, secrets for `API_KEY` and DB creds.

### 2. `kubernetes/supply-chain/`
- **Files**: Deployment and Service manifests for `inventory-service`, `logistics-service`, `tracking-ui`, `analytics-service`, plus `analytics-service-hpa.yaml`.
- **Details**: 2 replicas, `supply-us` namespace, LoadBalancer for `tracking-ui`, ClusterIP for APIs, HPA for `analytics-service` (CPU > 70%, max 4).

### 3. `kubernetes/ingress/`
- **File**: `ingress.yaml`.
- **Details**: NGINX Ingress routes `supplychain-crm.globalretail.com` to all services via path-based rules.

---

## Notes on Deliverables
- **Clean & Optimized**:
  - Separate files per service improve readability and maintenance.
  - Minimal resource requests/limits (e.g., `100m` CPU for `analytics-service`) optimize cost.
- **Original Structure**: Updates `kubernetes/` only, aligning with prior layout.
- **Placeholders**: `<aws_account_id>`, `<rds-endpoint>` to be replaced with real values post-deployment.
- **Multi-Region**: Manifests are for `us-east-1` (`crm-us`, `supply-us`); duplicate for `crm-eu`, `supply-eu` in `eu-west-1` with adjusted ECR region.
- **DevSecOps**: Secrets (`api-key-secret`, `db-secret`) and HPA embed security and scalability.

---

## Next Steps
- **Deploy**: Use `kubectl apply -f kubernetes/` on an EKS cluster after setting up namespaces and secrets.
- **Infra**: Phase 5 will add Terraform IaC to provision EKS and RDS.
- **CI/CD**: Jenkins pipeline (Phase 5) will automate manifest application.
