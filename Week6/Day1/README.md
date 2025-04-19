## Week 6, Day 1: Capstone Kickoff - Plan Microservices, Swap a Tool Mid-Plan
**Objective**: Design a Kubernetes-based microservices architecture for an e-commerce platform, incorporating DevSecOps best practices, and adapt to a tool swap mid-plan to demonstrate flexibility.

- **Duration**: ~7-8 hours.
- **Structure**: 
  - Theoretical Deep Dive (~3 hours): Understand Kubernetes architecture, DevSecOps principles, and tool swapping.
  - Practical Planning (~4-5 hours): Define project features, design architecture, document, and pivot CI/CD tool.

---

### Project Overview
- **Capstone Project**: **Secure, Scalable Microservices-Based E-commerce Platform on AWS EKS**
  - **Purpose**: A retail application managing 10,000+ products, scaling to handle 100K+ transactions during peak seasons (e.g., Black Friday).
  - **Components**: 
    - Frontend (React): User interface for browsing products.
    - Backend (Node.js API): Inventory and order management.
    - Database (RDS MySQL): Persistent storage for product/order data.
    - Storage (S3): Logs and static assets.
  - **Scale**: Supports 10K+ concurrent users, 100K+ transactions/day during peaks.
- **DevSecOps Perspective**: Security-first design, automated scaling, observability, and resilience baked into planning.

---

### Theoretical Deep Dive (3 Hours)
#### 1. Kubernetes Architecture in DevSecOps
- **Definition**: A container orchestration platform managing microservices with pods, services, and deployments, optimized for scalability, security, and automation.
- **Context**: Industry standard (Kubernetes since 2014, EKS since 2018), aligns with AWS Well-Architected (Reliability, Scalability, Security).
- **Importance**: 
  - Scales to millions of users (e.g., Amazon’s 375M items sold, 2023).
  - Reduces downtime by 50% with HA (Gartner 2023).
  - Enables DevSecOps automation (e.g., CI/CD, observability).
- **Key Concepts**: Pods, Deployments, Services, Ingress, Namespaces, HPA, Cluster Autoscaler.

#### 2. DevSecOps Principles in Design
- **Security**: RBAC, Network Policies, encryption (NIST 800-53 SC-13).
- **Automation**: IaC (Terraform), CI/CD pipelines (GitHub Actions).
- **Observability**: Metrics (CloudWatch), tracing (X-Ray), dashboards.
- **Resilience**: Multi-AZ, chaos engineering, zero-downtime deployments.
- **Cost Optimization**: Graviton2 nodes, resource limits (AWS Well-Architected Cost Optimization).

#### 3. Tool Swapping for Agility
- **Definition**: Mid-plan pivot (e.g., Jenkins to GitHub Actions) to adapt to new requirements or constraints.
- **Context**: Reflects real-world shifts (e.g., Netflix’s Spinnaker adoption, 2015).
- **Importance**: 
  - Saves 20-30% time/cost by adopting better tools (IDC 2023).
  - Prepares DevSecOps pros for dynamic environments.

---

### Practical Planning (4-5 Hours)

#### Project Features from a DevSecOps Perspective
The e-commerce platform is designed with features that prioritize DevSecOps principles, making it a model capstone for Kubernetes learning:
1. **Secure Product Browsing**:
   - **Feature**: Users browse 10,000+ products via a React frontend.
   - **DevSecOps**: TLS on ALB Ingress, RBAC restricts pod access, X-Ray traces latency.
   - **Why**: Ensures secure, observable user experience (e.g., Amazon’s retail frontend).
2. **Inventory Management API**:
   - **Feature**: Node.js API handles stock updates/orders for 100K+ transactions.
   - **DevSecOps**: Secrets Manager for API keys, Network Policies limit traffic, HPA scales pods.
   - **Why**: Balances security and scalability (e.g., Walmart’s 500M+ txns).
3. **Persistent Data Storage**:
   - **Feature**: RDS MySQL stores product/order data with encryption.
   - **DevSecOps**: KMS encryption, private subnet, CloudWatch monitors performance.
   - **Why**: Meets compliance (e.g., GDPR) and reliability (e.g., Netflix’s DB).
4. **Log and Asset Storage**:
   - **Feature**: S3 stores logs/static assets with lifecycle policies.
   - **DevSecOps**: Encrypted buckets, IAM roles for pod access, lifecycle to Glacier.
   - **Why**: Cost-efficient, secure storage (e.g., Amazon’s S3 for 1M+ customers).
5. **Resilient Scaling**:
   - **Feature**: Scales to 10K+ users during peaks with zero downtime.
   - **DevSecOps**: Karpenter for node scaling, rolling updates, chaos-tested resilience.
   - **Why**: Handles Black Friday-like spikes (e.g., Walmart’s 46M items, 2022).
6. **Observability Dashboard**:
   - **Feature**: Real-time metrics (e.g., CPU, latency, orders/min).
   - **DevSecOps**: CloudWatch Dashboard, custom metrics, X-Ray tracing.
   - **Why**: Proactive issue detection (e.g., Netflix’s 17B+ streaming hours).

#### Architecture Design with Kubernetes Best Practices
- **Components**:
  1. **EKS Cluster**:
     - 2 `t4g.medium` Graviton2 nodes (cost-efficient, 20% cheaper than x86).
     - Multi-AZ deployment (`us-east-1a/b/c`) for HA.
     - Namespace: `prod` for resource isolation.
  2. **Frontend Microservice**:
     - Deployment: 5 replicas, `requests: {cpu: "200m", memory: "256Mi"}, limits: {cpu: "500m", memory: "512Mi"}`.
     - Pod Anti-Affinity: Spreads pods across nodes/AZs.
     - Service: ClusterIP for internal access.
  3. **Backend Microservice**:
     - Same specs as frontend, exposes `/inventory` and `/orders`.
     - Secrets Manager for DB credentials.
  4. **RDS MySQL**:
     - Private subnet, KMS-encrypted, accessed via EKS Service.
  5. **S3 Bucket**:
     - Encrypted, IAM role for pod access, lifecycle policy to Glacier (30 days).
  6. **Networking**:
     - ALB Ingress with TLS (HTTPS), routes to frontend/backend.
     - Network Policy: Allows frontend-to-backend, denies others.
  7. **Scaling**:
     - HPA: Scales pods on CPU > 80% (min 2, max 10).
     - Karpenter: Scales nodes dynamically based on pod demand.
  8. **Security**:
     - RBAC: Limits namespace access (e.g., `ecomm-role`).
     - OPA Gatekeeper: Enforces Pod Security Standards (no privileged pods).
     - Image scanning via ECR.
  9. **Observability**:
     - CloudWatch: EKS metrics (CPU, memory), custom metric (orders/min).
     - X-Ray: Traces API calls.
     - Dashboard: Visualizes latency, CPU, orders.
  10. **IaC**:
      - Terraform: Defines EKS, ALB, Karpenter.
- **Diagram**:
  ```
  [Users] → [ALB Ingress (TLS)] → [EKS Cluster: prod namespace]
                                    ├── Frontend Pods (5x, Graviton2, HPA)
                                    ├── Backend Pods (5x, Graviton2, HPA)
                                    └── Karpenter (node scaling)
  [Backend] → [RDS MySQL (KMS)]  [S3 (logs/assets)]
  [Monitoring: CloudWatch + X-Ray + Dashboard]
  ```

#### Tool Swap Exercise
- **Initial Plan**: Use Jenkins for CI/CD pipeline (e.g., build Docker, deploy to EKS).
- **Mid-Plan Swap**: After 2 hours, pivot to GitHub Actions.
- **Rationale**: GitHub Actions is lighter, integrates natively with Git, and simplifies setup (e.g., Netflix’s shift to Spinnaker for agility).
- **Trade-Offs**:
  - Jenkins: Robust plugins, complex setup.
  - GitHub Actions: Simpler, less overhead, but fewer enterprise features.

#### Documentation
- **File**: `ecomm-architecture.md`
  - **Sections**:
    1. Overview: Purpose, scale (10K+ users, 100K+ txns).
    2. Architecture Diagram: EKS, ALB, RDS, S3, monitoring.
    3. Features: Secure browsing, inventory API, etc., with DevSecOps justification.
    4. Best Practices: List how each is met (e.g., HA with 3 AZs, security with RBAC).
    5. Tool Swap: Jenkins → GitHub Actions, pros/cons.
- **Example Snippet**:
  ```
  # E-commerce Platform Architecture
  ## Overview
  A retail app on EKS for 10,000+ products, scaling to 100K+ txns.

  ## Features
  - **Secure Browsing**: React frontend, TLS, X-Ray tracing.
  - **Inventory API**: Node.js, Secrets Manager, HPA scaling.

  ## Best Practices
  - **Modular**: Separate frontend/backend Deployments.
  - **HA**: 3 AZs, 5 replicas, anti-affinity.
  - **Security**: RBAC, KMS, OPA Gatekeeper.

  ## Tool Swap
  - **From**: Jenkins (complex, plugin-heavy).
  - **To**: GitHub Actions (light, Git-native).
  ```

---

### Learning Schedule (7-8 Hours)
- **09:00 - 12:00 (3h) - Theoretical Deep Dive**:
  - Kubernetes architecture (1h): Pods, Services, HA, scaling.
  - DevSecOps principles (1h): Security, automation, observability.
  - Tool swapping (1h): Real-world cases (Amazon, Netflix).
  - Resources: Slides, CNCF docs, AWS Well-Architected.
- **12:00 - 13:00 (1h) - Lunch/Break**
- **13:00 - 17:00 (4h) - Practical Planning**:
  - Define features (1h): Map to DevSecOps goals.
  - Design architecture (1.5h): EKS, ALB, RDS, S3, monitoring.
  - Tool swap (1h): Plan Jenkins, pivot to GitHub Actions.
  - Document (0.5h): `ecomm-architecture.md`.
- **Optional 17:00 - 18:00 (1h)**: Review, refine diagram.

---

### Deliverables
- **Architecture Diagram**: Visual representation in `ecomm-architecture.md`.
- **Documentation**: Detailed `ecomm-architecture.md` with features, best practices, and tool swap rationale.
- **CI/CD Plan**: Initial Jenkins sketch, updated GitHub Actions outline.

---

### Why This is a Model Capstone Project
1. **Comprehensive Planning**: Covers all aspects—microservices, security, scaling, observability—mirroring Fortune 100 designs (e.g., Amazon’s EKS for 1M+ customers).
2. **DevSecOps Focus**: Embeds security (RBAC, TLS), automation (IaC, CI/CD), and resilience (HA, Karpenter) from Day 1.
3. **Kubernetes Best Practices**: Fully aligns with modularity, HA, security, scaling, and observability (e.g., Netflix’s 247M subscriber scale).
4. **Real-World Agility**: Tool swap exercise prepares learners for dynamic environments (e.g., Walmart’s 2022 CI/CD pivot).
5. **Scalable Blueprint**: Extensible to Days 2-5, ensuring a production-ready outcome.

---

### Verification
- **Checklist**:
  - Features defined with DevSecOps justification.
  - Architecture includes all best practices (3 AZs, Graviton2, RBAC, etc.).
  - Tool swap documented with trade-offs.
- **Outcome**: A detailed, actionable plan ready for implementation, setting a high standard for Kubernetes learning.

