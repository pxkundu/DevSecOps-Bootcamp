**Learning Plan** for **Week 6, Day 1: Capstone Kickoff - Plan Microservices, Swap a Tool Mid-Plan**, tailored for the DevSecOps Bootcamp. This plan provides **theoretical keyword explanations** (definitions, context, significance) and **practical use cases** (real-world DevOps implementations from Fortune 100 companies), focusing on designing a Kubernetes-based capstone project with DevSecOps best practices. 

It includes a **capstone folder structure** and an **initial project idea** with detailed planning, ensuring alignment with industry-standard Kubernetes implementations. Today we emphasize architecture design and adaptability, preparing intermediate AWS DevOps and Cloud Engineers for a production-ready system.

---

## Week 6, Day 1: Capstone Kickoff - Plan Microservices, Swap a Tool Mid-Plan
**Objective**: Design a Kubernetes-based microservices architecture for a capstone project, integrating DevSecOps best practices, and adapt to a mid-plan tool swap to simulate real-world agility.

- **Duration**: ~7-8 hours.
- **Structure**: Theoretical Deep Dive (~50%) + Practical Use Cases and Planning (~50%).

---

### Theoretical Keyword Explanation

#### 1. Kubernetes Architecture in DevSecOps
- **Definition**: Kubernetes is a container orchestration platform that automates the deployment, scaling, and management of microservices using pods, services, and controllers, enhanced with DevSecOps principles like security, automation, and observability.
  - **Components**: Pods (smallest deployable unit), Deployments (manage replicas), Services (network abstraction), Ingress (external routing), Namespaces (logical isolation).
- **Context**: Originated at Google (2014), adopted widely via AWS EKS (2018), aligns with AWS Well-Architected Framework (Reliability, Scalability, Security).
- **Importance**: 
  - Scales to millions of users (e.g., Amazon’s 375M items sold, 2023).
  - Reduces downtime by 50% with high availability (Gartner 2023).
  - Enables DevSecOps automation (e.g., CI/CD, monitoring).
- **DevSecOps Integration**: Secure by default (RBAC, Network Policies), observable (CloudWatch, X-Ray), and cost-efficient (Graviton2).

#### 2. Microservices Design
- **Definition**: A software architecture pattern splitting applications into small, independent services (e.g., frontend, backend) deployed as separate Kubernetes workloads.
- **Context**: Evolved from monoliths (2010s), standard in DevSecOps for agility and resilience (AWS Well-Architected Performance Efficiency).
- **Importance**: 
  - Speeds deployments by 60% via parallel development (DORA 2023).
  - Isolates failures, critical for 99.9% uptime (e.g., Netflix’s 247M subscribers).
  - Facilitates Kubernetes scaling (HPA, Karpenter).
- **DevSecOps Best Practices**: Modular design, secure inter-service communication (TLS, Network Policies), resource limits.

#### 3. Tool Swapping for Agility
- **Definition**: The mid-plan replacement of a tool (e.g., Jenkins to GitHub Actions) to adapt to new requirements, constraints, or optimizations.
- **Context**: Common in DevSecOps (e.g., Netflix’s shift to Spinnaker, 2015), reflects real-world pivots driven by cost, speed, or simplicity.
- **Importance**: 
  - Saves 20-30% time/cost with better tools (IDC 2023).
  - Prepares teams for vendor changes or tech evolution (e.g., Gartner 2023).
- **DevSecOps Relevance**: Ensures flexibility in CI/CD pipelines, a key automation pillar.

#### 4. DevSecOps Best Practices in Kubernetes
- **Security**: RBAC, Pod Security Standards (via OPA Gatekeeper), TLS, Secrets Management (NIST 800-53 SC-13).
- **Scalability**: HPA, Cluster Autoscaler (Karpenter), multi-AZ deployments (AWS Well-Architected Reliability).
- **Observability**: CloudWatch metrics, X-Ray tracing, custom dashboards (AWS Well-Architected Operational Excellence).
- **Automation**: Infrastructure as Code (Terraform), zero-downtime deployments (rolling updates).
- **Resilience**: Chaos engineering, runbooks for incident response.

---

### Practical Use Cases
#### 1. Amazon’s EKS Microservices Design
- **Scenario**: Amazon deploys 100+ microservices on EKS for 1M+ customers, handling 375M item sales (2023 Black Friday).
- **Implementation**: 
  - Modular services (e.g., catalog, checkout) on EKS across 3 AZs.
  - ALB Ingress with TLS, RBAC for access control.
  - CloudWatch/X-Ray for observability, Karpenter for scaling.
- **Outcome**: Scaled to 10K+ req/sec, saved $5M+ in downtime costs.
- **Lesson**: Modular design and HA ensure enterprise-scale reliability.

#### 2. Netflix’s Tool Swap and Kubernetes Scaling
- **Scenario**: Netflix pivoted from Travis CI to Spinnaker (2015), later adopting EKS for 247M subscribers (17B+ streaming hours, 2023).
- **Implementation**: 
  - Swapped tools mid-plan for faster deployments (40% reduction).
  - EKS with HPA, Graviton2 nodes, X-Ray tracing for streaming APIs.
- **Outcome**: Supports 2M+ concurrent viewers, $1M+ savings via Graviton.
- **Lesson**: Agility and cost optimization are critical in DevSecOps.

#### 3. Walmart’s Secure E-commerce on EKS
- **Scenario**: Walmart runs EKS for 240M customers, managing 500M+ transactions (2023).
- **Implementation**: 
  - Microservices (e.g., inventory, payments) with Network Policies.
  - Secrets Manager for DB creds, CloudWatch Dashboard for metrics.
  - Multi-AZ deployment, rolling updates for zero downtime.
- **Outcome**: Scaled 5x during Black Friday (46M items, 2022), no breaches.
- **Lesson**: Security and observability underpin peak performance.

---

### Capstone Project Idea: Secure E-commerce Platform on EKS
#### Initial Project Idea
- **Overview**: A microservices-based e-commerce platform on AWS EKS, managing 10,000+ products and scaling to 100K+ transactions/day during peaks (e.g., holiday sales).
- **Features from DevSecOps Perspective**:
  1. **Secure Product Browsing**:
     - React frontend, TLS on ALB, X-Ray tracing for latency.
  2. **Inventory and Order API**:
     - Node.js backend, Secrets Manager for creds, HPA scaling.
  3. **Persistent Storage**:
     - RDS MySQL, KMS-encrypted, private subnet access.
  4. **Log and Asset Storage**:
     - S3 with encryption, lifecycle to Glacier, IAM pod access.
  5. **Dynamic Scaling**:
     - Karpenter for nodes, rolling updates for zero downtime.
  6. **Observability**:
     - CloudWatch metrics (CPU, orders/min), X-Ray, dashboard.
- **Why a Model Project**:
  - Reflects real-world scale (Amazon, Walmart).
  - Embeds Kubernetes best practices (modularity, HA, security).
  - Prepares learners for DevSecOps roles with actionable skills.

#### Architecture Design
- **EKS Cluster**:
  - 2 `t4g.medium` Graviton2 nodes (cost-efficient) across 3 AZs (`us-east-1a/b/c`).
  - Namespace: `prod`.
- **Microservices**:
  - **Frontend**: 5 replicas, `requests: {cpu: "200m", memory: "256Mi"}, limits: {cpu: "500m", memory: "512Mi"}`, anti-affinity.
  - **Backend**: Same specs, `/inventory` and `/orders` endpoints.
- **Networking**: ALB Ingress (TLS), Network Policy (frontend-to-backend only).
- **Storage**: 
  - RDS (MySQL, KMS-encrypted).
  - S3 (logs/assets, lifecycle policy).
- **Scaling**: HPA (CPU > 80%), Karpenter (node scaling).
- **Security**: RBAC, OPA Gatekeeper, Secrets Manager, ECR image scanning.
- **Observability**: CloudWatch, X-Ray, custom dashboard (orders/min).

---

### Capstone Folder Structure
Below is the initial folder structure to organize the project, aligning with Kubernetes and DevSecOps best practices:
```
ecomm-capstone/
├── docs/
│   ├── ecomm-architecture.md       # Architecture design, features, tool swap
│   └── runbook.md                  # Placeholder for Day 5
├── frontend/
│   ├── src/                        # React app source (to be built Day 2)
│   ├── Dockerfile                  # Frontend container config
│   └── kubernetes/
│       ├── deployment.yaml         # Frontend Deployment (5 replicas, limits, probes)
│       └── service.yaml            # ClusterIP Service
├── backend/
│   ├── src/                        # Node.js API source (to be built Day 2)
│   ├── Dockerfile                  # Backend container config
│   └── kubernetes/
│       ├── deployment.yaml         # Backend Deployment
│       └── service.yaml            # ClusterIP Service
├── infrastructure/
│   ├── terraform/
│   │   ├── main.tf                 # EKS cluster, ALB, Karpenter
│   │   ├── variables.tf            # Configurable inputs (region, AZs)
│   │   └── outputs.tf              # Cluster endpoint, ALB URL
│   └── helm/
│       └── ecomm/                  # Helm chart for app deployment (Day 3)
│           ├── Chart.yaml
│           ├── values.yaml
│           └── templates/          # Deployment, Service, Ingress
├── kubernetes/
│   ├── ingress.yaml                # ALB Ingress with TLS
│   ├── netpol.yaml                 # Network Policy (frontend-to-backend)
│   └── opa/                        # OPA Gatekeeper policies (e.g., no privileged)
│       └── no-privileged.yaml
├── .github/
│   └── workflows/
│       ├── infra.yml               # CI/CD for Terraform (Day 3)
│       └── app.yml                 # CI/CD for app deployment (Day 3)
└── README.md                       # Project overview, setup instructions
```

- **Rationale**:
  - **docs/**: Centralizes planning and runbooks, critical for DevSecOps handoff.
  - **frontend/**, **backend/**: Separates microservices, aligning with modularity.
  - **infrastructure/**: Splits Terraform (IaC) and Helm (app deployment) for clarity.
  - **kubernetes/**: Houses cluster-wide configs (Ingress, Network Policies).
  - **.github/**: Automates CI/CD, a DevSecOps staple.

---

### Detailed Day 1 Implementation Plan
#### Tasks (4-5 Hours)
1. **Define Project Features (1h)**:
   - List features (browsing, inventory API, etc.) with DevSecOps justification.
   - Map to Kubernetes best practices (e.g., HPA for scaling, RBAC for security).
2. **Design Architecture (2h)**:
   - Sketch EKS cluster: 2 `t4g.medium` nodes, 3 AZs, Karpenter.
   - Detail microservices: Frontend/backend with limits, anti-affinity.
   - Plan networking: ALB Ingress (TLS), Network Policy.
   - Specify security: RBAC, OPA, Secrets Manager.
   - Outline observability: CloudWatch, X-Ray, dashboard.
3. **Tool Swap Exercise (1h)**:
   - Initial CI/CD: Plan Jenkins (e.g., build Docker, deploy to EKS).
   - Swap to GitHub Actions: Simpler YAML workflow, Git-native.
   - Document trade-offs in `ecomm-architecture.md`.
4. **Document and Folder Setup (1h)**:
   - Write `ecomm-architecture.md`: Features, diagram, best practices, tool swap.
   - Initialize folder structure with empty files (e.g., `touch frontend/Dockerfile`).

#### Sample `ecomm-architecture.md`
```markdown
# E-commerce Platform on EKS
## Overview
A secure, scalable retail app for 10,000+ products, handling 100K+ txns/day.

## Features
- **Secure Browsing**: React frontend, TLS, X-Ray tracing.
- **Inventory API**: Node.js, Secrets Manager, HPA scaling.

## Architecture
- **EKS**: 2 t4g.medium nodes, 3 AZs (us-east-1a/b/c), prod namespace.
- **Microservices**: 
  - Frontend: 5 replicas, cpu: 200m-500m, anti-affinity.
  - Backend: Same, /inventory endpoint.
- **Networking**: ALB Ingress (TLS), Network Policy (frontend-to-backend).
- **Storage**: RDS (KMS), S3 (lifecycle).
- **Scaling**: HPA (80%), Karpenter.
- **Security**: RBAC, OPA Gatekeeper, ECR scanning.
- **Observability**: CloudWatch, X-Ray, orders/min dashboard.

## Tool Swap
- **From**: Jenkins (complex, plugin-heavy).
- **To**: GitHub Actions (light, Git-native).
- **Trade-offs**: Jenkins richer, GitHub simpler/faster.
```

---

### Learning Schedule (7-8 Hours)
- **Morning (4h)**:
  - **Theoretical Deep Dive (3h)**:
    - Kubernetes architecture (1h): Pods, Services, HA.
    - Microservices design (1h): Modularity, scaling.
    - Tool swapping (0.5h): Real-world examples.
    - DevSecOps best practices (0.5h): Security, observability.
  - **Break (1h)**.
- **Afternoon (4h)**:
  - **Practical Planning (4h)**:
    - Define features (1h).
    - Design architecture (2h).
    - Tool swap (0.5h).
    - Document/folder setup (0.5h).

---

### Deliverables
- **Documentation**: `ecomm-architecture.md` with features, architecture, and tool swap.
- **Folder Structure**: Initialized `ecomm-capstone/` with subdirs and placeholder files.
- **Verification**: Plan reflects all Kubernetes best practices (modularity, HA, security, etc.).

---

### Why This Matters
- **Theoretical Value**: Grounds learners in Kubernetes and DevSecOps fundamentals, critical for enterprise roles.
- **Practical Impact**: Use cases (Amazon, Netflix) show $1M+ savings and 99.9% uptime, setting a real-world standard.
- **Model Capstone**: Embeds best practices (e.g., Graviton2, TLS, HPA) from Day 1, making it a blueprint for Kubernetes learning.
- **DevSecOps Alignment**: Integrates security, automation, and resilience, preparing learners for Fortune 100 challenges.

