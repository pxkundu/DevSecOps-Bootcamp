## Practical Implementation Plan: Week 5 - Cost-Optimized Secure E-commerce Platform

### Project Overview
- **Objective**: Build, secure, and optimize a multi-tier e-commerce platform (web frontend, API, database, storage) on AWS, simulating a startup scaling to enterprise during a peak season (e.g., Black Friday).
- **Duration**: ~10-12 hours (can be split across days).
- **Tools**: AWS (EKS, EC2, RDS, S3, Lambda, etc.), Jenkins, SonarQube, OWASP ZAP, OPA, Karpenter, QuickSight, Graviton instances.
- **Deliverables**: Deployed platform, security report, cost optimization summary, dashboard.

### Project Scope
- **Architecture**: 
  - Web frontend (EC2/EKS), API (Lambda), database (RDS), storage (S3).
  - CI/CD pipeline (Jenkins) with security and cost controls.
- **Learning Topics Covered**: All Week 5 topics (Days 1-5) integrated into a single workflow.

---

## Implementation Steps

### Day 1: Security Fundamentals (2 hours)
- **Objective**: Establish a secure foundation for the platform.
- **Tasks**:
  1. **Secure Infrastructure Basics**:
     - Launch EC2 (`t3.medium`, Amazon Linux 2) for web frontend in `us-east-1`.
     - Enable IMDSv2: `aws ec2 modify-instance-metadata-options --instance-id <id> --http-tokens required`.
  2. **Secrets Management**:
     - Store RDS password in AWS Secrets Manager (`ecomm-secret`).
     - Configure EC2 IAM role to access Secrets Manager.
  3. **Network Security**:
     - Create VPC with private subnets, NAT Gateway, and Security Group (allow HTTP/HTTPS only).
- **Verification**: SSH to EC2 fails without IMDSv2 token; Secrets Manager retrieves password.

---

### Day 2: Security Advanced - DevSecOps Practices (2.5 hours)
- **Objective**: Harden the platform with DevSecOps security practices.
- **Tasks**:
  1. **Shift-Left Security**:
     - Set up Jenkins, add SonarQube plugin, scan `app.js`:
       ```groovy
       stage('SAST') { sh 'sonar-scanner -Dsonar.projectKey=ecomm' }
       ```
  2. **DAST**:
     - Deploy app to EC2, run OWASP ZAP: `zap-cli quick-scan http://<ec2-ip>`.
  3. **Policy as Code**:
     - Deploy EKS cluster (`eksctl create cluster --name ecomm --nodes 2`).
     - Apply OPA policy:
       ```rego
       deny[msg] { input.spec.privileged; msg = "No privileged pods" }
       ```
  4. **Threat Modeling**:
     - Document STRIDE risks (e.g., “Spoofing: Fake API calls” → JWT auth).
  5. **Secure CI/CD**:
     - Sign Docker image: `docker trust sign <ecr-repo>/ecomm:latest`.
  6. **CSPM**:
     - Enable Security Hub, fix “EKS public endpoint” finding.
  7. **Compliance Frameworks**:
     - Add Config Rule: `RDS_STORAGE_ENCRYPTED`.
- **Verification**: SonarQube flags issues, ZAP reports clean, OPA blocks privileged pods, Security Hub shows compliance.

---

### Day 3: Cost Optimization - Basics & Tools (2 hours)
- **Objective**: Apply basic cost optimization to the platform.
- **Tasks**:
  1. **AWS Cost Explorer**:
     - Analyze 7-day spend: EC2 ($5/day), RDS ($3/day).
  2. **Resource Right-Sizing**:
     - Downsize EC2 to `t3.micro` (CPU < 20%).
  3. **S3 Lifecycle Policies**:
     - Create S3 bucket (`ecomm-logs`), set policy: Transition to Glacier (30 days).
  4. **Budget Alerts**:
     - Set $5/day budget, alert at $4 via email.
  5. **Cost Allocation Tags**:
     - Tag resources: `Environment=Prod`.
  6. **Reserved Instances**:
     - Simulate 1-year RI for `t3.micro` ($100 savings).
  7. **AWS Trusted Advisor**:
     - Terminate idle EC2 if flagged.
- **Verification**: Spend drops to $4/day, email alert triggers at $4, tags visible in Cost Explorer.

---

### Day 4: Cost Optimization - Advanced Tracking & Automation (2.5 hours)
- **Objective**: Implement advanced tracking and automation.
- **Tasks**:
  1. **AWS Cost Anomaly Detection**:
     - Enable, detect $2/day EC2 spike.
  2. **Cost Automation with Lambda**:
     - Create Lambda to stop EC2 at 10 PM:
       ```python
       import boto3
       def lambda_handler(event, context):
           ec2 = boto3.client('ec2')
           ec2.stop_instances(InstanceIds=['<id>'])
       ```
     - Trigger via CloudWatch Schedule.
  3. **Spot Instances**:
     - Launch Spot `t3.micro` for batch jobs ($0.003/hr vs. $0.01/hr).
  4. **Cost Forecasting**:
     - Forecast next 30 days in Cost Explorer: $150 → Plan $120.
  5. **Infrastructure Cost Optimization**:
     - Use Karpenter on EKS to scale nodes dynamically.
  6. **Billing APIs**:
     - Export CUR to S3, query with Athena: `SELECT SUM(cost) WHERE service='AmazonEC2'`.
- **Verification**: Anomaly alert received, EC2 stops nightly, Spot saves 70%, forecast matches plan.

---

### Day 5: Cost Optimization - Advanced Optimization (3 hours)
- **Objective**: Apply advanced optimization techniques.
- **Tasks**:
  1. **Advanced Right-Sizing with Compute Optimizer**:
     - Enable Compute Optimizer, downsize RDS to `db.t3.medium`.
  2. **Savings Plans Deep Dive**:
     - Commit $1/hour to 1-year Compute Savings Plan for EC2/Lambda.
  3. **Multi-Account Cost Management**:
     - Create AWS Organization, add second account, enforce tags via SCP.
  4. **Advanced S3 Cost Optimization**:
     - Enable Intelligent-Tiering on `ecomm-logs`.
  5. **Auto-Scaling Cost Efficiency**:
     - Configure Karpenter to scale EKS nodes from 2 to 1 off-peak.
  6. **Cost Optimization Dashboards**:
     - Set up QuickSight with CUR data, visualize daily spend.
  7. **Graviton-Based Cost Savings**:
     - Migrate EC2 to `t4g.micro` (Graviton2).
- **Verification**: Spend drops to $3/day, QuickSight shows savings, Graviton reduces costs 20%.

---

## Final Validation & Deliverables (1 hour)
- **Validation**:
  - **Security**: Run ZAP (no vulnerabilities), check Security Hub (compliant).
  - **Cost**: Cost Explorer shows $3/day (from $8/day), 60% savings.
  - **Functionality**: Web app accessible, API returns data, logs stored in S3.
- **Deliverables**:
  - **Code**: Jenkinsfile, Lambda script, EKS manifests, CUR queries.
  - **Security Report**: `week5-security.md` (SAST/DAST results, compliance status).
  - **Cost Summary**: `week5-cost.md` (before: $8/day, after: $3/day, $150/month saved).
  - **Dashboard**: QuickSight screenshot of spend trends.

---

## Learning Topics Verified
- **Day 1**: Secure Infra, Secrets, Network Security.
- **Day 2**: Shift-Left, DAST, Policy as Code, Threat Modeling, Secure CI/CD, CSPM, Compliance.
- **Day 3**: Cost Explorer, Right-Sizing, S3 Lifecycle, Budget Alerts, Tags, RIs, Trusted Advisor.
- **Day 4**: Anomaly Detection, Lambda Automation, Spot Instances, Forecasting, Infra Optimization, Billing APIs.
- **Day 5**: Compute Optimizer, Savings Plans, Multi-Account, Advanced S3, Auto-Scaling, Dashboards, Graviton.

---

## Why This Project Matters
- **Simplicity**: A basic e-commerce app (web, API, DB) is easy to deploy yet mirrors real-world complexity.
- **Significance**: Integrates security and cost optimization, scaling from $8/day to $3/day, saving $1,800/year—significant for a startup or enterprise team.
- **Real-World Alignment**: Reflects Amazon’s Black Friday prep or Netflix’s encoding pipeline, preparing learners for Fortune 100 challenges.
- **DevSecOps Focus**: Embeds security in CI/CD, automates cost control, and optimizes at scale.

