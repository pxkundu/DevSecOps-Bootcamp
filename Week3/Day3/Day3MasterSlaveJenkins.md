Let’s explore the **Jenkins Master-Slave Architecture** in depth and implement an advanced, secure, and reusable version of the SaaS Task Manager project using this setup. 

This will leverage **AWS EC2** instances with **Docker** for compute services and incorporate other AWS services (e.g., ECR, S3, Secrets Manager, Auto Scaling) to demonstrate a production-grade CI/CD pipeline. 

The focus is on a dynamic, reusable pipeline for a multi-member DevOps team, adhering to Fortune 100 security and scalability standards as of March 11, 2025.

---

### Understanding Jenkins Master-Slave Architecture

#### Theoretical Explanation
The **Jenkins Master-Slave Architecture** (also called Controller-Agent in newer terminology) is a distributed system where a central **master node** orchestrates CI/CD workflows, delegating execution to **slave nodes** (agents). This setup enhances scalability, performance, and resource efficiency.

1. **Master Node**
   - **Definition**: The central Jenkins server that schedules jobs, manages configurations, and serves the UI.
   - **Responsibilities**:
     - Job scheduling and queuing.
     - Pipeline orchestration (e.g., parsing `Jenkinsfile`).
     - Storing build history and configs (e.g., `/var/lib/jenkins`).
   - **Key Features**:
     - Lightweight: Executes minimal tasks itself (e.g., UI rendering).
     - Highly available: Can be backed up or clustered (advanced setups).
   - **Real-World**: Walmart’s Jenkins master schedules 1000s of daily builds.

2. **Slave Node (Agent)**
   - **Definition**: A worker node that executes build tasks assigned by the master.
   - **Responsibilities**:
     - Running pipeline stages (e.g., build, test, deploy).
     - Reporting results back to the master.
   - **Key Features**:
     - **Static**: Pre-provisioned EC2 instances (e.g., always-on slaves).
     - **Dynamic**: Auto-scaled EC2 instances spawned on demand (e.g., via AWS Auto Scaling).
     - **Labeling**: Assigned labels (e.g., `docker-slave`) to match job requirements.
   - **Real-World**: Netflix uses 100+ slaves to parallelize microservice builds.

3. **Communication**
   - **Definition**: Master and slaves communicate via protocols like JNLP (Java Network Launch Protocol) or SSH.
   - **Keywords**:
     - **JNLP**: Default agent protocol over TCP (port 50000).
     - **SSH**: Secure alternative using key-based auth.
     - **Remoting**: Jenkins’ internal framework for task delegation.
   - **Security**: SSH preferred for encrypted, auditable connections.

4. **Advantages**
   - **Scalability**: Add slaves to handle load (e.g., 10 builds → 10 slaves).
   - **Isolation**: Separate environments (e.g., Linux vs. Windows slaves).
   - **Resilience**: Master failure doesn’t stop running slave jobs.
   - **Real-World**: Goldman Sachs scales slaves for trading app CI/CD.

5. **Challenges**
   - **Agent Sprawl**: Too many idle slaves waste cost.
   - **Network Latency**: Slow master-slave comms delay builds.
   - **Security**: Weak auth exposes pipeline to attacks.

#### Best Practices for Fortune 100 Standards
- **Security**: Use SSH with Secrets Manager for keys, enforce least privilege IAM roles.
- **Scalability**: Dynamic slaves with Auto Scaling, cap at need (e.g., 10 max).
- **Reusability**: Shared libraries for pipeline code, labels for agent flexibility.
- **Auditability**: Log all actions to S3/CloudWatch, track via CloudTrail.
- **Team Collaboration**: RBAC in Jenkins, GitHub branch protection.

---

### Practical Project: Advanced Master-Slave Task Manager

#### Objective
Build a Jenkins pipeline for the Task Manager with:
- **Master**: EC2 instance managing multi-branch jobs.
- **Slaves**: Dynamic EC2 Auto Scaling group running Docker-based builds.
- **Deployment**: Backend (task API) and frontend (task UI) on dedicated EC2s in us-east-1.
- **Security**: Secrets Manager, Trivy scans, encrypted artifacts.
- **Team**: Reusable for 10+ DevOps members.

#### Tools
- Jenkins, AWS EC2 (master + slaves + app hosts), Docker, AWS ECR, AWS S3, AWS Secrets Manager, AWS Auto Scaling, Nginx, Trivy, Slack.

#### Project Structure
```
task-manager/
├── backend/
│   ├── app.js
│   ├── package.json
│   ├── Dockerfile
│   └── .dockerignore
├── frontend/
│   ├── app.js
│   ├── package.json
│   ├── Dockerfile
│   └── .dockerignore
├── scripts/
│   ├── install_base.sh
│   ├── install_nginx.sh
│   ├── install_nodejs.sh
│   └── config_docker.sh
├── Jenkinsfile
├── README.md
└── .gitignore
```

---

### Step-by-Step Implementation

#### Step 1: Set Up Jenkins Master on EC2
- **Goal**: Launch a secure master node.
- **Commands**:
  ```bash
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

  ssh -i <your-key>.pem ec2-user@<master-ip>
  sudo cat /var/lib/jenkins/secrets/initialAdminPassword
  ```
- **Configure**:
  - Access: `http://<master-ip>:8080`
  - Install plugins: Git, Pipeline, SSH Agent, Credentials Binding, EC2, Slack Notification.
  - Enable CSRF: `Manage Jenkins` > `Configure Global Security`.
  - SSH Key: `ssh-keygen -t rsa -b 4096 -f ~/.ssh/jenkins_master_key -N ""`.

#### Step 2: Create Shared Library in GitHub
- **Goal**: Modularize pipeline logic.
- **Implementation**:
  - Repo: `pipeline-lib`
  - `vars/buildDocker.groovy`:
    ```groovy
    def call(String imageName, String dir) {
        dir(dir) {
            sh "docker build -t ${imageName} ."
            withAWS(credentials: 'aws-creds', region: 'us-east-1') {
                sh "aws ecr get-login-password | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com"
                sh "docker tag ${imageName} <account-id>.dkr.ecr.us-east-1.amazonaws.com/${imageName}"
                sh "docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/${imageName}"
                sh "aws s3 cp Dockerfile s3://<your-bucket>/artifacts/${imageName.split(':')[0]}-${BUILD_NUMBER}/"
            }
        }
    }
    ```
  - `vars/deployEC2.groovy`:
    ```groovy
    def call(String imageName, String instanceTag) {
        withAWS(credentials: 'aws-creds', region: 'us-east-1') {
            def instanceIp = sh(script: "aws ec2 describe-instances --filters Name=tag:Name,Values=${instanceTag} Name=instance-state-name,Values=running --query 'Reservations[0].Instances[0].PublicIpAddress' --output text", returnStdout: true).trim()
            sh "ssh -i ~/.ssh/jenkins_master_key -o StrictHostKeyChecking=no ec2-user@${instanceIp} 'docker stop ${imageName.split(':')[0]} || true'"
            sh "ssh -i ~/.ssh/jenkins_master_key ec2-user@${instanceIp} 'docker rm ${imageName.split(':')[0]} || true'"
            sh "ssh -i ~/.ssh/jenkins_master_key ec2-user@${instanceIp} 'aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com'"
            sh "ssh -i ~/.ssh/jenkins_master_key ec2-user@${instanceIp} 'docker pull <account-id>.dkr.ecr.us-east-1.amazonaws.com/${imageName}'"
            sh "ssh -i ~/.ssh/jenkins_master_key ec2-user@${instanceIp} 'docker run -d --name ${imageName.split(':')[0]} -p ${imageName.contains('backend') ? '3000:3000' : '8080:8080'} <account-id>.dkr.ecr.us-east-1.amazonaws.com/${imageName}'"
        }
    }
    ```
  - `vars/scanImage.groovy`:
    ```groovy
    def call(String imageName) {
        sh "docker run --rm aquasec/trivy image --severity HIGH,CRITICAL ${imageName}"
    }
    ```
  - Push:
    ```bash
    git init
    git add .
    git commit -m "Shared library for master-slave"
    git remote add origin https://github.com/<your-username>/pipeline-lib.git
    git push origin main
    git tag 1.0
    git push origin 1.0
    ```

#### Step 3: Configure Dynamic EC2 Slaves with Auto Scaling
- **Goal**: Set up scalable slaves.
- **Implementation**:
  - **Launch Template**:
    ```bash
    aws ec2 create-launch-template \
      --launch-template-name JenkinsSlaveTemplate \
      --version-description "v1" \
      --launch-template-data '{
        "ImageId": "ami-0c55b159cbfafe1f0",
        "InstanceType": "t2.micro",
        "KeyName": "<your-key>",
        "SecurityGroupIds": ["<sg-id>"],
        "UserData": "IyEvYmluL2Jhc2gKeXVtIHVwZGF0ZSAteQp5dW0gaW5zdGFsbCAteSBqYXZhLTExLW9wZW5qZGsgZG9ja2VyIGdpdCBub2RlanMKc3lzdGVtY3RsIHN0YXJ0IGRvY2tlcgp1c2VybW9kIC1hRyBkb2NrZXIgZWMyLXVzZXIKZWNobyA8bWFzdGVyLXB1YmxpYy1rZXk+ID4gL2hvbWUvZWMyLXVzZXIvLnNzaC9hdXRob3JpemVkX2tleXMKY2htb2QgNjAwIC9ob21lL2VjMi11c2VyLy5zc2gvYXV0aG9yaXplZF9rZXlzCmNobW9kIDcwMCAvaG9tZS9lYzItdXNlci8uc3No"
      }'
    ```
  - **Auto Scaling Group**:
    ```bash
    aws autoscaling create-auto-scaling-group \
      --auto-scaling-group-name JenkinsDynamicSlaves \
      --launch-template LaunchTemplateName=JenkinsSlaveTemplate \
      --min-size 0 \
      --max-size 10 \
      --desired-capacity 1 \
      --vpc-zone-identifier "<subnet-id>" \
      --region us-east-1 \
      --target-group-arns <target-group-arn>  # Optional for load balancing
    ```
  - **Jenkins Config**:
    - Install `Amazon EC2 Plugin`.
    - `Manage Jenkins` > `Manage Nodes and Clouds` > `Configure Clouds`:
      - Add: `Amazon EC2`
      - Name: `dynamic-ec2-cloud`
      - AMI: Use `JenkinsSlaveTemplate`.
      - Instance Cap: 10
      - Label: `docker-slave`
      - SSH Key: `~/.ssh/jenkins_master_key`.

#### Step 4: Set Up EC2 App Hosts
- **Goal**: Deploy Task Manager to dedicated EC2s.
- **Implementation**:
  - **Backend EC2**:
    ```bash
    aws ec2 run-instances \
      --image-id ami-0c55b159cbfafe1f0 \
      --instance-type t2.micro \
      --key-name <your-key> \
      --security-group-ids <sg-id> \
      --subnet-id <subnet-id> \
      --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=TaskManagerBackend}]' \
      --user-data '#!/bin/bash
        yum update -y
        yum install -y docker
        systemctl start docker
        systemctl enable docker
        usermod -aG docker ec2-user'
    ```
  - **Frontend EC2 with Nginx**:
    ```bash
    aws ec2 run-instances \
      --image-id ami-0c55b159cbfafe1f0 \
      --instance-type t2.micro \
      --key-name <your-key> \
      --security-group-ids <sg-id> \
      --subnet-id <subnet-id> \
      --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=TaskManagerFrontend}]' \
      --user-data '#!/bin/bash
        yum update -y
        yum install -y docker nginx
        systemctl start docker nginx
        systemctl enable docker nginx
        usermod -aG docker ec2-user
        echo "server { listen 80; location /tasks { proxy_pass http://<backend-ip>:3000; } location / { proxy_pass http://localhost:8080; } }" > /etc/nginx/conf.d/task-manager.conf
        systemctl restart nginx'
    ```

#### Step 5: Update Task Manager Jenkinsfile
- **Goal**: Leverage master-slave architecture.
- **Implementation**:
  - `Jenkinsfile`:
    ```groovy
    @Library('pipeline-lib@1.0') _
    pipeline {
        agent none
        parameters {
            string(name: 'BRANCH_NAME', defaultValue: 'main', description: 'Git branch')
            choice(name: 'ENVIRONMENT', choices: ['dev', 'staging', 'prod'], description: 'Deployment env')
        }
        environment {
            APP_NAME = 'task-manager'
            GIT_REPO = 'https://github.com/<your-username>/task-manager.git'
            BACKEND_IMAGE = "task-backend:${BUILD_NUMBER}"
            FRONTEND_IMAGE = "task-frontend:${BUILD_NUMBER}"
            S3_BUCKET = '<your-bucket>'
        }
        stages {
            stage('Setup') {
                agent { label 'docker-slave' }
                steps {
                    withAWS(credentials: 'aws-creds', region: 'us-east-1') {
                        script {
                            def githubSecret = sh(script: 'aws secretsmanager get-secret-value --secret-id github-token --query SecretString --output text', returnStdout: true).trim()
                            def githubCreds = readJSON text: githubSecret
                            env.GIT_USER = githubCreds.username
                            env.GIT_TOKEN = githubCreds.token
                        }
                        git url: "${GIT_REPO}", branch: "${BRANCH_NAME}", credentialsId: 'github-token'
                    }
                    sh 'chmod +x scripts/*.sh'
                    sh './scripts/install_base.sh'
                    sh './scripts/install_nginx.sh'
                    sh './scripts/install_nodejs.sh'
                    sh './scripts/config_docker.sh'
                }
            }
            stage('Build and Scan') {
                parallel {
                    stage('Backend') {
                        agent { label 'docker-slave' }
                        steps {
                            buildDocker("${BACKEND_IMAGE}", 'backend')
                            scanImage("${BACKEND_IMAGE}")
                        }
                    }
                    stage('Frontend') {
                        agent { label 'docker-slave' }
                        steps {
                            buildDocker("${FRONTEND_IMAGE}", 'frontend')
                            scanImage("${FRONTEND_IMAGE}")
                        }
                    }
                }
            }
            stage('Approval') {
                when { expression { params.ENVIRONMENT == 'prod' && BRANCH_NAME == 'main' } }
                steps {
                    input message: 'Approve prod deploy?', submitter: 'ops-team'
                }
            }
            stage('Deploy') {
                when { expression { params.ENVIRONMENT == 'prod' && BRANCH_NAME == 'main' } }
                parallel {
                    stage('Backend') {
                        agent { label 'docker-slave' }
                        steps {
                            deployEC2("${BACKEND_IMAGE}", 'TaskManagerBackend')
                        }
                    }
                    stage('Frontend') {
                        agent { label 'docker-slave' }
                        steps {
                            deployEC2("${FRONTEND_IMAGE}", 'TaskManagerFrontend')
                            withAWS(credentials: 'aws-creds', region: 'us-east-1') {
                                sh "ssh -i ~/.ssh/jenkins_master_key ec2-user@$(aws ec2 describe-instances --filters Name=tag:Name,Values=TaskManagerFrontend --query 'Reservations[0].Instances[0].PublicIpAddress' --output text) 'sudo systemctl restart nginx'"
                            }
                        }
                    }
                }
            }
        }
        post {
            always {
                sh 'docker logs task-backend > backend.log 2>&1 || true'
                sh 'docker logs task-frontend > frontend.log 2>&1 || true'
                withAWS(credentials: 'aws-creds', region: 'us-east-1') {
                    sh "aws s3 cp backend.log s3://${S3_BUCKET}/logs/backend-${BUILD_NUMBER}.log"
                    sh "aws s3 cp frontend.log s3://${S3_BUCKET}/logs/frontend-${BUILD_NUMBER}.log"
                }
                archiveArtifacts artifacts: '*.log', allowEmptyArchive: true
                sh 'rm -f *.log'
            }
            success {
                slackSend(channel: '#devops', message: "Pipeline succeeded for ${APP_NAME} - ${BRANCH_NAME} in ${ENVIRONMENT}")
            }
        }
    }
    ```

#### Step 6: Test the Pipeline
- **Steps**:
  - `New Item` > `TaskManagerMultiBranch` > Multibranch Pipeline:
    - Git: `https://github.com/<your-username>/task-manager.git`, Credentials: `github-token`.
  - Build `main` (prod):
    - Dynamic slaves spawn.
    - Builds, scans, and deploys.
  - Validation:
    ```bash
    FRONTEND_IP=$(aws ec2 describe-instances --filters Name=tag:Name,Values=TaskManagerFrontend --region us-east-1 --query 'Reservations[0].Instances[0].PublicIpAddress' --output text)
    curl -X POST -H "Content-Type: application/json" -d '{"title":"Test Task"}' "http://$FRONTEND_IP/tasks"
    curl "http://$FRONTEND_IP/tasks"  # Shows "Test Task"
    ```

---

### Real-World DevOps Implementations
1. **SaaS Task Manager**:
   - Master-slave scales to 50+ daily builds, dynamic EC2s save costs, secure pipeline serves 1M+ users.
2. **Finance (JPMorgan)**:
   - Master schedules trading app builds, slaves deploy to EC2s, audited for compliance.
3. **Retail (Walmart)**:
   - 100+ slaves handle peak e-commerce deploys, ensuring zero downtime.

---

### Best Practices Applied
- **Security**: Secrets Manager, SSH, Trivy scans, encrypted S3.
- **Scalability**: Auto Scaling slaves (0-10).
- **Reusability**: Shared libraries, dynamic labels.
- **Team**: Multi-branch, RBAC, Slack notifications.

---

This master-slave setup is secure, scalable, and team-ready.

Reference linked to Day3DiveDeepMasterSlaveJenkins.md file 
