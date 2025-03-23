Let’s refine the **Week 4, Day 5: Capstone Project** plan by combining the original **Global Supply Chain Management System** (from your initial Day 5 plan) with the existing **CRM Platform** (from Day 2) into a unified **CRM-Integrated Global Supply Chain System**. 

This hybrid capstone will simulate a production-grade, real-world use case for Fortune 100 companies like Walmart, Amazon, or DHL, emphasizing **DevSecOps best practices** and a robust architecture. 

Below is a brief plan that merges both projects while aligning with the initial Day 5 objectives and enhancing them with CRM integration.

---

## Week 4, Day 5: Capstone Project - CRM-Integrated Global Supply Chain System

### Overview
- Build a multi-region, production-grade system integrating CRM (customer management) with supply chain operations (inventory, logistics).
- Leverage Terraform, Kubernetes, and Jenkins for automation, resilience, and security.

### Objectives
- Provision multi-region infra (EKS, RDS) with Terraform.
- Deploy CRM and supply chain microservices on EKS with Kubernetes.
- Automate via Jenkins pipeline with GitOps and zero-downtime updates.
- Incorporate DevSecOps practices for security, compliance, and observability.

### Time Allocation
- **Planning & Review**: 1 hour
- **Implementation**: 2 hours
- **Total**: 3 hours

### Combined Plan
1. **Infrastructure Setup (Terraform)**:
   - Reuse Day 2’s EKS clusters in `us-east-1` and `eu-west-1` with VPC modules.
   - Extend with:
     - RDS (PostgreSQL) in `us-east-1` for inventory and CRM data.
     - S3 for state/logs, DynamoDB for locking.
     - ECR for all microservice images.
   - Outputs: EKS endpoints, RDS connection string.

2. **Application Development**:
   - **CRM Microservices** (from Day 2):
     - `crm-api`: Customer orders and data.
     - `crm-ui`: Customer dashboard.
     - `crm-analytics`: Sales insights.
   - **Supply Chain Microservices** (from initial Day 5):
     - `inventory-service`: Tracks stock (stateful, PostgreSQL).
     - `logistics-service`: Optimizes shipping (stateless).
     - `order-service`: Processes orders (stateless, links CRM to supply chain).
     - `analytics-service`: Real-time supply chain dashboards (compute-heavy).
     - `api-gateway`: NGINX-based traffic routing.
   - Dockerize all services.

3. **Kubernetes Deployment**:
   - Namespaces: `crm-us`, `crm-eu`, `supply-us`, `supply-eu`.
   - Deployments/Services:
     - CRM: `crm-api`, `crm-ui`, `crm-analytics` (LoadBalancer for UI).
     - Supply Chain: `inventory-service` (Persistent Volume for RDS), `logistics-service`, `order-service`, `analytics-service`, `api-gateway` (Ingress).
   - Features:
     - Ingress: `supplychain-crm.globalretail.com` routes to all services.
     - HPA: Scale `analytics-service` (CPU > 70%).
     - Multi-region failover: `us-east-1` primary, `eu-west-1` secondary.

4. **CI/CD Pipeline (Jenkins)**:
   - Update Day 2’s `Jenkinsfile`:
     - Build Docker images for all 8 services.
     - Push to ECR (`<account>.dkr.ecr.us-east-1.amazonaws.com/supplychain-crm`).
     - Apply Terraform, then K8s manifests for both regions.
     - Zero-downtime: Rolling updates via K8s.
   - GitOps: Trigger on GitHub `main` commits.

5. **Verification**:
   - Test CRM: Place order via `crm-ui`, check stock via `inventory-service`.
   - Test Supply Chain: Track shipment in `logistics-service`, view dashboard in `analytics-service`.
   - Validate: Multi-region failover, pipeline automation, security checks.

### DevSecOps Best Practices
- **Security**: IAM roles (least privilege), RBAC for K8s, encrypted RDS/S3.
- **Compliance**: State versioning in S3, audit logs via Jenkins.
- **Observability**: Prep for Prometheus (metrics), basic logging in services.
- **Modularity**: Reusable Terraform modules (VPC, EKS).
- **Resilience**: Multi-region failover, HPA for scalability.

### Tools
- Terraform, Kubernetes (EKS), Docker, Jenkins, GitHub, AWS (EKS, ECR, RDS, S3, DynamoDB).

### Deliverables
- Running system at `supplychain-crm.globalretail.com`.
- Automated pipeline with zero-downtime updates.
- Multi-region failover demo.

### Real-World Use Case
- **Scenario**: A retailer like Walmart integrates CRM (customer orders) with supply chain (inventory, shipping) across North America and Europe.
- **How**: Terraform provisions EKS and RDS in `us-east-1`/`eu-west-1`. Kubernetes runs microservices with Ingress routing and HPA scaling. Jenkins automates deployments, ensuring real-time stock updates and logistics for 10,000+ stores.

---

### Alignment with Initial Plan
- **Microservices**: Adds CRM to inventory, logistics, order, analytics, and API gateway.
- **Multi-Region**: Retains `us-east-1`, `eu-west-1` focus.
- **Pipeline as Code**: Enhances Day 2’s Jenkinsfile.
- **GitOps**: Git-driven, as planned.
- **Zero-Downtime**: Rolling updates implemented.

This combined plan creates a Fortune 100-grade, DevSecOps-ready application, merging CRM and supply chain seamlessly. 