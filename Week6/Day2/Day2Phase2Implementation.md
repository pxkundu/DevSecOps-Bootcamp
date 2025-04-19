## Phase 2: Build and Automate - CI/CD + EKS, Scale for a DDoS
**Objective**: Build the Kubernetes infrastructure on AWS EKS, deploy microservices (frontend and backend), and establish a CI/CD pipeline, ensuring scalability under a simulated DDoS attack.

- **Duration**: ~7-8 hours.
- **Focus**: Infrastructure building with Kubernetes, initial microservices deployment, CI/CD setup, and DDoS resilience.
- **Outcome**: A fully functional EKS cluster with deployed microservices, automated via CI/CD, and validated for scalability.

---

### How We’re Thinking About Phase 2
- **Strategic Mindset**: Phase 2 is the operational backbone, translating the Phase 1 blueprint into a tangible, running system. We approach it as a real-world DevSecOps deployment scenario, prioritizing:
  - **Infrastructure as Code (IaC)**: Automating EKS setup for repeatability and consistency.
  - **Microservices Deployment**: Building and deploying frontend/backend to validate the architecture.
  - **Automation**: Establishing CI/CD to streamline future updates.
  - **Resilience**: Testing scalability under DDoS-like conditions to ensure production readiness.
- **Industry Benchmarking**: We emulate Fortune 100 practices (e.g., Netflix’s EKS for 247M subscribers, Walmart’s Black Friday scaling) to ensure the infrastructure meets enterprise-grade standards.
- **Why This Approach**: 
  - A robust backbone ensures the project can scale, secure, and monitor effectively in later phases.
  - Hands-on Kubernetes experience prepares learners for real-world DevSecOps roles.
  - DDoS testing validates resilience, a critical skill for production systems.

---

### Designing Each Solution Component
Each component is designed with Kubernetes best practices, DevSecOps principles, and a clear rationale to ensure industry-standard execution.

#### 1. EKS Cluster Infrastructure
- **Solution**: Deploy an AWS EKS cluster with 2 `t4g.medium` Graviton2 nodes across 3 AZs (`us-east-1a/b/c`).
- **Design**:
  - **Nodes**: Graviton2 for cost efficiency (20% cheaper than x86, AWS 2023).
  - **Multi-AZ**: High availability (HA) across `us-east-1a/b/c`.
  - **Namespace**: `prod` for resource isolation.
  - **Scaling**: Karpenter for dynamic node scaling.
- **DevSecOps**:
  - IAM roles for least-privilege access (AWS Well-Architected Security).
  - Karpenter ensures elastic scaling (AWS Well-Architected Performance Efficiency).
- **How**:
  - Terraform (`main.tf`) defines the EKS cluster, node group, and Karpenter.
- **Why**:
  - HA prevents downtime (e.g., Amazon’s 99.99% uptime, 2023).
  - Graviton2 optimizes costs (e.g., Netflix’s $1M+ savings).
  - Karpenter handles spikes (e.g., Walmart’s 5x scaling, 2022).
- **Diagram**:
  ```
  [EKS Cluster]
    ├── Node 1 (t4g.medium, us-east-1a)
    ├── Node 2 (t4g.medium, us-east-1b)
    └── Karpenter (us-east-1c, scales nodes)
  ```

#### 2. Microservices (Frontend and Backend)
- **Solution**:
  - **Frontend**: React app, 5 replicas, containerized with Docker.
  - **Backend**: Node.js API (`/inventory`, `/orders`), 5 replicas.
- **Design**:
  - **Resources**: `requests: {cpu: "200m", memory: "256Mi"}, limits: {cpu: "500m", memory: "512Mi"}`.
  - **Anti-Affinity**: Spreads pods across nodes/AZs for HA.
  - **Probes**: Liveness (`/health`), Readiness (`/ready`) for zero-downtime.
- **DevSecOps**:
  - Resource limits ensure QoS (Kubernetes best practice).
  - Anti-affinity enhances resilience (AWS Well-Architected Reliability).
  - Probes enable rolling updates (DevSecOps automation).
- **How**:
  - Dockerfiles for containerization.
  - Kubernetes manifests (`deployment.yaml`, `service.yaml`) for deployment.
  - Push images to ECR with scanning.
- **Why**:
  - Resource optimization prevents over-provisioning (e.g., Google’s GKE).
  - HA ensures availability (e.g., Netflix’s 2M+ viewers).
  - Probes support zero-downtime (e.g., Walmart’s 500M+ txns).
- **Diagram**:
  ```
  [prod Namespace]
    ├── Frontend Deployment (5 pods)
    │   ├── Pod 1 (t4g.medium, us-east-1a, /health)
    │   └── Pod 2 (t4g.medium, us-east-1b, /ready)
    └── Backend Deployment (5 pods)
        ├── Pod 1 (t4g.medium, us-east-1a, /health)
        └── Pod 2 (t4g.medium, us-east-1c, /ready)
  ```

#### 3. Networking
- **Solution**: ALB Ingress with TLS for external access.
- **Design**:
  - ALB routes HTTPS traffic to frontend/backend Services (ClusterIP).
  - TLS enabled with an AWS ACM certificate.
- **DevSecOps**:
  - TLS ensures secure communication (NIST 800-53 SC-13).
  - ALB provides load balancing (AWS Well-Architected Performance Efficiency).
- **How**:
  - `ingress.yaml`: Configures ALB with SSL cert ARN.
  - Terraform integrates ALB with EKS.
- **Why**:
  - Secure routing protects users (e.g., Amazon’s 1M+ customers).
  - Load balancing scales traffic (e.g., Netflix’s 17B+ hours).
- **Diagram**:
  ```
  [Users] → [ALB Ingress (TLS)]
            ├── Frontend Service (ClusterIP)
            └── Backend Service (ClusterIP)
  ```

#### 4. CI/CD Pipeline
- **Solution**: GitHub Actions for automating infrastructure and app deployment.
- **Design**:
  - **Infra Pipeline**: Deploys EKS via Terraform (`infra.yml`).
  - **App Pipeline**: Builds Docker images, pushes to ECR, deploys to EKS (`app.yml`).
- **DevSecOps**:
  - Automation reduces manual errors (AWS Well-Architected Operational Excellence).
  - GitHub Actions ensures agility (e.g., Phase 1 tool swap).
- **How**:
  - `.github/workflows/infra.yml`: Runs `terraform apply`.
  - `.github/workflows/app.yml`: Builds, pushes, and applies manifests.
- **Why**:
  - Cuts deployment time by 70% (DORA 2023).
  - Reflects industry CI/CD (e.g., Netflix’s 100+ daily releases).
- **Diagram**:
  ```
  [Git Push]
    ├── Infra Pipeline → [Terraform → EKS Cluster]
    └── App Pipeline → [Docker → ECR → EKS Deployment]
  ```

#### 5. Scaling and DDoS Resilience
- **Solution**: HPA and Karpenter for pod and node scaling, tested with a DDoS simulation.
- **Design**:
  - **HPA**: Scales pods on CPU > 80% (min 2, max 10).
  - **Karpenter**: Adds nodes dynamically under load.
  - **DDoS Test**: Simulate with `ab -n 10000 -c 100 <alb-url>`.
- **DevSecOps**:
  - Auto-scaling ensures performance (AWS Well-Architected Reliability).
  - DDoS testing validates resilience (e.g., CNCF 2023).
- **How**:
  - `hpa.yaml`: Configures HPA.
  - Terraform installs Karpenter.
  - Run `ab` tool to simulate traffic spike.
- **Why**:
  - Handles 10x spikes (e.g., Walmart’s 46M items, 2022).
  - Saves $1M+ in downtime (e.g., Amazon’s 2023 DDoS defense).
- **Diagram**:
  ```
  [DDoS Traffic Spike]
    ├── HPA → Scales pods (2 → 10)
    └── Karpenter → Adds nodes (2 → 4)
  ```

---

### Why This Backbone is Industry-Standard and DevSecOps-Compliant
- **Kubernetes Best Practices**:
  - **Modularity**: Separate frontend/backend Deployments (e.g., Netflix’s 100+ services).
  - **HA**: Multi-AZ, anti-affinity (e.g., Amazon’s 99.99% uptime).
  - **Scaling**: HPA/Karpenter (e.g., Walmart’s 5x pod scaling).
  - **Resource Optimization**: Limits/probes (e.g., Google’s GKE).
- **DevSecOps Principles**:
  - **Security**: TLS on ALB (e.g., Amazon’s 1M+ customers).
  - **Automation**: Terraform/CI-CD (e.g., HashiCorp’s 90% drift reduction).
  - **Resilience**: DDoS testing (e.g., Netflix’s Chaos Monkey).
- **Model Project**: 
  - Hands-on EKS deployment mirrors real-world ops.
  - Scalable, secure backbone sets learners up for enterprise roles.

---

### Detailed Implementation Plan for Phase 2
#### Tasks (7-8 Hours)
1. **Setup Environment (1h)**:
   - Install Terraform, kubectl, AWS CLI.
   - Configure AWS credentials.
2. **Build EKS Infrastructure (2h)**:
   - Write `main.tf` for EKS, Graviton2 nodes, Karpenter.
   - Apply: `terraform init && terraform apply`.
3. **Develop Microservices (2h)**:
   - **Frontend**: Create React app (`npx create-react-app`), add `/health` endpoint, Dockerize.
   - **Backend**: Create Node.js API (`/inventory`, `/orders`, `/health`), Dockerize.
   - Push to ECR: `docker push <ecr-repo>/frontend:latest`.
4. **Deploy to EKS (1h)**:
   - Write `deployment.yaml`, `service.yaml` for frontend/backend.
   - Apply: `kubectl apply -f .`.
   - Configure ALB Ingress (`ingress.yaml`) with TLS.
5. **Setup CI/CD (1h)**:
   - Write `.github/workflows/infra.yml` and `app.yml`.
   - Push to GitHub, verify pipeline runs.
6. **Test DDoS Resilience (1h)**:
   - Apply HPA (`hpa.yaml`).
   - Simulate DDoS: `ab -n 10000 -c 100 <alb-url>`.
   - Check pod/node scaling: `kubectl get pods`, `kubectl get nodes`.

#### Sample Code Snippets
- **Terraform (`infrastructure/terraform/main.tf`)**:
  ```hcl
  provider "aws" { region = "us-east-1" }
  module "eks" {
    source          = "terraform-aws-modules/eks/aws"
    cluster_name    = "ecomm-cluster"
    cluster_version = "1.29"
    subnets         = ["subnet-1a", "subnet-1b", "subnet-1c"]
    node_groups = {
      ng1 = {
        instance_types = ["t4g.medium"]
        min_size       = 2
        max_size       = 4
        desired_size   = 2
      }
    }
  }
  # Karpenter setup (simplified)
  resource "aws_eks_addon" "karpenter" {
    cluster_name = module.eks.cluster_id
    addon_name   = "karpenter"
  }
  ```
- **Frontend Deployment (`frontend/kubernetes/deployment.yaml`)**:
  ```yaml
  apiVersion: apps/v1
  kind: Deployment
  metadata:
    name: frontend
    namespace: prod
  spec:
    replicas: 5
    selector:
      matchLabels:
        app: frontend
    template:
      metadata:
        labels:
          app: frontend
      spec:
        affinity:
          podAntiAffinity:
            preferredDuringSchedulingIgnoredDuringExecution:
            - podAffinityTerm:
                labelSelector:
                  matchExpressions:
                  - key: app
                    operator: In
                    values: ["frontend"]
                topologyKey: "topology.kubernetes.io/zone"
        containers:
        - name: frontend
          image: <ecr-repo>/frontend:latest
          resources:
            requests:
              cpu: "200m"
              memory: "256Mi"
            limits:
              cpu: "500m"
              memory: "512Mi"
          livenessProbe:
            httpGet:
              path: /health
              port: 80
          readinessProbe:
            httpGet:
              path: /ready
              port: 80
  ```

---

### Deliverables
- **EKS Cluster**: Running with 2 nodes, Karpenter installed.
- **Microservices**: Frontend/backend deployed (5 pods each).
- **CI/CD**: GitHub Actions pipelines (`infra.yml`, `app.yml`) functional.
- **Verification**: ALB URL accessible, pods scale under DDoS load.

---

### Why This Matters
- **Backbone Strength**: A scalable, secure EKS setup ensures success in later phases (security, chaos testing).
- **Industry Standard**: Matches Amazon’s EKS deployments (1M+ customers), Netflix’s CI/CD (100+ releases/day).
- **DevSecOps Best Practices**: Automation (Terraform), resilience (HPA), security (TLS) embedded.
- **Model Project**: Hands-on Kubernetes infrastructure building, ideal for learners aiming for enterprise roles.

