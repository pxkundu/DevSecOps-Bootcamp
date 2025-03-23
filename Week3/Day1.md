Let’s kick off **Week 3, Day 1: Jenkins Basics - "Pipeline Foundations"** with an **extensively informative** breakdown, blending deep theoretical explanations with practical, real-world DevOps implementations. 

This day is designed for an intermediate DevOps engineer transitioning from basic concepts to hands-on CI/CD automation, using Jenkins, AWS EC2, and GitHub. 

We’ll anchor it to the To-Do app from Week 2, providing a comprehensive foundation in Jenkins pipeline creation with detailed keyword explanations and industry-relevant use cases. As of March 10, 2025, this reflects modern DevOps practices seen in companies like Walmart, Netflix, and smaller tech firms.

---

### Week 3, Day 1: Jenkins Basics - "Pipeline Foundations"

#### Objective
Establish a solid foundation in Jenkins CI/CD by automating the To-Do app’s build, test, and deployment process on AWS EKS, integrated with GitHub.

#### Tools
- Jenkins, AWS EC2, GitHub, Docker, AWS ECR, AWS EKS, AWS CloudWatch, `kubectl`.

#### Duration
5-6 hours (2h theory, 3-4h practical + engagement).

---

### Theoretical Keyword Explanation
Below are key concepts with detailed explanations, tying them to DevOps theory and real-world relevance.

1. **Jenkins Architecture**
   - **Definition**: Jenkins is an open-source automation server with a master-agent model. The master handles scheduling, UI, and job management, while agents (nodes) execute tasks.
   - **Keywords**: 
     - **Master**: Central controller, hosts `~/.jenkins/` (configs in `config.xml`, jobs in `jobs/`).
     - **Agent**: Worker nodes (e.g., EC2 instances) running builds/tests, connected via SSH or JNLP.
     - **Plugin Ecosystem**: Extends Jenkins (e.g., Git Plugin, Docker Plugin).
   - **Real-World**: Netflix uses a Jenkins master with hundreds of agents to build microservices, ensuring scalability.
   - **Why It Matters**: Understanding this split prevents overloading the master, a common rookie mistake.

2. **CI/CD Principles**
   - **Definition**: Continuous Integration (CI) and Continuous Deployment (CD) automate software delivery.
   - **Keywords**:
     - **Continuous Integration (CI)**: Developers integrate code frequently (e.g., 10 commits/day), validated by automated builds/tests.
     - **Continuous Delivery (CDelivery)**: Code is always deployable, with manual prod deployment.
     - **Continuous Deployment (CDeployment)**: Every passing build auto-deploys to prod.
     - **Feedback Loops**: Quick failure detection (e.g., test fails → notify in <5 mins).
   - **Real-World**: Walmart’s CI ensures frequent e-commerce updates; Netflix’s CDeployment pushes streaming fixes live.
   - **Why It Matters**: Reduces integration hell and accelerates release cycles (days → hours).

3. **Pipeline as Code**
   - **Definition**: Defining CI/CD workflows in a `Jenkinsfile`, stored in VCS (e.g., GitHub), rather than UI jobs.
   - **Keywords**:
     - **Declarative Pipeline**: Structured syntax (e.g., `pipeline { stages { ... } }`).
     - **Scripted Pipeline**: Groovy-based, more flexible but complex.
     - **Version Control**: Tracks pipeline changes alongside app code.
   - **Real-World**: Spotify uses declarative pipelines in Git for playlist service deploys, enabling auditability.
   - **Why It Matters**: Makes pipelines portable, repeatable, and collaborative.

4. **Automation Benefits**
   - **Definition**: Replacing manual tasks with scripted processes.
   - **Keywords**:
     - **Consistency**: Identical builds across envs (e.g., dev = prod).
     - **Speed**: Cuts deploy time (e.g., manual 2h → automated 10m).
     - **Error Reduction**: No human typos or forgotten steps.
   - **Real-World**: A fintech firm automates compliance checks, saving 100+ hours/month.
   - **Why It Matters**: Scales DevOps beyond small teams.

5. **Best Practices**
   - **Keywords**:
     - **Secrets Management**: Store creds in AWS SSM Parameter Store, not plaintext.
     - **Incremental Builds**: Only rebuild changed parts (e.g., Docker caching).
     - **Logging**: Centralize logs (e.g., CloudWatch) for debugging.
     - **Modularity**: Break pipelines into reusable stages.
   - **Real-World**: AWS’s own CI/CD uses SSM for creds, ensuring PCI DSS compliance.
   - **Why It Matters**: Prevents security leaks and optimizes performance.

6. **Common Pitfalls**
   - **Keywords**:
     - **Overloaded Master**: Running builds on master slows it down—use agents.
     - **Untested Code**: Skipping tests risks prod failures.
     - **No Logging**: Blind debugging without logs.
   - **Real-World**: A startup lost 2 days debugging a silent failure due to no logs.
   - **Why It Matters**: Avoids downtime and frustration.

---

### Practical Use Cases and Implementation
We’ll automate the To-Do app’s CI/CD pipeline with Jenkins on EC2, integrating GitHub and AWS. Below are step-by-step commands and real-world parallels.

#### Step 1: Set Up Jenkins on AWS EC2
- **Use Case**: A small e-commerce firm sets up Jenkins to automate product page updates.
- **Commands**:
  ```bash
  # Launch EC2 (t2.medium, Amazon Linux 2)
  aws ec2 run-instances \
    --image-id ami-0c55b159cbfafe1f0 \
    --instance-type t2.medium \
    --key-name <your-key> \
    --security-group-ids <sg-id> \
    --subnet-id <subnet-id> \
    --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=JenkinsMaster}]' \
    --user-data '#!/bin/bash
      yum update -y
      yum install -y java-11-openjdk docker git
      systemctl start docker
      usermod -aG docker ec2-user
      wget -O /etc/yum.repos.d/jenkins.repo https://pkg.jenkins.io/redhat-stable/jenkins.repo
      rpm --import https://pkg.jenkins.io/redhat-stable/jenkins.io.key
      yum install -y jenkins
      systemctl start jenkins
      systemctl enable jenkins
      echo "jenkins ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/jenkins'

  # SSH and verify
  ssh -i <your-key>.pem ec2-user@<ec2-public-ip>
  sudo cat /var/lib/jenkins/secrets/initialAdminPassword
  ```
  - Access: `http://<ec2-public-ip>:8080`, install plugins (Git, Docker, Pipeline, AWS Credentials).

- **Real-World**: Similar to how a retail company provisions Jenkins for catalog updates, ensuring Docker for container builds.

#### Step 2: Configure GitHub and AWS Integration
- **Use Case**: A SaaS startup links Jenkins to GitHub for feature branch builds and ECR for image storage.
- **Commands**:
  ```bash
  # Push To-Do app to GitHub
  cd todo-app
  git init
  git add .
  git commit -m "Initial To-Do app commit"
  git remote add origin https://github.com/<your-username>/todo-app.git
  git push origin main

  # Create ECR repos
  aws ecr create-repository --repository-name todo-api --region us-east-1
  aws ecr create-repository --repository-name todo-frontend --region us-east-1

  # In Jenkins UI:
  # - Manage Jenkins > Manage Plugins > Install: "GitHub Integration", "AWS Credentials"
  # - Manage Jenkins > Global Credentials > Add:
  #   - GitHub token (ID: github-token, generate at github.com/settings/tokens)
  #   - AWS creds (ID: aws-creds, Access Key + Secret Key)

  # Test GitHub connectivity
  git ls-remote https://<github-token>@github.com/<your-username>/todo-app.git
  ```
- **Real-World**: A fintech uses GitHub for code and ECR for PCI-compliant image storage, mirroring this setup.

#### Step 3: Create a Basic Jenkins Pipeline
- **Use Case**: A media company automates a content API’s build and deploy to Kubernetes.
- **Implementation**:
  - Add `Jenkinsfile` to `todo-app/` root:
    ```groovy
    pipeline {
        agent any
        stages {
            stage('Checkout') {
                steps {
                    git url: 'https://github.com/<your-username>/todo-app.git', credentialsId: 'github-token'
                }
            }
            stage('Build Backend') {
                steps {
                    sh 'cd backend && docker build -t todo-api .'
                    withAWS(credentials: 'aws-creds', region: 'us-east-1') {
                        sh 'aws ecr get-login-password | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com'
                        sh 'docker tag todo-api:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/todo-api:latest'
                        sh 'docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/todo-api:latest'
                    }
                }
            }
            stage('Build Frontend') {
                steps {
                    sh 'cd frontend && docker build -t todo-frontend .'
                    withAWS(credentials: 'aws-creds', region: 'us-east-1') {
                        sh 'docker tag todo-frontend:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/todo-frontend:latest'
                        sh 'docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/todo-frontend:latest'
                    }
                }
            }
            stage('Test Backend') {
                steps {
                    sh 'cd backend && npm install && npm test'
                }
            }
            stage('Deploy to EKS') {
                steps {
                    sh 'aws eks update-kubeconfig --region us-east-1 --name TodoCluster'
                    sh 'kubectl apply -f k8s/'
                    sh 'kubectl rollout status deployment/backend'
                    sh 'kubectl rollout status deployment/frontend'
                }
            }
        }
        post {
            always {
                sh '''
                    aws logs create-log-group --log-group-name /jenkins/pipelines || true
                    aws logs create-log-stream --log-group-name /jenkins/pipelines --log-stream-name $BUILD_ID || true
                    echo "[{\\"timestamp\\": $(date +%s000), \\"message\\": \\"Pipeline completed with status: $BUILD_STATUS\\"}]" > log.json
                    aws logs put-log-events --log-group-name /jenkins/pipelines --log-stream-name $BUILD_ID --log-events file://log.json
                '''
            }
        }
    }
    ```
  - Update `backend/package.json`:
    ```json
    "scripts": {
      "start": "node src/index.js",
      "test": "jest"
    }
    ```
  - Add `backend/tests/api.test.js`:
    ```javascript
    const request = require('supertest');
    const app = require('../src/index');

    describe('API Tests', () => {
        test('GET /api/todos returns empty array initially', async () => {
            const res = await request(app).get('/api/todos');
            expect(res.status).toBe(200);
            expect(res.body).toEqual([]);
        });
    });
    ```
  - Install Jest: `cd backend && npm install --save-dev jest supertest`.

- **Commands**:
  ```bash
  # Build and run pipeline
  # In Jenkins UI: New Item > Pipeline > SCM: Git, Repo: https://github.com/<your-username>/todo-app.git, Script Path: Jenkinsfile > Build Now

  # Check Docker images
  docker images | grep todo

  # Verify ECR push
  aws ecr list-images --repository-name todo-api --region us-east-1

  # Debug pipeline
  tail -f /var/log/jenkins/jenkins.log
  cat /var/lib/jenkins/jobs/<job-name>/builds/<build-number>/log

  # Check EKS
  kubectl get pods
  kubectl logs -l app=backend
  kubectl describe deployment backend
  ```

- **Real-World**: A streaming service uses this to deploy API updates hourly, with CloudWatch logs for postmortems.

#### Step 4: Validate Deployment
- **Use Case**: An e-commerce site tests a new checkout feature before prod rollout.
- **Commands**:
  ```bash
  ALB_DNS=$(kubectl get ingress todo-ingress -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')
  curl "http://$ALB_DNS/api/todos"  # Expect []
  curl -X POST "http://$ALB_DNS/api/todos" -H "Content-Type: application/json" -d '{"title":"Buy groceries"}'
  curl "http://$ALB_DNS/api/todos"  # Expect [{"id":...,"title":"Buy groceries","completed":false}]
  ```
- **Real-World**: Similar to how Walmart validates cart updates in staging.

#### Engagement: "Build Blitz"
- **Goal**: Optimize pipeline runtime (<5 mins).
- **Steps**: 
  - Check `BUILD_DURATION` in Jenkins UI.
  - Parallelize Build Backend + Frontend (hint: add `parallel {}` in `Jenkinsfile`).
  - Share fastest time—winner gets bragging rights!

---

### Real-World DevOps Implementations
1. **E-Commerce (Walmart-like)**:
   - Jenkins on EC2 builds product APIs, pushes to ECR, deploys to EKS for Black Friday readiness.
   - Outcome: 100+ deploys/day, 99.9% uptime.
2. **Media (Netflix-like)**:
   - Pipelines automate encoding microservices, with CloudWatch logging for latency tracking.
   - Outcome: Sub-second content updates globally.
3. **Fintech (Startup)**:
   - Basic pipeline ensures compliance checks before prod, using GitHub for code reviews.
   - Outcome: Audit-ready deployments in <15 mins.

---

### Learning Outcome
- **Theory**: Understand Jenkins architecture, CI/CD principles, and automation benefits with actionable best practices.
- **Practical**: Automate the To-Do app’s CI/CD with Jenkins on EC2, GitHub, and AWS, using daily commands for setup, execution, and debugging.
- **Real-World**: Apply skills to e-commerce, media, or fintech scenarios, mirroring industry standards.

---

This Day 1 is now a deep dive into Jenkins basics, packed with theory and practical commands for real-world DevOps. 