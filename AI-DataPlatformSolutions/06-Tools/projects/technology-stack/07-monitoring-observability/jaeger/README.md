# Jaeger - Distributed Tracing

## 🔍 Overview
Jaeger provides distributed tracing for microservices, helping you monitor and troubleshoot complex distributed systems in DevSecOps environments.

## 📁 Directory Structure

```
jaeger/
├── README.md
├── configurations/
│   ├── jaeger-config.yaml
│   └── sampling-config.yaml
├── kubernetes/
│   ├── jaeger-operator/
│   └── jaeger-deployment/
└── examples/
    ├── tracing-examples/
    └── instrumentation/
```

## 🛠️ Jaeger Configuration

### 1. Jaeger Configuration
```yaml
# configurations/jaeger-config.yaml
apiVersion: jaegertracing.io/v1
kind: Jaeger
metadata:
  name: jaeger
spec:
  strategy: production
  collector:
    maxReplicas: 5
    resources:
      limits:
        cpu: 500m
        memory: 512Mi
      requests:
        cpu: 100m
        memory: 128Mi
  query:
    replicas: 2
    resources:
      limits:
        cpu: 200m
        memory: 256Mi
      requests:
        cpu: 100m
        memory: 128Mi
  storage:
    type: elasticsearch
    elasticsearch:
      nodeCount: 3
      storage:
        storageClassName: "fast-ssd"
        size: 50Gi
      resources:
        requests:
          cpu: 1000m
          memory: 1Gi
        limits:
          cpu: 2000m
          memory: 2Gi
```

### 2. Sampling Configuration
```yaml
# configurations/sampling-config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: jaeger-sampling-config
data:
  sampling: |
    {
      "default_strategy": {
        "type": "probabilistic",
        "param": 0.1
      },
      "per_operation_strategies": [
        {
          "operation": "health-check",
          "type": "probabilistic",
          "param": 0.0
        },
        {
          "operation": "metrics",
          "type": "probabilistic",
          "param": 0.0
        }
      ]
    }
```

## ☸️ Kubernetes Deployment

### 1. Jaeger Operator
```yaml
# kubernetes/jaeger-operator/jaeger-operator.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: jaeger-operator
  namespace: jaeger-system
spec:
  replicas: 1
  selector:
    matchLabels:
      name: jaeger-operator
  template:
    metadata:
      labels:
        name: jaeger-operator
    spec:
      serviceAccountName: jaeger-operator
      containers:
      - name: jaeger-operator
        image: jaegertracing/jaeger-operator:1.35.0
        ports:
        - containerPort: 8080
        env:
        - name: WATCH_NAMESPACE
          value: ""
        - name: POD_NAME
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
        - name: OPERATOR_NAME
          value: "jaeger-operator"
```

### 2. Jaeger Deployment
```yaml
# kubernetes/jaeger-deployment/jaeger.yaml
apiVersion: jaegertracing.io/v1
kind: Jaeger
metadata:
  name: jaeger
  namespace: default
spec:
  strategy: production
  collector:
    maxReplicas: 5
    resources:
      limits:
        cpu: 500m
        memory: 512Mi
      requests:
        cpu: 100m
        memory: 128Mi
  query:
    replicas: 2
    resources:
      limits:
        cpu: 200m
        memory: 256Mi
      requests:
        cpu: 100m
        memory: 128Mi
  storage:
    type: elasticsearch
    elasticsearch:
      nodeCount: 3
      storage:
        storageClassName: "fast-ssd"
        size: 50Gi
```

## 🔧 Application Instrumentation

### 1. Node.js Example
```javascript
// examples/instrumentation/nodejs-tracing.js
const jaeger = require('jaeger-client');
const opentracing = require('opentracing');

// Initialize Jaeger tracer
const config = {
  serviceName: 'myapp',
  sampler: {
    type: 'const',
    param: 1,
  },
  reporter: {
    logSpans: true,
    agentHost: 'jaeger-agent',
    agentPort: 6832,
  },
};

const tracer = jaeger.initTracer(config);

// Create spans
function createSpan(operationName, parentSpan = null) {
  const span = tracer.startSpan(operationName, {
    childOf: parentSpan,
    tags: {
      'service.name': 'myapp',
      'operation.name': operationName,
    },
  });
  
  return span;
}

// Example usage
function processRequest(req, res) {
  const span = createSpan('processRequest');
  
  try {
    // Your business logic here
    span.setTag('http.method', req.method);
    span.setTag('http.url', req.url);
    
    // Create child span
    const childSpan = createSpan('databaseQuery', span);
    // Database operation
    childSpan.finish();
    
    res.json({ success: true });
  } catch (error) {
    span.setTag('error', true);
    span.log({ event: 'error', message: error.message });
    res.status(500).json({ error: error.message });
  } finally {
    span.finish();
  }
}
```

### 2. Python Example
```python
# examples/instrumentation/python-tracing.py
from jaeger_client import Config
import opentracing
from opentracing_instrumentation.client_hooks import install_all_patches

# Initialize Jaeger tracer
def init_tracer(service_name):
    config = Config(
        config={
            'sampler': {
                'type': 'const',
                'param': 1,
            },
            'logging': True,
        },
        service_name=service_name,
        validate=True,
    )
    return config.initialize_tracer()

# Initialize tracer
tracer = init_tracer('myapp')

# Install instrumentation
install_all_patches()

# Example usage
def process_request():
    with tracer.start_span('process_request') as span:
        span.set_tag('service.name', 'myapp')
        span.set_tag('operation.name', 'process_request')
        
        # Create child span
        with tracer.start_span('database_query', child_of=span) as child_span:
            # Database operation
            child_span.set_tag('db.statement', 'SELECT * FROM users')
            pass
        
        span.set_tag('http.status_code', 200)
```

## 🚀 Deployment Scripts

### 1. Install Jaeger
```bash
#!/bin/bash
# scripts/install-jaeger.sh

echo "Installing Jaeger..."

# Create namespace
kubectl create namespace jaeger-system

# Install Jaeger Operator
kubectl apply -f kubernetes/jaeger-operator/

# Wait for operator to be ready
kubectl wait --for=condition=ready pod -l name=jaeger-operator -n jaeger-system --timeout=300s

# Deploy Jaeger
kubectl apply -f kubernetes/jaeger-deployment/

# Wait for Jaeger to be ready
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=jaeger -n default --timeout=300s

echo "Jaeger installation completed"
```

### 2. Configure Sampling
```bash
#!/bin/bash
# scripts/configure-sampling.sh

echo "Configuring Jaeger sampling..."

# Apply sampling configuration
kubectl apply -f configurations/sampling-config.yaml

# Update Jaeger configuration
kubectl patch jaeger jaeger --type='merge' -p='{"spec":{"collector":{"options":{"sampling":{"strategies":[{"type":"probabilistic","param":0.1}]}}}}}'

echo "Sampling configuration completed"
```

## 📊 Monitoring and Dashboards

### 1. Grafana Dashboard
```json
{
  "dashboard": {
    "title": "Jaeger Tracing Dashboard",
    "panels": [
      {
        "title": "Traces per Second",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(jaeger_traces_received_total[5m])",
            "legendFormat": "Traces/sec"
          }
        ]
      },
      {
        "title": "Error Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(jaeger_traces_received_total{level=\"error\"}[5m]) / rate(jaeger_traces_received_total[5m])",
            "legendFormat": "Error Rate"
          }
        ]
      }
    ]
  }
}
```

### 2. Prometheus Metrics
```yaml
# kubernetes/jaeger-deployment/jaeger-metrics.yaml
apiVersion: v1
kind: ServiceMonitor
metadata:
  name: jaeger-metrics
spec:
  selector:
    matchLabels:
      app.kubernetes.io/name: jaeger
  endpoints:
  - port: 14269
    path: /metrics
```

## 📋 Best Practices

### 1. Tracing Strategy
- Use appropriate sampling rates
- Implement trace context propagation
- Add meaningful tags and logs
- Monitor trace performance

### 2. Performance
- Optimize sampling configuration
- Use async reporting
- Monitor trace storage
- Implement trace retention

### 3. Security
- Secure trace data
- Implement access controls
- Use TLS for communication
- Regular security updates

---

**Ready to master Jaeger?** Start with basic tracing setup and work your way up to comprehensive distributed tracing!
