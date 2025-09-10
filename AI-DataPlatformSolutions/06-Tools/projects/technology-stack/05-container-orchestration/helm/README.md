# Helm - Kubernetes Package Manager

## 🎯 Overview
Helm is the package manager for Kubernetes that simplifies application deployment and management. This section provides practical guides for using Helm in DevSecOps workflows.

## 📁 Directory Structure

```
helm/
├── README.md
├── charts/
│   ├── myapp/
│   ├── monitoring/
│   └── security/
├── values/
│   ├── dev/
│   ├── staging/
│   └── production/
└── scripts/
    ├── install.sh
    ├── upgrade.sh
    └── uninstall.sh
```

## 🛠️ Essential Helm Charts

### 1. Basic Application Chart
```yaml
# charts/myapp/Chart.yaml
apiVersion: v2
name: myapp
description: A Helm chart for MyApp
type: application
version: 0.1.0
appVersion: "1.0.0"
dependencies:
  - name: postgresql
    version: 12.1.2
    repository: https://charts.bitnami.com/bitnami
```

### 2. Values Files
```yaml
# values/dev/values.yaml
replicaCount: 1
image:
  repository: myapp
  tag: "dev"
  pullPolicy: IfNotPresent

service:
  type: ClusterIP
  port: 80

ingress:
  enabled: true
  className: "nginx"
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-staging"
  hosts:
    - host: myapp-dev.example.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: myapp-dev-tls
      hosts:
        - myapp-dev.example.com

resources:
  limits:
    cpu: 500m
    memory: 512Mi
  requests:
    cpu: 250m
    memory: 256Mi

postgresql:
  auth:
    postgresPassword: "devpassword"
    database: "myapp"
```

### 3. Deployment Template
```yaml
# charts/myapp/templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "myapp.fullname" . }}
  labels:
    {{- include "myapp.labels" . | nindent 4 }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      {{- include "myapp.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      labels:
        {{- include "myapp.selectorLabels" . | nindent 8 }}
    spec:
      containers:
        - name: {{ .Chart.Name }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
          imagePullPolicy: {{ .Values.image.pullPolicy }}
          ports:
            - name: http
              containerPort: 3000
              protocol: TCP
          livenessProbe:
            httpGet:
              path: /health
              port: http
          readinessProbe:
            httpGet:
              path: /ready
              port: http
          resources:
            {{- toYaml .Values.resources | nindent 12 }}
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: {{ include "myapp.fullname" . }}-postgresql
                  key: postgres-password
```

## 🚀 Deployment Scripts

### 1. Install Script
```bash
#!/bin/bash
# scripts/install.sh

set -e

CHART_NAME=${1:-myapp}
RELEASE_NAME=${2:-myapp-release}
NAMESPACE=${3:-default}
VALUES_FILE=${4:-values/dev/values.yaml}

echo "Installing Helm chart: $CHART_NAME"

helm install $RELEASE_NAME ./charts/$CHART_NAME \
    --namespace $NAMESPACE \
    --create-namespace \
    --values $VALUES_FILE \
    --wait

echo "Installation completed successfully"
```

### 2. Upgrade Script
```bash
#!/bin/bash
# scripts/upgrade.sh

set -e

CHART_NAME=${1:-myapp}
RELEASE_NAME=${2:-myapp-release}
NAMESPACE=${3:-default}
VALUES_FILE=${4:-values/dev/values.yaml}

echo "Upgrading Helm chart: $CHART_NAME"

helm upgrade $RELEASE_NAME ./charts/$CHART_NAME \
    --namespace $NAMESPACE \
    --values $VALUES_FILE \
    --wait

echo "Upgrade completed successfully"
```

## 📋 Best Practices

### 1. Chart Development
- Use semantic versioning
- Include comprehensive values.yaml
- Add proper labels and annotations
- Implement health checks
- Use ConfigMaps and Secrets appropriately

### 2. Security
- Use least privilege RBAC
- Encrypt sensitive data
- Scan images for vulnerabilities
- Use network policies
- Regular security updates

### 3. Production Readiness
- Set resource limits
- Configure monitoring
- Implement backup strategies
- Use proper logging
- Plan for disaster recovery

---

**Ready to master Helm?** Start with the basic application chart and work your way up to complex multi-service deployments!
