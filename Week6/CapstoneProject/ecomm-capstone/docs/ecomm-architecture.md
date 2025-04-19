# Secure, Scalable E-commerce Platform on AWS EKS

## Overview
A microservices-based retail application on AWS EKS, designed to manage 10,000+ products and scale to 100K+ transactions/day during peak seasons (e.g., holiday sales). This capstone project embeds DevSecOps best practices and Kubernetes industry standards for security, scalability, and resilience.

## Features
1. **Secure Product Browsing**
   - **Description**: React frontend for browsing 10,000+ products.
   - **DevSecOps**: TLS on ALB Ingress, X-Ray tracing for latency, RBAC for pod access.
   - **Why**: Ensures secure, observable user experience (e.g., Amazon’s retail frontend).
2. **Inventory and Order Management**
   - **Description**: Node.js API for stock updates and orders (100K+ txns/day).
   - **DevSecOps**: Secrets Manager for credentials, HPA scaling, Network Policies.
   - **Why**: Balances security and scalability (e.g., Walmart’s 500M+ txns).
3. **Persistent Data Storage**
   - **Description**: RDS MySQL for product/order data.
   - **DevSecOps**: KMS encryption, private subnet, CloudWatch monitoring.
   - **Why**: Meets compliance and reliability (e.g., Netflix’s DB).
4. **Log and Asset Storage**
   - **Description**: S3 for logs and static assets.
   - **DevSecOps**: Encrypted bucket, IAM pod access, lifecycle to Glacier (30 days).
   - **Why**: Cost-efficient, secure storage (e.g., Amazon’s S3).
5. **Dynamic Scaling**
   - **Description**: Scales to 10K+ users during peaks.
   - **DevSecOps**: Karpenter for nodes, HPA for pods, rolling updates.
   - **Why**: Handles Black Friday-like spikes (e.g., Walmart’s 46M items).
6. **Observability Dashboard**
   - **Description**: Real-time metrics (CPU, orders/min).
   - **DevSecOps**: CloudWatch metrics, X-Ray tracing, custom dashboard.
   - **Why**: Proactive issue detection (e.g., Netflix’s 17B+ hours).

## Architecture Design
### EKS Cluster
- **Nodes**: 2 t4g.medium (Graviton2) across 3 AZs (us-east-1a/b/c).
- **Namespace**: prod.
- **Scaling**: Karpenter for node auto-scaling.
- **Diagram**:
```
[EKS Cluster]
  ├── Node 1 (t4g.medium, us-east-1a)
  ├── Node 2 (t4g.medium, us-east-1b)
  └── Karpenter (us-east-1c, scales nodes)
```

### Microservices
- **Frontend**: React, 5 replicas, requests: {cpu: "200m", memory: "256Mi"}, limits: {cpu: "500m", memory: "512Mi"}, anti-affinity.
- **Backend**: Node.js API (/inventory, /orders), same specs.
- **Diagram**:
```
[prod Namespace]
  ├── Frontend Deployment (5 pods)
  │   ├── Pod 1 (t4g.medium, us-east-1a)
  │   └── Pod 2 (t4g.medium, us-east-1b)
  └── Backend Deployment (5 pods)
      ├── Pod 1 (t4g.medium, us-east-1a)
      └── Pod 2 (t4g.medium, us-east-1c)
```

### Networking
- **ALB Ingress**: TLS-enabled, routes to frontend/backend.
- **Network Policy**: Allows frontend-to-backend only.
- **Diagram**:
```
[Users] → [ALB Ingress (TLS)]
          ├── Frontend Service (ClusterIP)
          └── Backend Service (ClusterIP)
              └── Network Policy (allow frontend → backend)
```

### Storage
- **RDS MySQL**: KMS-encrypted, private subnet.
- **S3**: Encrypted, lifecycle to Glacier.
- **Diagram**:
```
[EKS Cluster]
  ├── Backend Pods → [RDS MySQL (KMS, private subnet)]
  └── Pods → [S3 Bucket (encrypted, lifecycle)]
```

### Scaling
- **HPA**: CPU > 80%, min 2, max 10 pods.
- **Karpenter**: Node scaling on demand.
- **Diagram**:
```
[Workload Spike]
  ├── HPA → Scales pods (2 → 10)
  └── Karpenter → Adds nodes (2 → 4)
```

### Security
- **RBAC**: Limits prod namespace access.
- **OPA Gatekeeper**: Denies privileged pods.
- **Secrets Manager**: Stores RDS credentials.
- **ECR**: Image scanning enabled.

### Observability
- **CloudWatch**: EKS metrics (CPU, memory), custom metric (orders/min).
- **X-Ray**: Traces API calls.
- **Dashboard**: Visualizes latency, CPU, orders.

## Tool Swap
- **Initial Plan**: Jenkins CI/CD (build Docker, deploy to EKS).
- **Swapped To**: GitHub Actions (simpler, Git-native).
- **Trade-offs**:
  - **Jenkins**: Robust plugins, complex setup.
  - **GitHub Actions**: Lightweight, faster, fewer enterprise features.
- **Why**: Reflects real-world agility (e.g., Netflix’s Spinnaker shift).

## Why This Design
- **Industry Standard**: Mirrors Amazon’s EKS (1M+ customers), Netflix’s scaling (247M subscribers).
- **DevSecOps**: Security (RBAC, TLS), automation (Terraform), resilience (HA, Karpenter).
- **Reference**: Comprehensive blueprint for future Kubernetes projects.
