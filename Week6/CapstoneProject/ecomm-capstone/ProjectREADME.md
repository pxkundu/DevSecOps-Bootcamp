# E-commerce Capstone Project on AWS EKS

## Overview
A secure, scalable microservices-based e-commerce platform on AWS EKS, designed for 10,000+ products and 100K+ transactions/day. Built with Kubernetes best practices and DevSecOps principles.

## Prerequisites
- AWS account (EKS, ECR, S3, RDS, ACM).
- Terraform, kubectl, AWS CLI, Node.js, Docker, Helm, Git.
- GitHub repo with secrets (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY).
- ACM certificate for TLS.

## Setup
### Phase 1: Planning
1. Clone repo: `git clone <repo-url>`
2. Review `docs/ecomm-architecture.md`.

### Phase 2: Build and Automate
1. Deploy EKS: `cd infrastructure/terraform && terraform init && terraform apply`.
2. Build/push images: `docker build -t <ecr-repo>/frontend:latest ./frontend` (and backend).
3. Initial deploy: `kubectl apply -f frontend/kubernetes/ -f backend/kubernetes/ -f kubernetes/ingress.yaml`.

### Phase 3: Secure and Monitor
1. Apply security: `kubectl apply -f kubernetes/rbac/ -f kubernetes/netpol.yaml -f kubernetes/opa/`.
2. Enable observability: Update backend, redeploy.

### Phase 4: Chaos Crunch
1. Apply HPA: `kubectl apply -f kubernetes/hpa-frontend.yaml -f kubernetes/hpa-backend.yaml`.
2. Simulate chaos: Pod kill (`kubectl delete pod`), traffic spike (`ab -n 10000 -c 100`).

### Phase 5: Production Polish
1. Enhance observability:
   - Deploy dashboard: `aws cloudwatch put-dashboard --dashboard-name EcommDashboard --dashboard-body file://observability/dashboard.json`
   - Set alarms:
     - Latency: `aws cloudwatch put-metric-alarm --alarm-name latency-high --metric-name OrderLatency --namespace EcommMetrics --threshold 1000 --comparison-operator GreaterThanThreshold --evaluation-periods 2 --period 300 --statistic Average --alarm-actions <SNS_TOPIC_ARN>`
     - Errors: `aws cloudwatch put-metric-alarm --alarm-name errors-high --metric-name Errors5xx --namespace EcommMetrics --threshold 5 --comparison-operator GreaterThanThreshold --evaluation-periods 2 --period 300 --statistic Average --alarm-actions <SNS_TOPIC_ARN>`
2. Update backend: `cd backend && npm install && docker build -t <ecr-repo>/backend:latest . && docker push ...`
3. Deploy with Helm:
   - Staging: `helm install ecomm-staging infrastructure/helm/ecomm/ -n staging --create-namespace -f infrastructure/helm/ecomm/values-staging.yaml`
   - Production: `helm upgrade --install ecomm infrastructure/helm/ecomm/ -n prod`
4. Verify:
   - Dashboard: Check CloudWatch UI.
   - Alarms: Simulate load, check SNS.
   - Helm: `helm ls -n staging` and `helm ls -n prod`.

## Structure
- `docs/`: Architecture and runbook.
- `frontend/`, `backend/`: Microservices.
- `infrastructure/`: Terraform and Helm configs.
- `kubernetes/`: Legacy manifests (now in Helm).
- `observability/`: CloudWatch dashboard.
- `.github/`: CI/CD workflows.

## Verification
- Dashboard shows CPU, orders, latency, errors.
- Alarms trigger on latency >1s, errors >5%.
- Staging (2 pods) and prod (5 pods) deployments active.
