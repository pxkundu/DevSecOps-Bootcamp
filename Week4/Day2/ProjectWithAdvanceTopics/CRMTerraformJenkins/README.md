# CRM Platform with Terraform and Jenkins

This project automates a multi-region CRM platform on AWS using Terraform, Docker, Jenkins, and GitHub.

## Prerequisites
- AWS CLI configured.
- EC2 key pair (`my-key` in `us-east-1`).
- GitHub repo (`<your-username>/CRMTerraformJenkins`).
- Docker, Terraform installed.

## Setup Instructions
**Create S3 and DynamoDB for State**
   ```bash
   aws s3 mb s3://crm-tf-state-2025 --region us-east-1
   aws dynamodb create-table --table-name tf-lock --attribute-definitions AttributeName=LockID,AttributeType=S --key-schema AttributeName=LockID,KeyType=HASH --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 --region us-east-1

---

### Project Overview: CRM Platform Deployment
- **Scenario**: A Salesforce-like CRM platform deployed across `us-east-1` and `eu-west-1` for global sales teams.
- **Teams**: Infra (VPCs, EKS), App (microservices), Security (policies).
- **Components**:
  - **AWS**: VPCs, EKS clusters, S3 (state/logs), ECR (Docker images), DynamoDB (state locking).
  - **Docker**: Containers for `crm-api` (Node.js), `crm-ui` (React), `crm-analytics` (Python).
  - **Jenkins**: CI/CD pipeline from GitHub.
  - **GitHub**: Hosts Terraform modules and app code.
  - **Terraform**: Provisions all infra with advanced features.

---

### Project Structure
```
CRMTerraformJenkins/
├── terraform/
│   ├── main.tf              # Root config with module calls
│   ├── variables.tf         # Input variables
│   ├── outputs.tf           # Output values
│   ├── backend.tf           # Remote state config
│   ├── modules/
│   │   ├── vpc/            # VPC module
│   │   │   ├── main.tf
│   │   │   ├── variables.tf
│   │   │   └── outputs.tf
│   │   ├── eks/            # EKS module
│   │   │   ├── main.tf
│   │   │   ├── variables.tf
│   │   │   └── outputs.tf
│   │   └── jenkins/        # Jenkins module
│   │       ├── main.tf
│   │       ├── variables.tf
│   │       └── outputs.tf
├── app/
│   ├── crm-api/            # Node.js API
│   │   ├── Dockerfile
│   │   ├── server.js
│   │   └── package.json
│   ├── crm-ui/             # React UI
│   │   ├── Dockerfile
│   │   ├── src/App.js
│   │   ├── src/index.js
│   │   └── package.json
│   ├── crm-analytics/      # Python analytics
│   │   ├── Dockerfile
│   │   ├── app.py
│   │   └── requirements.txt
├── jenkins/
│   ├── Jenkinsfile         # Pipeline definition
│   └── setup-jenkins.sh    # Jenkins setup script
├── .github/
│   ├── workflows/
│   │   └── terraform.yml  # GitHub Actions for PR validation
├── .gitignore              # Ignore files
└── README.md               # Setup instructions
```

---

 **Pre-Setup**:
   - Create S3 bucket and DynamoDB table for state (see `README.md`).
   - Replace `<your-username>` in `Jenkinsfile` and `README.md`.
   - Update ECR registry in `Jenkinsfile` (`866934333672` → your AWS account ID).

**Deploy Terraform**:
   - Run `terraform init` and `apply` as per `README.md`.
   - Takes ~15-20 minutes for VPCs, EKS, and Jenkins.

**Configure Jenkins**:
   - SSH into Jenkins EC2, install Docker CLI if missing.
   - Set up pipeline, trigger on `dev` branch push.

**Test**:
   - Push to `dev` → Jenkins builds Docker images, applies Terraform.
   - Verify EKS clusters (`kubectl get nodes`) and ECR repos.

---

### Best Practices Implemented
- **Modules**: Reusable VPC, EKS, Jenkins configs.
- **State**: S3 with DynamoDB locking, encrypted.
- **Workspaces**: `dev-us`, `prod-us` isolation.
- **Governance**: GitHub Actions validates Terraform.
- **Security**: IAM roles, no public exposure beyond Jenkins.

