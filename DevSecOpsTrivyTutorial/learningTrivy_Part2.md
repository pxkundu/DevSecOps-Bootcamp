Are you  enjoying the structure—we’re building something **seriously next-level** here?! 🌍🔥  
Let’s dive into **Part 2**, keeping everything aligned with the **enterprise-scale vision** of **SecureCloudPay**, our DevSecOps simulation for Fortune 100-level security practices.

---

# 📗 PART 2: Using Trivy in Local Development & CI – Building Strong DevSecOps Habits

---

### 🧭 Goal of This Module

In this part, we’ll explore how **developers and DevOps teams** use Trivy in the **local dev phase and early CI stages**, preventing security risks from even entering the pipeline.

---

## 🏗️ SecureCloudPay: Dev Stage Integration (Real-World Context)

Here's how the Fortune 100 do it—and how we’ll simulate it in **SecureCloudPay**:

| Stage | What Happens | Tools |
|-------|--------------|-------|
| **Dev (Local)** | Developers scan code, secrets, Dockerfiles | Trivy CLI |
| **PR Creation** | Security scans before merge | GitHub Actions + Trivy |
| **CI Pipeline** | Container images scanned post-build | Trivy + GitHub Code Scanning |
| **IaC Scan** | Terraform/Kubernetes scanned pre-deploy | Trivy config scan |
| **Gatekeeping** | Fail build if CRITICAL issues | Trivy exit codes + pipeline rules |

---

## 🎯 Learning Objectives for Part 2

- Use Trivy effectively as a **local development tool**
- Build a developer habit of scanning code and Dockerfiles before pushing
- Integrate Trivy into GitHub Actions pipeline for pull request scanning
- Learn how Trivy influences CI/CD gates and developer workflows
- Visualize and export results for visibility

---

## 🔧 1. Local Dev Workflow: Developers Using Trivy

### ✅ Use Case:
Before pushing a new microservice to `SecureCloudPay/backend`, a dev runs:

```bash
cd backend/
trivy fs .
trivy config .
trivy image my-app:dev
```

### 🔍 Output Examples:

- Shows if they hardcoded an AWS key
- Warns about a vulnerable `express` package
- Flags a Dockerfile using `root` user

💡 **Pro Tip**: Add a script called `precommit-scan.sh` and automate this:

```bash
#!/bin/bash
echo "Scanning source code and secrets..."
trivy fs --scanners vuln,secret .
echo "Scanning Dockerfile and IaC..."
trivy config .
```

Hook it with Husky (or pre-commit framework) to enforce on commit.

---

## 🤖 2. CI Workflow: GitHub Actions + Trivy

### 🌐 Folder: `.github/workflows/security-scan.yml`

```yaml
name: Trivy Security Scan

on:
  pull_request:
    branches: [ "main" ]

jobs:
  trivy-scan:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v3

      - name: Install Trivy
        run: |
          curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin

      - name: File System Scan (Secrets + Vuln)
        run: trivy fs --exit-code 1 --severity HIGH,CRITICAL .

      - name: Config Scan (IaC + Dockerfile)
        run: trivy config --exit-code 1 --severity HIGH,CRITICAL .
```

This:
- Automatically scans PRs for secrets, config issues, and vulnerabilities
- Fails PRs with critical issues
- Can output to GitHub Security Dashboard via SARIF format

---

## 📦 3. Container Image Scan (Post-Build)

Add this step after building the Docker image in CI:

```yaml
      - name: Scan Docker Image
        run: trivy image --exit-code 1 --severity HIGH,CRITICAL my-app:latest
```

You can push your image to a registry (e.g., GitHub Container Registry) and scan it remotely:

```bash
trivy image ghcr.io/finserve-devops/securecloudpay/backend:latest
```

---

## 📊 4. Output Scan Results – JSON, SARIF, Markdown

For automated pipelines or dashboards:

```bash
trivy fs --format json --output trivy-result.json .
trivy image --format sarif --output trivy-scan.sarif my-app:latest
```

### ✨ Bonus: Upload to GitHub Security Dashboard

```yaml
      - name: Upload Trivy Report to GitHub
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: trivy-scan.sarif
```

---

## 🚦 5. Fail Build on Vulnerabilities

Control build pass/fail based on exit codes:

| `--exit-code` | Behavior |
|---------------|----------|
| `0`           | No vulnerabilities |
| `1`           | Vulnerabilities found, fail build |
| `0,1`         | Continue regardless, useful for logging only |

🎯 Example:
```bash
trivy image --exit-code 1 --severity CRITICAL my-app:latest
```

---

## 🛡️ GitHub Advanced Setup (Fortune 100 Style)

To align with large-scale practices:

- **Secrets scanning runs in a separate job**
- **SARIF outputs uploaded to GitHub dashboard**
- **Automated PR comments created via bot**
- **Centralized policy enforcement via OPA (coming in Part 4)**

---

## 🧪 Hands-On Exercise

1. Clone your `securecloudpay` repo and add a sample microservice
2. Write a basic Dockerfile and intentionally add a vulnerable dependency or secret
3. Run Trivy locally
4. Set up `security-scan.yml` in GitHub Actions
5. Create a PR and see Trivy in action

---

## 🔮 Coming Up in Part 3

We’re going **full CI/CD**: 
- Multi-stage Docker scanning  
- Scanning Kubernetes manifests  
- Integrating Trivy into GitLab CI, Jenkins  
- Automating Slack alerts, GitHub PR comments, fail/pass logic

---
