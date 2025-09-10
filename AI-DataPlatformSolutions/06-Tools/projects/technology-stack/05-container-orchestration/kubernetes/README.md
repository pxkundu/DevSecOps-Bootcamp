# Kubernetes - Container Orchestration Platform

## ☸️ Overview
This section covers comprehensive Kubernetes implementation for DevSecOps container orchestration. It includes Kubernetes fundamentals, advanced features, security, monitoring, and best practices for enterprise-grade container management.

## 🏗️ Kubernetes Architecture

```mermaid
graph TB
    subgraph "Kubernetes Cluster"
        A[Control Plane] --> B[Worker Nodes]
        B --> C[Pods]
        C --> D[Containers]
        
        E[API Server] --> A
        F[etcd] --> A
        G[Scheduler] --> A
        H[Controller Manager] --> A
        I[kubelet] --> B
        J[kube-proxy] --> B
        K[Container Runtime] --> B
        L[Pods] --> C
        M[Services] --> C
        N[Volumes] --> C
    end
```

## 📁 Directory Structure

```
kubernetes/
├── README.md
├── manifests/
│   ├── deployments/
│   ├── services/
│   ├── ingress/
│   └── configmaps/
├── helm-charts/
│   ├── myapp/
│   ├── monitoring/
│   └── security/
├── operators/
│   ├── custom-resources/
│   └── controllers/
└── best-practices/
    ├── security/
    ├── performance/
    ├── monitoring/
    └── troubleshooting/
```

## 🛠️ Kubernetes Fundamentals

### 1. Basic Pod Configuration
```yaml
# manifests/pods/basic-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-pod
  labels:
    app: nginx
    tier: frontend
spec:
  containers:
  - name: nginx
    image: nginx:1.21
    ports:
    - containerPort: 80
    resources:
      requests:
        memory: "64Mi"
        cpu: "250m"
      limits:
        memory: "128Mi"
        cpu: "500m"
    env:
    - name: ENV_VAR
      value: "production"
    volumeMounts:
    - name: nginx-config
      mountPath: /etc/nginx/conf.d
  volumes:
  - name: nginx-config
    configMap:
      name: nginx-config
```

### 2. Deployment Configuration
```yaml
# manifests/deployments/web-app.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
  labels:
    app: web-app
    tier: frontend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web-app
  template:
    metadata:
      labels:
        app: web-app
        tier: frontend
    spec:
      containers:
      - name: web-app
        image: nginx:1.21
        ports:
        - containerPort: 80
        resources:
          requests:
            memory: "64Mi"
            cpu: "250m"
          limits:
            memory: "128Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 80
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 80
          initialDelaySeconds: 5
          periodSeconds: 5
        env:
        - name: NODE_ENV
          value: "production"
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: web-app-secrets
              key: database-url
        volumeMounts:
        - name: app-config
          mountPath: /etc/app
        - name: logs
          mountPath: /var/log/app
      volumes:
      - name: app-config
        configMap:
          name: web-app-config
      - name: logs
        emptyDir: {}
      restartPolicy: Always
```

### 3. Service Configuration
```yaml
# manifests/services/web-app-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: web-app-service
  labels:
    app: web-app
spec:
  selector:
    app: web-app
  ports:
  - name: http
    port: 80
    targetPort: 80
    protocol: TCP
  - name: https
    port: 443
    targetPort: 443
    protocol: TCP
  type: ClusterIP
---
apiVersion: v1
kind: Service
metadata:
  name: web-app-loadbalancer
  labels:
    app: web-app
spec:
  selector:
    app: web-app
  ports:
  - name: http
    port: 80
    targetPort: 80
    protocol: TCP
  type: LoadBalancer
  loadBalancerIP: 10.0.0.100
```

### 4. Ingress Configuration
```yaml
# manifests/ingress/web-app-ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: web-app-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/force-ssl-redirect: "true"
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
spec:
  tls:
  - hosts:
    - webapp.example.com
    secretName: webapp-tls
  rules:
  - host: webapp.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: web-app-service
            port:
              number: 80
  - host: api.example.com
    http:
      paths:
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: api-service
            port:
              number: 8080
```

### 5. ConfigMap and Secret
```yaml
# manifests/configmaps/web-app-config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: web-app-config
  labels:
    app: web-app
data:
  nginx.conf: |
    server {
        listen 80;
        server_name _;
        
        location / {
            root /usr/share/nginx/html;
            index index.html;
        }
        
        location /health {
            access_log off;
            return 200 "healthy\n";
            add_header Content-Type text/plain;
        }
    }
  app.properties: |
    server.port=8080
    spring.profiles.active=production
    logging.level.root=INFO
---
apiVersion: v1
kind: Secret
metadata:
  name: web-app-secrets
  labels:
    app: web-app
type: Opaque
data:
  database-url: cG9zdGdyZXNxbDovL3VzZXI6cGFzc3dvcmRAbG9jYWxob3N0OjU0MzIvbXlkYg==
  api-key: YWJjZGVmZ2hpams=
stringData:
  database-url: postgresql://user:password@localhost:5432/mydb
  api-key: abcdefghijk
```

## 🔧 Advanced Kubernetes Features

### 1. StatefulSet
```yaml
# manifests/statefulsets/database.yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres
  labels:
    app: postgres
spec:
  serviceName: postgres
  replicas: 3
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:13
        ports:
        - containerPort: 5432
        env:
        - name: POSTGRES_DB
          value: mydb
        - name: POSTGRES_USER
          value: postgres
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: postgres-secrets
              key: password
        volumeMounts:
        - name: postgres-storage
          mountPath: /var/lib/postgresql/data
        - name: postgres-config
          mountPath: /etc/postgresql
  volumeClaimTemplates:
  - metadata:
      name: postgres-storage
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 10Gi
```

### 2. DaemonSet
```yaml
# manifests/daemonsets/logging.yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: fluentd
  labels:
    app: fluentd
spec:
  selector:
    matchLabels:
      app: fluentd
  template:
    metadata:
      labels:
        app: fluentd
    spec:
      containers:
      - name: fluentd
        image: fluent/fluentd:latest
        ports:
        - containerPort: 24224
        volumeMounts:
        - name: varlog
          mountPath: /var/log
        - name: varlibdockercontainers
          mountPath: /var/lib/docker/containers
          readOnly: true
        - name: fluentd-config
          mountPath: /fluentd/etc
      volumes:
      - name: varlog
        hostPath:
          path: /var/log
      - name: varlibdockercontainers
        hostPath:
          path: /var/lib/docker/containers
      - name: fluentd-config
        configMap:
          name: fluentd-config
      tolerations:
      - key: node-role.kubernetes.io/master
        operator: Exists
        effect: NoSchedule
```

### 3. Job and CronJob
```yaml
# manifests/jobs/backup-job.yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: database-backup
  labels:
    app: database-backup
spec:
  template:
    spec:
      containers:
      - name: backup
        image: postgres:13
        command:
        - /bin/bash
        - -c
        - |
          pg_dump -h postgres-service -U postgres mydb > /backup/mydb-$(date +%Y%m%d-%H%M%S).sql
        env:
        - name: PGPASSWORD
          valueFrom:
            secretKeyRef:
              name: postgres-secrets
              key: password
        volumeMounts:
        - name: backup-storage
          mountPath: /backup
      volumes:
      - name: backup-storage
        persistentVolumeClaim:
          claimName: backup-pvc
      restartPolicy: Never
  backoffLimit: 3
---
apiVersion: batch/v1
kind: CronJob
metadata:
  name: database-backup-cron
  labels:
    app: database-backup
spec:
  schedule: "0 2 * * *"  # Daily at 2 AM
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: backup
            image: postgres:13
            command:
            - /bin/bash
            - -c
            - |
              pg_dump -h postgres-service -U postgres mydb > /backup/mydb-$(date +%Y%m%d-%H%M%S).sql
            env:
            - name: PGPASSWORD
              valueFrom:
                secretKeyRef:
                  name: postgres-secrets
                  key: password
            volumeMounts:
            - name: backup-storage
              mountPath: /backup
          volumes:
          - name: backup-storage
            persistentVolumeClaim:
              claimName: backup-pvc
          restartPolicy: OnFailure
```

### 4. PersistentVolume and PersistentVolumeClaim
```yaml
# manifests/storage/pv-pvc.yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: postgres-pv
  labels:
    type: local
spec:
  storageClassName: manual
  capacity:
    storage: 10Gi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: "/mnt/data"
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: postgres-pvc
spec:
  storageClassName: manual
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
```

## 🧪 Hands-On Labs

### Lab 1: Basic Kubernetes Setup
```bash
# Lab 1: Setting up basic Kubernetes cluster
# 1. Install minikube
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# 2. Start minikube
minikube start --driver=docker

# 3. Verify cluster
kubectl get nodes
kubectl get pods --all-namespaces

# 4. Create basic pod
cat > nginx-pod.yaml << 'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: nginx-pod
  labels:
    app: nginx
spec:
  containers:
  - name: nginx
    image: nginx:1.21
    ports:
    - containerPort: 80
EOF

# 5. Apply configuration
kubectl apply -f nginx-pod.yaml

# 6. Check pod status
kubectl get pods
kubectl describe pod nginx-pod

# 7. Access pod
kubectl port-forward nginx-pod 8080:80

# 8. Clean up
kubectl delete -f nginx-pod.yaml
```

### Lab 2: Deployment and Service
```bash
# Lab 2: Creating deployment and service
# 1. Create deployment
cat > web-app-deployment.yaml << 'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
  labels:
    app: web-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web-app
  template:
    metadata:
      labels:
        app: web-app
    spec:
      containers:
      - name: web-app
        image: nginx:1.21
        ports:
        - containerPort: 80
        resources:
          requests:
            memory: "64Mi"
            cpu: "250m"
          limits:
            memory: "128Mi"
            cpu: "500m"
EOF

# 2. Create service
cat > web-app-service.yaml << 'EOF'
apiVersion: v1
kind: Service
metadata:
  name: web-app-service
spec:
  selector:
    app: web-app
  ports:
  - port: 80
    targetPort: 80
  type: LoadBalancer
EOF

# 3. Apply configurations
kubectl apply -f web-app-deployment.yaml
kubectl apply -f web-app-service.yaml

# 4. Check status
kubectl get deployments
kubectl get services
kubectl get pods

# 5. Scale deployment
kubectl scale deployment web-app --replicas=5

# 6. Check service
kubectl get service web-app-service
minikube service web-app-service

# 7. Clean up
kubectl delete -f web-app-deployment.yaml
kubectl delete -f web-app-service.yaml
```

### Lab 3: ConfigMap and Secret
```bash
# Lab 3: Using ConfigMap and Secret
# 1. Create ConfigMap
cat > app-config.yaml << 'EOF'
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  nginx.conf: |
    server {
        listen 80;
        server_name _;
        location / {
            root /usr/share/nginx/html;
            index index.html;
        }
    }
  app.properties: |
    server.port=8080
    spring.profiles.active=production
EOF

# 2. Create Secret
cat > app-secrets.yaml << 'EOF'
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
type: Opaque
stringData:
  database-url: postgresql://user:password@localhost:5432/mydb
  api-key: abcdefghijk
EOF

# 3. Create pod with ConfigMap and Secret
cat > app-pod.yaml << 'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: app-pod
spec:
  containers:
  - name: app
    image: nginx:1.21
    volumeMounts:
    - name: config-volume
      mountPath: /etc/nginx/conf.d
    - name: secrets-volume
      mountPath: /etc/secrets
  volumes:
  - name: config-volume
    configMap:
      name: app-config
  - name: secrets-volume
    secret:
      secretName: app-secrets
EOF

# 4. Apply configurations
kubectl apply -f app-config.yaml
kubectl apply -f app-secrets.yaml
kubectl apply -f app-pod.yaml

# 5. Check pod
kubectl get pods
kubectl describe pod app-pod

# 6. Access pod
kubectl exec -it app-pod -- /bin/bash

# 7. Clean up
kubectl delete -f app-pod.yaml
kubectl delete -f app-secrets.yaml
kubectl delete -f app-config.yaml
```

## 📊 Best Practices

### 1. Security Best Practices
- **RBAC**: Implement Role-Based Access Control
- **Network Policies**: Use network policies for traffic control
- **Pod Security**: Use pod security standards
- **Secret Management**: Use proper secret management
- **Image Security**: Scan container images for vulnerabilities

### 2. Performance Best Practices
- **Resource Limits**: Set appropriate resource limits
- **Horizontal Scaling**: Use HPA for automatic scaling
- **Node Affinity**: Use node affinity for pod placement
- **Resource Quotas**: Implement resource quotas
- **Monitoring**: Set up comprehensive monitoring

### 3. Organization Best Practices
- **Namespaces**: Use namespaces for organization
- **Labels and Selectors**: Use consistent labeling
- **Helm Charts**: Use Helm for package management
- **GitOps**: Implement GitOps workflows
- **Documentation**: Document all configurations

## 📚 Learning Resources

### Documentation
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Kubernetes API Reference](https://kubernetes.io/docs/reference/)
- [Kubernetes Best Practices](https://kubernetes.io/docs/concepts/configuration/overview/)
- [Kubernetes Security](https://kubernetes.io/docs/concepts/security/)

### Community Resources
- [Kubernetes Community](https://kubernetes.io/community/)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/kubernetes)
- [Reddit](https://www.reddit.com/r/kubernetes/)
- [GitHub](https://github.com/kubernetes/kubernetes)

## 🎓 Certification Preparation

### Kubernetes Certifications
- **CKA**: Certified Kubernetes Administrator
- **CKS**: Certified Kubernetes Security Specialist
- **CKAD**: Certified Kubernetes Application Developer
- **DevOps Engineer**: General DevOps certification

### Study Materials
- **Official Documentation**: Kubernetes documentation
- **Practice Labs**: Hands-on Kubernetes projects
- **Kubernetes Challenges**: Practice with real-world scenarios
- **Community Forums**: Expert discussions and Q&A

## 🤝 Contributing

### How to Contribute
1. **Fork the repository**
2. **Create a feature branch**
3. **Add Kubernetes content or improvements**
4. **Submit a pull request**

### Contribution Areas
- **New manifest examples**
- **Updated best practices**
- **Additional Helm charts**
- **Improved documentation**

## 📞 Support

### Getting Help
- **Documentation**: Comprehensive guides in each folder
- **Issues**: GitHub issues for Kubernetes problems
- **Discussions**: Community discussions for orchestration questions
- **Mentorship**: Connect with Kubernetes experts

### Community Resources
- **Slack**: #kubernetes
- **Discord**: Kubernetes Learning Community
- **LinkedIn**: Kubernetes Professionals Group
- **YouTube**: Kubernetes Tutorials Channel

---

**Ready to master Kubernetes?** Start with basic pods and work your way up to advanced orchestration patterns!
