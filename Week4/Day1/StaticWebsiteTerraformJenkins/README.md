# Static Website with Terraform and Jenkins

This project automates an AWS infrastructure to host a ReactJS static website on S3 with CloudFront, using Terraform for IaC and Jenkins for CI/CD from GitHub.

### Project Overview
- **Goal**: Host a ReactJS static site on S3 with a deployment pipeline.
- **Components**:
  - **AWS Infrastructure**: S3 bucket (static hosting), CloudFront (CDN), IAM roles, Route 53 (optional DNS).
  - **ReactJS App**: Simple static site built and uploaded to S3.
  - **Jenkins Pipeline**: Automates build and deployment from GitHub.
  - **Terraform**: Provisions all AWS resources and Jenkins setup.
- **Best Practices**:
  - S3: Versioning, public access blocked, static hosting enabled.
  - Security: IAM least privilege, CloudFront with OAI (Origin Access Identity).
  - Automation: No manual AWS steps; all via Terraform and Jenkins.

---

## Prerequisites
- AWS CLI configured (`aws configure`).
- EC2 key pair in `us-east-1` (e.g., `my-key`).
- GitHub repo with this code (`<your-username>/StaticWebsiteTerraformJenkins`).
- Terraform installed (`brew install terraform`).

## Setup Instructions
1. **Initialize Terraform**
   ```bash
   cd terraform
   terraform init

---

### Project Structure
```
StaticWebsiteTerraformJenkins/
├── terraform/
│   ├── main.tf              # Main Terraform config (S3, CloudFront, IAM)
│   ├── variables.tf         # Input variables
│   ├── outputs.tf           # Output values (e.g., S3 URL, CloudFront domain)
│   ├── jenkins.tf           # Jenkins EC2 setup
│   └── provider.tf          # AWS provider config
├── react-app/
│   ├── src/
│   │   ├── App.js          # Simple React component
│   │   ├── index.js        # React entry point
│   │   └── App.css         # Basic styling
│   ├── package.json        # Node.js dependencies
│   └── .gitignore          # Ignore node_modules
├── jenkins/
│   ├── Jenkinsfile         # Pipeline definition
│   └── setup-jenkins.sh    # Jenkins initialization script
├── .gitignore              # Project-wide ignore file
└── README.md               # Setup instructions
```

---

**Deploy Infrastructure**
   ```bash
   terraform apply -var="bucket_name=my-static-website-2025" -var="key_name=my-key"
   ```
   - Confirm with `yes` after reviewing the plan.

**Configure Jenkins**
   - Access: `http://<JenkinsPublicIP>:8080` (from outputs).
   - Initial Password: `ssh -i my-key.pem ec2-user@<JenkinsPublicIP> "sudo cat /var/lib/jenkins/secrets/initialAdminPassword"`.
   - Install Plugins: `Git`, `NodeJS`, `Pipeline`.
   - Add AWS Credentials: `Manage Credentials > Global > AWS`.
   - Create Pipeline: Point to GitHub repo, use `Jenkinsfile`.

## Usage
- **Branches**:
  - `main`: Deploys to `s3://my-static-website-2025/main/`.
  - `staging`: Deploys to `s3://my-static-website-2025/staging/`.
- **Access**: Use CloudFront URL (`outputs.cloudfront_domain`).

## Cleanup
```bash
terraform destroy
```

## Notes
- Update `bucket_name` to be globally unique.
- Secure Jenkins SG (`0.0.0.0/0` → your IP).
  
---

### Best Practices Implemented
- **S3**: Versioning enabled, public access blocked, policy restricts to CloudFront.
- **CloudFront**: HTTPS enforced, OAI secures S3 access, caching optimized.
- **IAM**: Least privilege for Jenkins (S3-only permissions).
- **Jenkins**: Automated builds, branch-specific deployments (`main`, `staging`).
- **Terraform**: Modular (separate files), outputs for usability, no manual AWS steps.
