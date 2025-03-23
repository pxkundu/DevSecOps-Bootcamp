## Week 4, Day 2: Advanced Terraform

### Overview
Day 2 advances your Terraform skills to handle enterprise-scale infrastructure, focusing on modularity, parameterization, and state management. You’ll enhance the static website project by modularizing the S3 and CloudFront setup, adding multi-environment support (e.g., `dev`, `staging`), and securing state with a remote backend. These skills are critical for the Week 4 capstone—a Global Supply Chain Management System—and reflect real-world DevOps demands in companies like Amazon or Walmart.

### Learning Objectives
- Master Terraform modules for reusable, maintainable code.
- Use variables and outputs for flexible configurations.
- Implement remote state management with S3 and DynamoDB.
- Leverage workspaces for multi-environment deployments.
- Apply dynamic resource creation with `count` and `for_each`.

### Prerequisites
- Day 1’s Terraform setup (`StaticWebsiteTerraformJenkins/terraform/` with S3 and Jenkins).
- AWS CLI configured, Terraform installed.
- Basic understanding of Day 1’s `main.tf` (S3, CloudFront).

### Time Allocation
- **Theory**: 1.5 hours
- **Practical**: 1.5 hours
- **Total**: 3 hours

---

### Theoretical Explanation

#### Key Concepts & Keywords
1. **Module**:
   - **Definition**: A reusable, encapsulated set of Terraform resources stored in a separate directory (e.g., `modules/s3`).
   - **Purpose**: Promotes DRY (Don’t Repeat Yourself) principles, simplifying complex configs.
   - **Structure**: Contains `main.tf`, `variables.tf`, `outputs.tf`.
   - **Example**: `module "s3" { source = "./modules/s3" }`.

2. **Variables**:
   - **Definition**: Parameterized inputs to customize Terraform configs (e.g., `variable "bucket_name" {}`).
   - **Types**: String, number, list, map; supports defaults and validation.
   - **Usage**: Passed via CLI (`-var`), `terraform.tfvars`, or environment vars (`TF_VAR_`).
   - **Why**: Enables flexibility without hardcoding (e.g., `var.region`).

3. **Outputs**:
   - **Definition**: Values exported after `terraform apply` (e.g., `output "bucket_url" {}`).
   - **Purpose**: Shares resource attributes (e.g., S3 URL) for use elsewhere or documentation.
   - **Scope**: Available at root or module level.

4. **Remote Backend**:
   - **Definition**: Stores `terraform.tfstate` externally (e.g., S3 with DynamoDB locking) instead of locally.
   - **Components**: 
     - **S3**: Hosts state file.
     - **DynamoDB**: Provides state locking and consistency.
   - **Why**: Enables team collaboration, prevents state conflicts, and secures sensitive data.

5. **Workspace**:
   - **Definition**: A Terraform feature to manage multiple environments (e.g., `dev`, `prod`) within one config.
   - **Command**: `terraform workspace new dev`, `terraform workspace select prod`.
   - **State**: Separate `.tfstate` files per workspace (e.g., `terraform.tfstate.d/dev`).
   - **Why**: Simplifies multi-env deployments without duplicating code.

6. **Count/Meta-Arguments**:
   - **Definition**: Creates multiple instances of a resource dynamically (e.g., `count = 2`).
   - **Variants**: 
     - `count`: Numeric iteration.
     - `for_each`: Iterates over maps/sets.
   - **Example**: `resource "aws_instance" "servers" { count = 3 }`.

7. **Drift**:
   - **Definition**: When actual infrastructure deviates from Terraform state (e.g., manual AWS Console changes).
   - **Detection**: `terraform plan` shows discrepancies.
   - **Resolution**: `terraform apply` re-aligns or `terraform import` syncs existing resources.

#### Why Advanced Terraform Matters
- **Scalability**: Modules and dynamic resources handle 100s of resources efficiently.
- **Collaboration**: Remote backends ensure team sync and state integrity.
- **Flexibility**: Variables and workspaces support multi-env deployments.
- **Maintainability**: Reduces code duplication and simplifies updates.

#### Best Practices
- Modularize reusable components (e.g., S3, VPC).
- Use remote backends for production (S3 + DynamoDB).
- Define variables with defaults and descriptions.
- Version state files (S3 versioning).
- Avoid drift with strict IaC governance.

---

### Practical Use Cases & Real-World Applications

#### Practical Activity Plan
- **Objective**: Enhance the static website project with advanced Terraform features.
- **Setup**: Build on `StaticWebsiteTerraformJenkins/terraform/` from Day 1.
- **Tasks**:
  1. **Modularize S3**:
     - Move S3 resources to `modules/s3/`.
     - Call module in `main.tf`.
  2. **Add Variables & Outputs**:
     - Parameterize `bucket_name`, `region`.
     - Output CloudFront URL and Jenkins IP.
  3. **Configure Remote Backend**:
     - Use S3 bucket and DynamoDB table for state.
  4. **Set Up Workspaces**:
     - Create `dev` and `staging` workspaces.
  5. **Dynamic Resources**:
     - Deploy 2 Jenkins instances with `count`.
- **Outcome**: A modular, multi-env Terraform setup with secure state management.

#### Real-World Use Case 1: E-Commerce Multi-Environment Deployment
- **Scenario**: An e-commerce company (e.g., Shopify) deploys a static storefront across `dev`, `staging`, and `prod`.
- **Context**: Each environment needs an S3 bucket and CloudFront, with consistent configs but isolated resources.
- **Theoretical Application**:
  - **Module**: `modules/static-site` defines S3 and CloudFront.
  - **Variables**: `var.env` (e.g., `dev`) prefixes bucket names.
  - **Workspaces**: `dev`, `staging`, `prod` with separate state files.
  - **Outputs**: Returns CloudFront URLs per env.
- **Practical Workflow**:
  - `main.tf`: `module "site" { source = "./modules/static-site" env = terraform.workspace }`.
  - `terraform workspace new staging`.
  - `terraform apply`: Creates `staging-my-static-website-2025`.
  - Outcome: Isolated `dev` and `staging` sites, accessible via unique CloudFront URLs.
- **DevOps Impact**: 
  - Rapid env setup without code changes.
  - Test features in `staging` before `prod` rollout.

#### Real-World Use Case 2: Global Media CDN Infrastructure
- **Scenario**: A media company (e.g., Netflix) provisions S3 buckets and CloudFront in multiple regions.
- **Context**: Content delivery requires buckets in `us-east-1`, `eu-west-1`, and `ap-southeast-1` for low latency.
- **Theoretical Application**:
  - **Module**: `modules/cdn` for S3 + CloudFront.
  - **For_Each**: Iterates over regions (`{ "us-east-1" = "use1", "eu-west-1" = "euw1" }`).
  - **Remote Backend**: S3 bucket (`media-tf-state`) with DynamoDB (`tf-lock`).
- **Practical Workflow**:
  - `main.tf`: `module "cdn" { for_each = var.regions source = "./modules/cdn" }`.
  - `terraform init -backend-config="bucket=media-tf-state"`.
  - `terraform apply`: Deploys 3 S3 buckets and CloudFront distros.
  - Outcome: Global CDN network, state synced across teams.
- **DevOps Impact**: 
  - Scales content delivery with minimal code.
  - Team-safe state management avoids conflicts.

#### Real-World Use Case 3: Jenkins Cluster Expansion
- **Scenario**: Your static website project needs a Jenkins cluster for parallel builds.
- **Context**: Day 1’s single Jenkins EC2 scales to a 3-node cluster for `main`, `staging`, and PR builds.
- **Theoretical Application**:
  - **Count**: `resource "aws_instance" "jenkins" { count = 3 }`.
  - **Variables**: `var.instance_count` controls scale.
  - **Outputs**: Lists public IPs for node access.
  - **Drift**: Detects manual EC2 additions.
- **Practical Workflow**:
  - Update `jenkins.tf`: Add `count = var.instance_count`.
  - `terraform apply -var="instance_count=3"`.
  - Outcome: 3 Jenkins nodes, load-balanced builds.
- **DevOps Impact**: 
  - Speeds up CI/CD for multiple branches.
  - Detects and corrects unauthorized manual changes.

---

### Lesson Plan Details

#### Theory Session (1.5 hr)
- **Topics**:
  1. **Modules (20 min)**:
     - Why modularize? DRY, reusability.
     - Anatomy: `main.tf`, `variables.tf`, `outputs.tf`.
  2. **Variables & Outputs (30 min)**:
     - Types: String, list, map; CLI vs. `.tfvars`.
     - Outputs: Accessing post-apply (e.g., `terraform output`).
  3. **Remote Backends & Workspaces (40 min)**:
     - S3/DynamoDB setup, locking benefits.
     - Workspaces: Multi-env state management.
     - Dynamic resources: `count` vs. `for_each`, drift handling.
- **Delivery**: Slides, live demo of `terraform workspace new dev`.

#### Practical Session (1.5 hr)
- **Activity**: Enhance the static website Terraform setup.
- **Steps**:
  1. **Setup (15 min)**:
     - Navigate to `StaticWebsiteTerraformJenkins/terraform/`.
     - Create `modules/s3/` and move S3 resources.
  2. **Modularize & Parameterize (30 min)**:
     - Update `main.tf`: `module "s3" { source = "./modules/s3" bucket_name = var.bucket_name }`.
     - Add `env` variable for workspace prefix.
  3. **Execute Advanced Workflow (45 min)**:
     - Configure backend: `terraform init -backend-config="bucket=tf-state-2025"`.
     - Create workspaces: `terraform workspace new dev`.
     - Apply: `terraform apply`.
     - Verify: Check S3 bucket (`dev-my-static-website-2025`) and outputs.
- **Tools**: Terraform CLI, AWS Console for validation.
- **Outcome**: Modular S3 setup with remote state and `dev` workspace.

---

### Assessment
- **Quiz (15 min)**:
  - What’s the purpose of a Terraform module?
  - How does a remote backend improve collaboration?
  - Explain `count` vs. `for_each`.
- **Hands-On Check**: 
  - Show `terraform.tfstate` in S3.
  - List workspaces with `terraform workspace list`.

---

### Real-World Alignment
- **E-Commerce**: Amazon uses modules for S3/CloudFront across envs.
- **Media**: Disney leverages remote backends for global teams.
- **Your Project**: Prepares Jenkins for multi-env deployments.

---

### Next Steps
- **Day 3**: Kubernetes basics for website containerization.
- **Capstone**: Multi-region supply chain with these advanced features.

This Day 2 plan deepens your Terraform expertise with theory and practice, setting up a scalable, team-ready IaC foundation.