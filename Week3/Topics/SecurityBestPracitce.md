Let’s enhance the security of the **Task Manager pipeline** from Week 3, Day 2 by integrating **AWS Secrets Manager** and applying **best practices** to design a **bulletproof, production-grade CI/CD pipeline** suitable for Fortune 100 companies (e.g., Walmart, JPMorgan Chase). 

This will involve securing credentials, ensuring robust access control, and addressing multi-team, multi-environment challenges. 

Below, I’ll outline the enhancements, explain best practices with theoretical depth, and provide a detailed step-by-step implementation tied to the Task Manager project, reflecting industry standards as of March 11, 2025.

---

### Objective
- Integrate AWS Secrets Manager to securely manage credentials in the Jenkins pipeline.
- Design a secure, scalable CI/CD pipeline for the Task Manager app, meeting Fortune 100 security and compliance needs.
- Address multi-team collaboration and multi-environment deployment (dev, staging, prod) complexities.

---

### Enhancing Security with AWS Secrets Manager
AWS Secrets Manager securely stores, retrieves, and rotates sensitive data (e.g., GitHub tokens, SSH keys), replacing hardcoded or Jenkins-stored credentials. Here’s how it enhances the pipeline:

1. **Centralized Secret Storage**: Secrets (e.g., `github-token`, `ssh-slave-key`) move from Jenkins to Secrets Manager.
2. **Dynamic Retrieval**: Pipeline fetches secrets at runtime via AWS SDK or CLI, avoiding exposure.
3. **Rotation**: Automatically rotate secrets (e.g., every 30 days) without pipeline changes.
4. **Access Control**: IAM policies restrict secret access to specific roles/users.
5. **Auditability**: Secrets Manager logs access attempts in CloudTrail.

---

### Best Practices for a Bulletproof Production-Grade CI/CD Pipeline
Below are best practices tailored for Fortune 100 companies, with explanations and Task Manager relevance:

1. **Secrets Management**
   - **Practice**: Use AWS Secrets Manager or HashiCorp Vault; avoid Jenkins Credentials or plaintext.
   - **Why**: Prevents leaks (e.g., accidental Git commits), ensures compliance (e.g., PCI DSS).
   - **Task Manager**: Store GitHub token and SSH keys in Secrets Manager, not Jenkins.
   - **Real-World**: JPMorgan uses Secrets Manager for API keys in trading apps.

2. **Least Privilege Access (IAM)**
   - **Practice**: Assign minimal IAM roles to Jenkins master/agents (e.g., S3 write, EKS deploy).
   - **Why**: Limits blast radius if compromised (e.g., agent can’t delete prod).
   - **Task Manager**: Role for agents allows ECR push, not cluster admin.
   - **Real-World**: Walmart restricts CI/CD roles to prevent prod overwrites.

3. **Network Security**
   - **Practice**: Use VPCs, private subnets, and security groups; disable public Jenkins UI access.
   - **Why**: Protects against external attacks (e.g., DDoS, brute force).
   - **Task Manager**: Jenkins master in private subnet, agents communicate via VPC peering.
   - **Real-World**: Netflix runs Jenkins in VPCs for streaming CI/CD.

4. **Code and Pipeline Security**
   - **Practice**: Scan code (e.g., Trivy for Docker images), enforce PR approvals, sign commits.
   - **Why**: Catches vulnerabilities (e.g., Log4j) and ensures pipeline integrity.
   - **Task Manager**: Add Trivy scan stage; require PRs for `Jenkinsfile` changes.
   - **Real-World**: Goldman Sachs scans microservices in CI/CD for compliance.

5. **Encryption**
   - **Practice**: Encrypt data in transit (TLS) and at rest (S3, EKS volumes).
   - **Why**: Meets regulatory standards (e.g., GDPR, HIPAA).
   - **Task Manager**: S3 artifacts encrypted; EKS uses encrypted EBS.
   - **Real-World**: Healthcare firms encrypt patient data in CI/CD.

6. **Audit and Monitoring**
   - **Practice**: Log all pipeline actions (CloudWatch, CloudTrail); set up alerts for failures/unauthorized access.
   - **Why**: Enables forensic analysis (e.g., who deployed what).
   - **Task Manager**: Log secret access and deploy events to CloudWatch.
   - **Real-World**: Amazon tracks CI/CD in CloudTrail for audit trails.

7. **Immutable Infrastructure**
   - **Practice**: Use Docker images and Kubernetes manifests as immutable artifacts.
   - **Why**: Ensures consistency (e.g., prod = staging); simplifies rollback.
   - **Task Manager**: Tag images with `$BUILD_NUMBER`, rollback via `kubectl`.
   - **Real-World**: Netflix deploys immutable streaming pods.

8. **Multi-Environment Isolation**
   - **Practice**: Use namespaces (EKS) or separate clusters for dev/staging/prod.
   - **Why**: Prevents dev bugs from hitting prod; isolates resources.
   - **Task Manager**: Deploy to `task-dev`, `task-staging`, `task-prod` namespaces.
   - **Real-World**: Walmart isolates e-commerce envs for stability.

9. **Team Collaboration**
   - **Practice**: Role-based access (RBAC) in Jenkins/GitHub, branch protection, documentation.
   - **Why**: Prevents unauthorized changes; clarifies ownership.
   - **Task Manager**: Devs access `dev`, ops control `prod` deploys.
   - **Real-World**: Fortune 100 teams segregate CI/CD duties.

10. **Disaster Recovery**
    - **Practice**: Backup Jenkins configs, automate recovery, test rollbacks.
    - **Why**: Minimizes downtime (e.g., <1h recovery).
    - **Task Manager**: S3 backups, rollback tested in staging.
    - **Real-World**: Banks recover trading apps in minutes.

---

### Key Areas for Multi-Team, Multi-Environment Deployment
1. **Access Control**: RBAC in Jenkins/EKS/GitHub ensures devs can’t deploy to prod.
2. **Environment Segregation**: Separate namespaces or clusters avoid conflicts (e.g., dev overwrites prod).
3. **Pipeline Consistency**: Standardized `Jenkinsfile` across envs reduces errors.
4. **Communication**: Slack/Email notifications for team sync (e.g., prod deploy done).
5. **Testing**: Staging mirrors prod (e.g., same EKS config) to catch issues early.
6. **Versioning**: Tag images and manifests for traceability across teams/envs.

---

### Enhanced Pipeline Implementation with AWS Secrets Manager

#### Step 1: Set Up AWS Secrets Manager
- **Goal**: Store GitHub token and SSH key securely.
- **Commands**:
  ```bash
  # Create secrets
  aws secretsmanager create-secret \
    --name "github-token" \
    --secret-string '{"username":"<your-username>","token":"<github-token>"}' \
    --region us-east-1

  aws secretsmanager create-secret \
    --name "ssh-slave-key" \
    --secret-string "$(cat ~/.ssh/jenkins_master_key)" \
    --region us-east-1
  ```
- **IAM Role for Jenkins**:
  - Create `JenkinsPipelineRole` with:
    ```json
    {
      "Version": "2012-10-17",
      "Statement": [
        {"Effect": "Allow", "Action": "secretsmanager:GetSecretValue", "Resource": "arn:aws:secretsmanager:us-east-1:<account-id>:secret:github-token-*"},
        {"Effect": "Allow", "Action": "secretsmanager:GetSecretValue", "Resource": "arn:aws:secretsmanager:us-east-1:<account-id>:secret:ssh-slave-key-*"},
        {"Effect": "Allow", "Action": ["s3:PutObject", "s3:GetObject"], "Resource": "arn:aws:s3:::<your-bucket>/*"},
        {"Effect": "Allow", "Action": "eks:*", "Resource": "*"},
        {"Effect": "Allow", "Action": "ecr:*", "Resource": "*"}
      ]
    }
    ```
  - Attach to master and agent EC2 instances via instance profile.

#### Step 2: Update GitHub Repository
- **Goal**: Enhance `Jenkinsfile` with Secrets Manager and security features.
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
            AWS_REGION = 'us-east-1'
        }
        stages {
            stage('Setup Slave') {
                agent { label 'linux-slave' }
                steps {
                    withAWS(credentials: 'aws-creds', region: "${AWS_REGION}") {
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
                    sh './scripts/install_nodejs.sh'
                    sh './scripts/config_docker.sh'
                }
            }
            stage('Security Scan') {
                agent { label 'linux-slave' }
                steps {
                    sh 'docker run --rm aquasec/trivy image --severity HIGH,CRITICAL ${BACKEND_IMAGE}'
                    sh 'docker run --rm aquasec/trivy image --severity HIGH,CRITICAL ${FRONTEND_IMAGE}'
                }
            }
            stage('Build') {
                parallel {
                    stage('Backend') {
                        agent { label 'linux-slave-backend' }
                        steps {
                            dir('backend') {
                                sh 'docker build -t ${BACKEND_IMAGE} .'
                                withAWS(credentials: 'aws-creds', region: "${AWS_REGION}") {
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
                                withAWS(credentials: 'aws-creds', region: "${AWS_REGION}") {
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
                    withAWS(credentials: 'aws-creds', region: "${AWS_REGION}") {
                        sh 'aws eks update-kubeconfig --name ${EKS_CLUSTER} --region ${AWS_REGION}'
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
                withAWS(credentials: 'aws-creds', region: "${AWS_REGION}") {
                    sh 'aws s3 cp backend.log s3://${S3_BUCKET}/logs/backend-${BUILD_NUMBER}.log'
                    sh 'aws s3 cp frontend.log s3://${S3_BUCKET}/logs/frontend-${BUILD_NUMBER}.log'
                }
                archiveArtifacts artifacts: '*.log', allowEmptyArchive: true
                sh 'rm -f *.log'
            }
            success {
                slackSend(channel: '#devops', message: "Pipeline succeeded for ${APP_NAME} - ${BRANCH_NAME} in ${ENVIRONMENT}")
            }
            failure {
                slackSend(channel: '#devops', message: "Pipeline failed for ${APP_NAME} - ${BRANCH_NAME} in ${ENVIRONMENT}")
            }
        }
    }
    ```
  - Push:
    ```bash
    git add Jenkinsfile
    git commit -m "Enhance pipeline with Secrets Manager and security"
    git push origin main
    ```

#### Step 3: Secure Jenkins Master and Agents
- **Master**:
  - Move to private subnet, access via VPN/bastion host.
  - Update SG: Allow 8080 only from VPC CIDR.
  - Backup:
    ```bash
    tar -czf jenkins-backup.tar.gz /var/lib/jenkins/config.xml /var/lib/jenkins/jobs/
    aws s3 cp jenkins-backup.tar.gz s3://<your-bucket>/backups/
    ```

- **Agents**:
  - Attach `JenkinsPipelineRole` to instances.
  - Update `slave-backend` and `slave-frontend` with SSH key from Secrets Manager (manual update for now; Day 3 will automate).

#### Step 4: Configure Jenkins with AWS Credentials
- **Steps**:
  - `Manage Jenkins` > `Manage Credentials` > Add:
    - Kind: AWS Credentials
    - ID: `aws-creds`
    - Access Key/Secret: IAM user with `JenkinsPipelineRole` perms.
  - Install `Slack Notification` plugin for `post` notifications.

#### Step 5: Test the Pipeline
- **Steps**:
  - `TaskManagerMultiBranch` > Scan Repository > Build `main` (prod):
    - Secrets fetched dynamically.
    - Trivy scans images.
    - Backend/fronted deploy to `task-prod`.
  - Validation:
    ```bash
    kubectl get pods -n task-prod
    ALB_DNS=$(kubectl get svc frontend-service -n task-prod -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')
    curl -X POST -H "Content-Type: application/json" -d '{"title":"Secure Task"}' "http://$ALB_DNS:3000/tasks"
    curl "http://$ALB_DNS:8080/tasks"  # Shows "Secure Task"
    aws cloudtrail lookup-events --lookup-attributes AttributeKey=ResourceName,AttributeValue=github-token
    ```

---

### Real-World Fortune 100 Use Cases
1. **Banking (JPMorgan)**:
   - Secrets Manager secures trading API keys, EKS deploys prod with rollback.
   - Outcome: 99.999% uptime, audited via CloudTrail.
2. **Retail (Walmart)**:
   - Multi-branch CI/CD with S3 artifacts supports 100s of daily catalog updates.
   - Outcome: Scales to Black Friday traffic.
3. **Tech (Amazon)**:
   - Encrypted, isolated envs with RBAC for 1000+ devs across teams.
   - Outcome: Secure, rapid feature delivery.

---

### Key Takeaways
- **Security**: Secrets Manager, IAM, encryption, and scans make it bulletproof.
- **Multi-Team**: RBAC, branch protection, and notifications streamline collaboration.
- **Multi-Env**: Namespaces and rollback ensure isolation and recovery.

