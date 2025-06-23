# DevSecOps AWS CLI Tools: Planning Document

This document outlines a plan to build 6 handy, installable CLI tools for day-to-day DevSecOps activities in AWS. Each tool is designed to automate, secure, and streamline common workflows for experienced DevSecOps engineers, and will include automation to suggest best practices based on usage or findings.

---

## 1. **Secrex** (aws-secret-scanner)
**Purpose:** Scan AWS resources (S3, EC2 user data, Lambda env vars, CodeCommit, etc.) for exposed secrets and credentials.

**Key Features:**
- Scan S3 buckets for files containing secrets (API keys, passwords, tokens)
- Check EC2 user data and Lambda environment variables for sensitive data
- Integrate with Git repositories (CodeCommit) for secret detection
- Output findings in JSON, CSV, or human-readable format
- Optional Slack/email alert integration
- **Automated Best Practices:** After each scan, suggest remediation steps and best practices (e.g., rotate keys, use Parameter Store, enable encryption) based on findings.

**Implementation Plan:**
- Use boto3 for AWS resource access
- Use regex and entropy checks for secret detection
- Package as a pip-installable CLI tool
- Add config for resource scope and alerting

---

## 2. **IAMply** (aws-iam-audit)
**Purpose:** Audit AWS IAM users, roles, and policies for security risks and best practice violations.

**Key Features:**
- List users with console access, inactive users, and unused credentials
- Detect overly permissive policies (wildcards, admin access)
- Highlight missing MFA, password policy issues
- Generate compliance reports (CSV/JSON)
- Suggest remediations
- **Automated Best Practices:** Provide actionable best practice recommendations (e.g., enforce MFA, remove unused users, restrict wildcards) based on audit results.

**Implementation Plan:**
- Use boto3 to fetch IAM data
- Implement rules for best practices (CIS, AWS Well-Architected)
- CLI output and export options
- Optionally, integrate with ticketing systems (Jira, ServiceNow)

---

## 3. **S3ntry** (aws-s3-bucket-checker)
**Purpose:** Quickly check S3 buckets for public access, misconfigurations, and compliance with security policies.

**Key Features:**
- List all buckets and their public/private status
- Detect open permissions, public ACLs, and policy issues
- Check for encryption, versioning, and logging
- Export findings and remediation steps
- **Automated Best Practices:** Suggest S3 security best practices (e.g., block public access, enable default encryption, enable versioning) based on scan results.

**Implementation Plan:**
- Use boto3 to enumerate and analyze S3 buckets
- Implement checks for common misconfigurations
- CLI with color-coded output and export options

---

## 4. **Costlyzer** (aws-cost-quickview)
**Purpose:** Provide a fast, terminal-based summary of AWS cost and usage, with breakdowns by service, tag, or account.

**Key Features:**
- Show current and historical spend (daily, monthly)
- Breakdown by service, region, or tag
- Detect cost spikes and anomalies
- Export reports for sharing
- **Automated Best Practices:** Suggest cost optimization best practices (e.g., rightsizing, reserved instances, unused resources) based on usage patterns.

**Implementation Plan:**
- Use boto3 (Cost Explorer API)
- Implement CLI with summary and detailed views
- Optional: Alert on cost anomalies

---

## 5. **SecuTide** (aws-security-group-tidy)
**Purpose:** Analyze and clean up unused or risky security group rules across AWS accounts.

**Key Features:**
- List all security groups and their rules
- Detect unused groups and overly permissive rules (0.0.0.0/0, open ports)
- Suggest or automate cleanup actions
- Export before/after reports
- **Automated Best Practices:** Recommend security group best practices (e.g., least privilege, remove unused groups, restrict open ports) based on findings.

**Implementation Plan:**
- Use boto3 to fetch and analyze security groups
- Implement logic for identifying risks and unused resources
- CLI with dry-run and apply modes

---

## 6. **Profilyze** (aws-profile-manager)
**Purpose:** Create, update, and manage multiple AWS CLI profiles directly from the terminal, making it easy to switch between accounts and roles securely.

**Key Features:**
- Create new AWS profiles interactively (access key, secret, region, MFA)
- List, update, and delete existing profiles
- Easily switch default profile for terminal sessions
- Validate credentials and test connectivity
- Securely store and rotate credentials
- **Automated Best Practices:** Suggest best practices for profile management (e.g., enable MFA, avoid root credentials, rotate keys regularly) and alert on risky configurations.

**Implementation Plan:**
- Use Python (Click or Typer) for CLI
- Read/write to AWS credentials and config files
- Integrate with AWS STS for role assumption and MFA
- Provide clear prompts and validation

---

*Each tool will be developed as a standalone, installable Python CLI (using Click or Typer), with clear documentation and extensibility for future enhancements. All tools will include automation to suggest best practices based on real-time usage and findings.* 