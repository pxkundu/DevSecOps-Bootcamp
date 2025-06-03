# SecureCloudPay – DevSecOps Simulation

A realistic enterprise-level microservices project to practice vulnerability scanning, IaC security, and DevSecOps pipeline automation.

## 🔧 Services
- Node.js + Go backend microservices
- Dockerized and K8s-deployed

## 🛡️ Security Scans via Trivy
- Image and file system scanning
- IaC misconfiguration detection
- Secret detection in code
- CI/CD scan enforcement via GitHub Actions

## 📦 Getting Started
```bash
cd backend/node-service
docker build -t node-service:latest .
trivy image node-service:latest
```

## 🚦 CI/CD
All pull requests are scanned using Trivy for vulnerabilities and secrets.

## 📁 Project Structure

securecloudpay/
├── backend/
│   ├── node-service/
│   │   ├── app.js
│   │   ├── package.json
│   │   └── Dockerfile
│   └── go-service/
│       ├── main.go
│       └── Dockerfile
├── terraform/
│   └── main.tf
├── k8s/
│   ├── deployment.yaml
│   └── service.yaml
├── .github/
│   └── workflows/
│       └── trivy-scan.yml
├── scripts/
│   └── precommit-scan.sh
└── README.md

