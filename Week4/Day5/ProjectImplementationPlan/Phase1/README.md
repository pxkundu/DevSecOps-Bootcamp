Let’s dive into **Phase 1: Design - Solutions Architecture for Infrastructure** of our **CRM-Integrated Global Supply Chain System** capstone project. This phase is the foundational blueprint, defining how we’ll architect a cost-optimized, multi-region infrastructure using Terraform and AWS to support both CRM and supply chain functionalities. 

We’ll detail the thought process, design each component, explain the "why" behind every decision, and ensure alignment with industry-standard DevSecOps best practices followed by Fortune 100 companies like Walmart, Amazon, and DHL. Diagrams will illustrate key components to enhance clarity, making this a professional, production-grade plan.

---

## Phase 1: Design - Solutions Architecture for Infrastructure

### Objective
- Define a scalable, secure, and cost-efficient infrastructure blueprint using Terraform to provision multi-region EKS clusters, RDS, S3, and ECR.
- Reuse and extend Day 2’s `CRMTerraformJenkins` setup while optimizing for budget and DevSecOps principles.

### Time Allocation
- ~35-40 minutes (within Day 5’s 3-hour capstone).

### Thought Process
- **Reuse Existing Work**: Leverage Day 2’s EKS clusters, VPCs, and Jenkins setup to avoid redundant costs and effort, reflecting Amazon’s efficiency-driven IaC reuse.
- **Multi-Region Strategy**: Deploy in `us-east-1` (primary) and `eu-west-1` (secondary) for global reach, mirroring Walmart’s supply chain coverage, with failover for resilience.
- **Cost Optimization**: Use t3 instances, limit replicas, and optimize storage tiers, aligning with DHL’s budget-conscious logistics systems.
- **DevSecOps Focus**: Embed security (IAM, encryption), modularity (Terraform modules), and observability prep (logging), per industry standards.
- **Scalability**: Design for growth (e.g., add regions/services later) while keeping initial footprint lean.

### Design Components and Solutions

#### 1. Multi-Region EKS Clusters
- **What**: Two EKS clusters—one in `us-east-1`, one in `eu-west-1`—running CRM and supply chain microservices.
- **How**:
  - Reuse Day 2’s `modules/eks` for provisioning.
  - Node Group: 2 t3.medium nodes per cluster (4 vCPUs, 8GB RAM total per region).
  - Autoscaling: Min 2, max 4 nodes (controlled via K8s HPA in Phase 4).
- **Why**:
  - **Multi-Region**: Ensures low-latency access (US/EU customers) and failover (e.g., `us-east-1` outage → `eu-west-1`).
  - **t3.medium**: Balances cost (~$0.0416/hr/node) and performance for 8 microservices.
  - **Reuse**: Speeds implementation, reduces errors, aligns with Amazon’s modular IaC.
- **DevSecOps**:
  - IAM Role: EKS-specific, least privilege (e.g., `AmazonEKSClusterPolicy` only).
  - RBAC: Planned for K8s (Phase 4), namespace isolation (`crm-us`, `supply-eu`).
- **Diagram**:
  ```
  +---------------------+       +---------------------+
  | us-east-1 EKS       |       | eu-west-1 EKS       |
  | - 2 t3.medium       |<----->| - 2 t3.medium       |
  | - Namespace:        |       | - Namespace:        |
  |   crm-us, supply-us |       |   crm-eu, supply-eu |
  +---------------------+       +---------------------+
  ```

#### 2. VPC Configuration
- **What**: Reusable VPCs in both regions with public/private subnets.
- **How**:
  - Reuse Day 2’s `modules/vpc`.
  - CIDR: `10.0.0.0/16` (`us-east-1`), `10.1.0.0/16` (`eu-west-1`).
  - Subnets: 2 public, 2 private per region; 1 NAT Gateway per region (cost-optimized).
- **Why**:
  - **Reuse**: Ensures consistency, reduces config drift (Walmart’s IaC practice).
  - **Public/Private**: Public for EKS control plane, private for worker nodes, enhancing security.
  - **Single NAT**: Cuts cost (~$0.045/hr vs. $0.09/hr for 2), sufficient for outbound traffic.
- **DevSecOps**:
  - Security Groups: Restrict ingress (e.g., port 443 for EKS, 5432 for RDS).
  - Tags: Enforce naming (e.g., `env=prod`, `region=us-east-1`) for auditability.
- **Diagram**:
  ```
  +------------------+       +------------------+
  | us-east-1 VPC    |       | eu-west-1 VPC    |
  | - 10.0.0.0/16    |       | - 10.1.0.0/16    |
  | - Public Subnets |       | - Public Subnets |
  | - Private Subnets|       | - Private Subnets|
  | - 1 NAT Gateway  |       | - 1 NAT Gateway  |
  +------------------+       +------------------+
  ```

#### 3. RDS (PostgreSQL) for Inventory and CRM Data
- **What**: Single PostgreSQL instance in `us-east-1` for shared CRM/supply chain data.
- **How**:
  - New `modules/rds`: t3.micro (1 vCPU, 1GB RAM), single-AZ.
  - DB: `crm_supply_db`, tables for customers, inventory, orders.
  - Backup: Daily snapshots, 7-day retention.
- **Why**:
  - **Single Instance**: Reduces cost (~$0.017/hr vs. $0.034/hr multi-AZ), sufficient for capstone scale.
  - **Shared DB**: Simplifies integration (`crm-api` ↔ `order-service`), mimics Walmart’s centralized inventory.
  - **Backup**: Ensures data recovery, a DHL compliance must.
- **DevSecOps**:
  - Encryption: At rest (AWS KMS), in transit (SSL).
  - IAM Auth: DB user with limited permissions.
- **Diagram**:
  ```
  +------------------+
  | us-east-1 RDS    |
  | - t3.micro       |
  | - crm_supply_db  |
  | - Encrypted      |
  | - Backup: 7 days |
  +------------------+
  ```

#### 4. S3 and DynamoDB for Terraform State
- **What**: Remote state storage and locking for Terraform.
- **How**:
  - Reuse Day 2’s S3 bucket (`crm-tf-state-2025`) with Standard-IA tier.
  - Reuse DynamoDB table (`tf-lock`) with on-demand billing.
- **Why**:
  - **Reuse**: Avoids new resource costs, maintains state continuity.
  - **Standard-IA**: Cuts storage cost (~$0.0125/GB vs. $0.023/GB Standard), infrequent access fits IaC.
  - **Locking**: Prevents concurrent edits, critical for team sync (Amazon’s practice).
- **DevSecOps**:
  - Versioning: Enabled for audit trails.
  - Encryption: SSE-S3 default.
- **Diagram**:
  ```
  +---------------------+       +------------------+
  | S3 Bucket           |       | DynamoDB Table   |
  | - crm-tf-state-2025 |       | - tf-lock        |
  | - Standard-IA       |       | - On-Demand      |
  | - Versioned         |       | - Locking        |
  +---------------------+       +------------------+
  ```

#### 5. ECR for Docker Images
- **What**: Container registry for all microservices (CRM + supply chain).
- **How**:
  - Extend Day 2’s ECR setup: 8 repos (e.g., `supplychain-crm/crm-api`, `supplychain-crm/inventory-service`).
  - Lifecycle Policy: Keep last 5 images per repo.
- **Why**:
  - **Centralized**: Simplifies image management, aligns with DHL’s container workflows.
  - **Lifecycle**: Reduces storage cost (~$0.10/GB), removes stale images.
- **DevSecOps**:
  - IAM: Restrict push/pull to Jenkins role.
  - Tagging: Consistent naming (e.g., `<service>:latest`).
- **Diagram**:
  ```
  +------------------------+
  | ECR Registry           |
  | - 8 Repos:             |
  |   crm-api, crm-ui, ... |
  | - Lifecycle: 5 images  |
  +------------------------+
  ```

#### Overall Solutions Architecture
- **Diagram**:
  ```
  +----------------------------------+       +----------------------------------+
  | us-east-1                        |       | eu-west-1                        |
  | +------------------+             |       | +------------------+             |
  | | VPC: 10.0.0.0/16 |             |       | | VPC: 10.1.0.0/16 |             |
  | | - Public Subnets |             |       | | - Public Subnets |             |
  | | - Private Subnets|             |       | | - Private Subnets|             |
  | | - 1 NAT Gateway  |             |       | | - 1 NAT Gateway  |             |
  | +------------------+             |       | +------------------+             |
  | | EKS: 2 t3.medium | <---------> |       | | EKS: 2 t3.medium |             |
  | | - crm-us         |  Failover   |       | | - crm-eu         |             |
  | | - supply-us      |             |       | | - supply-eu      |             |
  | +------------------+             |       | +------------------+             |
  | | RDS: t3.micro    |             |       |                                  |
  | | - crm_supply_db  |             |       |                                  |
  | +------------------+             |       |                                  |
  +----------------------------------+       +----------------------------------+
             |                                           |
  +------------------------+                    +-------------------+
  | S3: crm-tf-state-2025  |                    | DynamoDB: tf-lock |
  +------------------------+                    +-------------------+
  | ECR: supplychain-crm/* |
  +------------------------+
  ```

### Why This Design?
- **Scalability**: EKS and modular VPCs support adding regions/services (e.g., `ap-southeast-1`).
- **Cost Efficiency**: t3 instances, single-AZ RDS, and lifecycle policies keep AWS spend ~$60-70/month.
- **Resilience**: Multi-region failover ensures 99.9% uptime, critical for supply chain ops (DHL).
- **Security**: Encryption, IAM, and RBAC prep meet compliance (e.g., SOC 2, GDPR).
- **Industry Standard**: Modular Terraform, multi-region EKS, and centralized state mirror Amazon/Walmart practices.

### DevSecOps Best Practices
1. **Infrastructure as Code (IaC)**:
   - Modular Terraform ensures consistency and reusability.
2. **Least Privilege**:
   - IAM roles scoped to specific services (e.g., EKS, RDS).
3. **Encryption**:
   - RDS, S3 encrypted by default; KMS for sensitive data.
4. **Auditability**:
   - S3 versioning, Terraform state history for compliance.
5. **Resilience**:
   - Multi-region design with failover, rolling updates planned.
6. **Cost Management**:
   - Optimized instance types and storage tiers.

### Implementation Notes
- **Files**: Update `CRMSupplyChainCapstone/infrastructure/` with:
  - `main.tf`: Call `vpc`, `eks`, `rds` modules with `for_each` for regions.
  - `variables.tf`: Define regions, instance types.
  - `outputs.tf`: Expose EKS endpoints, RDS string.
  - `backend.tf`: Reuse Day 2’s S3/DynamoDB config.
- **Next Steps**: Phase 2 will build on this infra with backend services.

---

### Deliverable
- Updated `infrastructure/` directory with Terraform files reflecting this blueprint.
- Cost estimate: ~$60-70/month, optimized for capstone scale.

This Phase 1 design lays a professional, DevSecOps-aligned foundation, ensuring the project scales efficiently while staying budget-friendly and secure.