# Week 3, Day 4: Introduction to GitOps with ArgoCD - Security Enhanced

## Overview
This folder contains the implementation and documentation for **Week 3, Day 4** of our DevOps training, introducing **GitOps with ArgoCD** and emphasizing **security best practices**. We’ve evolved the SaaS Task Manager project from a Jenkins-driven pipeline to a secure GitOps model, using ArgoCD for declarative deployments on AWS EC2 with Docker. Key enhancements include least-privilege IAM roles, post-deployment ECR updates, AWS Secrets Manager for credentials, and GitOps security principles, aligning with Fortune 100 standards.

## Objectives
- Transition Task Manager deployments to **GitOps with ArgoCD**, replacing Jenkins `deployEC2`.
- Secure EC2 access with a **least-privilege IAM role** for ECR push/pull.
- Update **ECR repositories** with the latest images post-deployment.
- Manage all secrets (e.g., GitHub token, SSH key) via **AWS Secrets Manager**.
- Implement **multi-environment deployments** (dev, staging, prod) with secure GitOps workflows.

## Folder Structure
```
week3-day4/
├── README.md                # This index file
├── task-manager/            # Task Manager project source (updated)
│   ├── backend/            # Backend app (Node.js API)
│   │   ├── app.js
│   │   ├── package.json
│   │   ├── Dockerfile
│   │   └── .dockerignore
│   ├── frontend/           # Frontend app (Node.js UI)
│   │   ├── app.js
│   │   ├── package.json
│   │   ├── Dockerfile
│   │   └── .dockerignore
│   ├── scripts/            # Setup scripts for EC2 instances
│   │   ├── install_base.sh
│   │   ├── install_nginx.sh
│   │   ├── install_nodejs.sh
│   │   └── config_docker.sh
│   ├── Jenkinsfile         # Updated pipeline with GitOps integration
│   ├── README.md           # Project-specific README
│   └── .gitignore
├── pipeline-lib/           # Shared library (unchanged from Day 3)
│   ├── vars/
│   │   ├── buildDocker.groovy
│   │   ├── deployEC2.groovy
│   │   ├── scanImage.groovy
│   │   └── logToCloudWatch.groovy
│   ├── README.md
│   └── .gitignore
├── task-manager-gitops/    # New GitOps repo for declarative configs
│   ├── env/
│   │   ├── dev/
│   │   │   ├── backend.yaml
│   │   │   └── frontend.yaml
│   │   ├── staging/
│   │   │   ├── backend.yaml
│   │   │   └── frontend.yaml
│   │   └── prod/
│   │       ├── backend.yaml
│   │       └── frontend.yaml
│   ├── README.md           # GitOps repo README
│   └── .gitignore
├── docs/                   # Documentation
│   └── gitops-security.md  # Notes on GitOps security best practices
└── setup-scripts/          # AWS setup commands
    ├── argocd-install.sh   # ArgoCD EC2 setup
    ├── sync-ec2.sh         # Custom ArgoCD sync script
    └── iam-role-update.sh  # IAM role update script
```

## Contents Covered

### 1. GitOps with ArgoCD
- **Purpose**: Shift to declarative deployments using Git as the source of truth.
- **Implementation**: ArgoCD syncs `task-manager-gitops` manifests to EC2s.
- **Outcome**: Automated, consistent deployments with drift detection.

### 2. Security Best Practices
- **Least Privilege**: Updated `JenkinsSlaveRole` for ECR access only (e.g., `ecr:PutImage`).
- **Secrets Management**: GitHub token, SSH key, and ArgoCD creds in AWS Secrets Manager.
- **Immutable Artifacts**: Post-deploy ECR updates with env-specific tags (e.g., `prod-202503112359`).
- **GitOps Security**: Encrypted Git access, RBAC, and audit trails via Git/ArgoCD logs.
- **Auditability**: CloudTrail logs IAM/ECR actions, Git tracks manifest changes.

### 3. Updated Pipeline
- **Jenkinsfile**: Builds images, updates `task-manager-gitops`, triggers ArgoCD sync.
- **ECR Integration**: Pushes latest images post-deploy with secure IAM perms.
- **Secrets**: Fetches SSH key from Secrets Manager for Git operations.

### 4. Multi-Environment Deployments
- **Structure**: `env/dev`, `env/staging`, `env/prod` in `task-manager-gitops`.
- **Outcome**: Isolated, secure deployments per environment.

### 5. ArgoCD Custom Sync
- **Script**: `sync-ec2.sh` deploys Docker containers, updates ECR, uses Secrets Manager for Nginx configs.
- **Outcome**: Secure, non-Kubernetes deployment on EC2.

## Prerequisites
- AWS Account with IAM roles (`JenkinsSlaveRole` updated).
- GitHub repos: `task-manager`, `pipeline-lib`, `task-manager-gitops`.
- EC2 key pair (`<your-key>.pem`).
- S3 bucket (`<your-bucket>`), ECR repos (`task-backend`, `task-frontend`), Secrets Manager secrets (`github-token`, `jenkins-ssh-key`, `argocd-admin`).

## Setup Instructions
1. **IAM Role Update**: Run `setup-scripts/iam-role-update.sh`.
2. **ArgoCD Setup**: Run `setup-scripts/argocd-install.sh`.
3. **Secrets**: Configure Secrets Manager with GitHub token, SSH key, ArgoCD creds.
4. **GitOps Repo**: Push `task-manager-gitops` to GitHub, enable branch protection.
5. **Pipeline**: Update Jenkins with new `Jenkinsfile`, build `main` for `prod`.
6. **Test**: Verify at `http://<frontend-ip>/tasks`, check ECR tags.

## Key Learnings
- **Theory**: GitOps, ArgoCD, and security principles (least privilege, secrets, auditability).
- **Practical**: Secure Task Manager deployments with ECR updates and Secrets Manager.
- **Real-World**: Applies to SaaS, finance, retail for secure, automated CI/CD.

## Next Steps
- Simulate a security breach (e.g., leaked secret in Git).
- Add automated Trivy scans in ArgoCD sync.
- Prepare for Day 5 (e.g., observability with Prometheus).

---
