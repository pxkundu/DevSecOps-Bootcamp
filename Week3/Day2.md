**Week 3, Day 2: Intermediate Jenkins - "Scaling Pipelines"** with an **extensively informative** breakdown, combining deep theoretical explanations with practical, real-world DevOps implementations. 

Today we will build on the SaaS Task Manager project from Day 1, enhancing the Jenkins pipeline for intermediate-level scalability and team collaboration. We’ll focus on multi-branch pipelines, distributed builds with static EC2 agents, and AWS integrations (e.g., S3, EKS), tailored for a production-grade CI/CD workflow as of March 11, 2025. 

The content is designed for an intermediate DevOps engineer, tying theory to the Task Manager app’s evolution.

---

### Week 3, Day 2: Intermediate Jenkins - "Scaling Pipelines"

#### Objective
Scale the Task Manager’s Jenkins pipeline by:
- Supporting multiple Git branches (e.g., `main`, `dev`) for parallel development.
- Distributing builds across static EC2 agents for performance.
- Integrating AWS S3 for artifacts and EKS for deployment with rollback capabilities.

#### Tools
- Jenkins, AWS EC2 (master + agents), GitHub, Docker, AWS S3, AWS EKS, AWS IAM, `kubectl`.

#### Duration
5-6 hours (2h theory, 3-4h practical + engagement).

#### Relation to Task Manager
- Day 1 set up a basic pipeline with backend (task API) and frontend (task UI) containers on a single slave. Day 2 scales this to handle team workflows (e.g., feature branches) and production deployments.

---

### Theoretical Keyword Explanation
Below are key concepts with detailed explanations, linked to DevOps theory and real-world Task Manager use cases.

1. **Multi-Branch Pipelines**
   - **Definition**: Jenkins jobs that automatically detect and build all branches/PRs in a Git repo, enabling parallel development.
   - **Keywords**:
     - **Branch Discovery**: Scans GitHub for branches (e.g., `main`, `feature/add-user`).
     - **PR Validation**: Builds PRs before merging, ensuring code quality.
     - **Feature Toggles**: Conditional logic (e.g., `if (BRANCH_NAME == 'main')`) for env-specific deploys.
   - **Real-World**: Spotify uses multi-branch pipelines to test playlist features in `dev` before merging to `main`.
   - **Task Manager Use**: Devs work on `dev` (new task filters), ops deploy `main` to prod—parallel builds cut conflicts.
   - **Why It Matters**: Speeds up team velocity (e.g., 5 devs → 5 branches) and catches bugs early.

2. **Distributed Builds**
   - **Definition**: Offloading pipeline stages to multiple agents (e.g., EC2 instances) for parallel execution.
   - **Keywords**:
     - **Static Agents**: Pre-provisioned nodes (e.g., EC2) with fixed capacity.
     - **Load Balancing**: Jenkins assigns jobs to least-busy agents.
     - **Agent Provisioning**: Manual setup (Day 2) vs. dynamic (Day 3).
   - **Real-World**: Netflix runs 100+ agents to build microservices concurrently, handling 1000s of daily commits.
   - **Task Manager Use**: Backend and frontend builds run on separate agents, reducing build time from 10m to 5m.
   - **Why It Matters**: Scales CI/CD for growing teams and complex apps.

3. **Environment Isolation**
   - **Definition**: Separating dev, staging, and prod workflows in pipelines to prevent cross-contamination.
   - **Keywords**:
     - **Environment Variables**: `ENV` (e.g., `dev`, `prod`) drives behavior.
     - **Conditional Stages**: Skip prod steps in `dev` builds.
     - **Namespace Segregation**: EKS namespaces (e.g., `task-dev`, `task-prod`).
   - **Real-World**: A fintech isolates staging (test payments) from prod (real transactions) to meet compliance.
   - **Task Manager Use**: `dev` builds test locally, `main` deploys to EKS prod namespace.
   - **Why It Matters**: Ensures prod stability while devs experiment.

4. **Artifact Management**
   - **Definition**: Storing build outputs (e.g., Docker images, logs) in a durable repository like S3.
   - **Keywords**:
     - **Versioning**: Tag artifacts (e.g., `task-backend:1.2-$BUILD_NUMBER`).
     - **Durability**: S3 persists artifacts beyond Jenkins workspace.
     - **Retrieval**: Pull artifacts for rollback or audits.
   - **Real-World**: Walmart stores catalog images in S3 for rollback during sales peaks.
   - **Task Manager Use**: Backend/fronted images in S3 allow reverting to last stable version.
   - **Why It Matters**: Enables traceability and recovery.

5. **Rollback Strategies**
   - **Definition**: Reverting to a previous state (e.g., Docker image) after a failed deploy.
   - **Keywords**:
     - **Image Tagging**: Stable tags (e.g., `:1.2`) for rollback.
     - **kubectl Rollout**: `kubectl rollout undo` reverts EKS deployments.
     - **Post-Failure**: Automate rollback in `post` block.
   - **Real-World**: An e-commerce site rolls back a buggy checkout update in <5 mins.
   - **Task Manager Use**: Failed prod deploy (e.g., API crash) reverts to last working image.
   - **Why It Matters**: Minimizes downtime (e.g., MTTR <10m).

6. **AWS Integration**
   - **Definition**: Leveraging AWS services (S3, EKS, IAM) to enhance Jenkins pipelines.
   - **Keywords**:
     - **IAM Roles**: Limit agent perms (e.g., S3 write, EKS deploy).
     - **S3**: Artifact storage with lifecycle policies.
     - **EKS**: Scalable Kubernetes for prod deploys.
   - **Real-World**: A SaaS firm uses EKS for task apps, S3 for logs, and IAM for security.
   - **Task Manager Use**: S3 stores images, EKS runs prod, IAM secures access.
   - **Why It Matters**: Aligns with cloud-native DevOps trends.

7. **Scaling Challenges**
   - **Keywords**:
     - **Agent Sprawl**: Too many idle agents waste cost—cap at need.
     - **Pipeline Bottlenecks**: Slow tests delay deploys—parallelize.
     - **Dependency Hell**: Unpinned versions break builds—lock `package.json`.
   - **Real-World**: A startup over-provisioned agents, costing $500/month extra.
   - **Task Manager Use**: Two agents suffice for now, avoiding sprawl.
   - **Why It Matters**: Optimizes cost and speed.

---

### Practical Use Cases and Implementation
We’ll enhance the Task Manager pipeline from Day 1, scaling it with multi-branch support, two static EC2 agents, and AWS integration.

#### Step 1: Update GitHub Repository
- **Goal**: Add multi-branch logic and EKS manifests.
- **Implementation**:
  - Update `Jenkinsfile`:
    ```groovy
    pipeline {
        agent none
        parameters {
            string(name: 'BRANCH_NAME', defaultValue: 'main', description: 'Git branch to build')
            choice(name: 'ENVIRONMENT', choices: ['dev', 'staging', 'prod'], description: 'Deployment env')
        }
        environment {
            APP_NAME = 'task-manager'
            GIT_REPO = 'https://github.com/<your-username>/task-manager.git'
            BACKEND_IMAGE = "task-backend:${BUILD_NUMBER}"
            FRONTEND_IMAGE = "task-frontend:${BUILD_NUMBER}"
            S3_BUCKET = '<your-bucket>'
            EKS_CLUSTER = 'TaskCluster'
        }
        stages {
            stage('Setup Slave') {
                agent { label 'linux-slave' }
                steps {
                    withCredentials([usernamePassword(credentialsId: 'github-token', usernameVariable: 'GIT_USER', passwordVariable: 'GIT_TOKEN')]) {
                        git url: "${GIT_REPO}", branch: "${BRANCH_NAME}", credentialsId: 'github-token'
                    }
                    sh 'chmod +x scripts/*.sh'
                    sh './scripts/install_base.sh'
                    sh './scripts/install_nodejs.sh'
                    sh './scripts/config_docker.sh'
                }
            }
            stage('Build') {
                parallel {
                    stage('Backend') {
                        agent { label 'linux-slave-backend' }
                        steps {
                            dir('backend') {
                                sh 'docker build -t ${BACKEND_IMAGE} .'
                                withAWS(credentials: 'aws-creds', region: 'us-east-1') {
                                    sh 'aws ecr get-login-password | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com'
                                    sh 'docker tag ${BACKEND_IMAGE} <account-id>.dkr.ecr.us-east-1.amazonaws.com/${BACKEND_IMAGE}'
                                    sh 'docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/${BACKEND_IMAGE}'
                                    sh 'aws s3 cp Dockerfile s3://${S3_BUCKET}/artifacts/backend-${BUILD_NUMBER}/'
                                }
                            }
                        }
                    }
                    stage('Frontend') {
                        agent { label 'linux-slave-frontend' }
                        steps {
                            dir('frontend') {
                                sh 'docker build -t ${FRONTEND_IMAGE} .'
                                withAWS(credentials: 'aws-creds', region: 'us-east-1') {
                                    sh 'docker tag ${FRONTEND_IMAGE} <account-id>.dkr.ecr.us-east-1.amazonaws.com/${FRONTEND_IMAGE}'
                                    sh 'docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/${FRONTEND_IMAGE}'
                                    sh 'aws s3 cp Dockerfile s3://${S3_BUCKET}/artifacts/frontend-${BUILD_NUMBER}/'
                                }
                            }
                        }
                    }
                }
            }
            stage('Deploy to EKS') {
                agent { label 'linux-slave' }
                when { expression { params.ENVIRONMENT == 'prod' && BRANCH_NAME == 'main' } }
                steps {
                    withAWS(credentials: 'aws-creds', region: 'us-east-1') {
                        sh 'aws eks update-kubeconfig --name ${EKS_CLUSTER} --region us-east-1'
                        sh 'kubectl apply -f k8s/ -n task-${ENVIRONMENT}'
                        sh 'kubectl set image deployment/backend backend=<account-id>.dkr.ecr.us-east-1.amazonaws.com/${BACKEND_IMAGE} -n task-${ENVIRONMENT}'
                        sh 'kubectl set image deployment/frontend frontend=<account-id>.dkr.ecr.us-east-1.amazonaws.com/${FRONTEND_IMAGE} -n task-${ENVIRONMENT}'
                        sh 'kubectl rollout status deployment/backend -n task-${ENVIRONMENT}'
                        sh 'kubectl rollout status deployment/frontend -n task-${ENVIRONMENT}'
                    }
                }
                post {
                    failure {
                        sh 'kubectl rollout undo deployment/backend -n task-${ENVIRONMENT}'
                        sh 'kubectl rollout undo deployment/frontend -n task-${ENVIRONMENT}'
                    }
                }
            }
        }
        post {
            always {
                sh 'docker logs task-backend > backend.log 2>&1 || true'
                sh 'docker logs task-frontend > frontend.log 2>&1 || true'
                archiveArtifacts artifacts: '*.log', allowEmptyArchive: true
                sh 'rm -f *.log'
            }
        }
    }
    ```
  - Add `k8s/backend-deployment.yaml`:
    ```yaml
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: backend
    spec:
      replicas: 2
      selector:
        matchLabels:
          app: backend
      template:
        metadata:
          labels:
            app: backend
        spec:
          containers:
          - name: backend
            image: <account-id>.dkr.ecr.us-east-1.amazonaws.com/task-backend:latest
            ports:
            - containerPort: 3000
    ---
    apiVersion: v1
    kind: Service
    metadata:
      name: backend-service
    spec:
      selector:
        app: backend
      ports:
      - port: 3000
        targetPort: 3000
    ```
  - Add `k8s/frontend-deployment.yaml`:
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
            image: <account-id>.dkr.ecr.us-east-1.amazonaws.com/task-frontend:latest
            ports:
            - containerPort: 8080
    ---
    apiVersion: v1
    kind: Service
    metadata:
      name: frontend-service
    spec:
      selector:
        app: frontend
      ports:
      - port: 8080
        targetPort: 8080
    ```
  - Push:
    ```bash
    mkdir -p task-manager/k8s
    git add Jenkinsfile k8s/*
    git commit -m "Add multi-branch and EKS deployment"
    git push origin main
    git checkout -b dev
    git push origin dev
    ```

#### Step 2: Set Up Two Static EC2 Agents
- **Goal**: Add agents for backend and frontend builds.
- **Commands**:
  - Agent 1 (Backend):
    ```bash
    aws ec2 run-instances \
      --image-id ami-0c55b159cbfafe1f0 \
      --instance-type t2.micro \
      --key-name <your-key> \
      --security-group-ids <sg-id> \
      --subnet-id <subnet-id> \
      --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=JenkinsSlaveBackend}]'
    ssh -i <your-key>.pem ec2-user@<backend-agent-ip>
    mkdir -p ~/.ssh
    echo "<master-public-key>" >> ~/.ssh/authorized_keys
    chmod 600 ~/.ssh/authorized_keys
    chmod 700 ~/.ssh
    ```
  - Agent 2 (Frontend):
    ```bash
    aws ec2 run-instances \
      --image-id ami-0c55b159cbfafe1f0 \
      --instance-type t2.micro \
      --key-name <your-key> \
      --security-group-ids <sg-id> \
      --subnet-id <subnet-id> \
      --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=JenkinsSlaveFrontend}]'
    ssh -i <your-key>.pem ec2-user@<frontend-agent-ip>
    mkdir -p ~/.ssh
    echo "<master-public-key>" >> ~/.ssh/authorized_keys
    chmod 600 ~/.ssh/authorized_keys
    chmod 700 ~/.ssh
    ```
  - Configure in Jenkins:
    - `Manage Nodes` > `New Node`:
      - Name: `slave-backend`, Label: `linux-slave-backend`, SSH: `<backend-agent-ip>`, Credentials: `ssh-slave-key`.
      - Name: `slave-frontend`, Label: `linux-slave-frontend`, SSH: `<frontend-agent-ip>`, Credentials: `ssh-slave-key`.

#### Step 3: Configure AWS Resources
- **S3 Bucket**:
  ```bash
  aws s3 mb s3://<your-bucket> --region us-east-1
  ```
- **EKS Cluster** (if not from Week 2):
  ```bash
  eksctl create cluster --name TaskCluster --region us-east-1 --node-type t3.medium --nodes 2
  kubectl create namespace task-dev
  kubectl create namespace task-prod
  ```
- **IAM Role**:
  - Create role `JenkinsAgentRole` with `AmazonS3FullAccess`, `AmazonEKSClusterPolicy`, attach to agents.

#### Step 4: Create Multi-Branch Pipeline
- **Steps**:
  - Jenkins UI: `New Item` > `TaskManagerMultiBranch` > `Multibranch Pipeline`:
    - Branch Sources: Git, URL: `https://github.com/<your-username>/task-manager.git`, Credentials: `github-token`.
    - Build Configuration: Script Path: `Jenkinsfile`.
  - Save > Scan Repository Now.

- **Validation**:
  - Builds run for `main` and `dev`.
  - Console for `main` (prod):
    ```
    [Pipeline] stage (Build)
    [Backend] + docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/task-backend:1
    [Frontend] + docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/task-frontend:1
    [Pipeline] stage (Deploy to EKS)
    + kubectl rollout status deployment/backend -n task-prod
    ```
  - Check EKS:
    ```bash
    kubectl get pods -n task-prod
    ALB_DNS=$(kubectl get svc frontend-service -n task-prod -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')
    curl -X POST -H "Content-Type: application/json" -d '{"title":"Prod Task"}' "http://$ALB_DNS:3000/tasks"
    curl "http://$ALB_DNS:8080/tasks"  # Shows "Prod Task"
    ```

#### Engagement: "Agent Arena"
- **Goal**: Parallelize builds across agents, aim for <5 mins total.
- **Steps**: Time `main` build, tweak agent allocation, share fastest result.

---

### Real-World DevOps Implementations
1. **SaaS Task Manager (Startup)**:
   - Multi-branch pipeline tests `dev` features (e.g., task priority), deploys `main` to EKS prod.
   - Outcome: 10 devs work concurrently, prod updates in <15 mins.
2. **E-Commerce (Walmart-like)**:
   - Distributed builds on agents handle catalog + checkout, S3 stores rollback images.
   - Outcome: Scales to 100+ daily deploys.
3. **Media (Netflix-like)**:
   - Multi-branch CI validates streaming fixes, EKS deploys prod with rollback.
   - Outcome: 99.99% uptime during peaks.

---

### Learning Outcome
- **Theory**: Master multi-branch pipelines, distributed builds, and AWS integration for scalable CI/CD.
- **Practical**: Scale the Task Manager pipeline with parallel agents, S3 artifacts, and EKS deployment.
- **Real-World**: Apply to SaaS, e-commerce, or media workflows, enhancing team productivity.

---

Day 2 evolves the Task Manager into a scalable, team-ready solution. 