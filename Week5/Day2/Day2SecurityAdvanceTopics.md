## Week 5, Day 2: Security Advanced - DevSecOps Practices
**Objective**: Dive into advanced DevSecOps security practices used by Fortune 100 companies, emphasizing automation, compliance, and proactive security in cloud-native environments.

- **Duration**: ~7-8 hours.
- **Structure**: Theoretical explanations (~50%) + Practical use cases (~50%).

---

### Key Learning Topics

#### 1. Shift-Left Security
- **Theoretical Keyword Explanation**:
  - **Definition**: Shift-Left Security integrates security practices early in the development lifecycle (e.g., coding, testing) rather than at deployment, using tools like Static Application Security Testing (SAST).
  - **Context**: A core DevSecOps principle from the DevOps Handbook, it reduces vulnerabilities by catching them before production, aligning with NIST SP 800-53’s “secure by design.”
  - **Importance**: Speeds up delivery (e.g., fixing a flaw in code vs. prod), cuts costs (e.g., 10x cheaper pre-deploy per IBM), and meets compliance (e.g., OWASP Top 10 mitigation).
  - **Tools**: Checkmarx, SonarQube, GitHub CodeQL integrated into CI/CD pipelines (e.g., Jenkins, GitHub Actions).
- **Practical Use Cases**:
  - **Amazon’s Code Scanning**: Amazon embeds SAST with CodeGuru in its CI/CD pipelines to scan millions of lines of code daily for AWS services (e.g., Lambda). A DevSecOps engineer might configure:
    ```yaml
    # .github/workflows/sast.yml
    name: SAST Scan
    on: [push]
    jobs:
      scan:
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v3
          - run: sonar-scanner -Dsonar.projectKey=app -Dsonar.sources=.
    ```
    - **Scale**: Catches 1000s of vulnerabilities pre-deploy, securing 1B+ API calls daily.
  - **Microsoft’s SDL**: Microsoft’s Security Development Lifecycle (SDL) uses Shift-Left with Checkmarx for Azure, identifying SQL injection risks in dev, protecting 300M+ users monthly.

---

#### 2. Dynamic Application Security Testing (DAST)
- **Theoretical Keyword Explanation**:
  - **Definition**: DAST tests running applications for vulnerabilities (e.g., XSS, CSRF) by simulating attacks, complementing SAST’s static analysis.
  - **Context**: A DevSecOps practice for runtime security (OWASP ZAP, Burp Suite), often run in staging to catch issues missed in code reviews.
  - **Importance**: Ensures apps are secure under real-world conditions (e.g., 2020 SolarWinds runtime exploit), critical for customer-facing systems and compliance (e.g., PCI DSS 6.6).
  - **Tools**: OWASP ZAP, Burp Suite, integrated with CI/CD or standalone scans.
- **Practical Use Cases**:
  - **Netflix’s DAST for Streaming**: Netflix uses OWASP ZAP to test its streaming APIs in staging, identifying XSS flaws before 247M subscribers access new content.
    - **Example**: `zap-cli quick-scan --spider -r http://staging.netflix.com/api` flags runtime issues.
    - **Scale**: Secures 17B+ streaming hours annually, preventing UI exploits.
  - **Walmart’s Checkout Security**: Walmart runs DAST on its e-commerce checkout (e.g., OWASP ZAP in Jenkins) to catch CSRF risks, protecting 240M weekly customers during peak sales.

---

#### 3. Policy as Code
- **Theoretical Keyword Explanation**:
  - **Definition**: Policy as Code defines security and compliance rules programmatically (e.g., Open Policy Agent - OPA) for automated enforcement in Kubernetes, IaC, or CI/CD.
  - **Context**: A DevSecOps shift from manual audits to codified governance (e.g., CIS Kubernetes Benchmarks), enabling scalability and consistency.
  - **Importance**: Reduces human error, ensures compliance (e.g., SOC 2), and scales security for microservices (e.g., 2021 Kaseya breach mitigation).
  - **Tools**: OPA, Conftest, integrated with Kubernetes admission controllers or Terraform.
- **Practical Use Cases**:
  - **Goldman Sachs’ OPA for Kubernetes**: Goldman Sachs uses OPA to enforce pod security policies (e.g., no privileged containers) in EKS:
    ```rego
    # opa-policy.rego
    deny[msg] {
      input.kind == "Pod"
      input.spec.privileged
      msg = "Privileged containers are not allowed"
    }
    ```
    - **Scale**: Secures 1000s of financial pods, processing $1T+ in trades annually.
  - **Netflix’s Network Policies**: Netflix applies OPA to restrict pod-to-pod traffic in EKS, ensuring Zero Trust for 100,000+ containers serving 2M+ concurrent viewers.

---

#### 4. Threat Modeling
- **Theoretical Keyword Explanation**:
  - **Definition**: Threat Modeling identifies and prioritizes potential security risks (e.g., STRIDE: Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege) in system design.
  - **Context**: A proactive DevSecOps practice (Microsoft STRIDE, OWASP Threat Dragon), done pre-build to guide security controls.
  - **Importance**: Prevents costly redesigns (e.g., 2017 Equifax data flow flaw), aligns with NIST 800-53 RA-3, and prepares for audits.
  - **Tools**: STRIDE methodology, Threat Dragon, integrated into architecture reviews.
- **Practical Use Cases**:
  - **Amazon’s Pre-Launch Reviews**: Amazon threat models AWS Lambda deployments with STRIDE, identifying elevation risks (e.g., over-privileged roles), securing 1M+ customers’ functions.
    - **Example**: “Tampering: Can API input alter DB?” → Add input validation.
    - **Scale**: Protects 10,000+ new Lambda deployments monthly.
  - **Walmart’s Supply Chain**: Walmart models threats for its EKS-based inventory app (e.g., DoS from API floods), adding rate limiting for 150M weekly shoppers.

---

#### 5. Secure CI/CD
- **Theoretical Keyword Explanation**:
  - **Definition**: Secure CI/CD hardens pipelines against attacks (e.g., code injection, credential leaks) using signed artifacts, RBAC, and secrets management.
  - **Context**: A DevSecOps necessity as pipelines are attack vectors (e.g., 2021 Codecov breach), per CIS DevOps Security Guide.
  - **Importance**: Ensures trusted deployments, protects millions of users (e.g., SolarWinds supply chain attack), and scales automation securely.
  - **Tools**: Docker Content Trust, Jenkins RBAC, AWS Secrets Manager in pipelines.
- **Practical Use Cases**:
  - **Netflix’s Signed Images**: Netflix signs Docker images with Notary in its Spinnaker pipeline, ensuring only verified builds reach 247M users:
    ```bash
    docker trust sign <ecr-repo>/app:latest
    ```
    - **Scale**: Deploys 100,000+ secure containers daily.
  - **Amazon’s Pipeline RBAC**: Amazon restricts Jenkins access with IAM roles (e.g., `ecr:PutImage` only), securing 1B+ API deployments for AWS customers.

---

#### 6. Cloud Security Posture Management (CSPM)
- **Theoretical Keyword Explanation**:
  - **Definition**: CSPM continuously monitors cloud configurations for misconfigurations (e.g., open S3 buckets) using tools like AWS Security Hub or Prisma Cloud.
  - **Context**: A DevSecOps evolution from reactive to proactive security (e.g., 2020 Twilio misconfig), per Gartner’s security trends.
  - **Importance**: Scales compliance (e.g., CIS AWS Foundations), prevents breaches (e.g., 2019 Capital One), and automates audits.
  - **Tools**: AWS Security Hub, GuardDuty, third-party CSPM (e.g., Palo Alto Prisma).
- **Practical Use Cases**:
  - **Salesforce’s Security Hub**: Salesforce uses AWS Security Hub to monitor 1000s of AWS resources, flagging unencrypted RDS for 150M+ users:
    - **Example**: “RDS Encryption Disabled” → Auto-remediate with Lambda.
    - **Scale**: Secures 10B+ transactions annually.
  - **Walmart’s CSPM**: Walmart scans EKS clusters with Security Hub, ensuring CIS compliance for 11,000+ stores’ inventory systems.

---

#### 7. Compliance Frameworks
- **Theoretical Keyword Explanation**:
  - **Definition**: Compliance Frameworks (e.g., NIST SP 800-53, CIS Benchmarks) provide structured security controls for cloud systems, enforced via DevSecOps practices.
  - **Context**: Mandatory for Fortune 100s (e.g., PCI DSS for retail, SOC 2 for SaaS), guiding audits and risk management.
  - **Importance**: Ensures legal/market trust (e.g., GDPR fines avoided), scales security for millions, and standardizes DevSecOps processes.
  - **Tools**: AWS Config Rules, CIS AWS Benchmark scripts, compliance dashboards.
- **Practical Use Cases**:
  - **Amazon’s NIST Compliance**: Amazon maps EC2/EKS to NIST 800-53 (e.g., AC-3 Access Control), using Config Rules to enforce encryption for 1M+ customers:
    ```hcl
    resource "aws_config_rule" "rds_encrypted" {
      name = "rds-storage-encrypted"
      source { owner = "AWS" identifier = "RDS_STORAGE_ENCRYPTED" }
    }
    ```
    - **Scale**: Audits 100,000+ resources daily.
  - **Walmart’s CIS Hardening**: Walmart hardens RDS with CIS Benchmarks (e.g., disable public access), securing 500M+ annual customers’ data.

---

#### 8. Real-World Use Case: Securing a Microservices App on EKS for a Financial Client
- **Theoretical Keyword Explanation**:
  - **Definition**: A comprehensive scenario applying Day 2 topics to secure an EKS-based microservices app, meeting financial compliance (e.g., SOC 2, PCI DSS).
  - **Context**: Fortune 100 financial firms require end-to-end security, a DevSecOps showcase of advanced practices.
  - **Importance**: Integrates Shift-Left, DAST, Policy as Code, etc., scaling security for high-stakes apps.
- **Practical Use Case**:
  - **Goldman Sachs’ Trading App**: A DevSecOps team secures an EKS trading platform:
    - **Shift-Left**: SonarQube in Jenkins scans code for 100M+ trades.
    - **DAST**: OWASP ZAP tests APIs in staging, catching XSS.
    - **Policy as Code**: OPA denies privileged pods:
      ```rego
      deny[msg] { input.spec.privileged; msg = "No privileged pods" }
      ```
    - **Threat Modeling**: STRIDE flags DoS risks → Rate limiting added.
    - **Secure CI/CD**: Signed images deployed to EKS.
    - **CSPM**: Security Hub ensures encrypted RDS.
    - **Compliance**: NIST 800-53 controls audited.
    - **Scale**: Processes $1T+ in trades annually, securing 10,000+ pods.

---

## Learning Schedule (7-8 Hours)
- **Morning (3-4 hours)**:
  - **Theoretical Deep Dive**: Shift-Left Security, DAST, Policy as Code, Threat Modeling (slides, videos, NIST/CIS docs).
  - **Practical Exploration**: Review tools (SonarQube, OPA) and Fortune 100 examples (Amazon, Netflix).
- **Afternoon (4 hours)**:
  - **Theoretical Deep Dive**: Secure CI/CD, CSPM, Compliance Frameworks, Financial Use Case.
  - **Practical Exploration**: Hands-on with Jenkins configs, Security Hub, and Goldman Sachs-style EKS policies.

---

## Why This Matters
- **Theoretical Value**: These keywords define modern DevSecOps—automation, runtime security, and compliance at scale.
- **Practical Impact**: Use cases from Netflix, Amazon, and Goldman Sachs show how to secure millions of users/transactions, preparing learners for Fortune 100 complexity.
- **DevSecOps Alignment**: Covers OWASP, NIST, CIS, and Gartner trends, ensuring industry-standard expertise.

