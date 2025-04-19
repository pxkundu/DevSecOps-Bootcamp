# Secure, Scalable Microservices-Based E-commerce Platform on AWS EKS

## Project Overview
This is a capstone project designed to build a secure, scalable e-commerce platform on AWS Elastic Kubernetes Service (EKS), capable of managing 10,000+ products and 100K+ transactions/day during peak seasons (e.g., Black Friday). It follows a five-phase approach—Planning, Build and Automate, Secure and Monitor, Chaos Crunch, and Production Polish—integrating Kubernetes best practices and DevSecOps principles to achieve high availability, security, observability, and resilience.

The project mirrors real-world systems like Amazon’s EKS deployments (1M+ customers), Netflix’s chaos engineering (247M subscribers), and Google’s SRE practices (1B+ users), making it a professional-grade reference for learners and engineers.

---

## Project Folder Structure
Below is the complete folder structure after all phases are implemented, providing a roadmap of the project’s components:

```
ecomm-capstone/
├── docs/
│   ├── ecomm-architecture.md       # Architecture blueprint (Phase 1)
│   └── runbook.md                  # Operational runbook with RCA and postmortem (Phase 5)
├── frontend/
│   ├── src/                        # React app source code
│   │   ├── App.js                  # Main React component
│   │   └── index.js                # Entry point with health endpoints
│   ├── Dockerfile                  # Frontend container config
│   └── kubernetes/                 # Legacy manifests (moved to Helm in Phase 5)
│       ├── deployment.yaml         # Frontend Deployment
│       └── service.yaml            # Frontend ClusterIP Service
├── backend/
│   ├── src/                        # Node.js API source code
│   │   ├── index.js                # API with observability (X-Ray, CloudWatch)
│   ├── Dockerfile                  # Backend container config
│   └── kubernetes/                 # Legacy manifests (moved to Helm in Phase 5)
│       ├── deployment.yaml         # Backend Deployment with X-Ray sidecar
│       └── service.yaml            # Backend ClusterIP Service
├── infrastructure/
│   ├── terraform/
│   │   ├── main.tf                 # EKS cluster, node group, Karpenter config
│   │   ├── variables.tf            # Terraform variables (region, VPC, subnets)
│   │   └── outputs.tf              # Terraform outputs (cluster endpoint, ALB URL)
│   └── helm/
│       └── ecomm/                  # Helm chart for deployment
│           ├── Chart.yaml          # Helm chart metadata
│           ├── values.yaml         # Production values
│           ├── values-staging.yaml # Staging-specific overrides
│           └── templates/          # Helm templates for Deployment, Service, HPA, Ingress
├── kubernetes/
│   ├── ingress.yaml                # Legacy ALB Ingress (moved to Helm)
│   ├── netpol.yaml                 # Network Policy for frontend-to-backend
│   ├── hpa-frontend.yaml           # Legacy HPA for frontend (moved to Helm)
│   ├── hpa-backend.yaml            # Legacy HPA for backend (moved to Helm)
│   ├── rbac/                       # RBAC configurations
│   │   ├── role.yaml               # Role for prod namespace
│   │   └── rolebinding.yaml        # RoleBinding to service account
│   └── opa/                        # OPA Gatekeeper policies
│       └── no-privileged.yaml      # Policy to deny privileged pods
├── observability/
│   └── dashboard.json              # CloudWatch dashboard definition
├── .github/
│   └── workflows/
│       ├── infra.yml               # CI/CD for Terraform infrastructure
│       └── app.yml                 # CI/CD for app build and deployment
└── README.md                       # This file
```

---

## Setup Instructions for DevOps Engineers
Follow these step-by-step instructions to set up and run the project from scratch. Each step assumes you’re starting fresh and includes prerequisites, configurations, and verifications to ensure a successful deployment.

### Prerequisites
Before beginning, ensure you have the following tools and accounts configured:
1. **AWS Account**:
   - Permissions: EKS, ECR, S3, RDS, ACM, IAM.
   - Create an IAM user with programmatic access; note the `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`.
2. **Tools**:
   - **Git**: For cloning the repository.
   - **AWS CLI**: `aws --version` (v2+ recommended).
   - **Terraform**: `terraform -v` (v1.5.0+).
   - **kubectl**: `kubectl version --client`.
   - **Docker**: `docker --version`.
   - **Node.js and npm**: `node -v` (v18+), `npm -v`.
   - **Helm**: `helm version` (v3+).
   - **Apache Benchmark (ab)**: For chaos testing (`sudo apt install apache2-utils` on Ubuntu).
3. **GitHub Repository**:
   - Fork or create a repo for CI/CD.
   - Add secrets: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` (Settings > Secrets and variables > Actions).
4. **ACM Certificate**:
   - Request a certificate in AWS Certificate Manager (ACM) for your domain (e.g., `ecomm.example.com`).
   - Note the ARN (e.g., `arn:aws:acm:us-east-1:123456789012:certificate/abc-123`).

### Step 1: Clone the Repository and Generate Files
1. **Clone the Repository**:
   ```bash
   git clone <your-repo-url>
   cd ecomm-capstone
   ```
2. **Run Phase Scripts**:
   - Execute each phase’s generation script to populate the folder structure:
     ```bash
     chmod +x generate-phase1.sh generate-phase2.sh generate-phase3.sh generate-phase4.sh generate-phase5.sh
     ./generate-phase1.sh
     ./generate-phase2.sh
     ./generate-phase3.sh
     ./generate-phase4.sh
     ./generate-phase5.sh
     ```
   - Verify: Check that all files match the structure above.

### Step 2: Configure AWS Environment
1. **Set Up AWS CLI**:
   ```bash
   aws configure
   # Enter AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, region (us-east-1), output (json)
   ```
2. **Create ECR Repositories**:
   ```bash
   aws ecr create-repository --repository-name frontend --region us-east-1
   aws ecr create-repository --repository-name backend --region us-east-1
   ```
   - Note your AWS account ID (e.g., `123456789012`) from the output.

### Step 3: Deploy EKS Cluster with Terraform (Phase 2)
1. **Configure Terraform Variables**:
   - Edit `infrastructure/terraform/variables.tf`:
     ```hcl
     variable "region" { default = "us-east-1" }
     variable "vpc_id" { default = "vpc-12345678" }  # Replace with your VPC ID
     variable "subnet_ids" {
       default = ["subnet-1a", "subnet-1b", "subnet-1c"]  # Replace with 3 subnet IDs across AZs
     }
     ```
   - Find your VPC and subnet IDs in the AWS VPC console.
2. **Initialize and Apply Terraform**:
   ```bash
   cd infrastructure/terraform
   terraform init
   terraform apply -auto-approve
   ```
   - Wait ~10-15 minutes for EKS cluster creation.
   - Note the `cluster_endpoint` from `outputs.tf`.
3. **Update kubeconfig**:
   ```bash
   aws eks update-kubeconfig --region us-east-1 --name ecomm-cluster
   kubectl get nodes  # Verify 2 t4g.medium nodes
   ```

### Step 4: Build and Push Microservices (Phase 2)
1. **Frontend**:
   ```bash
   cd ../../frontend
   npm init -y && npm install react-scripts express --save
   docker build -t 123456789012.dkr.ecr.us-east-1.amazonaws.com/frontend:latest .
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789012.dkr.ecr.us-east-1.amazonaws.com
   docker push 123456789012.dkr.ecr.us-east-1.amazonaws.com/frontend:latest
   ```
2. **Backend**:
   ```bash
   cd ../backend
   npm init -y && npm install express aws-xray-sdk --save
   docker build -t 123456789012.dkr.ecr.us-east-1.amazonaws.com/backend:latest .
   docker push 123456789012.dkr.ecr.us-east-1.amazonaws.com/backend:latest
   ```

### Step 5: Initial Deployment with kubectl (Phase 2)
1. **Create Namespace**:
   ```bash
   kubectl create namespace prod
   ```
2. **Deploy Microservices**:
   - Update image references in `frontend/kubernetes/deployment.yaml` and `backend/kubernetes/deployment.yaml` with your ECR URLs.
   - Apply:
     ```bash
     kubectl apply -f frontend/kubernetes/ -f backend/kubernetes/ -f kubernetes/ingress.yaml
     ```
   - Replace `<YOUR_ACM_CERT_ARN>` in `kubernetes/ingress.yaml` with your ACM ARN.
3. **Verify**:
   ```bash
   kubectl get pods -n prod  # 5 frontend, 5 backend pods
   kubectl get ingress -n prod  # Note ALB URL (e.g., ecomm-1234567890.us-east-1.elb.amazonaws.com)
   curl <alb-url>  # Should display frontend
   ```

### Step 6: Secure the Cluster (Phase 3)
1. **Apply RBAC**:
   ```bash
   kubectl apply -f kubernetes/rbac/
   kubectl get role -n prod  # Verify ecomm-role
   ```
2. **Apply Network Policy**:
   ```bash
   kubectl apply -f kubernetes/netpol.yaml
   ```
3. **Install OPA Gatekeeper**:
   ```bash
   kubectl apply -f https://raw.githubusercontent.com/open-policy-agent/gatekeeper/master/deploy/gatekeeper.yaml
   kubectl apply -f kubernetes/opa/
   kubectl get constraint -A  # Verify K8sDenyPrivileged
   ```

### Step 7: Enable Observability (Phase 3-5)
1. **Enable Container Insights**:
   ```bash
   aws eks update-cluster-config --name ecomm-cluster --region us-east-1 --logging '{"clusterLogging":[{"types":["api","audit","authenticator","controllerManager","scheduler"],"enabled":true}]}'
   ```
2. **Redeploy Backend with Metrics**:
   - Rebuild and push backend (Step 4) after Phase 5 script updates `index.js`.
   ```bash
   kubectl apply -f backend/kubernetes/
   ```
3. **Deploy CloudWatch Dashboard**:
   ```bash
   aws cloudwatch put-dashboard --dashboard-name EcommDashboard --dashboard-body file://observability/dashboard.json
   ```
4. **Set Alarms**:
   ```bash
   aws cloudwatch put-metric-alarm --alarm-name latency-high --metric-name OrderLatency --namespace EcommMetrics --threshold 1000 --comparison-operator GreaterThanThreshold --evaluation-periods 2 --period 300 --statistic Average --alarm-actions arn:aws:sns:us-east-1:123456789012:ecomm-alerts
   aws cloudwatch put-metric-alarm --alarm-name errors-high --metric-name Errors5xx --namespace EcommMetrics --threshold 5 --comparison-operator GreaterThanThreshold --evaluation-periods 2 --period 300 --statistic Average --alarm-actions arn:aws:sns:us-east-1:123456789012:ecomm-alerts
   ```
   - Replace SNS ARN with your own (create via AWS SNS console if needed).

### Step 8: Test Resilience with Chaos (Phase 4)
1. **Apply HPA**:
   ```bash
   kubectl apply -f kubernetes/hpa-frontend.yaml -f kubernetes/hpa-backend.yaml
   kubectl get hpa -n prod  # Verify frontend-hpa, backend-hpa
   ```
2. **Simulate Pod Failure**:
   ```bash
   kubectl delete pod -l app=frontend -n prod --force  # Kill ~50% (e.g., 2-3 pods)
   kubectl get pods -n prod -w  # Watch recovery to 5 pods
   ```
3. **Simulate Traffic Spike**:
   ```bash
   ab -n 10000 -c 100 http://<alb-url>/
   kubectl get hpa -n prod -w  # Watch pods scale to 10
   kubectl get nodes  # Verify Karpenter adds nodes (e.g., 2 → 4)
   ```

### Step 9: Final Deployment with Helm (Phase 5)
1. **Install Helm** (if not already installed):
   ```bash
   curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash
   helm version
   ```
2. **Update Helm Values**:
   - Edit `infrastructure/helm/ecomm/values.yaml`:
     - Replace `<YOUR_AWS_ACCOUNT_ID>`, `<YOUR_ACM_CERT_ARN>`, `<YOUR_ALB_DNS>` (use ALB URL from Step 5 or a custom domain).
   - Edit `infrastructure/helm/ecomm/values-staging.yaml`:
     - Update `host` to `staging-<YOUR_ALB_DNS>` or a staging domain.
3. **Deploy Staging**:
   ```bash
   helm install ecomm-staging infrastructure/helm/ecomm/ -n staging --create-namespace -f infrastructure/helm/ecomm/values-staging.yaml
   kubectl get pods -n staging  # 2 pods each for frontend/backend
   ```
4. **Deploy Production**:
   ```bash
   helm upgrade --install ecomm infrastructure/helm/ecomm/ -n prod
   kubectl get pods -n prod  # 5 pods each for frontend/backend
   ```
5. **Verify**:
   ```bash
   helm ls -n staging  # ecomm-staging
   helm ls -n prod     # ecomm
   curl http://<staging-alb-url>  # Staging frontend
   curl http://<prod-alb-url>     # Production frontend
   ```

### Step 10: Configure CI/CD (Phase 2)
1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Complete project setup"
   git push origin main
   ```
2. **Verify Pipelines**:
   - Check GitHub Actions (`infra.yml`, `app.yml`) in the repo’s Actions tab.
   - Ensure Terraform applies and apps deploy successfully (requires AWS secrets set).

### Step 11: Final Verification
1. **Observability**:
   - Open CloudWatch Dashboards in AWS console, verify CPU, orders, latency, errors.
   - Simulate load (`ab -n 1000 -c 10 <alb-url>/orders`), check alarms in SNS (e.g., email).
2. **Chaos Recovery**:
   - Repeat Step 8, use `runbook.md` to recover, validate <5 min MTTR.
3. **Deployment**:
   - Confirm staging (2 pods) and prod (5 pods) are running via `kubectl get pods -n <namespace>`.

---

## Troubleshooting
- **Terraform Fails**: Check AWS credentials, VPC/subnet IDs.
- **Pods Not Starting**: Verify ECR image URLs, pull policies.
- **Ingress Not Working**: Ensure ACM ARN and ALB DNS are correct.
- **CI/CD Errors**: Confirm GitHub secrets and ECR permissions.

---

## Why This Project Matters
- **Industry Alignment**: Matches Amazon’s EKS (1M+ customers), Netflix’s Helm (247M subscribers), and Google’s SRE (1B+ users).
- **DevSecOps Best Practices**: Security (RBAC, OPA), observability (CloudWatch, X-Ray), resilience (HPA, chaos), automation (CI/CD, Helm).
- **Learning Outcome**: Equips engineers with end-to-end Kubernetes and DevSecOps skills for enterprise roles.

Congratulations! You’ve deployed a production-ready e-commerce platform on AWS EKS. Refer to `docs/runbook.md` for ongoing operations and incident response.