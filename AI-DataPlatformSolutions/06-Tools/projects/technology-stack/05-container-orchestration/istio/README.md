# Istio - Service Mesh Platform

## 🕸️ Overview
Istio is a service mesh that provides traffic management, security, and observability for microservices. This section covers practical implementation of Istio in DevSecOps environments.

## 📁 Directory Structure

```
istio/
├── README.md
├── configurations/
│   ├── gateway/
│   ├── virtual-services/
│   └── destination-rules/
├── security/
│   ├── authentication/
│   ├── authorization/
│   └── mTLS/
└── monitoring/
    ├── telemetry/
    └── dashboards/
```

## 🛠️ Essential Istio Configurations

### 1. Gateway Configuration
```yaml
# configurations/gateway/myapp-gateway.yaml
apiVersion: networking.istio.io/v1alpha3
kind: Gateway
metadata:
  name: myapp-gateway
spec:
  selector:
    istio: ingressgateway
  servers:
  - port:
      number: 80
      name: http
      protocol: HTTP
    hosts:
    - myapp.example.com
    tls:
      httpsRedirect: true
  - port:
      number: 443
      name: https
      protocol: HTTPS
    hosts:
    - myapp.example.com
    tls:
      mode: SIMPLE
      credentialName: myapp-tls
```

### 2. Virtual Service
```yaml
# configurations/virtual-services/myapp-vs.yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: myapp-vs
spec:
  hosts:
  - myapp.example.com
  gateways:
  - myapp-gateway
  http:
  - match:
    - uri:
        prefix: /api
    route:
    - destination:
        host: myapp-service
        port:
          number: 3000
    timeout: 30s
    retries:
      attempts: 3
      perTryTimeout: 10s
  - match:
    - uri:
        prefix: /
    route:
    - destination:
        host: myapp-frontend
        port:
          number: 80
```

### 3. Destination Rules
```yaml
# configurations/destination-rules/myapp-dr.yaml
apiVersion: networking.istio.io/v1alpha3
kind: DestinationRule
metadata:
  name: myapp-dr
spec:
  host: myapp-service
  trafficPolicy:
    loadBalancer:
      simple: ROUND_ROBIN
    connectionPool:
      tcp:
        maxConnections: 100
      http:
        http1MaxPendingRequests: 10
        maxRequestsPerConnection: 2
    circuitBreaker:
      consecutiveErrors: 3
      interval: 30s
      baseEjectionTime: 30s
```

## 🔒 Security Configurations

### 1. mTLS Configuration
```yaml
# security/mTLS/peer-authentication.yaml
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: istio-system
spec:
  mtls:
    mode: STRICT
---
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: myapp-mtls
  namespace: default
spec:
  selector:
    matchLabels:
      app: myapp
  mtls:
    mode: STRICT
```

### 2. Authorization Policy
```yaml
# security/authorization/auth-policy.yaml
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: myapp-auth
spec:
  selector:
    matchLabels:
      app: myapp
  rules:
  - from:
    - source:
        principals: ["cluster.local/ns/default/sa/myapp-frontend"]
    to:
    - operation:
        methods: ["GET", "POST"]
        paths: ["/api/*"]
  - from:
    - source:
        namespaces: ["monitoring"]
    to:
    - operation:
        methods: ["GET"]
        paths: ["/metrics"]
```

## 📊 Monitoring and Observability

### 1. Telemetry Configuration
```yaml
# monitoring/telemetry/telemetry.yaml
apiVersion: telemetry.istio.io/v1alpha1
kind: Telemetry
metadata:
  name: myapp-telemetry
spec:
  metrics:
  - providers:
    - name: prometheus
  - overrides:
    - match:
        metric: ALL_METRICS
      tagOverrides:
        request_protocol:
          value: "http"
  tracing:
  - providers:
    - name: jaeger
  - randomSamplingPercentage: 10.0
```

### 2. Access Logging
```yaml
# monitoring/telemetry/access-logging.yaml
apiVersion: telemetry.istio.io/v1alpha1
kind: Telemetry
metadata:
  name: myapp-access-logging
spec:
  accessLogging:
  - providers:
    - name: otel
  - match:
      mode: CLIENT_AND_SERVER
```

## 🚀 Deployment Scripts

### 1. Install Istio
```bash
#!/bin/bash
# scripts/install-istio.sh

# Download Istio
curl -L https://istio.io/downloadIstio | sh -
cd istio-*

# Install Istio
./bin/istioctl install --set values.defaultRevision=default

# Verify installation
kubectl get pods -n istio-system

# Enable sidecar injection
kubectl label namespace default istio-injection=enabled
```

### 2. Deploy Application
```bash
#!/bin/bash
# scripts/deploy-app.sh

# Deploy application with Istio
kubectl apply -f configurations/gateway/
kubectl apply -f configurations/virtual-services/
kubectl apply -f configurations/destination-rules/
kubectl apply -f security/
kubectl apply -f monitoring/

# Verify deployment
kubectl get gateway,virtualservice,destinationrule
```

## 📋 Best Practices

### 1. Service Mesh
- Use sidecar injection for microservices
- Implement proper traffic management
- Configure circuit breakers and retries
- Set up proper load balancing

### 2. Security
- Enable mTLS for service-to-service communication
- Implement proper authorization policies
- Use JWT for authentication
- Regular security audits

### 3. Observability
- Enable distributed tracing
- Configure metrics collection
- Set up proper logging
- Monitor service mesh health

---

**Ready to master Istio?** Start with basic gateway configuration and work your way up to advanced service mesh patterns!
