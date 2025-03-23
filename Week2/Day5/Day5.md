Let’s cap off Week 2 with **Week 2, Day 5: Kubernetes on AWS EKS Capstone - "Production Siege"**, an advanced, real-world-focused exploration of Kubernetes on **Amazon EKS**. This day ties together CI/CD (Day 1), serverless (Day 2), containers (Day 3), and Kubernetes fundamentals (Day 4), delivering an **extensively informative** capstone with deep **AWS and Kubernetes theory**, **DevOps theoretical knowledge**, and **practical use cases** rooted in real-world DevOps implementations. 

We’ll deploy a production-grade microservices application (e.g., a streaming platform), integrating EKS with AWS services like **Elastic Load Balancer (ALB)**, **Amazon EBS CSI Driver**, **Amazon CloudWatch Container Insights**, and **AWS CodePipeline**, while surviving a "Production Siege" challenge (e.g., traffic spikes, node failures). Keyword explanations draw from AWS and Kubernetes docs (e.g., [EKS User Guide](https://docs.aws.amazon.com/eks/latest/userguide/), [Kubernetes Concepts](https://kubernetes.io/docs/concepts/)), ensuring relevance to Fortune 500-scale DevOps workflows like those at Netflix, Spotify, or Airbnb.

---

### Week 2, Day 5: Kubernetes on AWS EKS Capstone - "Production Siege"

#### Objective
Deploy a **production-ready microservices application** (React frontend, Node.js API, Redis cache) on **Amazon EKS**, integrating AWS-native tools and a CI/CD pipeline, and defending against a simulated "Production Siege" (e.g., traffic overload, pod failures, misconfigurations) to ensure scalability, resilience, and observability in a real-world DevOps context.

#### Duration
6-7 hours (capstone depth)

#### Tools
- AWS Management Console, AWS CLI, `kubectl`, `eksctl`, Helm, Docker, Git, AWS CodePipeline, Bash, Text Editor (e.g., VS Code).

#### Goal as a DevOps Engineer
- **Practical Implementation**: Automate the deployment of a microservices app on EKS, leveraging Kubernetes constructs (pods, deployments, services, ingress) and AWS integrations (ALB, EBS, CloudWatch), with a CI/CD pipeline for continuous deployment.
- **Focus**: Build a scalable, fault-tolerant, and observable Kubernetes cluster, embodying AWS and DevOps best practices (e.g., automation, resilience, shift-left security) tailored to real-world production scenarios.

---

### Content Breakdown

#### 1. Theory: EKS, Kubernetes in Production, and DevOps Best Practices (1.5 hours)
- **Goal**: Provide a comprehensive theoretical foundation for running Kubernetes on EKS in production, with detailed keyword explanations tied to real-world DevOps use cases.
- **Materials**: Slides/video, [EKS Docs](https://docs.aws.amazon.com/eks/latest/userguide/), [Kubernetes Production](https://kubernetes.io/docs/setup/production-environment/), [AWS Well-Architected](https://docs.aws.amazon.com/wellarchitected/latest/framework/).
- **Key Concepts & Keywords**:
  - **EKS and Kubernetes Theory**:
    - **Amazon EKS**: AWS-managed Kubernetes control plane, running master nodes ([EKS Overview](https://docs.aws.amazon.com/eks/latest/userguide/what-is-eks.html)).
      - **Explanation**: AWS manages API server, etcd; you configure worker nodes or Fargate.
    - **Cluster**: EKS control plane + worker nodes (e.g., EC2 or Fargate).
      - **Explanation**: Hosts production workloads with high availability (HA).
    - **Pod**: Smallest unit, running containers (e.g., API pod with Redis sidecar).
      - **Explanation**: Scales horizontally in production.
    - **Deployment**: Manages pod replicas, updates, and rollbacks.
      - **Explanation**: Ensures app versioning (e.g., v1.0 to v1.1).
    - **Service**: Stable endpoint for pods (e.g., LoadBalancer with ALB).
      - **Explanation**: Exposes apps internally/externally.
    - **Ingress**: Routes HTTP traffic via ALB ([Ingress Concepts](https://kubernetes.io/docs/concepts/services-networking/ingress/)).
      - **Explanation**: Maps domains to services (e.g., `stream.example.com`).
    - **Horizontal Pod Autoscaler (HPA)**: Scales pods based on CPU/memory metrics.
      - **Explanation**: Handles traffic spikes (e.g., 10 to 50 pods).
    - **PersistentVolume (PV)**: Storage for stateful apps via EBS ([PV Concepts](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)).
      - **Explanation**: Persists data (e.g., Redis cache).
  - **AWS Integrations**:
    - **AWS Load Balancer Controller**: Integrates ALB with Ingress for dynamic routing.
      - **Explanation**: Replaces Nginx Ingress, AWS-native.
    - **Amazon EBS CSI Driver**: Provides EBS volumes for pods.
      - **Explanation**: Ensures stateful resilience (e.g., Redis persistence).
    - **Amazon CloudWatch Container Insights**: Monitors cluster metrics/logs.
      - **Explanation**: Tracks pod health, CPU/memory in production.
    - **AWS CodePipeline**: Automates CI/CD for Kubernetes deployments.
      - **Explanation**: Deploys updates from GitHub to EKS.
    - **AWS Shared Responsibility Model**: AWS secures EKS control plane; you secure apps, nodes, and data.
      - **Explanation**: Defines production security boundaries.
  - **DevOps Best Practices**:
    - **Automation**: CI/CD pipelines deploy to EKS.
    - **Collaboration**: GitOps with manifests in Git.
    - **Continuous Deployment**: Zero-downtime updates via rolling deployments.
    - **Observability**: CloudWatch, X-Ray, and kubectl for monitoring.
    - **Shift Left**: Security checks in CI (e.g., image scanning).
    - **Resilience**: Self-healing, auto-scaling, and HA clusters.
    - **Cost Optimization**: Right-size nodes, use Spot Instances.
    - **Security**: IAM roles, RBAC, network policies.
- **Keywords**: Amazon EKS, Kubernetes, Cluster, Pod, Deployment, Service, Ingress, Horizontal Pod Autoscaler, PersistentVolume, AWS Load Balancer Controller, Amazon EBS CSI Driver, Amazon CloudWatch Container Insights, AWS CodePipeline, Automation, Collaboration, Continuous Deployment, Observability, Shift Left, Resilience, Cost Optimization, Security, AWS Shared Responsibility Model, Microservices, Production Readiness.

- **Sub-Activities**:
  1. **EKS in Production (20 min)**:
     - **Concept**: EKS runs Kubernetes with AWS HA.
     - **Keywords**: Amazon EKS, Cluster, Deployment.
     - **Details**: Managed control plane across AZs; workers scale.
     - **Use Case**: Netflix runs EKS for global streaming APIs.
     - **Why**: Simplifies Kubernetes ops at scale.
  2. **Scaling and Resilience (20 min)**:
     - **Concept**: HPA and self-healing handle production loads.
     - **Keywords**: Horizontal Pod Autoscaler, Self-Healing.
     - **Details**: Scales pods; restarts failures automatically.
     - **Use Case**: Spotify scales pods during playlist surges.
     - **Why**: Ensures uptime, a DevOps must.
  3. **Storage and State (15 min)**:
     - **Concept**: EBS CSI Driver persists data.
     - **Keywords**: PersistentVolume, Amazon EBS CSI Driver.
     - **Details**: EBS volumes for Redis, databases.
     - **Use Case**: Airbnb stores booking data in EKS.
     - **Why**: Supports stateful apps in production.
  4. **CI/CD and Automation (20 min)**:
     - **Concept**: CodePipeline deploys to EKS.
     - **Keywords**: AWS CodePipeline, Continuous Deployment.
     - **Details**: Automates Git-to-cluster updates.
     - **Use Case**: Netflix deploys microservices continuously.
     - **Why**: Speeds releases, a DevOps pillar.
  5. **Observability and Security (15 min)**:
     - **Concept**: CloudWatch and IAM secure/monitor clusters.
     - **Keywords**: Amazon CloudWatch Container Insights, Security.
     - **Details**: Logs metrics; RBAC restricts access.
     - **Use Case**: Netflix monitors pod latency, secures APIs.
     - **Why**: Visibility and safety are DevOps essentials.

---

#### 2. Lab: Deploy a Production-Grade App on EKS with CI/CD (3-3.5 hours)
- **Goal**: Deploy a microservices app (React frontend, Node.js API, Redis cache) on EKS, automate with CodePipeline, and prepare for production.

##### Initial Setup
- **Tools**: AWS CLI, `eksctl`, `kubectl`, Docker, Helm.
- **Commands**:
  1. **Install AWS CLI**:
     ```bash
     curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
     unzip awscliv2.zip
     sudo ./aws/install
     aws --version
     ```
  2. **Install `eksctl`**:
     ```bash
     curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp
     sudo mv /tmp/eksctl /usr/local/bin
     eksctl version
     ```
  3. **Install `kubectl`**:
     ```bash
     curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
     sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
     kubectl version --client
     ```
  4. **Install Docker**:
     ```bash
     sudo yum install docker -y
     sudo systemctl start docker
     sudo usermod -aG docker ec2-user
     docker --version
     ```
  5. **Install Helm**:
     ```bash
     curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3
     chmod +x get_helm.sh
     ./get_helm.sh
     helm version
     ```
  6. **Set Up Project**:
     ```bash
     mkdir eks-capstone
     cd eks-capstone
     git init
     echo "node_modules/
     *.zip
     build/" > .gitignore
     git remote add origin https://github.com/<your-username>/eks-capstone.git
     ```

##### Practical Implementation
- **Folder Structure**:
  ```
  eks-capstone/
  ├── frontend/                # React frontend
  │   ├── src/
  │   │   ├── App.js          # Main component
  │   │   └── index.js        # Entry point
  │   ├── Dockerfile          # Docker config
  │   ├── package.json        # Dependencies
  │   └── nginx.conf          # Nginx config
  ├── api/                    # Node.js API
  │   ├── index.js           # API logic
  │   ├── Dockerfile         # Docker config
  │   └── package.json       # Dependencies
  ├── k8s/                    # Kubernetes manifests
  │   ├── frontend-deployment.yaml
  │   ├── frontend-service.yaml
  │   ├── api-deployment.yaml
  │   ├── api-service.yaml
  │   ├── redis-deployment.yaml
  │   ├── redis-service.yaml
  │   ├── ingress.yaml
  │   └── redis-pvc.yaml
  ├── pipeline/               # CI/CD
  │   ├── buildspec.yml       # CodeBuild spec
  │   └── pipeline.yml        # CodePipeline config
  └── README.md              # Docs
  ```

- **Task 1: Build Containers**:
  - **Frontend (React)**:
    ```bash
    cd frontend
    npx create-react-app .
    nano src/App.js
    ```
    - **Content** (`src/App.js`):
      ```javascript
      import React, { useState, useEffect } from 'react';

      function App() {
        const [status, setStatus] = useState('Loading...');
        useEffect(() => {
          fetch('/api/status')
            .then(res => res.json())
            .then(data => setStatus(data.message))
            .catch(err => setStatus('Error: ' + err.message));
        }, []);

        return (
          <div>
            <h1>Streaming Platform</h1>
            <p>API Status: {status}</p>
          </div>
        );
      }

      export default App;
      ```
    ```bash
    nano Dockerfile
    ```
    - **Content** (`Dockerfile`):
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
    ```bash
    nano nginx.conf
    ```
    - **Content** (`nginx.conf`):
      ```nginx
      server {
          listen 80;
          location / {
              root /usr/share/nginx/html;
              try_files $uri $uri/ /index.html;
          }
          location /api/ {
              proxy_pass http://api-service:3000/;
              proxy_set_header Host $host;
          }
      }
      ```
  - **API (Node.js)**:
    ```bash
    cd ../api
    npm init -y
    npm install express redis
    nano index.js
    ```
    - **Content** (`index.js`):
      ```javascript
      const express = require('express');
      const redis = require('redis');
      const app = express();
      const port = process.env.PORT || 3000;

      const client = redis.createClient({ url: 'redis://redis-service:6379' });
      client.connect().catch(console.error);

      app.get('/api/status', async (req, res) => {
        const cached = await client.get('status');
        if (cached) return res.json({ message: cached, source: 'cache' });
        const message = 'API is live';
        await client.setEx('status', 60, message);
        res.json({ message, source: 'live' });
      });

      app.listen(port, () => console.log(`API on port ${port}`));
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

- **Task 2: Push to ECR**:
  - **Commands**: 
    ```bash
    aws ecr create-repository --repository-name streaming-frontend --region us-east-1
    aws ecr create-repository --repository-name streaming-api --region us-east-1
    aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com
    cd frontend
    docker build -t streaming-frontend .
    docker tag streaming-frontend:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/streaming-frontend:latest
    docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/streaming-frontend:latest
    cd ../api
    docker build -t streaming-api .
    docker tag streaming-api:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/streaming-api:latest
    docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/streaming-api:latest
    ```

- **Task 3: Create EKS Cluster**:
  - **Commands**: 
    ```bash
    eksctl create cluster \
      --name StreamingCluster \
      --region us-east-1 \
      --nodegroup-name prod-workers \
      --node-type t3.large \
      --nodes 3 \
      --nodes-min 2 \
      --nodes-max 6 \
      --managed \
      --asg-access
    kubectl get nodes  # Verify
    ```

- **Task 4: Install Add-ons**:
  - **AWS Load Balancer Controller**:
    ```bash
    eksctl utils associate-iam-oidc-provider --cluster StreamingCluster --approve
    aws iam create-policy --policy-name AWSLoadBalancerControllerIAMPolicy --policy-document file://<(curl -s https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/main/docs/install/iam_policy.json)
    eksctl create iamserviceaccount \
      --cluster StreamingCluster \
      --namespace kube-system \
      --name aws-load-balancer-controller \
      --attach-policy-arn arn:aws:iam::<account-id>:policy/AWSLoadBalancerControllerIAMPolicy \
      --approve
    helm repo add eks https://aws.github.io/eks-charts
    helm install aws-load-balancer-controller eks/aws-load-balancer-controller \
      --namespace kube-system \
      --set clusterName=StreamingCluster \
      --set serviceAccount.create=false \
      --set serviceAccount.name=aws-load-balancer-controller
    ```
  - **EBS CSI Driver**:
    ```bash
    eksctl create addon --name aws-ebs-csi-driver --cluster StreamingCluster --service-account-role-arn arn:aws:iam::<account-id>:role/AmazonEKS_EBS_CSI_DriverRole --force
    ```
  - **CloudWatch Container Insights**:
    ```bash
    eksctl create addon --name aws-cloudwatch-metrics --cluster StreamingCluster --force
    ```

- **Task 5: Deploy App with Kubernetes Manifests**:
  - **Commands**: 
    ```bash
    cd k8s
    nano frontend-deployment.yaml
    ```
    - **Content**:
      ```yaml
      apiVersion: apps/v1
      kind: Deployment
      metadata:
        name: frontend
      spec:
        replicas: 3
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
              resources:
                limits:
                  cpu: "500m"
                  memory: "512Mi"
                requests:
                  cpu: "200m"
                  memory: "256Mi"
              livenessProbe:
                httpGet:
                  path: /
                  port: 80
                initialDelaySeconds: 5
                periodSeconds: 10
      ```
    ```bash
    nano frontend-service.yaml
    ```
    - **Content**:
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
    - **Content**:
      ```yaml
      apiVersion: apps/v1
      kind: Deployment
      metadata:
        name: api
      spec:
        replicas: 3
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
              resources:
                limits:
                  cpu: "500m"
                  memory: "512Mi"
                requests:
                  cpu: "200m"
                  memory: "256Mi"
              livenessProbe:
                httpGet:
                  path: /api/status
                  port: 3000
                initialDelaySeconds: 5
                periodSeconds: 10
      ```
    ```bash
    nano api-service.yaml
    ```
    - **Content**:
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
    nano redis-deployment.yaml
    ```
    - **Content**:
      ```yaml
      apiVersion: apps/v1
      kind: Deployment
      metadata:
        name: redis
      spec:
        replicas: 1
        selector:
          matchLabels:
            app: redis
        template:
          metadata:
            labels:
              app: redis
          spec:
            containers:
            - name: redis
              image: redis:alpine
              ports:
              - containerPort: 6379
              volumeMounts:
              - name: redis-storage
                mountPath: /data
            volumes:
            - name: redis-storage
              persistentVolumeClaim:
                claimName: redis-pvc
      ```
    ```bash
    nano redis-service.yaml
    ```
    - **Content**:
      ```yaml
      apiVersion: v1
      kind: Service
      metadata:
        name: redis-service
      spec:
        selector:
          app: redis
        ports:
        - port: 6379
          targetPort: 6379
      ```
    ```bash
    nano redis-pvc.yaml
    ```
    - **Content**:
      ```yaml
      apiVersion: v1
      kind: PersistentVolumeClaim
      metadata:
        name: redis-pvc
      spec:
        accessModes:
        - ReadWriteOnce
        resources:
          requests:
            storage: 1Gi
        storageClassName: gp2
      ```
    ```bash
    nano ingress.yaml
    ```
    - **Content**:
      ```yaml
      apiVersion: networking.k8s.io/v1
      kind: Ingress
      metadata:
        name: streaming-ingress
        annotations:
          kubernetes.io/ingress.class: alb
          alb.ingress.kubernetes.io/scheme: internet-facing
          alb.ingress.kubernetes.io/target-type: ip
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
    kubectl apply -f .
    kubectl get ingress streaming-ingress -o jsonpath='{.status.loadBalancer.ingress[0].hostname}'
    ```

- **Task 6: Set Up CI/CD with CodePipeline**:
  - **Commands**: 
    ```bash
    cd ../pipeline
    nano buildspec.yml
    ```
    - **Content**:
      ```yaml
      version: 0.2
      phases:
        pre_build:
          commands:
            - echo Logging in to Amazon ECR...
            - aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com
        build:
          commands:
            - echo Building frontend...
            - cd frontend
            - docker build -t streaming-frontend .
            - docker tag streaming-frontend:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/streaming-frontend:latest
            - docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/streaming-frontend:latest
            - cd ../api
            - docker build -t streaming-api .
            - docker tag streaming-api:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/streaming-api:latest
            - docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/streaming-api:latest
        post_build:
          commands:
            - echo Deploying to EKS...
            - kubectl apply -f ../k8s/
      ```
    ```bash
    nano pipeline.yml
    ```
    - **Content**:
      ```yaml
      AWSTemplateFormatVersion: '2010-09-09'
      Resources:
        Pipeline:
          Type: AWS::CodePipeline::Pipeline
          Properties:
            RoleArn: !GetAtt PipelineRole.Arn
            ArtifactStore:
              Type: S3
              Location: !Ref S3Bucket
            Stages:
              - Name: Source
                Actions:
                  - Name: Source
                    ActionTypeId:
                      Category: Source
                      Owner: ThirdParty
                      Provider: GitHub
                      Version: '1'
                    OutputArtifacts:
                      - Name: SourceOutput
                    Configuration:
                      Owner: <your-username>
                      Repo: eks-capstone
                      Branch: main
                      OAuthToken: <github-token>
              - Name: Build
                Actions:
                  - Name: Build
                    ActionTypeId:
                      Category: Build
                      Owner: AWS
                      Provider: CodeBuild
                      Version: '1'
                    InputArtifacts:
                      - Name: SourceOutput
                    OutputArtifacts:
                      - Name: BuildOutput
                    Configuration:
                      ProjectName: !Ref BuildProject
        S3Bucket:
          Type: AWS::S3::Bucket
        PipelineRole:
          Type: AWS::IAM::Role
          Properties:
            AssumeRolePolicyDocument:
              Version: '2012-10-17'
              Statement:
                - Effect: Allow
                  Principal:
                    Service: codepipeline.amazonaws.com
                  Action: sts:AssumeRole
            Policies:
              - PolicyName: PipelinePolicy
                PolicyDocument:
                  Version: '2012-10-17'
                  Statement:
                    - Effect: Allow
                      Action:
                        - s3:*
                        - codebuild:*
                        - eks:*
                        - iam:PassRole
                      Resource: '*'
        BuildProject:
          Type: AWS::CodeBuild::Project
          Properties:
            Name: EKSBuild
            Source:
              Type: CODEPIPELINE
              BuildSpec: pipeline/buildspec.yml
            Artifacts:
              Type: CODEPIPELINE
            Environment:
              Type: LINUX_CONTAINER
              Image: aws/codebuild/standard:5.0
              ComputeType: BUILD_GENERAL1_SMALL
            ServiceRole: !GetAtt BuildRole.Arn
        BuildRole:
          Type: AWS::IAM::Role
          Properties:
            AssumeRolePolicyDocument:
              Version: '2012-10-17'
              Statement:
                - Effect: Allow
                  Principal:
                    Service: codebuild.amazonaws.com
                  Action: sts:AssumeRole
            Policies:
              - PolicyName: BuildPolicy
                PolicyDocument:
                  Version: '2012-10-17'
                  Statement:
                    - Effect: Allow
                      Action:
                        - s3:*
                        - ecr:*
                        - eks:*
                        - logs:*
                      Resource: '*'
      ```
  - **Deploy**:
    ```bash
    aws cloudformation create-stack --stack-name EKSPipeline --template-body file://pipeline.yml --capabilities CAPABILITY_NAMED_IAM
    aws cloudformation wait stack-create-complete --stack-name EKSPipeline
    ```
  - **Push to GitHub**:
    ```bash
    git add .
    git commit -m "Initial EKS capstone"
    git push origin main
    ```

##### 3. Chaos Twist: "Production Siege" (1-1.5 hours)
- **Goal**: Defend against a simulated production siege (e.g., traffic spike, node failure), reinforcing real-world DevOps skills.
- **Scenario**: Instructor simulates load (`ab -n 10000 -c 100 http://<alb-dns>/`) or terminates nodes (EKS > Node Groups > Delete).
- **Task**: 
  - Monitor: `kubectl get pods -w`, `aws cloudwatch get-metric-statistics --namespace AWS/EKS --metric-name CPUUtilization --dimensions Name=ClusterName,Value=StreamingCluster`.
  - Scale: `kubectl scale deployment api --replicas=6`.
  - Check HPA: `kubectl get hpa` (add if needed: `kubectl autoscale deployment api --cpu-percent=70 --min=3 --max=10`).
  - Recover: `eksctl scale nodegroup --cluster StreamingCluster --name prod-workers --nodes 4`.
- **Use Case**: Netflix handles a new season drop with millions of viewers.
- **Outcome**: App scales, recovers, remains available.

##### 4. Wrap-Up: War Room Debrief (45 min)
- **Goal**: Reflect on production readiness and DevOps lessons.
- **Activities**: 
  - Demo: Visit `http://<alb-dns>` and `/api/status`.
  - Discuss siege fixes (e.g., HPA, node scaling).
  - Review pipeline logs (CodePipeline Console).
- **Use Case**: Lessons apply to Spotify’s playlist API or Airbnb’s booking system.

---

#### Key Outcomes
- **Theory Learned**: EKS production architecture, Kubernetes scaling, DevOps practices.
- **Practical Skills**: Deployed a microservices app on EKS with CI/CD, survived production challenges.

#### Practical Use Cases
1. **Netflix Streaming**: EKS cluster with frontend, API, and Redis; scales for global viewers.
2. **Spotify Playlists**: API caches playlists in Redis, ALB routes traffic, pipeline deploys updates.
3. **Airbnb Bookings**: Stateful Redis for bookings, EKS ensures HA, CloudWatch tracks latency.

---

This Day 5 delivers a real-world DevOps capstone, blending EKS, Kubernetes, and AWS for production-grade scenarios.