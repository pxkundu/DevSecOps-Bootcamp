**Week 2, Day 4: Kubernetes Fundamentals - "Cluster Sabotage"** on the **basics of Kubernetes**, diving deep into its core concepts, day-to-day commands, practical use cases, best practices, and tips/tricks for real-world DevOps activities. 

We’ll keep it **extensively informative**, emphasizing **theoretical keyword explanations** and **practical implementations** without jumping straight to Amazon EKS. Instead, we’ll use a local Kubernetes setup (e.g., Minikube) to master the fundamentals, ensuring a solid foundation before integrating AWS-specific services like EKS in a future session (e.g., Day 5 capstone). 

This will align with real-world DevOps needs, drawing from Kubernetes documentation ([Kubernetes Concepts](https://kubernetes.io/docs/concepts/)) and industry practices.

---

### Week 2, Day 4: Kubernetes Fundamentals - "Cluster Sabotage"

#### Objective
Master the **basics of Kubernetes** by understanding its architecture, core constructs, and day-to-day operations, deploying a simple multi-service app (frontend and API) on a local cluster (Minikube), and recovering from a "sabotage" challenge (e.g., pod failures, resource limits) to build practical DevOps skills.

#### Duration
5-6 hours

#### Tools
- Minikube (local Kubernetes), `kubectl`, Docker, Git, Bash, Text Editor (e.g., VS Code).

#### Goal as a DevOps Engineer
- **Practical Implementation**: Deploy and manage a microservices app on Kubernetes, using basic commands and manifests, with a focus on resilience, scalability, and observability.
- **Focus**: Build a foundational understanding of Kubernetes concepts and operations, applying DevOps best practices (e.g., automation, self-healing) for real-world scenarios.

---

### Content Breakdown

#### 1. Theory: Kubernetes Core Concepts and DevOps Integration (1 hour)
- **Goal**: Provide a deep, beginner-friendly foundation for Kubernetes, explaining key concepts with detailed keywords and real-world DevOps context.
- **Materials**: Slides/video, [Kubernetes Docs](https://kubernetes.io/docs/home/), [Kubernetes Basics](https://kubernetes.io/docs/tutorials/kubernetes-basics/).
- **Key Concepts & Keywords**:
  - **Kubernetes Overview**:
    - **Kubernetes**: Open-source platform for **container orchestration**, automating deployment, scaling, and management of containerized apps ([What is Kubernetes](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)).
      - **Explanation**: Manages Docker containers across nodes, ensuring desired state.
    - **Cluster**: A set of nodes (master + workers) running Kubernetes.
      - **Explanation**: Master controls scheduling; workers run app workloads.
    - **Node**: A physical or virtual machine in the cluster (e.g., VM running Minikube).
      - **Explanation**: Hosts pods, managed by the control plane.
    - **Pod**: Smallest deployable unit, typically one container, sharing network/storage.
      - **Explanation**: Ephemeral, runs an app instance (e.g., Nginx pod).
    - **Control Plane**: Components managing the cluster (e.g., API Server, Scheduler).
      - **Explanation**: Brain of Kubernetes, hosted on the master node.
  - **Core Constructs**:
    - **Deployment**: Manages pod replicas and updates (e.g., rolling updates).
      - **Explanation**: Ensures X pods are running, handles version upgrades.
    - **ReplicaSet**: Ensures a specified number of pod replicas are running.
      - **Explanation**: Lower-level construct used by Deployments.
    - **Service**: Abstracts pod IPs with a stable endpoint (e.g., ClusterIP, LoadBalancer).
      - **Explanation**: Provides internal/external access (e.g., `frontend-service`).
    - **Ingress**: Routes external HTTP/HTTPS traffic to services via rules.
      - **Explanation**: Manages URLs (e.g., `app.example.com/api`).
    - **ConfigMap**: Externalizes configuration data (e.g., env vars).
      - **Explanation**: Decouples config from code (e.g., DB URL).
    - **Secret**: Stores sensitive data (e.g., API keys, passwords).
      - **Explanation**: Encoded, secure alternative to ConfigMaps.
    - **Namespace**: Logical partitioning of cluster resources.
      - **Explanation**: Isolates teams/environments (e.g., `dev`, `prod`).
  - **Operational Features**:
    - **Self-Healing**: Auto-restarts failed pods, reschedules on node failure.
      - **Explanation**: Maintains desired state without manual fixes.
    - **Horizontal Scaling**: Adjusts pod count based on load (e.g., HPA).
      - **Explanation**: Scales dynamically (e.g., 2 to 10 pods).
    - **Rolling Updates**: Deploys new versions with zero downtime.
      - **Explanation**: Gradually replaces old pods with new ones.
    - **Resource Limits**: Caps CPU/memory per pod (e.g., 500m CPU, 512Mi memory).
      - **Explanation**: Prevents resource hogging, ensures stability.
  - **DevOps Integration**:
    - **Automation**: Kubernetes automates deployment and scaling.
    - **Collaboration**: Git stores manifests for team alignment.
    - **Continuous Deployment**: Updates roll out via CI/CD.
    - **Observability**: Logs and metrics via `kubectl` and tools like Prometheus.
    - **Shift Left**: Test pods early in CI pipelines.
    - **Resilience**: Self-healing ensures uptime in production.
- **Keywords**: Kubernetes, Cluster, Node, Pod, Control Plane, Deployment, ReplicaSet, Service, Ingress, ConfigMap, Secret, Namespace, Self-Healing, Horizontal Scaling, Rolling Updates, Resource Limits, Automation, Collaboration, Continuous Deployment, Observability, Shift Left, Resilience.

- **Sub-Activities**:
  1. **Kubernetes 101 (15 min)**:
     - **Concept**: Kubernetes manages containers at scale.
     - **Keywords**: Kubernetes, Cluster, Pod.
     - **Details**: Pods run apps; clusters group nodes.
     - **Use Case**: Netflix runs thousands of pods for streaming.
     - **Why**: Simplifies container ops, a DevOps enabler.
  2. **Core Constructs (15 min)**:
     - **Concept**: Deployments, Services, and Ingress define apps.
     - **Keywords**: Deployment, Service, Ingress.
     - **Details**: Deployments ensure replicas; Services expose pods.
     - **Use Case**: Netflix deploys UI and API with Services.
     - **Why**: Enables modular microservices.
  3. **Configuration Management (10 min)**:
     - **Concept**: ConfigMaps and Secrets externalize settings.
     - **Keywords**: ConfigMap, Secret.
     - **Details**: ConfigMaps for env vars; Secrets for passwords.
     - **Use Case**: Netflix stores API keys securely.
     - **Why**: Decouples config, a DevOps best practice.
  4. **Resilience Features (10 min)**:
     - **Concept**: Self-healing and scaling keep apps running.
     - **Keywords**: Self-Healing, Horizontal Scaling.
     - **Details**: Auto-restarts pods; scales with demand.
     - **Use Case**: Netflix scales during peak streaming hours.
     - **Why**: Ensures reliability, a DevOps priority.
  5. **Day-to-Day Operations (10 min)**:
     - **Concept**: `kubectl` commands manage clusters.
     - **Keywords**: Observability, Resource Limits.
     - **Details**: Check logs, set CPU/memory caps.
     - **Use Case**: Netflix monitors pod health daily.
     - **Why**: Practical DevOps operations.

---

#### 2. Lab: Deploy and Manage a Kubernetes App with Minikube (2.5-3 hours)
- **Goal**: Deploy a simple microservices app (Nginx frontend, Node.js API) on Minikube, mastering basic `kubectl` commands and real-world operations.

##### Initial Setup with Minikube, `kubectl`, and Docker
- **Why Minikube**: Runs a local Kubernetes cluster for learning ([Minikube Docs](https://minikube.sigs.k8s.io/docs/)).
- **Why `kubectl`**: CLI for Kubernetes management.
- **Why Docker**: Builds container images.

- **Setup Steps**:
  1. **Install Docker**:
     ```bash
     sudo yum install docker -y
     sudo systemctl start docker
     sudo usermod -aG docker ec2-user
     docker --version  # Verify: Docker version 20.x.x
     ```
  2. **Install Minikube**:
     ```bash
     curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
     sudo install minikube-linux-amd64 /usr/local/bin/minikube
     minikube version  # Verify: minikube version: v1.x.x
     ```
  3. **Install `kubectl`**:
     ```bash
     curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
     sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
     kubectl version --client  # Verify: v1.x.x
     ```
  4. **Start Minikube**:
     ```bash
     minikube start --driver=docker
     minikube status  # Verify: host, kubelet, apiserver running
     ```
  5. **Set Up Project**:
     ```bash
     mkdir k8s-basics
     cd k8s-basics
     git init
     echo "node_modules/
     *.zip" > .gitignore
     ```

##### Practical Implementation
- **Folder Structure**:
  ```
  k8s-basics/
  ├── frontend/                # Nginx frontend
  │   ├── Dockerfile          # Docker config
  │   └── nginx.conf          # Nginx config
  ├── api/                    # Node.js API
  │   ├── index.js           # API logic
  │   ├── Dockerfile         # Docker config
  │   └── package.json       # Dependencies
  ├── manifests/              # Kubernetes manifests
  │   ├── frontend-deployment.yaml
  │   ├── frontend-service.yaml
  │   ├── api-deployment.yaml
  │   ├── api-service.yaml
  │   ├── configmap.yaml
  │   └── secret.yaml
  └── README.md              # Docs
  ```

- **Task 1: Create Containers**:
  - **Frontend (Nginx)**:
    ```bash
    cd frontend
    nano Dockerfile
    ```
    - **Content** (`Dockerfile`):
      ```dockerfile
      FROM nginx:alpine
      COPY nginx.conf /etc/nginx/conf.d/default.conf
      EXPOSE 80
      CMD ["nginx", "-g", "daemon off;"]
      ```
    ```bash
    nano nginx.conf
    ```
    - **Content** (`nginx.conf`):
      ```nginx
      server {
          listen 80;
          server_name localhost;
          location / {
              return 200 "Welcome to Kubernetes Frontend\n";
          }
      }
      ```
    - **Build**: 
      ```bash
      docker build -t frontend:latest .
      ```

  - **API (Node.js)**:
    ```bash
    cd ../api
    npm init -y
    npm install express
    nano index.js
    ```
    - **Content** (`index.js`):
      ```javascript
      const express = require('express');
      const app = express();
      const port = process.env.PORT || 3000;

      app.get('/api/status', (req, res) => {
        res.json({ message: `API running on ${process.env.NODE_ENV || 'dev'}`, timestamp: new Date().toISOString() });
      });

      app.listen(port, () => {
        console.log(`API on port ${port}`);
      });
      ```
    ```bash
    nano Dockerfile
    ```
    - **Content** (`Dockerfile`):
      ```dockerfile
      FROM node:20-alpine
      WORKDIR /app
      COPY package*.json ./
      RUN npm ci --production
      COPY . .
      EXPOSE 3000
      CMD ["node", "index.js"]
      ```
    - **Build**: 
      ```bash
      docker build -t api:latest .
      ```

- **Task 2: Deploy to Minikube**:
  - **Load Images**: 
    ```bash
    minikube image load frontend:latest
    minikube image load api:latest
    ```
  - **Manifests**:
    ```bash
    cd ../manifests
    nano frontend-deployment.yaml
    ```
    - **Content** (`frontend-deployment.yaml`):
      ```yaml
      apiVersion: apps/v1
      kind: Deployment
      metadata:
        name: frontend
      spec:
        replicas: 2
        selector:
          matchLabels:
            app: frontend
        template:
          metadata:
            labels:
              app: frontend
          spec:
            containers:
            - name: frontend
              image: frontend:latest
              ports:
              - containerPort: 80
              resources:
                limits:
                  cpu: "500m"
                  memory: "512Mi"
                requests:
                  cpu: "200m"
                  memory: "256Mi"
      ```
    ```bash
    nano frontend-service.yaml
    ```
    - **Content** (`frontend-service.yaml`):
      ```yaml
      apiVersion: v1
      kind: Service
      metadata:
        name: frontend-service
      spec:
        selector:
          app: frontend
        ports:
        - port: 80
          targetPort: 80
        type: NodePort
      ```
    ```bash
    nano api-deployment.yaml
    ```
    - **Content** (`api-deployment.yaml`):
      ```yaml
      apiVersion: apps/v1
      kind: Deployment
      metadata:
        name: api
      spec:
        replicas: 2
        selector:
          matchLabels:
            app: api
        template:
          metadata:
            labels:
              app: api
          spec:
            containers:
            - name: api
              image: api:latest
              ports:
              - containerPort: 3000
              env:
              - name: NODE_ENV
                valueFrom:
                  configMapKeyRef:
                    name: app-config
                    key: environment
              resources:
                limits:
                  cpu: "500m"
                  memory: "512Mi"
                requests:
                  cpu: "200m"
                  memory: "256Mi"
      ```
    ```bash
    nano api-service.yaml
    ```
    - **Content** (`api-service.yaml`):
      ```yaml
      apiVersion: v1
      kind: Service
      metadata:
        name: api-service
      spec:
        selector:
          app: api
        ports:
        - port: 3000
          targetPort: 3000
        type: NodePort
      ```
    ```bash
    nano configmap.yaml
    ```
    - **Content** (`configmap.yaml`):
      ```yaml
      apiVersion: v1
      kind: ConfigMap
      metadata:
        name: app-config
      data:
        environment: "production"
      ```
    ```bash
    nano secret.yaml
    ```
    - **Content** (`secret.yaml`):
      ```yaml
      apiVersion: v1
      kind: Secret
      metadata:
        name: app-secret
      type: Opaque
      data:
        api-key: YXBpLWtleS1leGFtcGxl  # echo -n "api-key-example" | base64
      ```
  - **Apply**:
    ```bash
    kubectl apply -f configmap.yaml
    kubectl apply -f secret.yaml
    kubectl apply -f frontend-deployment.yaml
    kubectl apply -f frontend-service.yaml
    kubectl apply -f api-deployment.yaml
    kubectl apply -f api-service.yaml
    ```

- **Task 3: Day-to-Day `kubectl` Commands**:
  - **Basic Commands**:
    - List Pods: `kubectl get pods` (shows pod status).
    - List Services: `kubectl get services` (shows ports).
    - Describe Pod: `kubectl describe pod <pod-name>` (details events, issues).
    - Logs: `kubectl logs <pod-name>` (view container output).
    - Exec into Pod: `kubectl exec -it <pod-name> -- sh` (interactive shell).
  - **Scaling**:
    - Scale Deployment: `kubectl scale deployment frontend --replicas=4`.
    - Check: `kubectl get pods`.
  - **Updates**:
    - Edit Deployment: `kubectl edit deployment frontend` (e.g., change image).
    - Rollout Status: `kubectl rollout status deployment frontend`.
    - Rollback: `kubectl rollout undo deployment frontend`.
  - **Debugging**:
    - Delete Pod: `kubectl delete pod <pod-name>` (tests self-healing).
    - Get Events: `kubectl get events` (cluster activity).
  - **Access Services**:
    - Frontend URL: `minikube service frontend-service --url`.
    - API URL: `minikube service api-service --url`.

##### Best Practices
- **Resource Limits**: Set CPU/memory limits to prevent resource exhaustion.
- **Namespaces**: Use `kubectl create namespace dev` for isolation.
- **Labels**: Tag resources (e.g., `app: frontend`) for filtering (`kubectl get pods -l app=frontend`).
- **Health Checks**: Add liveness/readiness probes in production.
- **Version Control**: Store manifests in Git for collaboration.

##### Tips and Tricks
- **Alias**: Add `alias k=kubectl` to `.bashrc` for brevity.
- **Dry Run**: `kubectl apply -f file.yaml --dry-run=client` (preview changes).
- **Watch**: `kubectl get pods -w` (real-time updates).
- **Port Forward**: `kubectl port-forward svc/api-service 3000:3000` (local testing).
- **Cleanup**: `kubectl delete -f .` (remove all manifests in dir).

##### 3. Chaos Twist: "Cluster Sabotage" (1-1.5 hours)
- **Goal**: Recover from sabotage (e.g., pod deletions, resource overload), mastering Kubernetes resilience.
- **Scenario**: Instructor deletes pods (`kubectl delete pod -l app=frontend`) or sets low resource limits (`kubectl edit deployment api`).
- **Task**: 
  - Check: `kubectl get pods` (see restarts).
  - Logs: `kubectl logs <pod-name>` (diagnose failures).
  - Scale: `kubectl scale deployment api --replicas=3`.
  - Fix Limits: `kubectl edit deployment api` (increase CPU/memory).
- **Use Case**: Netflix recovers from pod crashes during streaming spikes.
- **Outcome**: Cluster stabilizes, app remains accessible.

##### 4. Wrap-Up: War Room Debrief (30-45 min)
- **Goal**: Reflect on Kubernetes basics and prepare for Day 5.
- **Activities**: 
  - Demo: Access frontend (`minikube service frontend-service --url`).
  - Discuss sabotage fixes (e.g., self-healing, scaling).
  - Prep for EKS integration (Day 5).
- **Use Case**: Lessons apply to Netflix’s Kubernetes-based microservices.

---

#### Key Outcomes
- **Theory Learned**: Kubernetes architecture, core constructs, DevOps integration.
- **Practical Skills**: Deployed and managed a microservices app with `kubectl`, mastered day-to-day ops.

#### Practical Use Cases
1. **Netflix Microservices**: Deploy UI/API pods, scale with demand, recover from failures.
2. **E-Commerce**: Run storefront and checkout APIs, use ConfigMaps for settings.
3. **CI/CD**: Test pods locally before production (e.g., GitHub Actions).

---

Week 2 Day 4 focuses purely on Kubernetes basics, with extensive theory and practical commands for real-world DevOps. 