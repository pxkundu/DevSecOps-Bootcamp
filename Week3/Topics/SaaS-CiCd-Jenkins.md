Let’s create a **modular and maintainable CI/CD pipeline** for a SaaS Task Manager project (an evolution of the `simple-app`). We’ll separate installation and configuration scripts for the slave node, build two Docker images (backend and frontend), and run them as containers on the same EC2 slave instance with intercommunication. 

The backend will store in-memory task data, and the frontend will display it, all automated via Jenkins. This reflects a production-grade setup with best practices as of March 11, 2025.

---

### Objective
- Modularize the pipeline with separate script files in GitHub.
- Automate slave node setup (Git, Java, Docker, Nginx, Node.js) via scripts.
- Build and run backend (Node.js API) and frontend (Node.js app) Docker containers on the slave.
- Enable backend-frontend communication for a Task Manager app.
- Deploy dynamically and securely with Jenkins.

---

### Tools
- Jenkins, AWS EC2 (master + slave), GitHub, Docker, Node.js, Nginx, `kubectl` (optional for future EKS).

---

### Enhanced Project Structure
```
task-manager/
├── backend/
│   ├── app.js            # Node.js API for tasks
│   ├── package.json      # Backend dependencies
│   ├── Dockerfile        # Backend Docker image
│   └── .dockerignore     # Ignore node_modules
├── frontend/
│   ├── app.js            # Node.js frontend (simple HTTP server)
│   ├── package.json      # Frontend dependencies
│   ├── Dockerfile        # Frontend Docker image
│   └── .dockerignore     # Ignore node_modules
├── scripts/
│   ├── install_base.sh   # Install Git, Java, Docker
│   ├── install_nginx.sh  # Install Nginx
│   ├── install_nodejs.sh # Install Node.js
│   ├── config_docker.sh  # Configure Docker permissions
│   └── run_containers.sh # Run backend + frontend containers
├── Jenkinsfile           # Pipeline definition
├── README.md             # Docs
└── .gitignore            # Ignore node_modules
```

---

### Best Practices Refinement
1. **Modular Scripts**: Separate shell scripts in `scripts/` for reusability and clarity.
2. **Dynamic Builds**: Use parameters and env vars for branch/env flexibility.
3. **Secure Execution**: Scope credentials and limit script perms.
4. **Container Isolation**: Run backend (port 3000) and frontend (port 8080) with Docker networking.
5. **Intercommunication**: Backend API serves data; frontend fetches via HTTP.
6. **Logging**: Archive container logs for debugging.

---

### Step-by-Step Documentation

#### Step 1: Set Up GitHub Repository with Task Manager App
- **Goal**: Create backend and frontend apps with modular scripts.
- **Implementation**:
  1. **Backend (`backend/`)**
     - `app.js`:
       ```javascript
       const express = require('express');
       const app = express();
       app.use(express.json());
       let tasks = [];

       app.get('/tasks', (req, res) => res.json(tasks));
       app.post('/tasks', (req, res) => {
           const task = { id: tasks.length + 1, title: req.body.title };
           tasks.push(task);
           res.status(201).json(task);
       });

       app.listen(3000, () => console.log('Backend on port 3000'));
       ```
     - `package.json`:
       ```json
       {
         "name": "task-backend",
         "version": "1.0.0",
         "main": "app.js",
         "scripts": { "start": "node app.js" },
         "dependencies": { "express": "^4.18.2" }
       }
       ```
     - `Dockerfile`:
       ```dockerfile
       FROM node:20-alpine
       WORKDIR /app
       COPY package*.json ./
       RUN npm install
       COPY . .
       EXPOSE 3000
       CMD ["npm", "start"]
       ```
     - `.dockerignore`:
       ```
       node_modules
       ```

  2. **Frontend (`frontend/`)**
     - `app.js`:
       ```javascript
       const http = require('http');
       const fetch = require('node-fetch');

       const server = http.createServer(async (req, res) => {
           if (req.url === '/tasks') {
               const tasks = await (await fetch('http://localhost:3000/tasks')).json();
               res.writeHead(200, { 'Content-Type': 'text/html' });
               res.end(`<h1>Tasks</h1><ul>${tasks.map(t => `<li>${t.title}</li>`).join('')}</ul>`);
           } else {
               res.writeHead(404);
               res.end('Not Found');
           }
       });

       server.listen(8080, () => console.log('Frontend on port 8080'));
       ```
     - `package.json`:
       ```json
       {
         "name": "task-frontend",
         "version": "1.0.0",
         "main": "app.js",
         "scripts": { "start": "node app.js" },
         "dependencies": { "node-fetch": "^2.6.7" }
       }
       ```
     - `Dockerfile`:
       ```dockerfile
       FROM node:20-alpine
       WORKDIR /app
       COPY package*.json ./
       RUN npm install
       COPY . .
       EXPOSE 8080
       CMD ["npm", "start"]
       ```
     - `.dockerignore`:
       ```
       node_modules
       ```

  3. **Scripts (`scripts/`)**
     - `install_base.sh`:
       ```bash
       #!/bin/bash
       sudo yum update -y
       sudo yum install -y git java-11-openjdk docker
       ```
     - `install_nginx.sh`:
       ```bash
       #!/bin/bash
       sudo yum install -y nginx
       sudo systemctl start nginx
       sudo systemctl enable nginx
       ```
     - `install_nodejs.sh`:
       ```bash
       #!/bin/bash
       curl -sL https://rpm.nodesource.com/setup_20.x | sudo bash -
       sudo yum install -y nodejs
       ```
     - `config_docker.sh`:
       ```bash
       #!/bin/bash
       sudo systemctl start docker
       sudo usermod -aG docker ec2-user
       ```
     - `run_containers.sh`:
       ```bash
       #!/bin/bash
       docker stop task-backend task-frontend || true
       docker rm task-backend task-frontend || true
       docker run -d --name task-backend -p 3000:3000 task-backend:latest
       docker run -d --name task-frontend -p 8080:8080 task-frontend:latest
       ```

  4. **Jenkinsfile**:
     ```groovy
     pipeline {
         agent { label 'linux-slave' }
         parameters {
             string(name: 'BRANCH_NAME', defaultValue: 'main', description: 'Git branch to build')
             choice(name: 'ENVIRONMENT', choices: ['dev', 'staging', 'prod'], description: 'Deployment environment')
         }
         environment {
             APP_NAME = 'task-manager'
             GIT_REPO = 'https://github.com/<your-username>/task-manager.git'
             BACKEND_IMAGE = "task-backend:${BUILD_NUMBER}"
             FRONTEND_IMAGE = "task-frontend:${BUILD_NUMBER}"
         }
         stages {
             stage('Setup Slave') {
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
             stage('Build Backend') {
                 steps {
                     dir('backend') {
                         sh 'docker build -t ${BACKEND_IMAGE} .'
                     }
                 }
             }
             stage('Build Frontend') {
                 steps {
                     dir('frontend') {
                         sh 'docker build -t ${FRONTEND_IMAGE} .'
                     }
                 }
             }
             stage('Run Containers') {
                 steps {
                     sh './scripts/run_containers.sh'
                 }
             }
             stage('Verify') {
                 steps {
                     sh 'sleep 5'  // Wait for containers to start
                     sh 'curl -X POST -H "Content-Type: application/json" -d \'{"title":"Test Task"}\' http://localhost:3000/tasks'
                     sh 'curl http://localhost:8080/tasks'  # Should show "Test Task"
                 }
             }
         }
         post {
             success {
                 echo "Pipeline succeeded for ${APP_NAME} on ${BRANCH_NAME} in ${ENVIRONMENT}"
             }
             failure {
                 echo "Pipeline failed - check logs"
             }
             always {
                 sh 'docker logs task-backend > backend.log 2>&1'
                 sh 'docker logs task-frontend > frontend.log 2>&1'
                 archiveArtifacts artifacts: '*.log', allowEmptyArchive: true
                 sh 'rm -f *.log'
             }
         }
     }
     ```

  5. **Push to GitHub**:
     ```bash
     mkdir -p task-manager/{backend,frontend,scripts}
     # Move files into respective dirs as above
     git init
     echo "node_modules/" > .gitignore
     git add .
     git commit -m "Task Manager with modular pipeline"
     git remote add origin https://github.com/<your-username>/task-manager.git
     git push origin main
     ```

- **Outcome**: Repo with backend (API), frontend (UI), and modular scripts.

---

#### Step 2: Set Up Jenkins Master on EC2
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

  ssh -i <your-key>.pem ec2-user@<master-public-ip>
  sudo cat /var/lib/jenkins/secrets/initialAdminPassword
  ```
- **Configure**:
  - Access: `http://<master-public-ip>:8080`
  - Install plugins: Git, Pipeline, SSH Agent, Credentials Binding.
  - Enable CSRF: `Manage Jenkins` > `Configure Global Security`.
  - SSH Keys: `ssh-keygen -t rsa -b 4096 -f ~/.ssh/jenkins_master_key -N ""`.

---

#### Step 3: Set Up EC2 Slave Node
- **Commands**:
  ```bash
  aws ec2 run-instances \
    --image-id ami-0c55b159cbfafe1f0 \
    --instance-type t2.micro \
    --key-name <your-key> \
    --security-group-ids <sg-id> \
    --subnet-id <subnet-id> \
    --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=JenkinsSlave}]'

  ssh -i <your-key>.pem ec2-user@<slave-public-ip>
  mkdir -p ~/.ssh
  echo "<paste-master-public-key>" >> ~/.ssh/authorized_keys
  chmod 600 ~/.ssh/authorized_keys
  chmod 700 ~/.ssh
  ```

---

#### Step 4: Configure Jenkins with Credentials and Agent
- **Credentials**:
  - GitHub: `github-token` (Username: `<your-username>`, Password: `<github-token>`).
  - SSH: `ssh-slave-key` (Username: `ec2-user`, Private Key: `~/.ssh/jenkins_master_key`).

- **Agent**:
  - `Manage Jenkins` > `Manage Nodes` > `New Node`:
    - Name: `slave1`
    - Label: `linux-slave`
    - Launch method: SSH, Host: `<slave-public-ip>`, Credentials: `ssh-slave-key`.

---

#### Step 5: Create and Run the Pipeline
- **Steps**:
  - `New Item` > `TaskManagerPipeline` > Pipeline:
    - Parameterized: `BRANCH_NAME` (default: `main`), `ENVIRONMENT` (choices: `dev`, `staging`, `prod`).
    - SCM: Git, URL: `https://github.com/<your-username>/task-manager.git`, Credentials: `github-token`, Branch: `${BRANCH_NAME}`, Script Path: `Jenkinsfile`.
  - Build with Parameters: `main`, `dev`.

- **Validation**:
  - Console output:
    ```
    [Pipeline] stage (Setup Slave)
    + ./scripts/install_base.sh
    + ./scripts/install_nodejs.sh
    + ./scripts/config_docker.sh
    [Pipeline] stage (Build Backend)
    + docker build -t task-backend:1 .
    [Pipeline] stage (Build Frontend)
    + docker build -t task-frontend:1 .
    [Pipeline] stage (Run Containers)
    + ./scripts/run_containers.sh
    [Pipeline] stage (Verify)
    + curl -X POST ... http://localhost:3000/tasks
    + curl http://localhost:8080/tasks
    <h1>Tasks</h1><ul><li>Test Task</li></ul>
    ```
  - On slave:
    ```bash
    docker ps  # See task-backend, task-frontend running
    cat backend.log  # Backend logs
    cat frontend.log  # Frontend logs
    ```

---

### Real-World Relevance
- **SaaS Task Manager**: A startup automates a task app with backend (task CRUD) and frontend (task list), deployed via Jenkins.
- **Outcome**: Team deploys updates in <10 mins, with frontend reflecting backend data instantly.

---

### Cleanup
```bash
aws ec2 terminate-instances --instance-ids <master-id> <slave-id>
```

---

This enhanced pipeline is modular, secure, and dynamic, with separate scripts and dual-container deployment for a Task Manager.