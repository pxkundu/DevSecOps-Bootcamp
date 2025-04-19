# E-commerce Capstone Project on AWS EKS - Phase 2 Implementation

## Project Overview
The **Secure, Scalable Microservices-Based E-commerce Platform on AWS EKS** is a capstone project designed to manage 10,000+ products and scale to handle 100K+ transactions/day during peak seasons (e.g., holiday sales). Built with Kubernetes best practices and DevSecOps principles, this project simulates a real-world e-commerce application deployed on AWS Elastic Kubernetes Service (EKS).

**Phase 2: Build and Automate - CI/CD + EKS, Scale for a DDoS** focuses on establishing the infrastructure backbone, deploying initial microservices (frontend and backend), and setting up CI/CD pipelines using GitHub Actions. This phase ensures the system is scalable, resilient (tested against a simulated DDoS attack), and automated, mirroring enterprise-grade deployments like those of Amazon, Netflix, and Walmart.

---

## Phase 2 Objectives
- **Infrastructure**: Deploy an EKS cluster with Graviton2 nodes and Karpenter for scaling.
- **Microservices**: Build and deploy a React frontend and Node.js backend with Kubernetes manifests.
- **CI/CD**: Automate infrastructure and application deployment with GitHub Actions.
- **Resilience**: Validate scalability under a simulated DDoS attack (10,000 requests).

---

## Prerequisites
To replicate or extend this Phase 2 implementation, ensure you have:
- **AWS Account**: Access to EKS, ECR, S3, and ACM (for TLS certificates).
- **Tools Installed**:
  - Terraform (v1.5.0+)
  - kubectl
  - AWS CLI (configured with credentials)
  - Node.js and npm (v18+)
  - Docker
  - Git
- **GitHub Repository**: A repo with secrets configured:
  - `AWS_ACCESS_KEY_ID`
  - `AWS_SECRET_ACCESS_KEY`
- **ACM Certificate**: A valid certificate ARN for TLS (e.g., issued via AWS Certificate Manager).
- **Phase 1 Completed**: The `ecomm-capstone/` folder structure from Phase 1 (run `generate-phase1.sh` if not done).

---

## Phase 2 Deliverables
The following components were implemented in Phase 2:

1. **EKS Cluster**:
   - 2 `t4g.medium` Graviton2 nodes across 3 AZs (`us-east-1a/b/c`).
   - Karpenter installed for dynamic node scaling.
   - Defined in `infrastructure/terraform/main.tf`.

2. **Frontend Microservice**:
   - React app (`frontend/src/App.js`, `index.js`) with `/health` and `/ready` endpoints.
   - Dockerized (`frontend/Dockerfile`).
   - Deployed with 5 replicas (`frontend/kubernetes/deployment.yaml`, `service.yaml`).

3. **Backend Microservice**:
   - Node.js API (`backend/src/index.js`) with `/inventory`, `/orders`, `/health`, and `/ready` endpoints.
   - Dockerized (`backend/Dockerfile`).
   - Deployed with 5 replicas (`backend/kubernetes/deployment.yaml`, `service.yaml`).

4. **Networking**:
   - ALB Ingress with TLS (`kubernetes/ingress.yaml`) routing traffic to frontend and backend.

5. **CI/CD Pipelines**:
   - `infra.yml`: Deploys EKS infrastructure via Terraform.
   - `app.yml`: Builds Docker images, pushes to ECR, and deploys to EKS.

6. **Documentation**:
   - Updated `README.md` with Phase 2 instructions.

---

## Folder Structure
The project structure after Phase 2 implementation:
```
ecomm-capstone/
├── docs/
│   ├── ecomm-architecture.md       # Phase 1 blueprint
│   └── runbook.md                  # Placeholder for Day 5
├── frontend/
│   ├── src/                        # React app source
│   │   ├── App.js                  # Main component
│   │   └── index.js                # Entry point with health endpoints
│   ├── Dockerfile                  # Container config
│   └── kubernetes/
│       ├── deployment.yaml         # 5-replica Deployment
│       └── service.yaml            # ClusterIP Service
├── backend/
│   ├── src/                        # Node.js API source
│   │   ├── index.js                # API with endpoints
│   ├── Dockerfile                  # Container config
│   └── kubernetes/
│       ├── deployment.yaml         # 5-replica Deployment
│       └── service.yaml            # ClusterIP Service
├── infrastructure/
│   ├── terraform/
│   │   ├── main.tf                 # EKS cluster config
│   │   ├── variables.tf            # Variables (region, VPC, subnets)
│   │   └── outputs.tf              # Outputs (cluster endpoint)
│   └── helm/
│       └── ecomm/                  # Empty Helm chart (for Phase 3)
├── kubernetes/
│   ├── ingress.yaml                # ALB Ingress with TLS
│   ├── netpol.yaml                 # Empty (for Phase 3)
│   └── opa/                        # Empty OPA policies (for Phase 3)
├── .github/
│   └── workflows/
│       ├── infra.yml               # CI/CD for infrastructure
│       └── app.yml                 # CI/CD for app deployment
└── README.md                       # This file
```

---

## Setup Instructions
Follow these steps to set up and verify the Phase 2 implementation:

### 1. Clone and Prepare the Repository
```bash
git clone <repo-url>
cd ecomm-capstone
```

### 2. Configure Terraform
- Update `infrastructure/terraform/variables.tf` with your VPC and subnet IDs:
  ```hcl
  variable "vpc_id" { default = "vpc-12345678" }
  variable "subnet_ids" { default = ["subnet-1a", "subnet-1b", "subnet-1c"] }
  ```
- Deploy the EKS cluster:
  ```bash
  cd infrastructure/terraform
  terraform init
  terraform apply -auto-approve
  ```
- Note the `cluster_endpoint` from `outputs.tf`.

### 3. Build and Push Microservices
- **Frontend**:
  ```bash
  cd ../../frontend
  npm init -y && npm install react-scripts express --save
  docker build -t <your-aws-account-id>.dkr.ecr.us-east-1.amazonaws.com/frontend:latest .
  aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <your-aws-account-id>.dkr.ecr.us-east-1.amazonaws.com
  docker push <your-aws-account-id>.dkr.ecr.us-east-1.amazonaws.com/frontend:latest
  ```
- **Backend**:
  ```bash
  cd ../backend
  npm init -y && npm install express --save
  docker build -t <your-aws-account-id>.dkr.ecr.us-east-1.amazonaws.com/backend:latest .
  docker push <your-aws-account-id>.dkr.ecr.us-east-1.amazonaws.com/backend:latest
  ```

### 4. Deploy to EKS
- Update image references in `frontend/kubernetes/deployment.yaml` and `backend/kubernetes/deployment.yaml` with your ECR URLs.
- Configure `kubectl`:
  ```bash
  aws eks update-kubeconfig --region us-east-1 --name ecomm-cluster
  ```
- Create namespace and deploy:
  ```bash
  kubectl create namespace prod
  kubectl apply -f frontend/kubernetes/
  kubectl apply -f backend/kubernetes/
  kubectl apply -f kubernetes/ingress.yaml
  ```
- Replace `<YOUR_ACM_CERT_ARN>` in `kubernetes/ingress.yaml` with your certificate ARN before applying.

### 5. Set Up CI/CD
- Push changes to GitHub:
  ```bash
  git add .
  git commit -m "Phase 2 implementation"
  git push origin main
  ```
- Ensure GitHub secrets (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`) are set in the repository settings.
- Verify pipelines run successfully in GitHub Actions.

### 6. Test DDoS Resilience
- Get the ALB URL:
  ```bash
  kubectl get ingress -n prod
  ```
- Simulate a DDoS attack:
  ```bash
  ab -n 10000 -c 100 <alb-url>
  ```
- Check scaling:
  ```bash
  kubectl get pods -n prod -w  # Watch pods scale
  kubectl get nodes          # Watch nodes scale with Karpenter
  ```

---

## Verification
- **EKS Cluster**: `kubectl get nodes` shows 2 `t4g.medium` nodes across AZs.
- **Microservices**: 
  - `kubectl get pods -n prod` shows 5 frontend and 5 backend pods running.
  - Access `<alb-url>` displays the React frontend; `<alb-url>/inventory` returns JSON.
- **CI/CD**: GitHub Actions logs show successful `infra.yml` and `app.yml` runs.
- **DDoS Resilience**: Pods scale to 10+ and nodes increase under load, then stabilize.

---

## Why Phase 2 Matters
- **Industry Alignment**:
  - Matches Amazon’s EKS deployments (1M+ customers, 375M items sold, 2023).
  - Reflects Netflix’s CI/CD automation (100+ releases/day for 247M subscribers).
  - Emulates Walmart’s resilience (5x scaling for 46M items, 2022).
- **DevSecOps Best Practices**:
  - **Automation**: Terraform and GitHub Actions ensure consistency (90% drift reduction, HashiCorp 2023).
  - **Scalability**: HPA/Karpenter handle spikes (e.g., 10K+ req/sec).
  - **Resilience**: Probes and anti-affinity ensure 99.9% uptime (DORA 2023).
- **Model Project**: 
  - Hands-on Kubernetes infrastructure building.
  - Practical CI/CD setup for learners.
  - Real-world DDoS testing prepares for enterprise challenges.

---

## Next Steps (Phase 3)
- Enhance security with RBAC, Network Policies, and OPA Gatekeeper.
- Add observability with CloudWatch and X-Ray.
- Pass a penetration test (e.g., `kube-hunter`).

---
