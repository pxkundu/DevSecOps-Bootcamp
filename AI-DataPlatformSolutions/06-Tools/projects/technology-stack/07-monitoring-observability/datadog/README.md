# Datadog - Cloud Monitoring Platform

## 📊 Overview
Datadog provides comprehensive monitoring, logging, and security for cloud applications and infrastructure. This section covers practical implementation of Datadog in DevSecOps environments.

## 📁 Directory Structure

```
datadog/
├── README.md
├── configurations/
│   ├── datadog-agent/
│   ├── dashboards/
│   └── monitors/
├── kubernetes/
│   ├── datadog-agent/
│   └── custom-metrics/
└── scripts/
    ├── install-datadog.sh
    └── configure-monitoring.sh
```

## 🛠️ Datadog Agent Configuration

### 1. Agent Configuration
```yaml
# configurations/datadog-agent/datadog.yaml
api_key: <DATADOG_API_KEY>
site: datadoghq.com

# Log collection
logs_enabled: true
logs_config:
  container_collect_all: true

# APM
apm_config:
  enabled: true
  env: production

# Process monitoring
process_config:
  enabled: true

# Network monitoring
network_config:
  enabled: true

# Kubernetes integration
kubernetes_config:
  enabled: true
  collect_kubernetes_events: true
  kubernetes_leader_lease: true
```

### 2. Custom Metrics
```yaml
# configurations/datadog-agent/conf.d/custom_metrics.yaml
init_config:

instances:
  - name: myapp_metrics
    url: http://myapp:8080/metrics
    method: GET
    tags:
      - service:myapp
      - env:production
```

## ☸️ Kubernetes Deployment

### 1. Datadog Agent DaemonSet
```yaml
# kubernetes/datadog-agent/datadog-agent.yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: datadog-agent
  namespace: datadog
spec:
  selector:
    matchLabels:
      app: datadog-agent
  template:
    metadata:
      labels:
        app: datadog-agent
    spec:
      serviceAccountName: datadog-agent
      containers:
      - name: agent
        image: datadog/agent:latest
        ports:
        - containerPort: 8126
          name: traceport
        - containerPort: 8125
          name: dogstatsdport
        env:
        - name: DD_API_KEY
          valueFrom:
            secretKeyRef:
              name: datadog-secret
              key: api-key
        - name: DD_SITE
          value: "datadoghq.com"
        - name: DD_LOGS_ENABLED
          value: "true"
        - name: DD_LOGS_CONFIG_CONTAINER_COLLECT_ALL
          value: "true"
        - name: DD_APM_ENABLED
          value: "true"
        - name: DD_PROCESS_AGENT_ENABLED
          value: "true"
        - name: DD_KUBERNETES_KUBELET_HOST
          valueFrom:
            fieldRef:
              fieldPath: status.hostIP
        volumeMounts:
        - name: dockersocket
          mountPath: /var/run/docker.sock
        - name: procdir
          mountPath: /host/proc
          readOnly: true
        - name: cgroups
          mountPath: /host/sys/fs/cgroup
          readOnly: true
        - name: config
          mountPath: /etc/datadog-agent/datadog.yaml
          subPath: datadog.yaml
      volumes:
      - name: dockersocket
        hostPath:
          path: /var/run/docker.sock
      - name: procdir
        hostPath:
          path: /proc
      - name: cgroups
        hostPath:
          path: /sys/fs/cgroup
      - name: config
        configMap:
          name: datadog-config
```

### 2. Cluster Agent
```yaml
# kubernetes/datadog-agent/cluster-agent.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: datadog-cluster-agent
  namespace: datadog
spec:
  replicas: 1
  selector:
    matchLabels:
      app: datadog-cluster-agent
  template:
    metadata:
      labels:
        app: datadog-cluster-agent
    spec:
      serviceAccountName: datadog-cluster-agent
      containers:
      - name: cluster-agent
        image: datadog/cluster-agent:latest
        ports:
        - containerPort: 5005
        env:
        - name: DD_API_KEY
          valueFrom:
            secretKeyRef:
              name: datadog-secret
              key: api-key
        - name: DD_SITE
          value: "datadoghq.com"
        - name: DD_CLUSTER_AGENT_ENABLED
          value: "true"
        - name: DD_CLUSTER_AGENT_KUBERNETES_SERVICE_NAME
          value: "datadog-cluster-agent"
```

## 📈 Dashboards and Monitors

### 1. Application Dashboard
```json
{
  "title": "MyApp Dashboard",
  "widgets": [
    {
      "definition": {
        "type": "timeseries",
        "requests": [
          {
            "q": "avg:myapp.request.duration{service:myapp}",
            "display_type": "line"
          }
        ],
        "title": "Request Duration"
      }
    },
    {
      "definition": {
        "type": "query_value",
        "requests": [
          {
            "q": "sum:myapp.request.count{service:myapp}",
            "aggregator": "sum"
          }
        ],
        "title": "Total Requests"
      }
    }
  ]
}
```

### 2. Infrastructure Monitor
```json
{
  "name": "High CPU Usage",
  "type": "metric alert",
  "query": "avg(last_5m):avg:system.cpu.user{*} > 0.8",
  "message": "CPU usage is above 80%",
  "tags": ["env:production"],
  "options": {
    "thresholds": {
      "critical": 0.8,
      "warning": 0.6
    },
    "notify_audit": false,
    "require_full_window": false,
    "notify_no_data": false
  }
}
```

## 🔧 Application Instrumentation

### 1. Node.js APM
```javascript
// examples/instrumentation/nodejs-apm.js
const tracer = require('dd-trace').init({
  service: 'myapp',
  env: 'production',
  version: '1.0.0',
  logInjection: true,
  runtimeMetrics: true,
  profiling: true
});

// Express middleware
const express = require('express');
const app = express();

// Use tracer middleware
app.use(tracer.express());

// Custom spans
function processData(data) {
  const span = tracer.startSpan('process.data');
  
  try {
    // Your business logic
    span.setTag('data.size', data.length);
    return processBusinessLogic(data);
  } catch (error) {
    span.setTag('error', true);
    span.setTag('error.message', error.message);
    throw error;
  } finally {
    span.finish();
  }
}
```

### 2. Python APM
```python
# examples/instrumentation/python-apm.py
from ddtrace import tracer
from ddtrace.contrib.flask import TraceMiddleware
from flask import Flask

# Initialize tracer
tracer.configure(
    service='myapp',
    env='production',
    version='1.0.0'
)

app = Flask(__name__)

# Use tracer middleware
TraceMiddleware(app, tracer, service='myapp')

# Custom spans
@tracer.wrap(service='myapp', resource='process_data')
def process_data(data):
    with tracer.trace('process.business_logic') as span:
        span.set_tag('data.size', len(data))
        # Your business logic here
        return business_logic(data)
```

## 🚀 Deployment Scripts

### 1. Install Datadog
```bash
#!/bin/bash
# scripts/install-datadog.sh

echo "Installing Datadog..."

# Create namespace
kubectl create namespace datadog

# Create secret
kubectl create secret generic datadog-secret \
  --from-literal=api-key=$DATADOG_API_KEY \
  --namespace=datadog

# Apply RBAC
kubectl apply -f kubernetes/datadog-agent/rbac.yaml

# Deploy Datadog Agent
kubectl apply -f kubernetes/datadog-agent/

# Deploy Cluster Agent
kubectl apply -f kubernetes/datadog-agent/cluster-agent.yaml

# Wait for deployment
kubectl wait --for=condition=ready pod -l app=datadog-agent -n datadog --timeout=300s

echo "Datadog installation completed"
```

### 2. Configure Monitoring
```bash
#!/bin/bash
# scripts/configure-monitoring.sh

echo "Configuring Datadog monitoring..."

# Apply custom metrics
kubectl apply -f configurations/datadog-agent/

# Create dashboards
curl -X POST "https://api.datadoghq.com/api/v1/dashboard" \
  -H "Content-Type: application/json" \
  -H "DD-API-KEY: $DATADOG_API_KEY" \
  -d @configurations/dashboards/myapp-dashboard.json

# Create monitors
curl -X POST "https://api.datadoghq.com/api/v1/monitor" \
  -H "Content-Type: application/json" \
  -H "DD-API-KEY: $DATADOG_API_KEY" \
  -d @configurations/monitors/high-cpu-monitor.json

echo "Monitoring configuration completed"
```

## 📋 Best Practices

### 1. Monitoring Strategy
- Set up comprehensive dashboards
- Implement proper alerting
- Use custom metrics effectively
- Monitor application performance

### 2. Cost Optimization
- Optimize log collection
- Use appropriate sampling rates
- Implement data retention policies
- Monitor usage and costs

### 3. Security
- Secure API keys
- Implement access controls
- Use secure communication
- Regular security audits

---

**Ready to master Datadog?** Start with basic agent setup and work your way up to comprehensive monitoring!
