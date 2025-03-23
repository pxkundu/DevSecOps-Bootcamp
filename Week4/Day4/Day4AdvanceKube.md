## Week 4, Day 4: Advanced Kubernetes

### Overview
Day 4 elevates your Kubernetes skills with advanced concepts like Ingress, Horizontal Pod Autoscaling (HPA), ConfigMaps, Secrets, and RBAC (Role-Based Access Control). You’ll enhance the Message Encoder/Decoder app (or CRM microservices) on EKS, adding scalability, configuration management, and security. These skills reflect practices at companies like Netflix, Google, and Salesforce, where Kubernetes powers mission-critical workloads.

### Learning Objectives
- Implement Ingress for efficient traffic routing.
- Use HPA for automatic scaling based on load.
- Manage configurations with ConfigMaps and Secrets.
- Secure clusters with RBAC.
- Integrate with CI/CD pipelines (Jenkins) for production readiness.

### Prerequisites
- Day 3’s Kubernetes setup (`MessageEncoderDecoderK8s` or `CRMTerraformJenkins` with EKS).
- Tools: `kubectl`, `aws cli`, `eksctl`, Helm (`brew install helm` for macOS).
- Docker images in ECR (e.g., `encoder-frontend`, `encoder-backend`).

### Time Allocation
- **Theory**: 2 hours (for depth)
- **Practical**: 2 hours (hands-on implementation)
- **Total**: 4 hours

---

### Theoretical Explanation

#### Key Concepts & Keywords
1. **Ingress**:
   - **Definition**: A Kubernetes resource managing external HTTP/HTTPS traffic, routing to Services via rules (e.g., domain, path).
   - **Components**: Requires an Ingress Controller (e.g., NGINX, ALB).
   - **Features**: Load balancing, SSL termination, path-based routing.
   - **Why**: Replaces multiple LoadBalancer Services, reducing costs and complexity.

2. **Horizontal Pod Autoscaling (HPA)**:
   - **Definition**: Automatically scales Pod replicas based on metrics (e.g., CPU, memory).
   - **Mechanism**: Uses Metrics Server to monitor resource usage.
   - **Syntax**: `minReplicas`, `maxReplicas`, `targetCPUUtilizationPercentage`.
   - **Why**: Ensures performance under load without manual intervention.

3. **ConfigMap**:
   - **Definition**: A key-value store for non-sensitive configuration data (e.g., env vars, config files).
   - **Usage**: Mounted as volumes or env vars in Pods.
   - **Why**: Decouples config from code, enabling runtime changes.

4. **Secret**:
   - **Definition**: A secure key-value store for sensitive data (e.g., passwords, API keys).
   - **Features**: Base64-encoded, mounted as volumes or env vars.
   - **Why**: Enhances security by separating secrets from app code.

5. **Role-Based Access Control (RBAC)**:
   - **Definition**: Controls access to Kubernetes resources using Roles, RoleBindings, ClusterRoles, and ClusterRoleBindings.
   - **Components**:
     - **Role**: Namespace-scoped permissions.
     - **ClusterRole**: Cluster-wide permissions.
     - **Binding**: Links Roles to users/service accounts.
   - **Why**: Enforces least privilege, critical for multi-team security.

6. **Metrics Server**:
   - **Definition**: A cluster-wide aggregator of resource usage data (CPU, memory).
   - **Why**: Enables HPA and monitoring tools (e.g., Prometheus).

7. **Helm**:
   - **Definition**: A package manager for Kubernetes, templating manifests into charts.
   - **Why**: Simplifies deployment of complex apps (e.g., Ingress controllers).

#### Why Advanced Kubernetes Matters
- **Scalability**: HPA handles traffic spikes (e.g., Black Friday for e-commerce).
- **Efficiency**: Ingress optimizes external access vs. multiple LoadBalancers.
- **Security**: Secrets and RBAC protect sensitive data and access.
- **Maintainability**: ConfigMaps and Helm streamline updates across teams.

#### Best Practices
- Use Ingress for all external traffic.
- Set resource limits/requests with HPA for stability.
- Store configs in ConfigMaps, secrets in Secrets, not hardcoded.
- Restrict RBAC to specific namespaces/teams.
- Version Helm charts for reproducibility.

---

### Practical Use Cases & Real-World Applications

#### Practical Activity Plan
- **Objective**: Enhance the Message Encoder/Decoder app on EKS with advanced K8s features.
- **Setup**: Use `CRMTerraformJenkins` EKS cluster (`dev-us`) or adapt `MessageEncoderDecoderK8s` to EKS.
- **Tasks**:
  1. **Install Metrics Server**: Enable HPA.
  2. **Configure Ingress**: Route traffic to frontend/backend.
  3. **Add HPA**: Scale backend on CPU load.
  4. **Use ConfigMap/Secret**: Manage API settings and keys.
  5. **Implement RBAC**: Restrict access to `dev-us` namespace.
- **Outcome**: A production-ready, scalable, secure app.

#### Real-World Use Case 1: E-Commerce Traffic Management (Amazon)
- **Scenario**: Amazon manages a shopping app during peak sales (e.g., Prime Day).
- **Context**: Needs efficient routing and auto-scaling for millions of users.
- **Theoretical Application**:
  - **Ingress**: Routes `shop.amazon.com/api` to backend, `shop.amazon.com` to frontend.
  - **HPA**: Scales API Pods from 5 to 50 at 70% CPU.
  - **ConfigMap**: Stores discount configs.
  - **Secret**: Holds payment API keys.
  - **RBAC**: Limits ops team to `prod` namespace.
- **Practical Workflow**:
  - Deploy Ingress:
    ```yaml
    apiVersion: networking.k8s.io/v1
    kind: Ingress
    metadata:
      name: shop-ingress
      annotations:
        nginx.ingress.kubernetes.io/rewrite-target: /
    spec:
      rules:
      - host: "shop.local"
        http:
          paths:
          - path: /api
            pathType: Prefix
            backend:
              service:
                name: shop-api-service
                port:
                  number: 80
          - path: /
            pathType: Prefix
            backend:
              service:
                name: shop-frontend-service
                port:
                  number: 80
    ```
  - HPA:
    ```bash
    kubectl autoscale deployment shop-api --cpu-percent=70 --min=5 --max=50
    ```
  - Outcome: Handles 10M requests/sec with zero downtime.
- **DevOps Impact**: 
  - Saves costs vs. over-provisioning.
  - Ensures uptime during sales spikes.

#### Real-World Use Case 2: Netflix Streaming Optimization
- **Scenario**: Netflix scales video streaming microservices globally.
- **Context**: Requires secure config and team-specific access.
- **Theoretical Application**:
  - **Ingress**: Routes `streaming.netflix.com` to edge services.
  - **HPA**: Scales transcoders at 80% CPU.
  - **ConfigMap**: Defines bitrate settings.
  - **Secret**: Stores DRM keys.
  - **RBAC**: Grants dev team `read-only` in `staging`.
- **Practical Workflow**:
  - ConfigMap:
    ```yaml
    apiVersion: v1
    kind: ConfigMap
    metadata:
      name: stream-config
    data:
      bitrate: "4Mbps"
    ```
  - Secret:
    ```bash
    kubectl create secret generic drm-keys --from-literal=key=abc123
    ```
  - RBAC Role:
    ```yaml
    apiVersion: rbac.authorization.k8s.io/v1
    kind: Role
    metadata:
      namespace: staging
      name: dev-read
    rules:
    - apiGroups: [""]
      resources: ["pods"]
      verbs: ["get", "list"]
    ```
  - Outcome: Streams to 200M users, secure and scalable.
- **DevOps Impact**: 
  - Auto-scales for Super Bowl traffic.
  - Secures sensitive data.

#### Real-World Use Case 3: Your Encoder/Decoder App
- **Scenario**: Enhance Day 3’s app on EKS for production.
- **Context**: Add scalability and security for enterprise use.
- **Theoretical Application**:
  - **Ingress**: Routes `encoder.local` to frontend/backend.
  - **HPA**: Scales backend at 60% CPU.
  - **ConfigMap**: Sets max message length.
  - **Secret**: Stores an API token.
  - **RBAC**: Limits devs to `dev-us`.
- **Practical Workflow**:
  - See implementation below.
- **DevOps Impact**: 
  - Scales for 1000s of users.
  - Secures app for team collaboration.

---

### Lesson Plan Details

#### Theory Session (2 hr)
- **Topics**:
  1. **Ingress & Controllers (30 min)**:
     - Why Ingress over LoadBalancer.
     - NGINX vs. ALB controllers.
  2. **HPA & Metrics (40 min)**:
     - Metrics Server setup.
     - CPU/memory-based scaling.
  3. **ConfigMaps & Secrets (30 min)**:
     - Use cases (env vars, files).
     - Security best practices.
  4. **RBAC Basics (20 min)**:
     - Roles vs. ClusterRoles.
     - Binding to users/service accounts.
- **Delivery**: Slides, demo of `kubectl apply -f ingress.yaml`.

#### Practical Session (2 hr)
- **Activity**: Enhance Encoder/Decoder on EKS.
- **Steps**:
  1. **Setup (20 min)**:
     - Connect to EKS: `aws eks update-kubeconfig --name dev-us-crm-us-east-1 --region us-east-1`.
     - Install Metrics Server:
       ```bash
       kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
       ```
     - Install NGINX Ingress Controller via Helm:
       ```bash
       helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
       helm install nginx-ingress ingress-nginx/ingress-nginx --namespace ingress-nginx --create-namespace
       ```
  2. **Ingress & Config (50 min)**:
     - `k8s/config.yaml`:
       ```yaml
       apiVersion: v1
       kind: ConfigMap
       metadata:
         name: encoder-config
         namespace: dev-us
       data:
         max_length: "100"
       ---
       apiVersion: v1
       kind: Secret
       metadata:
         name: encoder-secret
         namespace: dev-us
       type: Opaque
       data:
         api_token: YWJjMTIz  # echo -n "abc123" | base64
       ```
     - Update `frontend-deployment.yaml`:
       ```yaml
       spec:
         template:
           spec:
             containers:
             - name: encoder-frontend
               image: <your-ecr>/dev-us-encoder-frontend:latest
               env:
               - name: MAX_LENGTH
                 valueFrom:
                   configMapKeyRef:
                     name: encoder-config
                     key: max_length
               - name: API_TOKEN
                 valueFrom:
                   secretKeyRef:
                     name: encoder-secret
                     key: api_token
       ```
     - `k8s/ingress.yaml`:
       ```yaml
       apiVersion: networking.k8s.io/v1
       kind: Ingress
       metadata:
         name: encoder-ingress
         namespace: dev-us
         annotations:
           nginx.ingress.kubernetes.io/rewrite-target: /
       spec:
         ingressClassName: nginx
         rules:
         - host: "encoder.local"
           http:
             paths:
             - path: /
               pathType: Prefix
               backend:
                 service:
                   name: encoder-frontend-service
                   port:
                     number: 80
             - path: /api
               pathType: Prefix
               backend:
                 service:
                   name: blog-backend-service
                   port:
                     number: 4000
       ```
  3. **HPA & RBAC (50 min)**:
     - `k8s/hpa.yaml`:
       ```yaml
       apiVersion: autoscaling/v2
       kind: HorizontalPodAutoscaler
       metadata:
         name: encoder-backend-hpa
         namespace: dev-us
       spec:
         scaleTargetRef:
           apiVersion: apps/v1
           kind: Deployment
           name: encoder-backend
         minReplicas: 2
         maxReplicas: 10
         metrics:
         - type: Resource
           resource:
             name: cpu
             target:
               type: Utilization
               averageUtilization: 60
       ```
     - `k8s/rbac.yaml`:
       ```yaml
       apiVersion: rbac.authorization.k8s.io/v1
       kind: Role
       metadata:
         namespace: dev-us
         name: dev-access
       rules:
       - apiGroups: [""]
         resources: ["pods", "services"]
         verbs: ["get", "list"]
       ---
       apiVersion: rbac.authorization.k8s.io/v1
       kind: RoleBinding
       metadata:
         name: dev-binding
         namespace: dev-us
       subjects:
       - kind: User
         name: "dev-user"
         apiGroup: rbac.authorization.k8s.io
       roleRef:
         kind: Role
         name: dev-access
         apiGroup: rbac.authorization.k8s.io
       ```
     - Apply:
       ```bash
       kubectl apply -f k8s/config.yaml
       kubectl apply -f k8s/frontend-deployment.yaml
       kubectl apply -f k8s/backend-deployment.yaml
       kubectl apply -f k8s/ingress.yaml
       kubectl apply -f k8s/hpa.yaml
       kubectl apply -f k8s/rbac.yaml
       ```
  4. **Verify (20 min)**:
     - `kubectl get ingress -n dev-us`: Get Ingress IP.
     - `kubectl get hpa -n dev-us`: Check scaling.
     - Test: `curl http://<ingress-ip>` or update `/etc/hosts` with `encoder.local`.

---

### Assessment
- **Quiz**: 
  - What’s the difference between Ingress and LoadBalancer?
  - How does HPA use Metrics Server?
- **Hands-On**: 
  - Show HPA scaling: `kubectl get pods -n dev-us -w`.
  - Verify RBAC: `kubectl auth can-i get pods -n dev-us --as=dev-user`.

---

### Real-World Alignment
- **Amazon**: Uses Ingress and HPA for e-commerce scaling.
- **Netflix**: Secures streaming with Secrets and RBAC.
- **Your App**: Prepares for enterprise-grade encoding/decoding.
