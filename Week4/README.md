### Week 4: Terraform, Kubernetes, and Capstone Project

#### Overview
Week 4 focuses on mastering **Terraform** for infrastructure provisioning and **Kubernetes** for container orchestration, culminating in a **Capstone Project** that automates a **Global Supply Chain Management System**. This system simulates a real-world enterprise application with microservices handling inventory, logistics, order processing, and analytics across multiple AWS regions. The capstone integrates Terraform and Kubernetes with Jenkins, reflecting complex DevOps workflows.

#### Learning Objectives
- Provision multi-region infrastructure with Terraform.
- Deploy and scale a microservices architecture on Kubernetes.
- Design a production-grade CI/CD pipeline for a complex application.
- Address real-world challenges like latency, resilience, and compliance.

#### Prerequisites
- Jenkins master-slave setup from Week 3.
- Docker, AWS CLI, `kubectl`, `eksctl`, and Terraform installed.
- Familiarity with microservices and CI/CD from prior weeks.

#### Time Allocation
- **Terraform**: 40% (2 days)
- **Kubernetes**: 40% (2 days)
- **Capstone Project**: 20% (1 day)

---

### Week 4 Detailed Lesson Plan

#### Day 1: Terraform Fundamentals (20% of Week)
- **Objective**: Learn Terraform basics to provision AWS infrastructure.
- **Theoretical Keywords**:
  - **Terraform**: Open-source IaC tool for multi-provider resource management.
  - **Provider**: Defines a platform (e.g., `aws`, `google`).
  - **Resource**: Infrastructure component (e.g., `aws_vpc`, `aws_eks_cluster`).
  - **State**: Tracks deployed resources (`terraform.tfstate`).
  - **Plan**: Previews changes before applying.
  - **HCL**: HashiCorp’s configuration language.
- **Why It Matters**: Terraform’s provider-agnostic nature supports hybrid/multi-cloud strategies, critical for global enterprises.
- **Activities**:
  1. **Theory (1.5 hr)**:
     - IaC principles: Declarative vs. imperative, idempotency.
     - Core workflow: `init`, `plan`, `apply`, `destroy`.
     - Best practices: Modular design, state versioning, avoid hardcoding.
  2. **Practical Prep (1.5 hr)**:
     - Plan: Provision a VPC and EC2 instance in `us-east-1`.
     - Tasks:
       - Define `provider "aws" { region = "us-east-1" }`.
       - Create `aws_vpc` and `aws_instance` resources.
       - Explore `terraform init` and `plan` outputs.
- **Real-World Use Case**:
  - **Scenario**: A global retailer provisions VPCs and EC2s for a warehouse management system.
  - **How**: Terraform defines a VPC with public/private subnets and EC2s for app servers in `us-east-1`, ensuring network isolation and scalability for regional warehouses.

---

#### Day 2: Advanced Terraform (20% of Week)
- **Objective**: Use Terraform modules and multi-region setups for complex infrastructure.
- **Theoretical Keywords**:
  - **Module**: Reusable IaC code (e.g., VPC module).
  - **Variables**: Parameterize configs (e.g., `var.region`).
  - **Outputs**: Export values (e.g., VPC ID).
  - **Remote Backend**: Stores state in S3 with DynamoDB locking.
  - **Workspace**: Manages environments (e.g., `dev`, `prod`).
  - **Count/For_Each**: Dynamic resource creation.
- **Why It Matters**: Advanced Terraform enables reusable, scalable IaC for global deployments with minimal duplication.
- **Activities**:
  1. **Theory (1.5 hr)**:
     - Modules: Encapsulation, DRY principles.
     - State management: Remote vs. local, locking for teams.
     - Multi-region: Cross-region resource dependencies.
  2. **Practical Prep (1.5 hr)**:
     - Plan: Provision EKS clusters in `us-east-1` and `eu-west-1`.
     - Tasks:
       - Create a `vpc` module with subnets.
       - Define EKS clusters with `for_each` for regions.
       - Set up S3 backend with DynamoDB for state locking.
- **Real-World Use Case**:
  - **Scenario**: A logistics company deploys EKS clusters in multiple regions for a shipment tracking platform.
  - **How**: Terraform modules define VPCs and EKS clusters, with `for_each` creating resources in `us-east-1` and `eu-west-1`. State in S3 ensures team consistency, and outputs provide cluster endpoints.

---

#### Day 3: Kubernetes Fundamentals (20% of Week)
- **Objective**: Master Kubernetes basics for container orchestration.
- **Theoretical Keywords**:
  - **Cluster**: Control plane + worker nodes.
  - **Pod**: Smallest deployable unit with containers.
  - **Deployment**: Manages pod replicas and updates.
  - **Service**: Stable networking abstraction (e.g., LoadBalancer).
  - **Namespace**: Resource isolation (e.g., `prod-us`, `prod-eu`).
  - **Kubeconfig**: Authenticates `kubectl` to clusters.
- **Why It Matters**: Kubernetes automates container lifecycle, enabling high availability and scalability for global apps.
- **Activities**:
  1. **Theory (1.5 hr)**:
     - Architecture: API Server, Scheduler, etcd, worker nodes.
     - Objects: Pods, Deployments, Services, Namespaces.
     - Best practices: Use labels, limit resources, avoid single points of failure.
  2. **Practical Prep (1.5 hr)**:
     - Plan: Deploy a simple app on an EKS cluster.
     - Tasks:
       - Set up EKS with `eksctl`.
       - Create a Deployment/Service for an `nginx` app.
       - Test with `kubectl get pods` and `kubectl describe svc`.
- **Real-World Use Case**:
  - **Scenario**: A streaming service deploys a content delivery app on EKS.
  - **How**: Kubernetes runs `content-delivery` pods in `us-east-1`, with a LoadBalancer Service exposing it globally. Namespaces isolate dev and prod environments.

---

#### Day 4: Advanced Kubernetes (20% of Week)
- **Objective**: Configure networking, storage, and scaling for complex apps.
- **Theoretical Keywords**:
  - **Ingress**: Manages external HTTP/HTTPS traffic.
  - **ConfigMap/Secret**: Stores configs and sensitive data.
  - **PersistentVolume (PV)**: Durable storage for stateful apps.
  - **HorizontalPodAutoscaler (HPA)**: Scales based on CPU/memory.
  - **Multi-Cluster**: Runs K8s across regions.
- **Why It Matters**: Advanced features support microservices, persistence, and global resilience, critical for enterprise systems.
- **Activities**:
  1. **Theory (1.5 hr)**:
     - Networking: Ingress vs. LoadBalancer, pod communication.
     - Storage: PVs, PVCs, StorageClasses.
     - Scaling: HPA vs. manual scaling, multi-cluster strategies.
  2. **Practical Prep (1.5 hr)**:
     - Plan: Deploy a multi-service app with Ingress and storage.
     - Tasks:
       - Define Deployments/Services for 3 microservices.
       - Set up Ingress with `nginx-ingress` controller.
       - Add PV for a database service.
- **Real-World Use Case**:
  - **Scenario**: A manufacturing firm runs a factory automation system on K8s.
  - **How**: Ingress routes traffic to `control-api` and `dashboard-ui`, Secrets store API keys, PVs persist factory data, and HPA scales pods during production peaks.

---

#### Day 5: Capstone Project - Global Supply Chain Management System (20% of Week)
- **Objective**: Automate a complex, multi-region supply chain system using Terraform and Kubernetes.
- **Theoretical Keywords**:
  - **Microservices**: Independent services (e.g., inventory, logistics).
  - **Multi-Region**: Deployments across geographies (e.g., `us-east-1`, `eu-west-1`).
  - **Pipeline as Code**: Jenkinsfile defining CI/CD.
  - **GitOps**: Git-driven deployments.
  - **Zero-Downtime**: Rolling updates or blue-green strategies.
- **Why It Matters**: This capstone simulates a real-world enterprise challenge—coordinating global supply chains with resilience, compliance, and automation.
- **Project Scope**:
  - **System Overview**: A **Global Supply Chain Management System** for a multinational retailer, managing:
    - **Inventory Service**: Tracks stock levels (stateful, uses PostgreSQL).
    - **Logistics Service**: Optimizes shipping routes (stateless).
    - **Order Service**: Processes customer orders (stateless).
    - **Analytics Service**: Generates real-time dashboards (compute-heavy).
    - **API Gateway**: Routes traffic (NGINX-based).
  - **Architecture**:
    - **Regions**: `us-east-1` (primary), `eu-west-1` (secondary).
    - **Infrastructure**: VPCs, EKS clusters, RDS (PostgreSQL), S3 (state/logs).
    - **Deployment**: Microservices on K8s with Ingress, multi-region failover.
    - **Pipeline**: Jenkins builds, pushes to ECR, deploys to EKS.
- **Activities**:
  1. **Theory (1 hr)**:
     - Multi-region challenges: Latency, data consistency, failover.
     - Integration: Terraform provisions infra, K8s runs apps, Jenkins automates.
     - Best practices: Modular IaC, K8s RBAC, pipeline stages, observability prep.
  2. **Practical Prep (2 hr)**:
     - **Terraform Tasks**:
       - Define VPC module (`modules/vpc`): Subnets, NAT Gateways.
       - Provision EKS clusters in `us-east-1` and `eu-west-1` (`main.tf`).
       - Set up RDS in `us-east-1` for inventory data.
       - Use S3/DynamoDB backend for state.
       - Outputs: EKS endpoints, RDS connection string.
     - **Kubernetes Tasks**:
       - Create namespaces: `supply-us`, `supply-eu`.
       - Define Deployments/Services for 5 microservices:
         - `inventory-service` (with PV for PostgreSQL).
         - `logistics-service`, `order-service`, `analytics-service` (stateless).
         - `api-gateway` (NGINX with Ingress).
       - Plan Ingress for `supplychain.globalretail.com`.
       - Add HPA for `analytics-service` (CPU > 70%).
     - **Jenkins Pipeline Tasks**:
       - Update `Jenkinsfile`:
         - Build Docker images for all services.
         - Push to ECR (`866934333672.dkr.ecr.us-east-1.amazonaws.com/supplychain`).
         - Deploy to EKS in `us-east-1`, with failover to `eu-west-1`.
       - Trigger on Git commits to `main` branch.
     - **Deliverables**:
       - Running system accessible at `supplychain.globalretail.com`.
       - Pipeline deploys updates with zero downtime.
       - Multi-region failover tested (e.g., disable `us-east-1` cluster).
- **Real-World Use Case**:
  - **Scenario**: A global retailer (e.g., Walmart) manages supply chains across North America and Europe.
  - **How**: Terraform provisions EKS clusters in `us-east-1` and `eu-west-1`, with RDS for inventory and S3 for logs. Kubernetes runs microservices, with Ingress routing traffic and HPA scaling analytics during demand spikes. Jenkins automates builds and deployments from a Git repo, ensuring real-time stock updates and shipping optimization for 10,000+ stores.

---

### Tools & Resources
- **Terraform**: `terraform.io`.
- **Kubernetes**: `kubectl`, `eksctl`.
- **AWS**: EKS, ECR, RDS, S3, DynamoDB.
- **Jenkins**: Your Week 3 setup.
- **Git Repo**: Hypothetical `globalretail/supplychain`.

---

### Assessment
- **Day 1-4 Quizzes**:
  - Terraform: Explain state locking, module benefits.
  - Kubernetes: Differentiate Ingress vs. Service, describe HPA triggers.
- **Capstone Evaluation**:
  - Criteria: Multi-region EKS up, microservices deployed, pipeline functional, failover works.
  - Demo: Access `supplychain.globalretail.com`, show pipeline run, simulate region failure.

---

### Real-World Alignment
- **Terraform**: Amazon uses it for multi-region infra (e.g., VPCs, EKS).
- **Kubernetes**: FedEx orchestrates logistics microservices.
- **Capstone**: DHL’s supply chain system leverages similar Terraform/K8s/Jenkins workflows.

---

### Progression Notes
- **Day 1-2**: Terraform sets up a complex, multi-region foundation.
- **Day 3-4**: Kubernetes scales microservices for a global app.
- **Day 5**: Capstone integrates both, mirroring enterprise DevOps pipelines.

This plan offers a challenging, real-world capstone while balancing Terraform and Kubernetes learning.