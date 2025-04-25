#!/bin/bash

set -e

echo "🚧 Setting up SecureCloudPay DevSecOps simulation..."

# Create folder structure
mkdir -p securecloudpay/{backend/{node-service,go-service},terraform,k8s,.github/workflows,scripts}

# --- Node.js service ---
cat <<'EOF' > securecloudpay/backend/node-service/app.js
const express = require('express');
const app = express();
const port = 3000;

const jwtSecret = 'super-secret-token'; // 🚨 Intentionally hardcoded

app.get('/', (req, res) => {
  res.send('Hello from Node.js!');
});

app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});
EOF

cat <<'EOF' > securecloudpay/backend/node-service/package.json
{
  "name": "node-service",
  "version": "1.0.0",
  "main": "app.js",
  "dependencies": {
    "express": "4.17.1"
  }
}
EOF

cat <<'EOF' > securecloudpay/backend/node-service/Dockerfile
FROM node:14-alpine

WORKDIR /app
COPY . .
RUN npm install

CMD ["node", "app.js"]
EOF

# --- Go service ---
cat <<'EOF' > securecloudpay/backend/go-service/main.go
package main

import (
    "fmt"
    "net/http"
)

func handler(w http.ResponseWriter, r *http.Request) {
    fmt.Fprintf(w, "Hello from Go!")
}

func main() {
    http.HandleFunc("/", handler)
    fmt.Println("Starting Go server on :8080")
    http.ListenAndServe(":8080", nil)
}
EOF

cat <<'EOF' > securecloudpay/backend/go-service/Dockerfile
FROM golang:1.17

WORKDIR /app
COPY . .
RUN go build -o app

CMD ["./app"]
EOF

# --- Terraform file ---
cat <<'EOF' > securecloudpay/terraform/main.tf
provider "aws" {
  region = "us-west-2"
}

resource "aws_s3_bucket" "insecure_bucket" {
  bucket = "securecloudpay-dev"
  acl    = "public-read"
}
EOF

# --- Kubernetes YAMLs ---
cat <<'EOF' > securecloudpay/k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: node-service
spec:
  replicas: 1
  selector:
    matchLabels:
      app: node-service
  template:
    metadata:
      labels:
        app: node-service
    spec:
      containers:
      - name: node-service
        image: node:14-alpine
        command: ["node", "app.js"]
        securityContext:
          runAsUser: 0
EOF

cat <<'EOF' > securecloudpay/k8s/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: node-service
spec:
  type: ClusterIP
  selector:
    app: node-service
  ports:
    - protocol: TCP
      port: 80
      targetPort: 3000
EOF

# --- GitHub Actions Trivy workflow ---
cat <<'EOF' > securecloudpay/.github/workflows/trivy-scan.yml
name: Trivy Security Scan

on:
  pull_request:
    branches: [ "main" ]

jobs:
  trivy-scan:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v3

    - name: Install Trivy
      run: |
        curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin

    - name: File system scan (Secrets, Vuln)
      run: trivy fs --exit-code 1 --severity HIGH,CRITICAL .

    - name: Config scan (IaC + Dockerfile)
      run: trivy config --exit-code 1 --severity HIGH,CRITICAL .

    - name: Upload results (SARIF)
      uses: github/codeql-action/upload-sarif@v2
      with:
        sarif_file: trivy-results.sarif
EOF

# --- Pre-commit scan script ---
cat <<'EOF' > securecloudpay/scripts/precommit-scan.sh
#!/bin/bash

echo "🛡️ Trivy Pre-commit Scan Started..."

echo "🔍 Scanning file system..."
trivy fs --scanners vuln,secret .

echo "🔧 Scanning Dockerfiles and IaC configs..."
trivy config .

echo "✅ Scan complete."
EOF

chmod +x securecloudpay/scripts/precommit-scan.sh

