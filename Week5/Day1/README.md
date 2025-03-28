## Week 5, Day 1: Security Basics & Encryption
**Objective**: Master foundational and advanced security practices for AWS, focusing on encryption and access control, with a 7-8 hour learning schedule. 

This plan covers the key learning topics identified for Day 1, providing both **theoretical keyword explanations** (definitions, context, and importance in DevSecOps) and **practical use cases** (real-world applications with examples from Fortune 100 companies or similar contexts). The content is designed to be informative, actionable, and aligned with industry-standard DevSecOps implementations, offering a deep dive into security fundamentals for intermediate AWS DevOps and Cloud Engineers.

- **Duration**: ~7-8 hours.
- **Structure**: Theoretical explanations (~50%) + Practical use cases (~50%).

---

### Key Learning Topics

#### 1. Encryption Fundamentals
- **Theoretical Keyword Explanation**:
  - **Definition**: Encryption is the process of encoding data to prevent unauthorized access, ensuring confidentiality at rest (stored data) and in transit (data moving between systems). In AWS, this involves AES-256 (Advanced Encryption Standard with 256-bit keys) for symmetric encryption and TLS (Transport Layer Security) for secure communication.
  - **Context**: Encryption is a cornerstone of DevSecOps, mandated by compliance frameworks like GDPR, HIPAA, and PCI DSS. It protects sensitive data (e.g., customer PII, financial records) from breaches.
  - **Importance**: Prevents data leaks (e.g., 2017 Equifax breach due to unencrypted data), ensures auditability, and aligns with the AWS Well-Architected Security Pillar’s “protect data” principle.
  - **AWS Tools**: 
    - **S3**: Default encryption with AES-256 or customer-managed KMS keys.
    - **RDS**: Storage encryption and TLS for connections.
    - **EKS**: Encrypting pod secrets and etcd data.
- **Practical Use Cases**:
  - **Amazon’s S3 Encryption**: Amazon encrypts S3 buckets storing customer data (e.g., Prime subscription details) with AES-256 by default, using KMS for key rotation. A DevSecOps team might configure this via Terraform:
    ```hcl
    resource "aws_s3_bucket" "data" {
      bucket = "customer-data"
      server_side_encryption_configuration {
        rule {
          apply_server_side_encryption_by_default {
            sse_algorithm = "AES256"
          }
        }
      }
    }
    ```
  - **Walmart’s RDS Security**: Walmart encrypts RDS instances for its e-commerce database (e.g., order history) with AES-256 at rest and enforces TLS for in-transit data, ensuring PCI DSS compliance during peak sales (e.g., Black Friday).

---

#### 2. IAM Best Practices
- **Theoretical Keyword Explanation**:
  - **Definition**: IAM (Identity and Access Management) governs who (users, services) can do what (actions) on which AWS resources. Best practices include least privilege, role assumption, and Multi-Factor Authentication (MFA).
  - **Context**: IAM is critical in DevSecOps to enforce the principle of least privilege—granting only the permissions needed for a task—reducing the attack surface (e.g., NIST SP 800-53 AC-6).
  - **Importance**: Prevents privilege escalation (e.g., 2019 Capital One breach via over-privileged IAM role) and ensures secure CI/CD pipelines (e.g., Jenkins accessing ECR).
  - **AWS Tools**: 
    - Policies (e.g., `ecr:PutImage` only), roles for EC2/EKS, MFA on root and IAM users.
- **Practical Use Cases**:
  - **Google’s IAM for GKE**: Google uses IAM roles with least privilege for Kubernetes Engine (GKE), restricting service accounts to specific APIs (e.g., storage read-only). A DevSecOps engineer might replicate this in AWS EKS:
    ```hcl
    resource "aws_iam_role" "eks_worker" {
      name = "eks-worker-role"
      assume_role_policy = jsonencode({
        Statement = [{
          Effect = "Allow"
          Principal = { Service = "ec2.amazonaws.com" }
          Action = "sts:AssumeRole"
        }]
      })
    }
    resource "aws_iam_role_policy" "eks_policy" {
      role = aws_iam_role.eks_worker.name
      policy = jsonencode({
        Statement = [{
          Effect = "Allow"
          Action = ["eks:DescribeCluster"]
          Resource = "*"
        }]
      })
    }
    ```
  - **Amazon’s MFA**: Amazon mandates MFA for all IAM users accessing production environments, a practice enforced via IAM conditions to block logins without it—critical for DevSecOps teams managing AWS accounts.

---

#### 3. S3 Security
- **Theoretical Keyword Explanation**:
  - **Definition**: S3 security involves protecting bucket data with policies, access controls, and versioning. Key features include bucket policies, public access blocks, and lifecycle rules for compliance.
  - **Context**: S3 is a common attack vector (e.g., exposed buckets in 2020 UpGuard findings); DevSecOps requires proactive hardening to meet standards like CIS AWS Benchmarks.
  - **Importance**: Ensures data confidentiality, prevents accidental leaks (e.g., public read access), and supports audit trails via versioning.
  - **AWS Tools**: 
    - Bucket policies, `aws_s3_bucket_public_access_block`, versioning for rollback.
- **Practical Use Cases**:
  - **Netflix’s S3 Hardening**: Netflix secures S3 buckets for video metadata with strict policies and blocks public access:
    ```hcl
    resource "aws_s3_bucket" "metadata" {
      bucket = "video-metadata"
    }
    resource "aws_s3_bucket_public_access_block" "metadata" {
      bucket = aws_s3_bucket.metadata.id
      block_public_acls = true
      block_public_policy = true
    }
    ```
    - A DevSecOps team remediates exposed buckets post-audit, ensuring no public leaks during content launches.
  - **Walmart’s Versioning**: Walmart enables S3 versioning for supply chain logs, allowing rollback after accidental deletions—a DevSecOps practice for audit compliance during supplier audits.

---

#### 4. RDS Security
- **Theoretical Keyword Explanation**:
  - **Definition**: RDS security protects relational databases with encryption, secure configurations, and network isolation. Features include storage encryption, TLS, and parameter groups.
  - **Context**: Databases are prime targets (e.g., 2018 Marriott breach); DevSecOps emphasizes encryption and access control to meet GDPR/HIPAA.
  - **Importance**: Safeguards customer data (e.g., orders, PII), ensures compliance, and prevents downtime from misconfiguration.
  - **AWS Tools**: 
    - `storage_encrypted`, TLS certificates, security groups, parameter groups for hardening (e.g., disable `log_bin_trust_function_creators`).
- **Practical Use Cases**:
  - **Target’s RDS Encryption**: Target encrypts RDS for its POS system with AES-256 and enforces TLS, configured via:
    ```hcl
    resource "aws_db_instance" "pos_db" {
      identifier = "pos-db"
      engine = "mysql"
      instance_class = "db.t3.medium"
      storage_encrypted = true
      parameter_group_name = aws_db_parameter_group.secure.name
    }
    resource "aws_db_parameter_group" "secure" {
      family = "mysql8.0"
      parameter { name = "require_secure_transport" value = "ON" }
    }
    ```
    - DevSecOps ensures PCI DSS compliance for payment data.
  - **Amazon’s Multi-Layer Security**: Amazon uses RDS parameter groups to disable insecure settings, a practice DevSecOps teams adopt to lock down production databases.

---

#### 5. Zero Trust Principles
- **Theoretical Keyword Explanation**:
  - **Definition**: Zero Trust assumes no entity (inside or outside the network) is trusted by default, requiring continuous verification. In AWS, this means IAM, VPC, and resource-level checks.
  - **Context**: A DevSecOps shift from perimeter-based security (e.g., Google’s BeyondCorp), critical for cloud-native apps.
  - **Importance**: Mitigates insider threats and lateral movement (e.g., 2021 SolarWinds attack), ensuring robust defense-in-depth.
  - **AWS Tools**: 
    - IAM conditions (e.g., `aws:SourceIp`), VPC endpoints, Security Hub for posture checks.
- **Practical Use Cases**:
  - **Google’s Zero Trust**: Google applies Zero Trust to GKE with network policies and service account restrictions. In AWS, a DevSecOps engineer might:
    ```hcl
    resource "aws_vpc_endpoint" "s3" {
      vpc_id = aws_vpc.main.id
      service_name = "com.amazonaws.us-east-1.s3"
      policy = jsonencode({
        Statement = [{
          Effect = "Allow"
          Principal = { AWS = "arn:aws:iam::<account>:role/eks-worker" }
          Action = "s3:GetObject"
          Resource = "arn:aws:s3:::metadata/*"
        }]
      })
    }
    ```
    - Ensures only verified pods access S3.
  - **Microsoft’s Azure AD**: Microsoft’s Zero Trust with conditional access inspires AWS IAM conditions (e.g., MFA required), a DevSecOps staple for production access.

---

#### 6. Secrets Management
- **Theoretical Keyword Explanation**:
  - **Definition**: Secrets management securely stores and rotates sensitive data (e.g., API keys, passwords) using tools like AWS Secrets Manager or HashiCorp Vault.
  - **Context**: A DevSecOps must to avoid hardcoding secrets (e.g., 2019 Uber breach via GitHub leak), supporting compliance (e.g., SOC 2).
  - **Importance**: Reduces credential exposure, automates rotation, and integrates with CI/CD pipelines.
  - **AWS Tools**: 
    - Secrets Manager for storage/rotation, IAM permissions for access, Kubernetes secrets integration.
- **Practical Use Cases**:
  - **Stripe’s Secrets Rotation**: Stripe uses Secrets Manager to rotate API keys for payment processing:
    ```hcl
    resource "aws_secretsmanager_secret" "api_key" {
      name = "stripe-api-key"
    }
    resource "aws_secretsmanager_secret_rotation" "api_key_rotation" {
      secret_id = aws_secretsmanager_secret.api_key.id
      rotation_lambda_arn = aws_lambda_function.rotator.arn
      rotation_rules { automatically_after_days = 30 }
    }
    ```
    - DevSecOps ensures zero downtime during rotation.
  - **Netflix’s Kubernetes Secrets**: Netflix injects secrets into EKS pods from Secrets Manager, avoiding plaintext in manifests—a DevSecOps practice for secure deployments.

---

#### 7. Container Security Basics
- **Theoretical Keyword Explanation**:
  - **Definition**: Container security protects Docker/Kubernetes workloads by scanning images, limiting privileges, and securing runtime environments.
  - **Context**: Essential in DevSecOps as containers proliferate (e.g., 2020 Docker Hub malware); aligns with CIS Docker Benchmarks.
  - **Importance**: Prevents supply chain attacks (e.g., 2021 Codecov breach), ensures secure CI/CD, and supports microservices.
  - **AWS Tools**: 
    - ECR image scanning, `USER` in Dockerfiles, Kubernetes pod security policies.
- **Practical Use Cases**:
  - **Netflix’s ECR Scanning**: Netflix scans Docker images in ECR for vulnerabilities:
    ```hcl
    resource "aws_ecr_repository" "app" {
      name = "app-repo"
      image_scanning_configuration { scan_on_push = true }
    }
    ```
    - DevSecOps rejects images with critical CVEs before deployment.
  - **Amazon’s Non-Root Containers**: Amazon runs EKS pods as non-root users (`USER 1000` in Dockerfile), a DevSecOps standard to limit container breakout risks.

---

#### 8. Real-World Use Case: Encrypting an S3 Bucket and RDS Instance for GDPR
- **Theoretical Keyword Explanation**:
  - **Definition**: A practical scenario applying encryption, IAM, and secrets management to meet GDPR’s data protection requirements (e.g., Article 32).
  - **Context**: Fortune 100 companies (e.g., retail, finance) must comply with global regulations, a DevSecOps priority.
  - **Importance**: Demonstrates end-to-end security in a compliance-driven app, integrating all Day 1 topics.
- **Practical Use Case**:
  - **Retail App (e.g., Target)**: A DevSecOps team secures a customer data pipeline:
    - **S3**: Encrypts `customer-orders` bucket with KMS, blocks public access.
    - **RDS**: Encrypts a MySQL instance with TLS and stores credentials in Secrets Manager.
    - **IAM**: Restricts access to an EKS role:
      ```hcl
      resource "aws_iam_policy" "data_access" {
        policy = jsonencode({
          Statement = [{
            Effect = "Allow"
            Action = ["s3:GetObject", "rds:DescribeDBInstances"]
            Resource = ["arn:aws:s3:::customer-orders/*", "arn:aws:rds:*:*"]
          }]
        })
      }
      ```
    - **Outcome**: GDPR-compliant data handling, audited by regulators, showcasing DevSecOps maturity.

---

## Learning Schedule (7-8 Hours)
- **Morning (3-4 hours)**:
  - Theoretical Deep Dive: Encryption Fundamentals, IAM Best Practices, S3 Security, RDS Security (slides, videos, or live discussion).
  - Practical Exploration: Review AWS Console (S3, RDS, IAM) and Fortune 100 examples (Amazon, Walmart).
- **Afternoon (4 hours)**:
  - Theoretical Deep Dive: Zero Trust, Secrets Management, Container Security, GDPR Use Case.
  - Practical Exploration: Hands-on with AWS CLI/Terraform snippets (e.g., encrypt S3, configure IAM), discuss Netflix/Stripe implementations.

---

## Why This Matters
- **Theoretical Value**: Understanding these keywords builds a DevSecOps mindset—security is proactive, not reactive.
- **Practical Impact**: Real-world use cases from Amazon, Netflix, and Walmart show how these practices scale to millions of users, preparing learners for Fortune 100 challenges.
- **DevSecOps Alignment**: Covers NIST SP 800-53, CIS Benchmarks, and AWS Well-Architected, ensuring industry-standard knowledge.
