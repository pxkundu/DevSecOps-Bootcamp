## Week 5: Security, Cost, and Troubleshooting

### Overview
- **Goal**: Build advanced skills in securing AWS environments, optimizing and automating costs, troubleshooting with modern tools, and applying these in a capstone project.
- **Duration**: 6 days, 7-8 hours per day (~42-48 hours total), with 25% time per major topic and 25% for the capstone.
- **Structure**: 
  - Days 1-2: Security (14-16 hours, ~25%).
  - Days 3-4: Cost Optimization (14-16 hours, ~25%).
  - Day 5: Troubleshooting & Monitoring Tools (7-8 hours, ~25%).
  - Day 6: Capstone Project (7-8 hours, ~25%).

---

### Day 1: Security Basics & Encryption (7-8 hours)
**Objective**: Master foundational and advanced security practices for AWS, focusing on encryption and access control.

- **Key Learning Topics**:
  - **Encryption Fundamentals**: Encryption at rest (AES-256) and in transit (TLS) for S3, RDS, and EKS, including KMS key management.
  - **IAM Best Practices**: Least privilege policies, role assumption, and MFA for AWS resources (Fortune 100 standard, e.g., Amazon’s IAM rigor).
  - **S3 Security**: Bucket policies, public access blocks, and versioning for audit compliance (e.g., PCI DSS).
  - **RDS Security**: Multi-layer encryption, parameter groups for secure configs, and snapshot encryption.
  - **Zero Trust Principles**: Implementing “never trust, always verify” with AWS IAM and network policies (e.g., Google’s BeyondCorp).
  - **Secrets Management**: AWS Secrets Manager for API keys and DB credentials, rotation policies (e.g., Stripe’s security).
  - **Container Security Basics**: Docker image scanning with ECR, avoiding root users in containers (e.g., Netflix’s practices).
  - **Real-World Use Case**: Encrypting an S3 bucket and RDS instance to meet GDPR-like requirements for a retail app.

---

### Day 2: Security Advanced - DevSecOps Practices (7-8 hours)
**Objective**: Dive into cutting-edge DevSecOps security practices used by Fortune 100 companies.

- **Key Learning Topics**:
  - **Shift-Left Security**: Static Application Security Testing (SAST) with tools like Checkmarx or SonarQube in CI/CD pipelines.
  - **Dynamic Application Security Testing (DAST)**: Using OWASP ZAP to scan running apps for vulnerabilities (e.g., Microsoft’s security).
  - **Policy as Code**: Open Policy Agent (OPA) for Kubernetes RBAC and network policies (e.g., Goldman Sachs’ compliance).
  - **Threat Modeling**: STRIDE methodology to identify risks in an EKS-based app (e.g., Amazon’s pre-launch reviews).
  - **Secure CI/CD**: Signing Docker images, securing Jenkins with RBAC, and pipeline secrets management (e.g., Walmart’s automation).
  - **Cloud Security Posture Management (CSPM)**: Using AWS Security Hub to detect misconfigurations (e.g., Salesforce’s monitoring).
  - **Compliance Frameworks**: Mapping to NIST SP 800-53, CIS Benchmarks for AWS hardening (e.g., Fortune 100 audits).
  - **Real-World Use Case**: Securing a microservices app on EKS with OPA and Security Hub for a financial services client.

---

### Day 3: Cost Optimization - Basics & Tools (7-8 hours)
**Objective**: Learn foundational cost management and introduce advanced AWS cost tools.

- **Key Learning Topics**:
  - **AWS Cost Explorer**: Analyzing spend trends, identifying high-cost services (e.g., EC2, RDS).
  - **Resource Right-Sizing**: Downsizing overprovisioned instances (e.g., `t3.micro` vs. `t2.large`) and RDS tiers.
  - **S3 Lifecycle Policies**: Transitioning to Glacier/Deep Archive for cost savings (e.g., Netflix’s archival).
  - **Budget Alerts**: Setting up AWS Budgets with thresholds and notifications for proactive cost control.
  - **Cost Allocation Tags**: Tagging resources (e.g., `Environment=Dev`) for granular cost tracking.
  - **Reserved Instances (RIs)**: Understanding RI purchasing for predictable workloads (e.g., Amazon’s savings).
  - **AWS Trusted Advisor**: Using cost optimization checks to identify idle resources.
  - **Real-World Use Case**: Reducing spend on a multi-tier app by right-sizing and tagging for a startup scaling to enterprise.

---

### Day 4: Cost Optimization - Advanced Tracking & Automation (7-8 hours)
**Objective**: Master advanced cost tracking and automation strategies for AWS environments.

- **Key Learning Topics**:
  - **AWS Cost Anomaly Detection**: Setting up anomaly alerts for unexpected spikes (e.g., Walmart’s cost monitoring).
  - **Cost Automation with Lambda**: Writing a Lambda function to stop idle EC2 instances nightly (e.g., Airbnb’s automation).
  - **CloudHealth or CloudCheckr**: Exploring third-party tools for multi-cloud cost analysis (beyond AWS native).
  - **Spot Instances**: Leveraging Spot Instances for non-critical workloads (e.g., Netflix’s batch processing).
  - **Cost Forecasting**: Using AWS Cost Explorer forecasts to predict monthly spend and adjust proactively.
  - **Infrastructure Cost Optimization**: Optimizing EKS node groups (e.g., Karpenter for auto-scaling) for cost efficiency.
  - **Billing APIs**: Querying AWS Cost and Usage Reports (CUR) programmatically for custom dashboards (e.g., Google’s analytics).
  - **Real-World Use Case**: Automating cost shutdowns and forecasting for a Fortune 100 retail app with seasonal traffic.

---

### Day 5: Troubleshooting & Monitoring Tools (7-8 hours)
**Objective**: Gain expertise in troubleshooting and monitoring with AWS and external tools for automation and alerting.

- **Key Learning Topics**:
  - **AWS X-Ray**: Distributed tracing for debugging microservices latency and failures (e.g., Amazon’s diagnostics).
  - **CloudWatch Logs & Metrics**: Setting up custom metrics, log insights, and dashboards for app health.
  - **CloudWatch Alarms**: Configuring alarms for CPU > 80% or failed requests (e.g., DHL’s monitoring).
  - **Elastic Observability**: Integrating Elasticsearch/Kibana with CloudWatch for advanced log analysis (e.g., Salesforce’s observability).
  - **Datadog**: Exploring external monitoring for cross-cloud visibility, APM, and alerting (e.g., Airbnb’s adoption).
  - **Prometheus & Grafana**: Setting up Kubernetes monitoring with metrics scraping and visualization (e.g., Netflix’s stack).
  - **Troubleshooting Frameworks**: Five Whys and RCA (Root Cause Analysis) for systematic issue resolution.
  - **Real-World Use Case**: Debugging a failing EKS pod with X-Ray and setting CloudWatch alarms for a logistics app.

---

### Day 6: Capstone Project - Real-World DevSecOps Showcase (7-8 hours)
**Objective**: Apply Week 5 topics (Security, Cost, Troubleshooting) to deploy a secure, cost-optimized, and monitored app, showcasing DevSecOps outcomes.

- **Key Learning Topics**:
  - **Security Integration**: 
    - Encrypt S3 buckets and RDS with KMS, implement RBAC for EKS, secure CI/CD with secrets management.
    - Use OPA to enforce pod security policies (e.g., no privileged containers).
  - **Cost Optimization**: 
    - Right-size EKS nodes, set lifecycle policies for logs, automate shutdowns with Lambda, and track with Budgets/CUR.
    - Forecast spend and adjust for a $10/day cap.
  - **Troubleshooting & Monitoring**: 
    - Deploy X-Ray for app tracing, CloudWatch alarms for health checks, and Prometheus/Grafana for EKS metrics.
    - Resolve a simulated outage (e.g., pod crash) using RCA.
  - **Real-World Simulation**: 
    - Build a microservices app (e.g., order processing API) on EKS, mimicking a retail system (e.g., Walmart’s order flow).
    - Pass a peer audit for security (no exposed resources), cost (< $10/day), and uptime (alarms triggered/resolved).
  - **DevSecOps Synthesis**: 
    - Document the process, lessons, and outcomes in a README, reflecting Fortune 100 standards (e.g., AWS Well-Architected).
  - **Gamified Element**: 
    - Best project (security, cost, monitoring) wins “DevSecOps Titan” title based on peer scoring.

---

## Time Allocation Breakdown
- **Total Hours**: ~42-48 hours (6 days x 7-8 hours).
- **Security (Days 1-2)**: 14-16 hours (~25%).
- **Cost Optimization (Days 3-4)**: 14-16 hours (~25%).
- **Troubleshooting & Monitoring (Day 5)**: 7-8 hours (~25%).
- **Capstone Project (Day 6)**: 7-8 hours (~25%).

---

## Enhanced Focus
- **Security**: Added Fortune 100-relevant topics like Zero Trust, Policy as Code (OPA), CSPM (Security Hub), and compliance (NIST, CIS), reflecting cutting-edge practices.
- **Cost**: Expanded with advanced tools (Cost Anomaly Detection, CloudHealth), automation (Lambda, Spot Instances), and programmatic tracking (CUR, forecasts) for enterprise-scale cost management.
- **Troubleshooting & Monitoring**: Broadened to include Elastic Observability, Datadog, and Prometheus/Grafana alongside AWS X-Ray and CloudWatch, offering a full toolkit for automation and alerting.

- **Capstone Project**: Introduced a real-world simulation with a microservices app, emphasizing the practical
