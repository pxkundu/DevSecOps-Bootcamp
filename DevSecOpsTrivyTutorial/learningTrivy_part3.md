Let's dive into **Part 3** of our tutorial series, which focuses on **Implementing Trivy in DevSecOps Pipelines** at a more **advanced level**.

This part will cover:

1. **Configuring Trivy for Continuous Integration/Continuous Deployment (CI/CD)**
   - We’ll use GitHub Actions to integrate Trivy security scans directly into the CI/CD pipeline.
   - Set up automated scans during pull requests.
   - Configure Trivy for Docker image scanning, Kubernetes manifests, and IaC (Infrastructure as Code) files.

2. **Scanning Docker Images in CI/CD**
   - We’ll implement Docker image vulnerability scanning within the pipeline.
   - Ensure Docker images are scanned for vulnerabilities before deployment to production.

3. **Infrastructure as Code (IaC) Security**
   - Implement scanning for misconfigurations and vulnerabilities in Terraform and Kubernetes manifests.
   - Integrate IaC security checks into the pipeline.

4. **Automated Failures and Alerts**
   - Define and configure security thresholds (severity levels) for failed scans.
   - Set up automated alerts and reporting mechanisms for critical vulnerabilities.

5. **Building an Industry-Grade DevSecOps Pipeline**
   - Learn how to implement a robust, scalable, and repeatable security scanning process across all environments.
   - Understand how to tailor Trivy and CI/CD pipeline configuration to support enterprise-level security needs.

---

### Part 3: **Detailed Plan**

---

### 1. **Overview of CI/CD Pipeline with Trivy**
   - **Goal:** Automate security scans during the CI/CD pipeline to catch vulnerabilities in Docker images, IaC files (Terraform, Kubernetes), and source code.
   - **Tools used:**
     - **GitHub Actions** for the CI/CD pipeline.
     - **Trivy** for security scanning.
     - **Docker** for container image building.
     - **Terraform** for infrastructure provisioning.
     - **Kubernetes** for orchestration.
     - **Slack/MS Teams/Email** for notifications (optional).

---

### 2. **Implementing Trivy in GitHub Actions**
   - **Objective:** Create a secure, automated scanning process for every pull request (PR) that includes:
     - **Vulnerability scans** for Docker images.
     - **Secrets detection** in source code.
     - **Misconfigurations in IaC** (Terraform, Kubernetes).
   - **CI Pipeline Configuration Steps:**
     1. **Install Trivy** in the GitHub Actions runner.
     2. **Docker image scanning**: Add a job to scan the container image (Node.js, Go, etc.) for vulnerabilities.
     3. **IaC scanning**: Add a job to scan Kubernetes YAML files and Terraform scripts.
     4. **Security thresholds**: Set the severity level and ensure the pipeline fails if high/critical vulnerabilities are found.
     5. **Slack/MS Teams/Email alerts**: Optional notification setup if critical vulnerabilities are found.

---

### 3. **Step-by-Step CI/CD Pipeline with Trivy (GitHub Actions)**
   Let's walk through setting up a robust GitHub Actions pipeline that integrates Trivy at multiple stages.

---

#### Step 1: **Create GitHub Actions Workflow for PR Scans**

**File Path:** `.github/workflows/trivy-scan.yml`

```yaml
name: Trivy Security Scan

on:
  pull_request:
    branches:
      - main

jobs:
  trivy-scan:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v3

    # Install Trivy
    - name: Install Trivy
      run: |
        curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin

    # Docker image vulnerability scan
    - name: Scan Docker image for vulnerabilities
      run: |
        docker build -t node-service:latest ./backend/node-service
        trivy image --exit-code 1 --severity HIGH,CRITICAL node-service:latest

    # Scan file system for secrets and vulnerabilities
    - name: Scan repository for secrets and vulnerabilities
      run: trivy fs --scanners vuln,secret --exit-code 1 .

    # Scan Infrastructure as Code (IaC) for misconfigurations
    - name: Scan Terraform and Kubernetes files
      run: |
        trivy config --exit-code 1 --severity HIGH,CRITICAL ./terraform
        trivy config --exit-code 1 --severity HIGH,CRITICAL ./k8s

    # Optional: Upload results to SARIF format (GitHub Security)
    - name: Upload SARIF results
      uses: github/codeql-action/upload-sarif@v2
      with:
        sarif_file: trivy-results.sarif
```

---

#### Step 2: **Set Security Failures and Alerts**

In the above YAML:
- We define `--exit-code 1` which will make the pipeline fail if high or critical vulnerabilities are found.
- Severity is set to **HIGH, CRITICAL** to focus on the most severe issues.
  
**Optional Step: Slack/MS Teams Integration for Alerts**

Add the following step to send alerts if the pipeline fails due to high severity vulnerabilities.

```yaml
- name: Send Slack Notification (if vulnerabilities found)
  if: failure()
  run: |
    curl -X POST -H 'Content-type: application/json' --data '{"text":"🚨 High/critical vulnerabilities detected in PR. Please review the Trivy results."}' ${{ secrets.SLACK_WEBHOOK_URL }}
```

Make sure to add your Slack Webhook URL as a secret in your GitHub repository settings.

---

#### Step 3: **Scan Docker Image for Vulnerabilities**

**Goal:** Perform vulnerability scanning on Docker images to ensure they are free of critical vulnerabilities before they can be deployed.

In the workflow above, Trivy scans the Docker image using the command:

```bash
docker build -t node-service:latest ./backend/node-service
trivy image --exit-code 1 --severity HIGH,CRITICAL node-service:latest
```

If any **high or critical vulnerabilities** are found in the image, the workflow will fail, ensuring that the image is not deployed to production.

---

#### Step 4: **Scan Infrastructure as Code (IaC)**

We use **Trivy** to scan Terraform and Kubernetes configurations for misconfigurations, which are common vulnerabilities in IaC:

```bash
trivy config --exit-code 1 --severity HIGH,CRITICAL ./terraform
trivy config --exit-code 1 --severity HIGH,CRITICAL ./k8s
```

This step ensures that no misconfigurations or vulnerabilities are introduced via infrastructure-as-code changes.

---

#### Step 5: **GitHub Security Dashboard**

- Trivy’s results can be uploaded as **SARIF** files (Static Analysis Results Interchange Format) so that they appear in the GitHub Security tab, making it easier to track and manage vulnerabilities.

---

### 4. **Extending the DevSecOps Pipeline**
You can extend this pipeline to include the following advanced topics:

- **Automated Snyk/Grype scans** alongside Trivy for comparison.
- **Automated Docker image signing** and verification using **Notary**.
- **Integration with security tools like OPA (Open Policy Agent)** to enforce security policies.
- **Deploy-time security checks** with Kubernetes admission controllers or Helm chart validation.

---

### 5. **Learning Outcomes**
By the end of **Part 3**, you will:
- Understand how to integrate **Trivy** in the **CI/CD pipeline**.
- Be able to scan **Docker images**, **Terraform**, and **Kubernetes manifests**.
- Set up **security thresholds** in your pipeline and use **Slack/MS Teams alerts** for critical issues.
- Gain real-world experience with **DevSecOps** practices that are used in **Fortune 100 companies**.

---

### Next Steps

In the **next part** (Part 4), we will cover how to:
- Set up **Security Monitoring** (e.g., continuous scans, periodic security audits).
- Introduce more advanced **incident response** measures.
- Use **Trivy in multi-cloud environments** (AWS, GCP, Azure).
  
---
