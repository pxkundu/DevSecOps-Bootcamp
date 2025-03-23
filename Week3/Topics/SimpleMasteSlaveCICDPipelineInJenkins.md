Let’s build a **very simple Jenkins pipeline** that connects to a GitHub repository, runs on an **AWS EC2 slave node (agent)**, and is managed by an **EC2 master node** using SSH keys for authentication. 

This setup automates a basic build process for a sample app (e.g., a "Hello World" Node.js app), reflecting a minimal yet real-world CI/CD workflow as of March 10, 2025. 

Below is a **detailed, step-by-step process** tailored for an intermediate DevOps engineer, ensuring clarity and practicality with commands, configurations, and best practices.

---

### Objective
Create a Jenkins pipeline that:
- Clones a GitHub repo with a simple Node.js app.
- Runs on an EC2 slave node (agent) connected to an EC2 master via SSH.
- Executes a build step (e.g., `npm install` and `node app.js`) and logs output.

---

### Tools
- **Jenkins**: CI/CD server on EC2 master.
- **AWS EC2**: Master and slave instances (Amazon Linux 2).
- **GitHub**: Hosts the sample app repo.
- **SSH Keys**: Secure master-agent communication.
- **Node.js**: Sample app runtime.

---

### Project Structure
```
simple-app/
├── app.js           # Simple Node.js app
├── package.json     # Dependencies
├── Jenkinsfile      # Pipeline definition
└── .gitignore       # Ignore node_modules
```

---

### Step-by-Step Process

#### Step 1: Set Up GitHub Repository
- **Goal**: Create a simple Node.js app and push it to GitHub.
- **Commands**:
  ```bash
  # Create local repo
  mkdir simple-app
  cd simple-app
  git init

  # Create app.js
  echo 'console.log("Hello from Jenkins Pipeline!");' > app.js

  # Create package.json
  echo '{"name": "simple-app", "version": "1.0.0", "main": "app.js", "scripts": {"start": "node app.js"}}' > package.json

  # Create .gitignore
  echo "node_modules/" > .gitignore

  # Commit and push to GitHub
  git add .
  git commit -m "Initial simple app setup"
  git remote add origin https://github.com/<your-username>/simple-app.git
  git push origin main

  # Generate GitHub token (for Jenkins auth)
  # Go to github.com > Settings > Developer settings > Personal access tokens > Generate new token (repo scope)
  # Save token: <github-token>
  ```

- **Outcome**: A GitHub repo (`https://github.com/<your-username>/simple-app`) with a basic app.

---

#### Step 2: Launch Jenkins Master on EC2
- **Goal**: Set up Jenkins on an EC2 instance as the master node.
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

  # SSH to EC2
  ssh -i <your-key>.pem ec2-user@<master-public-ip>

  # Get initial admin password
  sudo cat /var/lib/jenkins/secrets/initialAdminPassword
  ```
- **Configure Jenkins**:
  - Access: `http://<master-public-ip>:8080`
  - Enter password, install suggested plugins (Git, Pipeline, SSH Agent).
  - Set admin user/password (e.g., `admin`/`admin123`).

- **Generate SSH Keys for Master**:
  ```bash
  # On master EC2
  ssh-keygen -t rsa -b 4096 -f ~/.ssh/jenkins_master_key -N ""
  cat ~/.ssh/jenkins_master_key.pub  # Copy public key
  ```

- **Outcome**: Jenkins master running on EC2 with SSH keys ready.

---

#### Step 3: Launch EC2 Slave Node (Agent)
- **Goal**: Set up an EC2 instance as a Jenkins agent, connected via SSH.
- **Commands**:
  ```bash
  # Launch EC2 (t2.micro, Amazon Linux 2)
  aws ec2 run-instances \
    --image-id ami-0c55b159cbfafe1f0 \
    --instance-type t2.micro \
    --key-name <your-key> \
    --security-group-ids <sg-id> \
    --subnet-id <subnet-id> \
    --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=JenkinsSlave}]' \
    --user-data '#!/bin/bash
      yum update -y
      yum install -y java-11-openjdk docker git nodejs
      systemctl start docker
      usermod -aG docker ec2-user'

  # SSH to slave
  ssh -i <your-key>.pem ec2-user@<slave-public-ip>

  # Add master’s public key to authorized_keys
  mkdir -p ~/.ssh
  echo "<paste-master-public-key-from-step-2>" >> ~/.ssh/authorized_keys
  chmod 600 ~/.ssh/authorized_keys
  chmod 700 ~/.ssh
  ```

- **Outcome**: EC2 slave ready with Node.js and Docker, authenticated via SSH.

---

#### Step 4: Configure Jenkins Master to Use Slave Agent
- **Goal**: Connect the slave to the master via SSH.
- **Steps**:
  1. **In Jenkins UI**:
     - Go to `Manage Jenkins` > `Manage Nodes and Clouds` > `New Node`.
     - Name: `slave1`.
     - Type: Permanent Agent > OK.
     - Config:
       - # of executors: 1
       - Remote root directory: `/home/ec2-user`
       - Labels: `slave1`
       - Launch method: `Launch agents via SSH`
       - Host: `<slave-public-ip>`
       - Credentials: Add > SSH Username with private key
         - Username: `ec2-user`
         - Private Key: Paste contents of `~/.ssh/jenkins_master_key` from master
         - ID: `ssh-slave-key`
       - Host Key Verification: `Non-verifying` (for simplicity; production uses known hosts).
     - Save.

  2. **Test Connection**:
     - Click `slave1` > `Log` > Should see "Agent successfully connected".
     - If not, check:
       ```bash
       # On master
       ssh -i ~/.ssh/jenkins_master_key ec2-user@<slave-public-ip>  # Verify SSH works
       sudo tail -f /var/log/jenkins/jenkins.log  # Check errors
       ```

- **Outcome**: Slave node `slave1` connected to Jenkins master.

---

#### Step 5: Create a Simple Pipeline
- **Goal**: Define a pipeline in `Jenkinsfile` to run on the slave.
- **Implementation**:
  - Add `Jenkinsfile` to `simple-app/`:
    ```groovy
    pipeline {
        agent { label 'slave1' }  // Run on slave1
        stages {
            stage('Checkout') {
                steps {
                    git url: 'https://github.com/<your-username>/simple-app.git', credentialsId: 'github-token'
                }
            }
            stage('Build') {
                steps {
                    sh 'npm install'  // Install dependencies (none for this app, but good practice)
                    sh 'node app.js > output.log'  // Run app and save output
                }
            }
            stage('Verify') {
                steps {
                    sh 'cat output.log'  // Display output
                }
            }
        }
        post {
            always {
                echo "Pipeline completed on slave1"
            }
        }
    }
    ```
  - Push to GitHub:
    ```bash
    git add Jenkinsfile
    git commit -m "Add Jenkinsfile for simple pipeline"
    git push origin main
    ```

- **Configure Jenkins**:
  - In UI: `New Item` > Name: `SimplePipeline` > Type: Pipeline > OK.
  - Pipeline:
    - Definition: `Pipeline script from SCM`
    - SCM: Git
    - Repository URL: `https://github.com/<your-username>/simple-app.git`
    - Credentials: Add > Username/Password
      - Username: `<your-github-username>`
      - Password: `<github-token>`
      - ID: `github-token`
    - Script Path: `Jenkinsfile`
  - Save.

- **Outcome**: Pipeline defined to run on `slave1`, pulling from GitHub.

---

#### Step 6: Run and Validate the Pipeline
- **Goal**: Execute the pipeline and verify it works.
- **Commands**:
  - In Jenkins UI: Click `SimplePipeline` > `Build Now`.
  - Check console output:
    ```
    Started by user admin
    [Pipeline] node
    Running on slave1 in /home/ec2-user/workspace/SimplePipeline
    [Pipeline] stage (Checkout)
    Cloning repository https://github.com/<your-username>/simple-app.git
    [Pipeline] stage (Build)
    + npm install
    + node app.js
    [Pipeline] stage (Verify)
    + cat output.log
    Hello from Jenkins Pipeline!
    [Pipeline] echo
    Pipeline completed on slave1
    ```

- **Troubleshooting**:
  ```bash
  # On master
  sudo tail -f /var/log/jenkins/jenkins.log  # Pipeline errors
  ssh -i ~/.ssh/jenkins_master_key ec2-user@<slave-public-ip>  # Test SSH

  # On slave
  ls -l /home/ec2-user/workspace/SimplePipeline/  # Verify workspace
  cat /home/ec2-user/workspace/SimplePipeline/output.log  # Check output
  ```

- **Outcome**: Pipeline runs on slave, clones repo, builds, and outputs "Hello from Jenkins Pipeline!".

---

### Best Practices Applied
- **SSH Security**: Uses key-based auth, avoiding passwords.
- **Pipeline as Code**: `Jenkinsfile` in GitHub ensures version control.
- **Agent Offload**: Master delegates to slave, keeping it lightweight.
- **Minimal Scope**: Simple stages (checkout, build, verify) for clarity.

---

### Real-World Context
- **Use Case**: A startup automates a microservice build (e.g., user auth API) on a Jenkins slave to free the master for scheduling.
- **Outcome**: Cuts build time from 10 mins (master) to 5 mins (slave), scales to multiple services.

---

### Cleanup (Optional)
```bash
# Terminate EC2 instances
aws ec2 terminate-instances --instance-ids <master-instance-id> <slave-instance-id>
# Delete GitHub repo (manual via UI)
```

---

This setup provides a **simple, functional Jenkins pipeline** with detailed steps, from EC2 provisioning to pipeline execution.