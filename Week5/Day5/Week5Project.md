## Project Plan: Simple Inventory Management System with AWS Savings Plans

### Project Overview
- **Objective**: Deploy a basic inventory management system on AWS and optimize costs using AWS Savings Plans.
- **Duration**: ~3-4 hours.
- **Focus**: Cost optimization with Savings Plans (Week 5, Day 5 topic).
- **Tools**: Terraform, AWS (EC2, S3, Cost Explorer, Savings Plans).
- **Deliverables**: Deployed system, Terraform code, cost savings report.

### Project Scope
- **Architecture**: 
  - EC2 instance (web frontend) running a Node.js app.
  - S3 bucket for inventory logs.
- **Cost Optimization Feature**: AWS Savings Plans (Compute Savings Plan) to reduce EC2 costs.
- **Scenario**: A small retail app managing 1,000 products, aiming to save costs as it scales.

### Steps
1. **Setup Infrastructure with Terraform** (~1 hour):
   - Deploy EC2 and S3 using Terraform.
2. **Analyze Initial Costs** (~30 min):
   - Use Cost Explorer to check On-Demand pricing.
3. **Apply Savings Plans** (~1 hour):
   - Purchase a Compute Savings Plan via AWS Console.
   - Verify application to EC2.
4. **Validate Savings** (~30 min):
   - Compare costs pre- and post-Savings Plan in Cost Explorer.
5. **Cleanup** (~30 min):
   - Destroy resources with Terraform.

---

## Practical Implementation: Inventory Management System with AWS Savings Plans

### Prerequisites
- AWS account with IAM permissions (EC2, S3, Cost Explorer, Savings Plans).
- Terraform installed locally.
- Basic knowledge of AWS Console and Terraform.

### Step 1: Setup Infrastructure with Terraform
- **Objective**: Deploy a minimal system to simulate inventory management.
- **Terraform Code** (`main.tf`):
  ```hcl
  provider "aws" {
    region = "us-east-1"
  }

  # VPC and Subnet
  resource "aws_vpc" "inventory_vpc" {
    cidr_block = "10.0.0.0/16"
    tags       = { Name = "inventory-vpc" }
  }

  resource "aws_subnet" "inventory_subnet" {
    vpc_id     = aws_vpc.inventory_vpc.id
    cidr_block = "10.0.1.0/24"
    tags       = { Name = "inventory-subnet" }
  }

  # Security Group
  resource "aws_security_group" "inventory_sg" {
    vpc_id = aws_vpc.inventory_vpc.id
    ingress {
      from_port   = 80
      to_port     = 80
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    }
    egress {
      from_port   = 0
      to_port     = 0
      protocol    = "-1"
      cidr_blocks = ["0.0.0.0/0"]
    }
    tags = { Name = "inventory-sg" }
  }

  # EC2 Instance
  resource "aws_instance" "inventory_web" {
    ami           = "ami-0c55b159cbfafe1f0" # Amazon Linux 2
    instance_type = "t3.micro"
    subnet_id     = aws_subnet.inventory_subnet.id
    security_groups = [aws_security_group.inventory_sg.name]
    user_data     = <<-EOF
                    #!/bin/bash
                    yum update -y
                    yum install -y nodejs
                    echo 'console.log("Inventory Web Running")' > app.js
                    node app.js &
                    EOF
    tags          = { Name = "inventory-web", Environment = "Prod" }
  }

  # S3 Bucket
  resource "aws_s3_bucket" "inventory_logs" {
    bucket = "inventory-logs-${random_string.suffix.result}"
    tags   = { Name = "inventory-logs", Environment = "Prod" }
  }

  resource "random_string" "suffix" {
    length  = 8
    special = false
  }

  output "ec2_public_ip" {
    value = aws_instance.inventory_web.public_ip
  }
  ```
- **Execution**:
  1. Save as `main.tf`.
  2. Run `terraform init`, `terraform apply -auto-approve`.
  3. Wait ~5-10 minutes for EC2 to launch.
- **Verification**: Access `http://<ec2-public-ip>` → See "Inventory Web Running" in logs.

### Step 2: Analyze Initial Costs
- **Objective**: Establish baseline On-Demand costs.
- **Tasks**:
  1. AWS Console > Cost Explorer > Daily Costs.
  2. Filter: “EC2 - Other”, Last 1 day → ~$0.01/hour ($0.24/day) for `t3.micro`.
  3. Note S3 costs (~$0.01/day for minimal usage).
- **Verification**: Baseline cost ~$0.25/day ($7.50/month).

### Step 3: Apply AWS Savings Plans
- **Objective**: Reduce EC2 costs with a Compute Savings Plan.
- **Tasks**:
  1. AWS Console > Savings Plans > Purchase Compute Savings Plan.
     - Commitment: $0.005/hour (~$3.60/month).
     - Term: 1 year, No Upfront payment.
     - Confirm purchase (mock if budget-limited, note savings estimate).
  2. Wait ~24 hours for Savings Plan to apply (or simulate immediate effect for learning).
  3. Tag EC2 for tracking: `aws ec2 create-tags --resources <instance-id> --tags Key=CostCenter,Value=Inventory`.
- **Verification**: Savings Plan dashboard shows active commitment, EC2 tagged.

### Step 4: Validate Savings
- **Objective**: Confirm cost reduction with Savings Plans.
- **Tasks**:
  1. Cost Explorer > Daily Costs > Filter: “EC2 - Other”, Group by: “Usage Type”.
  2. Post-Savings Plan: ~$0.007/hour ($0.17/day) vs. $0.01/hour On-Demand.
  3. Calculate savings: $0.24/day → $0.17/day (~30% reduction).
- **Verification**: Monthly cost drops from $7.50 to ~$5.10, saving ~$2.40/month ($28.80/year).

### Step 5: Cleanup
- **Objective**: Avoid ongoing costs.
- **Tasks**:
  1. Run `terraform destroy -auto-approve`.
  2. Cancel Savings Plan if real (optional, for learning purposes).
- **Verification**: Resources deleted, Cost Explorer shows $0 spend.

---

## Deliverables
- **Terraform Code**: `main.tf` with EC2, S3, and tags.
- **Cost Savings Report**: `week5-savings.md`:
  ```
  # Inventory System Cost Optimization
  - Baseline: $0.25/day ($7.50/month)
  - With Savings Plan: $0.17/day ($5.10/month)
  - Savings: $0.08/day ($2.40/month, $28.80/year, ~30%)
  ```
- **Screenshot**: Cost Explorer before/after Savings Plan.

---

## Why This Project Matters
- **Simplicity**: A single EC2 and S3 setup is easy to deploy and manage, focusing on one key feature.
- **Significance**: Savings Plans reduce costs by ~30% ($28.80/year for one instance, scalable to $100K+ for fleets), impactful for any business.
- **Cost Optimization Focus**: Verifies Week 5, Day 5’s Savings Plans topic, a top-tier DevSecOps cost tool.
- **Terraform & AWS**: Aligns with modern IaC practices, preparing learners for real-world deployments.

This project keeps it simple while delivering significant cost savings, integrating Terraform and AWS for a practical DevSecOps use case.