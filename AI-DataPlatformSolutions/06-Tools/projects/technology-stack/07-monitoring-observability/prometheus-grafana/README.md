# Prometheus & Grafana - Monitoring & Observability

## 📊 Overview
Prometheus and Grafana form a powerful monitoring stack for DevSecOps. Prometheus collects metrics while Grafana provides visualization and alerting capabilities.

## 📁 Directory Structure

```
prometheus-grafana/
├── README.md
├── prometheus/
│   ├── config/
│   ├── rules/
│   └── scripts/
├── grafana/
│   ├── dashboards/
│   ├── datasources/
│   └── provisioning/
└── kubernetes/
    ├── prometheus/
    └── grafana/
```

## 🛠️ Prometheus Configuration

### 1. Prometheus Config
```yaml
# prometheus/config/prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "rules/*.yml"

alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - alertmanager:9093

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'node-exporter'
    static_configs:
      - targets: ['node-exporter:9100']

  - job_name: 'kubernetes-pods'
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
        action: replace
        target_label: __metrics_path__
        regex: (.+)
```

### 2. Alert Rules
```yaml
# prometheus/rules/alerts.yml
groups:
  - name: infrastructure
    rules:
      - alert: HighCPUUsage
        expr: 100 - (avg(rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 80
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High CPU usage detected"
          description: "CPU usage is above 80% for more than 5 minutes"

      - alert: HighMemoryUsage
        expr: (1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100 > 80
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High memory usage detected"
          description: "Memory usage is above 80% for more than 5 minutes"

      - alert: DiskSpaceLow
        expr: (1 - (node_filesystem_avail_bytes / node_filesystem_size_bytes)) * 100 > 80
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Disk space is low"
          description: "Disk usage is above 80% for more than 5 minutes"
```

## 📈 Grafana Configuration

### 1. Dashboard JSON
```json
{
  "dashboard": {
    "title": "DevSecOps Monitoring",
    "panels": [
      {
        "title": "CPU Usage",
        "type": "graph",
        "targets": [
          {
            "expr": "100 - (avg(rate(node_cpu_seconds_total{mode=\"idle\"}[5m])) * 100)",
            "legendFormat": "CPU Usage %"
          }
        ]
      },
      {
        "title": "Memory Usage",
        "type": "graph",
        "targets": [
          {
            "expr": "(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100",
            "legendFormat": "Memory Usage %"
          }
        ]
      }
    ]
  }
}
```

### 2. Data Source Config
```yaml
# grafana/datasources/prometheus.yml
apiVersion: 1
datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
```

## ☸️ Kubernetes Manifests

### 1. Prometheus Deployment
```yaml
# kubernetes/prometheus/prometheus.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: prometheus
spec:
  replicas: 1
  selector:
    matchLabels:
      app: prometheus
  template:
    metadata:
      labels:
        app: prometheus
    spec:
      containers:
      - name: prometheus
        image: prom/prometheus:latest
        ports:
        - containerPort: 9090
        volumeMounts:
        - name: config
          mountPath: /etc/prometheus
      volumes:
      - name: config
        configMap:
          name: prometheus-config
---
apiVersion: v1
kind: Service
metadata:
  name: prometheus
spec:
  selector:
    app: prometheus
  ports:
  - port: 9090
    targetPort: 9090
```

### 2. Grafana Deployment
```yaml
# kubernetes/grafana/grafana.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: grafana
spec:
  replicas: 1
  selector:
    matchLabels:
      app: grafana
  template:
    metadata:
      labels:
        app: grafana
    spec:
      containers:
      - name: grafana
        image: grafana/grafana:latest
        ports:
        - containerPort: 3000
        env:
        - name: GF_SECURITY_ADMIN_PASSWORD
          value: "admin"
        volumeMounts:
        - name: config
          mountPath: /etc/grafana/provisioning
      volumes:
      - name: config
        configMap:
          name: grafana-config
---
apiVersion: v1
kind: Service
metadata:
  name: grafana
spec:
  selector:
    app: grafana
  ports:
  - port: 3000
    targetPort: 3000
```

## 🚀 Deployment Scripts

### 1. Install Script
```bash
#!/bin/bash
# scripts/install.sh

echo "Installing Prometheus and Grafana..."

# Create namespace
kubectl create namespace monitoring

# Install Prometheus
kubectl apply -f kubernetes/prometheus/

# Install Grafana
kubectl apply -f kubernetes/grafana/

# Wait for deployments
kubectl wait --for=condition=available --timeout=300s deployment/prometheus -n monitoring
kubectl wait --for=condition=available --timeout=300s deployment/grafana -n monitoring

echo "Installation completed successfully"
```

### 2. Access Script
```bash
#!/bin/bash
# scripts/access.sh

echo "Accessing monitoring services..."

# Port forward Prometheus
kubectl port-forward svc/prometheus 9090:9090 -n monitoring &
PROMETHEUS_PID=$!

# Port forward Grafana
kubectl port-forward svc/grafana 3000:3000 -n monitoring &
GRAFANA_PID=$!

echo "Prometheus: http://localhost:9090"
echo "Grafana: http://localhost:3000 (admin/admin)"
echo "Press Ctrl+C to stop port forwarding"

# Cleanup on exit
trap "kill $PROMETHEUS_PID $GRAFANA_PID" EXIT
wait
```

## 📋 Best Practices

### 1. Monitoring
- Set up comprehensive metrics collection
- Implement proper alerting thresholds
- Use service discovery for dynamic targets
- Monitor both infrastructure and applications
- Regular review of alert rules

### 2. Performance
- Optimize query performance
- Use recording rules for complex queries
- Implement proper data retention policies
- Monitor Prometheus performance
- Use federation for multi-cluster setups

### 3. Security
- Secure Prometheus and Grafana access
- Use RBAC for user management
- Encrypt sensitive data
- Regular security updates
- Audit access logs

---

**Ready to master monitoring?** Start with basic Prometheus setup and work your way up to comprehensive observability!
