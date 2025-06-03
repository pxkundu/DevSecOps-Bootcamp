# 🔐 SecureCloudPay – DevSecOps Simulation

Welcome to **SecureCloudPay**, a realistic enterprise-level microservices project built to simulate how Fortune 100 companies secure their DevOps pipelines using tools like **Trivy**, **GitHub Actions**, and **IaC scanning**.

---

## 📦 Project Structure

```
securecloudpay/
├── backend/
│   ├── node-service/        # Node.js microservice
│   └── go-service/          # Go microservice
├── terraform/               # AWS S3 misconfigured bucket
├── k8s/                     # K8s deployment with root user
├── .github/workflows/       # GitHub Actions CI pipeline
├── scripts/                 # Pre-commit Trivy scan script
└── README.md
```

---

## 🧱 Architecture Overview

SecureCloudPay simulates a microservice architecture deployed via containers and Kubernetes, integrated into a CI/CD pipeline with security gates at each stage:

- ✅ Local development scanning (Trivy CLI)
- ✅ Dockerfile and IaC scans
- ✅ Secret detection in source
- ✅ GitHub Actions CI/CD security pipeline
- ✅ Pull request fail/pass based on scan severity
- ✅ SARIF reporting to GitHub Security Dashboard

---

## 🛠️ Toolchain Used

| Purpose                  | Tool                 |
|--------------------------|----------------------|
| Vulnerability Scanning   | [Trivy](https://github.com/aquasecurity/trivy) |
| CI/CD                    | GitHub Actions       |
| Infrastructure as Code   | Terraform            |
| Containers               | Docker               |
| Container Orchestration  | Kubernetes           |
| Language Runtimes        | Node.js, Golang      |

---

## 🚀 Getting Started Locally

### 1. Clone the repo & build services

```bash
git clone https://github.com/your-org/securecloudpay.git
cd securecloudpay/backend/node-service
docker build -t node-service:latest .
```

### 2. Run Trivy locally on image

```bash
trivy image node-service:latest
```

### 3. Scan file system for vulnerabilities/secrets

```bash
trivy fs --scanners vuln,secret .
```

### 4. Scan IaC (Dockerfile, Kubernetes, Terraform)

```bash
trivy config ../..
```

---

## 🔄 Running Pre-commit Scan

```bash
cd securecloudpay
./scripts/precommit-scan.sh
```

Add to Git hook using `husky` or `pre-commit` framework.

---

## 🔁 GitHub Actions CI/CD Pipeline

On every pull request, GitHub Actions will:

- Scan the repo with Trivy
- Detect vulnerabilities, secrets, and IaC misconfigs
- Fail the build if high/critical issues are found
- Upload results as SARIF to GitHub’s security dashboard

See: `.github/workflows/trivy-scan.yml`

---

## 📚 Learning Objectives

By working through SecureCloudPay, you'll learn to:

- Shift security left with Trivy CLI & GitHub Actions
- Automate scans across the full stack (containers, code, IaC)
- Interpret Trivy scan reports
- Design fail-safe CI pipelines used in real enterprises
- Build real-world DevSecOps confidence

---

## 📢 License

MIT License – free to use.
Let's build a full-blown security training platform 💼🛡️💥
