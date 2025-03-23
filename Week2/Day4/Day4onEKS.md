### Week 2, Day 4: Extension with Kubernetes on AWS EKS - "Cluster Sabotage"

#### Objective
Master **Kubernetes orchestration** by deploying a resilient multi-service application on **Amazon EKS**, integrating **AWS Load Balancer Controller**, **Amazon EBS CSI Driver**, and **Amazon CloudWatch Container Insights**, and recovering from intentional "sabotage" (e.g., pod deletions, misconfigured ingress) to ensure scalability and reliability.

#### Duration
5-6 hours

#### Tools
- AWS Management Console, AWS CLI, `kubectl`, `eksctl`, Helm, Git, Docker, Bash, Text Editor (e.g., VS Code).

#### Goal as a DevOps Engineer
- **Practical Implementation**: Automate the deployment of a microservices app (e.g., frontend and API) on EKS, leveraging Kubernetes constructs (pods, deployments, services) and AWS integrations, with production-grade security, scalability, and observability.
- **Focus**: Build a fault-tolerant, scalable Kubernetes cluster, embodying AWS and DevOps best practices like automation, self-healing, and operational excellence, tailored for real-world applications.

---

### Content Breakdown

#### 1. Theory: Kubernetes Fundamentals, EKS, and DevOps Ecosystem (1 hour)
- **Goal**: Establish a comprehensive theoretical foundation for Kubernetes, EKS, and DevOps principles, with detailed keyword explanations and real-world context, matching the depth of previous days.
- **Materials**: Slides/video, AWS docs (e.g., [EKS Concepts](https://docs.aws.amazon.com/eks/latest/userguide/what-is-eks.html), [Kubernetes Overview](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/), [AWS DevOps](https://aws.amazon.com/devops/)).
- **Key Concepts & Keywords**:
  - **Kubernetes Theory**:
    - **Kubernetes**: Open-source platform for **container orchestration**, managing Docker containers across a cluster ([Kubernetes What It Is](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)).
      - **Explanation**: Automates deployment, scaling, and management of containerized apps.
    - **Cluster**: Set of master (control plane) and worker nodes.
      - **Explanation**: Master schedules tasks; workers run pods.
    - **Pod**: Smallest deployable unit, typically one container, sharing network/storage.
      - **Explanation**: Ephemeral, scalable unit of work (e.g., a Node.js API pod).
    - **Deployment**: Manages pod replicas and updates (e.g., rolling updates).
      - **Explanation**: Ensures desired state (e.g., 3 pods always running).
    - **Service**: Abstracts pod IPs with a stable endpoint (e.g., ClusterIP, LoadBalancer).
      - **Explanation**: Provides discovery and load balancing.
    - **Ingress**: Routes external HTTP/HTTPS traffic to services via rules.
      - **Explanation**: Manages external access (e.g., `api.example.com`).
    - **Self-Healing**: Auto-restarts failed pods, reschedules on node failure.
      - **Explanation**: Ensures reliability without manual intervention.
    - **ConfigMap/Secret**: Externalizes configuration and sensitive data.
      - **Explanation**: Decouples app logic from environment (e.g., API keys).
  - **AWS EKS Theory**:
    - **Amazon EKS**: AWS-managed Kubernetes control plane, running master nodes ([EKS How It Works](https://docs.aws.amazon.com/eks/latest/userguide/how-eks-works.html)).
      - **Explanation**: AWS handles master HA; you manage worker nodes or use Fargate.
    - **AWS Load Balancer Controller**: Integrates ALB with Kubernetes Ingress.
      - **Explanation**: Routes traffic to pods dynamically.
    - **Amazon EBS CSI Driver**: Provides persistent storage for pods via EBS volumes ([EBS CSI Driver](https://docs.aws.amazon.com/eks/latest/userguide/ebs-csi.html)).
      - **Explanation**: Enables stateful apps (e.g., databases).
    - **Amazon CloudWatch Container Insights**: Monitors cluster metrics/logs ([Container Insights](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/ContainerInsights.html)).
      - **Explanation**: Tracks CPU, memory, and pod health.
    - **AWS Shared Responsibility Model**: AWS secures EKS control plane; you secure worker nodes, pods, and data.
      - **Explanation**: Shared duty ensures robust deployments.
  - **DevOps Theoretical Knowledge**:
    - **DevOps**: Culture of automation, collaboration, and continuous improvement for rapid, reliable delivery.
    - **Key DevOps Concepts**:
      - **Automation**: Kubernetes deployments via CI/CD (e.g., CodePipeline).
      - **Collaboration**: Git manages pod code across teams.
      - **Continuous Deployment**: Roll out updates with zero downtime.
      - **Observability**: Monitor with CloudWatch, trace with X-Ray.
      - **Shift Left**: Test pods early in CI (e.g., Docker builds).
      - **Resilience**: Self-healing and auto-scaling ensure uptime.
      - **Infrastructure as Code (IaC)**: Define EKS with Terraform or CloudFormation.
      - **Microservices**: Kubernetes excels at modular, independent services.
  - **AWS Keywords**: Amazon EKS, Kubernetes, AWS Load Balancer Controller, Amazon EBS, Amazon CloudWatch Container Insights, AWS IAM, Amazon VPC, AWS Auto Scaling, AWS KMS, AWS CloudFormation, Amazon Route 53, AWS Secrets Manager, AWS X-Ray, Amazon S3, AWS Trusted Advisor, Operational Excellence, Reliability, Scalability, Performance Efficiency, Security Best Practices, Cost Optimization, Continuous Deployment, AWS Shared Responsibility Model, Microservices Architecture, Container Orchestration, Self-Healing.

- **Sub-Activities**:
  1. **Kubernetes Basics (15 min)**:
     - **Concept**: Kubernetes orchestrates containers at scale.
     - **Keywords**: Kubernetes, Cluster, Pod, Deployment.
     - **Details**: Pods run containers; deployments ensure replicas.
     - **Action**: Open Console > EKS > “What is Amazon EKS?”.
     - **Use Case**: Netflix uses Kubernetes for streaming microservices.
     - **Why**: Enables scalability, a DevOps cornerstone.
  2. **EKS Architecture (10 min)**:
     - **Concept**: EKS manages Kubernetes control plane on AWS.
     - **Keywords**: Amazon EKS, AWS Load Balancer Controller.
     - **Details**: AWS runs master nodes; ALB routes traffic.
     - **Action**: Read [EKS Overview](https://docs.aws.amazon.com/eks/latest/userguide/what-is-eks.html).
     - **Use Case**: Netflix leverages EKS for global API deployment.
     - **Why**: Simplifies Kubernetes ops, aligns with AWS ecosystem.
  3. **Storage and Persistence (10 min)**:
     - **Concept**: EBS CSI Driver provides persistent volumes.
     - **Keywords**: Amazon EBS, EBS CSI Driver.
     - **Details**: EBS volumes attach to pods (e.g., 10GiB storage).
     - **Action**: Explore EKS > Add-ons in Console.
     - **Use Case**: Netflix stores metadata in persistent volumes.
     - **Why**: Supports stateful apps in Kubernetes.
  4. **Observability and Monitoring (10 min)**:
     - **Concept**: Container Insights tracks cluster health.
     - **Keywords**: Amazon CloudWatch Container Insights, AWS X-Ray.
     - **Details**: Monitors CPU/memory; X-Ray traces requests.
     - **Action**: Check CloudWatch > Container Insights in Console.
     - **Use Case**: Netflix monitors pod latency during streams.
     - **Why**: DevOps requires visibility for reliability.
  5. **Self-Healing and Resilience (10 min)**:
     - **Concept**: Kubernetes auto-recovers from failures.
     - **Keywords**: Self-Healing, AWS Auto Scaling.
     - **Details**: Restarts pods, scales nodes with demand.
     - **Action**: Read [Kubernetes Self-Healing](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#replica-failure).
     - **Use Case**: Netflix ensures uptime during node failures.
     - **Why**: Resilience is a DevOps priority.
  6. **Self-Check (5 min)**:
     - **Question**: “How does EKS differ from ECS in orchestration?”
     - **Answer**: “EKS uses Kubernetes for multi-cloud flexibility; ECS is AWS-native and simpler.”

---

#### 2. Lab: Deploy a Microservices App on Amazon EKS (2.5-3 hours)
- **Goal**: Deploy a production-ready microservices app (React frontend, Node.js API) on EKS, automating setup with `eksctl`, `kubectl`, and Helm.

##### Initial Setup with AWS CLI, `eksctl`, `kubectl`, and Docker
- **Why AWS CLI**: Automates EKS resource creation ([AWS CLI Setup](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html)).
- **Why `eksctl`**: Simplifies EKS cluster provisioning ([eksctl Docs](https://eksctl.io/)).
- **Why `kubectl`**: Manages Kubernetes resources ([kubectl Overview](https://kubernetes.io/docs/reference/kubectl/)).
- **Why Docker**: Builds container images for EKS.

- **Setup Steps**:
  1. **Install AWS CLI**:
     ```bash
     curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
     unzip awscliv2.zip
     sudo ./aws/install
     aws --version  # Verify: aws-cli/2.x.x
     ```
  2. **Configure AWS CLI**:
     ```bash
     aws configure
     # Access Key ID, Secret Key, us-east-1, json
     aws sts get-caller-identity  # Verify account
     ```
  3. **Install `eksctl`**:
     ```bash
     curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp
     sudo mv /tmp/eksctl /usr/local/bin
     eksctl version  # Verify: 0.x.x
     ```
  4. **Install `kubectl`**:
     ```bash
     curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
     sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
     kubectl version --client  # Verify: v1.x.x
     ```
  5. **Install Docker**:
     ```bash
     sudo yum install docker -y
     sudo systemctl start docker
     sudo usermod -aG docker ec2-user
     docker --version  # Verify: Docker version 20.x.x
     ```
  6. **Install Node.js**:
     ```bash
     curl -sL https://rpm.nodesource.com/setup_20.x | sudo bash -
     sudo yum install -y nodejs
     node -v  # Verify: v20.x.x
     ```
  7. **Set Up Project**:
     ```bash
     mkdir eks-streaming
     cd eks-streaming
     git init
     echo "node_modules/
     *.zip
     build/" > .gitignore
     ```

##### Practical Implementation
- **Folder Structure**:
  ```
  eks-streaming/
  ├── frontend/                # React frontend
  │   ├── src/
  │   │   ├── App.js          # Main component
  │   │   ├── App.css         # Styling
  │   │   └── index.js        # Entry point
  │   ├── public/
  │   │   └── index.html      # HTML template
  │   ├── Dockerfile          # Docker config
  │   ├── package.json        # Dependencies
  │   └── nginx.conf          # Nginx config
  ├── api/                    # Node.js API
  │   ├── index.js           # API logic
  │   ├── Dockerfile         # Docker config
  │   └── package.json       # Dependencies
  ├── k8s/                    # Kubernetes manifests
  │   ├── frontend-deployment.yaml  # Frontend deployment
  │   ├── frontend-service.yaml     # Frontend service
  │   ├── api-deployment.yaml       # API deployment
  │   ├── api-service.yaml          # API service
  │   └── ingress.yaml              # Ingress config
  └── README.md              # Docs
  ```

- **Task 1: Create Containers (Frontend and API)**:
  - **Frontend (React)**:
    ```bash
    cd frontend
    npx create-react-app .
    nano src/App.js
    ```
    - **Content** (`src/App.js` - Production-Ready):
      ```javascript
      import React, { useState, useEffect } from 'react';
      import './App.css';

      function App() {
        const [status, setStatus] = useState('Loading...');
        useEffect(() => {
          fetch('/api/status', { method: 'GET' })
            .then(res => res.json())
            .then(data => setStatus(data.message))
            .catch(err => setStatus('Error: ' + err.message));
        }, []);

        return (
          <div className="App">
            <h1>Streaming Frontend</h1>
            <p>Status: {status}</p>
          </div>
        );
      }

      export default App;
      ```
    - **Dockerfile**:
      ```dockerfile
      FROM node:20-alpine AS builder
      WORKDIR /app
      COPY package*.json ./
      RUN npm ci --production
      COPY . .
      RUN npm run build

      FROM nginx:alpine
      COPY --from=builder /app/build /usr/share/nginx/html
      COPY nginx.conf /etc/nginx/conf.d/default.conf
      EXPOSE 80
      CMD ["nginx", "-g", "daemon off;"]
      ```
    - **nginx.conf**:
      ```nginx
      server {
          listen 80;
          server_name localhost;
          location / {
              root /usr/share/nginx/html;
              index index.html;
              try_files $uri $uri/ /index.html;
          }
          location /api/ {
              proxy_pass http://api-service:3000/;
              proxy_set_header Host $host;
          }
      }
      ```
    - **Build**: 
      ```bash
      docker build -t streaming-frontend .
      ```

  - **API (Node.js)**:
    ```bash
    cd ../api
    npm init -y
    npm install express
    nano index.js
    ```
    - **Content** (`index.js` - Production-Ready):
      ```javascript
      const express = require('express');
      const app = express();
      const port = process.env.PORT || 3000;

      app.use(express.json());
      app.get('/api/status', (req, res) => {
        res.status(200).json({ message: 'API is running', timestamp: new Date().toISOString() });
      });

      app.listen(port, () => {
        console.log(`API running on port ${port}`);
      });
      ```
    - **Dockerfile**:
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
      docker build -t streaming-api .
      ```

- **Task 2: Push Images to Amazon ECR**:
  - **Commands**: 
    ```bash
    aws ecr create-repository --repository-name streaming-frontend --region us-east-1
    aws ecr create-repository --repository-name streaming-api --region us-east-1
    aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com
    docker tag streaming-frontend:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/streaming-frontend:latest
    docker tag streaming-api:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/streaming-api:latest
    docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/streaming-frontend:latest
    docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/streaming-api:latest
    ```

- **Task 3: Create EKS Cluster with `eksctl`**:
  - **Commands**: 
    ```bash
    eksctl create cluster \
      --name StreamingCluster \
      --region us-east-1 \
      --nodegroup-name standard-workers \
      --node-type t3.medium \
      --nodes 2 \
      --nodes-min 1 \
      --nodes-max 4 \
      --managed
    ```
  - **Details**: Creates a managed EKS cluster with 2 t3.medium nodes, scalable to 4.
  - **Why**: Managed nodes simplify worker management, a DevOps efficiency gain.

- **Task 4: Install AWS Load Balancer Controller**:
  - **Commands**: 
    ```bash
    eksctl utils associate-iam-oidc-provider --cluster StreamingCluster --approve
    aws iam create-policy --policy-name AWSLoadBalancerControllerIAMPolicy --policy-document file://<(curl -s https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/main/docs/install/iam_policy.json)
    eksctl create iamserviceaccount \
      --cluster StreamingCluster \
      --namespace kube-system \
      --name aws-load-balancer-controller \
      --attach-policy-arn arn:aws:iam::<account-id>:policy/AWSLoadBalancerControllerIAMPolicy \
      --approve
    kubectl apply -k "github.com/aws/eks-charts/stable/aws-load-balancer-controller//crds?ref=master"
    helm repo add eks https://aws.github.io/eks-charts
    helm install aws-load-balancer-controller eks/aws-load-balancer-controller \
      --namespace kube-system \
      --set clusterName=StreamingCluster \
      --set serviceAccount.create=false \
      --set serviceAccount.name=aws-load-balancer-controller
    ```
  - **Details**: Adds ALB controller for Ingress routing.
  - **Why**: Automates load balancing, a Netflix-like feature.

- **Task 5: Deploy App with Kubernetes Manifests**:
  - **Commands**: 
    ```bash
    cd ../k8s
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
              image: <account-id>.dkr.ecr.us-east-1.amazonaws.com/streaming-frontend:latest
              ports:
              - containerPort: 80
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
              image: <account-id>.dkr.ecr.us-east-1.amazonaws.com/streaming-api:latest
              ports:
              - containerPort: 3000
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
      ```
    ```bash
    nano ingress.yaml
    ```
    - **Content** (`ingress.yaml`):
      ```yaml
      apiVersion: networking.k8s.io/v1
      kind: Ingress
      metadata:
        name: streaming-ingress
        annotations:
          kubernetes.io/ingress.class: alb
          alb.ingress.kubernetes.io/scheme: internet-facing
      spec:
        rules:
        - http:
            paths:
            - path: /
              pathType: Prefix
              backend:
                service:
                  name: frontend-service
                  port:
                    number: 80
            - path: /api
              pathType: Prefix
              backend:
                service:
                  name: api-service
                  port:
                    number: 3000
      ```
  - **Apply**:
    ```bash
    kubectl apply -f frontend-deployment.yaml
    kubectl apply -f frontend-service.yaml
    kubectl apply -f api-deployment.yaml
    kubectl apply -f api-service.yaml
    kubectl apply -f ingress.yaml
    kubectl get ingress streaming-ingress -o jsonpath='{.status.loadBalancer.ingress[0].hostname}'
    ```

- **Task 6: Enable EBS CSI Driver and Container Insights**:
  - **Commands**: 
    ```bash
    eksctl create addon --name aws-ebs-csi-driver --cluster StreamingCluster --service-account-role-arn arn:aws:iam::<account-id>:role/AmazonEKS_EBS_CSI_DriverRole --force
    eksctl create addon --name aws-cloudwatch-metrics --cluster StreamingCluster --force
    ```
  - **Details**: Adds persistent storage and monitoring.
  - **Why**: Supports stateful apps and observability, Netflix-like features.

##### 3. Chaos Twist: "Cluster Sabotage" (1-1.5 hours)
- **Goal**: Recover from sabotage (e.g., pod deletions, ingress misconfig), reinforcing DevOps resilience.
- **Scenario**: Instructor deletes pods (`kubectl delete pod -l app=frontend`) or breaks ingress (e.g., wrong path).
- **Task**: 
  - Check Pods: `kubectl get pods`.
  - Verify Self-Healing: Watch pods restart (`kubectl get pods -w`).
  - Fix Ingress: `kubectl edit ingress streaming-ingress`.
  - Monitor: `aws cloudwatch get-metric-statistics --namespace AWS/EKS --metric-name CPUUtilization --dimensions Name=ClusterName,Value=StreamingCluster --start-time $(date -u -d "5 minutes ago" +%s) --end-time $(date -u +%s) --period 60 --statistics Average`.
- **AWS Keywords**: Troubleshooting, Reliability, Self-Healing, Amazon CloudWatch Container Insights, Scalability, Operational Excellence.
- **Practical Use Case**: Netflix recovers from pod failures during peak streaming.
- **Outcome**: Cluster restores, app remains accessible.

##### 4. Wrap-Up: War Room Debrief (30-45 min)
- **Goal**: Reflect on Kubernetes learnings and prepare for Day 5.
- **Activities**: 
  - Demo: Visit `http://<alb-dns>` and `/api/status`.
  - Discuss sabotage fixes (e.g., self-healing, ingress).
  - Prep for capstone (Day 5).
- **AWS Keywords**: Operational Excellence, Performance Efficiency, Cost Optimization, Reliability.
- **Practical Use Case**: Lessons apply to Netflix’s EKS-based streaming APIs.

---

#### Key Outcomes
- **Theory Learned**: Kubernetes orchestration, EKS architecture, DevOps resilience.
- **Practical Skills**: Deployed a microservices app on EKS with ALB, EBS, and Container Insights.

#### AWS Keywords Covered
- **Amazon EKS**: Managed Kubernetes.
- **Kubernetes**: Orchestration platform.
- **AWS Load Balancer Controller**: ALB integration.
- **Amazon EBS**: Persistent storage.
- **Amazon CloudWatch Container Insights**: Monitoring.
- **AWS IAM**: Access control.
- **Amazon VPC**: Network isolation.
- **AWS Auto Scaling**: Node scaling.
- **AWS KMS**: Encryption (future use).
- **AWS CloudFormation**: IaC (alternative).
- **Amazon Route 53**: DNS (future use).
- **AWS Secrets Manager**: Secrets (future use).
- **AWS X-Ray**: Tracing (future use).
- **Amazon S3**: Artifact storage (future use).
- **AWS Trusted Advisor**: Best practices.
- **Operational Excellence**: Efficiency.
- **Reliability**: Fault tolerance.
- **Scalability**: Pod scaling.
- **Performance Efficiency**: Optimized resources.
- **Security Best Practices**: Hardening.
- **Cost Optimization**: Managed nodes.
- **Continuous Deployment**: Pipeline-ready.

---

#### Practical Use Cases
1. **Netflix Streaming**: Deploy UI and API on EKS, scale with viewer demand, recover from failures.
2. **E-Commerce Platform**: Run storefront and payment API, use EBS for cart data.
3. **Real-Time Processing**: Process streaming analytics, monitor with Container Insights.

---
