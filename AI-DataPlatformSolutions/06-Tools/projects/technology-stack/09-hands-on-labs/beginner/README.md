# Beginner Hands-On Labs - DevSecOps Fundamentals

## 🚀 Overview
This section provides beginner-friendly hands-on labs for DevSecOps fundamentals. These labs are designed for newcomers to DevSecOps who want to learn the basics through practical, step-by-step exercises.

## 🏗️ Learning Path Architecture

```mermaid
graph TB
    subgraph "Beginner Learning Path"
        A[Lab 1: Environment Setup] --> B[Lab 2: Basic Git]
        B --> C[Lab 3: Docker Basics]
        C --> D[Lab 4: Simple CI/CD]
        D --> E[Lab 5: Basic Security]
        E --> F[Lab 6: Monitoring]
        F --> G[Lab 7: Final Project]
        
        H[Prerequisites] --> A
        I[Cloud Account] --> A
        J[Local Machine] --> A
        K[Basic Linux] --> A
    end
```

## 📁 Directory Structure

```
beginner/
├── README.md
├── lab-01-environment-setup/
├── lab-02-git-basics/
├── lab-03-docker-fundamentals/
├── lab-04-basic-cicd/
├── lab-05-security-basics/
├── lab-06-monitoring-intro/
├── lab-07-final-project/
└── resources/
    ├── cheat-sheets/
    ├── troubleshooting/
    └── additional-reading/
```

## 🎯 Learning Objectives

By the end of these beginner labs, you will be able to:
- Set up a complete DevSecOps development environment
- Use Git for version control and collaboration
- Create and manage Docker containers
- Build basic CI/CD pipelines
- Implement fundamental security practices
- Set up basic monitoring and logging
- Deploy a simple application using DevSecOps practices

## 🛠️ Lab Prerequisites

### Required Knowledge
- Basic command-line usage (Linux/macOS/Windows)
- Basic understanding of software development
- Basic networking concepts
- Basic security awareness

### Required Tools
- Git
- Docker
- A code editor (VS Code recommended)
- Cloud account (AWS, Azure, or GCP)
- Terminal/Command Prompt

### System Requirements
- 8GB RAM minimum
- 50GB free disk space
- Internet connection
- Modern operating system (Windows 10+, macOS 10.15+, or Linux)

## 🧪 Hands-On Labs

### Lab 1: Environment Setup
**Duration**: 2-3 hours  
**Difficulty**: Beginner  
**Prerequisites**: None

#### Objectives
- Set up a complete DevSecOps development environment
- Install and configure essential tools
- Create a cloud account and basic resources
- Verify all tools are working correctly

#### Tasks
1. **Install Git**
   ```bash
   # Ubuntu/Debian
   sudo apt update
   sudo apt install git
   
   # macOS
   brew install git
   
   # Windows
   # Download from https://git-scm.com/download/win
   ```

2. **Install Docker**
   ```bash
   # Ubuntu/Debian
   sudo apt update
   sudo apt install docker.io
   sudo systemctl start docker
   sudo systemctl enable docker
   sudo usermod -aG docker $USER
   
   # macOS
   brew install --cask docker
   
   # Windows
   # Download Docker Desktop from https://www.docker.com/products/docker-desktop
   ```

3. **Install VS Code**
   ```bash
   # Ubuntu/Debian
   wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
   sudo install -o root -g root -m 644 packages.microsoft.gpg /etc/apt/trusted.gpg.d/
   sudo sh -c 'echo "deb [arch=amd64,arm64,armhf signed-by=/etc/apt/trusted.gpg.d/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" > /etc/apt/sources.list.d/vscode.list'
   sudo apt update
   sudo apt install code
   
   # macOS
   brew install --cask visual-studio-code
   ```

4. **Create Cloud Account**
   - Sign up for AWS, Azure, or GCP
   - Create a free tier account
   - Set up billing alerts
   - Create access keys

5. **Verify Installation**
   ```bash
   git --version
   docker --version
   code --version
   ```

#### Deliverables
- [ ] Git installed and configured
- [ ] Docker installed and running
- [ ] VS Code installed with DevSecOps extensions
- [ ] Cloud account created and configured
- [ ] All tools verified working

---

### Lab 2: Git Basics
**Duration**: 3-4 hours  
**Difficulty**: Beginner  
**Prerequisites**: Lab 1

#### Objectives
- Learn Git fundamentals
- Practice version control workflows
- Understand branching and merging
- Collaborate using Git

#### Tasks
1. **Initialize Repository**
   ```bash
   mkdir devsecops-lab
   cd devsecops-lab
   git init
   git config --global user.name "Your Name"
   git config --global user.email "your.email@example.com"
   ```

2. **Create First Commit**
   ```bash
   echo "# DevSecOps Lab" > README.md
   git add README.md
   git commit -m "Initial commit"
   ```

3. **Create Branches**
   ```bash
   git checkout -b feature/new-feature
   echo "This is a new feature" > feature.txt
   git add feature.txt
   git commit -m "Add new feature"
   
   git checkout main
   git checkout -b bugfix/fix-issue
   echo "This fixes an issue" > fix.txt
   git add fix.txt
   git commit -m "Fix issue"
   ```

4. **Merge Branches**
   ```bash
   git checkout main
   git merge feature/new-feature
   git merge bugfix/fix-issue
   ```

5. **Create GitHub Repository**
   - Go to GitHub.com
   - Create a new repository
   - Connect local repository to remote
   ```bash
   git remote add origin https://github.com/yourusername/devsecops-lab.git
   git push -u origin main
   ```

#### Deliverables
- [ ] Local Git repository created
- [ ] Multiple commits made
- [ ] Branches created and merged
- [ ] GitHub repository created and connected
- [ ] Code pushed to remote repository

---

### Lab 3: Docker Fundamentals
**Duration**: 4-5 hours  
**Difficulty**: Beginner  
**Prerequisites**: Lab 2

#### Objectives
- Understand containerization concepts
- Create and manage Docker containers
- Build custom Docker images
- Use Docker Compose for multi-container applications

#### Tasks
1. **Run First Container**
   ```bash
   docker run hello-world
   docker run -it ubuntu:20.04 /bin/bash
   ```

2. **Create Dockerfile**
   ```dockerfile
   # Dockerfile
   FROM node:18-alpine
   WORKDIR /app
   COPY package*.json ./
   RUN npm install
   COPY . .
   EXPOSE 3000
   CMD ["npm", "start"]
   ```

3. **Build Custom Image**
   ```bash
   # Create package.json
   echo '{
     "name": "devsecops-app",
     "version": "1.0.0",
     "scripts": {
       "start": "node server.js"
     },
     "dependencies": {
       "express": "^4.18.0"
     }
   }' > package.json
   
   # Create server.js
   echo 'const express = require("express");
   const app = express();
   const port = 3000;
   
   app.get("/", (req, res) => {
     res.send("Hello from DevSecOps Lab!");
   });
   
   app.listen(port, () => {
     console.log(`Server running on port ${port}`);
   });' > server.js
   
   # Build image
   docker build -t devsecops-app .
   ```

4. **Run Custom Container**
   ```bash
   docker run -p 3000:3000 devsecops-app
   ```

5. **Create Docker Compose**
   ```yaml
   # docker-compose.yml
   version: '3.8'
   services:
     web:
       build: .
       ports:
         - "3000:3000"
       environment:
         - NODE_ENV=production
       depends_on:
         - db
     
     db:
       image: postgres:13
       environment:
         - POSTGRES_DB=myapp
         - POSTGRES_USER=user
         - POSTGRES_PASSWORD=password
       volumes:
         - postgres_data:/var/lib/postgresql/data
   
   volumes:
     postgres_data:
   ```

6. **Run Multi-Container Application**
   ```bash
   docker-compose up -d
   docker-compose ps
   docker-compose logs
   ```

#### Deliverables
- [ ] Docker containers running
- [ ] Custom Dockerfile created
- [ ] Docker image built and tested
- [ ] Docker Compose configuration created
- [ ] Multi-container application running

---

### Lab 4: Basic CI/CD
**Duration**: 5-6 hours  
**Difficulty**: Beginner  
**Prerequisites**: Lab 3

#### Objectives
- Understand CI/CD concepts
- Create basic GitHub Actions workflow
- Implement automated testing
- Deploy application automatically

#### Tasks
1. **Create GitHub Actions Workflow**
   ```yaml
   # .github/workflows/ci-cd.yml
   name: CI/CD Pipeline
   
   on:
     push:
       branches: [ main ]
     pull_request:
       branches: [ main ]
   
   jobs:
     test:
       runs-on: ubuntu-latest
       steps:
       - uses: actions/checkout@v3
       - name: Setup Node.js
         uses: actions/setup-node@v3
         with:
           node-version: '18'
           cache: 'npm'
       - name: Install dependencies
         run: npm install
       - name: Run tests
         run: npm test
   
     build:
       needs: test
       runs-on: ubuntu-latest
       steps:
       - uses: actions/checkout@v3
       - name: Build Docker image
         run: docker build -t devsecops-app .
       - name: Test Docker image
         run: docker run --rm devsecops-app npm test
   ```

2. **Add Testing**
   ```bash
   # Install testing framework
   npm install --save-dev jest
   
   # Create test file
   echo 'const request = require("supertest");
   const app = require("./server");
   
   describe("GET /", () => {
     it("responds with Hello from DevSecOps Lab!", async () => {
       const response = await request(app).get("/");
       expect(response.text).toBe("Hello from DevSecOps Lab!");
     });
   });' > server.test.js
   
   # Update package.json
   echo '{
     "name": "devsecops-app",
     "version": "1.0.0",
     "scripts": {
       "start": "node server.js",
       "test": "jest"
     },
     "dependencies": {
       "express": "^4.18.0"
     },
     "devDependencies": {
       "jest": "^29.0.0",
       "supertest": "^6.3.0"
     }
   }' > package.json
   ```

3. **Deploy to Cloud**
   ```yaml
   # Add to .github/workflows/ci-cd.yml
   deploy:
     needs: build
     runs-on: ubuntu-latest
     if: github.ref == 'refs/heads/main'
     steps:
     - uses: actions/checkout@v3
     - name: Deploy to cloud
       run: |
         echo "Deploying to cloud..."
         # Add your deployment commands here
   ```

4. **Test Pipeline**
   ```bash
   git add .
   git commit -m "Add CI/CD pipeline"
   git push origin main
   ```

#### Deliverables
- [ ] GitHub Actions workflow created
- [ ] Automated testing implemented
- [ ] Docker build automated
- [ ] Deployment pipeline configured
- [ ] Pipeline tested and working

---

### Lab 5: Security Basics
**Duration**: 4-5 hours  
**Difficulty**: Beginner  
**Prerequisites**: Lab 4

#### Objectives
- Understand basic security concepts
- Implement security scanning
- Use secrets management
- Apply security best practices

#### Tasks
1. **Add Security Scanning**
   ```yaml
   # Add to .github/workflows/ci-cd.yml
   security:
     runs-on: ubuntu-latest
     steps:
     - uses: actions/checkout@v3
     - name: Run security audit
       run: npm audit --audit-level=high
     - name: Run Snyk security scan
       uses: snyk/actions/node@master
       env:
         SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
   ```

2. **Implement Secrets Management**
   ```bash
   # Create .env file
   echo 'DATABASE_URL=postgresql://user:password@localhost:5432/myapp
   API_KEY=your-api-key
   JWT_SECRET=your-jwt-secret' > .env
   
   # Add to .gitignore
   echo '.env
   node_modules/
   .DS_Store' > .gitignore
   ```

3. **Add Security Headers**
   ```javascript
   // Update server.js
   const express = require('express');
   const helmet = require('helmet');
   const app = express();
   
   // Security middleware
   app.use(helmet());
   
   // Other middleware
   app.use(express.json());
   app.use(express.static('public'));
   
   // Routes
   app.get('/', (req, res) => {
     res.send('Hello from DevSecOps Lab!');
   });
   
   const port = process.env.PORT || 3000;
   app.listen(port, () => {
     console.log(`Server running on port ${port}`);
   });
   ```

4. **Configure HTTPS**
   ```yaml
   # Add to docker-compose.yml
   nginx:
     image: nginx:alpine
     ports:
       - "80:80"
       - "443:443"
     volumes:
       - ./nginx.conf:/etc/nginx/nginx.conf
       - ./ssl:/etc/nginx/ssl
     depends_on:
       - web
   ```

5. **Add Input Validation**
   ```javascript
   // Add validation middleware
   const { body, validationResult } = require('express-validator');
   
   app.post('/api/users', [
     body('email').isEmail(),
     body('password').isLength({ min: 6 })
   ], (req, res) => {
     const errors = validationResult(req);
     if (!errors.isEmpty()) {
       return res.status(400).json({ errors: errors.array() });
     }
     // Process valid data
   });
   ```

#### Deliverables
- [ ] Security scanning implemented
- [ ] Secrets management configured
- [ ] Security headers added
- [ ] Input validation implemented
- [ ] HTTPS configuration added

---

### Lab 6: Monitoring Introduction
**Duration**: 3-4 hours  
**Difficulty**: Beginner  
**Prerequisites**: Lab 5

#### Objectives
- Understand monitoring concepts
- Implement basic logging
- Set up health checks
- Monitor application performance

#### Tasks
1. **Add Logging**
   ```javascript
   // Update server.js
   const winston = require('winston');
   
   const logger = winston.createLogger({
     level: 'info',
     format: winston.format.combine(
       winston.format.timestamp(),
       winston.format.json()
     ),
     transports: [
       new winston.transports.File({ filename: 'error.log', level: 'error' }),
       new winston.transports.File({ filename: 'combined.log' })
     ]
   });
   
   // Add logging middleware
   app.use((req, res, next) => {
     logger.info(`${req.method} ${req.url}`, {
       ip: req.ip,
       userAgent: req.get('User-Agent')
     });
     next();
   });
   ```

2. **Implement Health Checks**
   ```javascript
   // Add health check endpoint
   app.get('/health', (req, res) => {
     res.status(200).json({
       status: 'healthy',
       timestamp: new Date().toISOString(),
       uptime: process.uptime()
     });
   });
   
   // Add readiness check
   app.get('/ready', (req, res) => {
     // Check database connection, external services, etc.
     res.status(200).json({
       status: 'ready',
       timestamp: new Date().toISOString()
     });
   });
   ```

3. **Add Metrics**
   ```javascript
   // Add Prometheus metrics
   const prometheus = require('prom-client');
   
   const register = new prometheus.Registry();
   prometheus.collectDefaultMetrics({ register });
   
   const httpRequestDuration = new prometheus.Histogram({
     name: 'http_request_duration_seconds',
     help: 'Duration of HTTP requests in seconds',
     labelNames: ['method', 'route', 'status_code']
   });
   
   register.registerMetric(httpRequestDuration);
   
   // Add metrics endpoint
   app.get('/metrics', (req, res) => {
     res.set('Content-Type', register.contentType);
     res.end(register.metrics());
   });
   ```

4. **Create Monitoring Dashboard**
   ```yaml
   # Add to docker-compose.yml
   prometheus:
     image: prom/prometheus
     ports:
       - "9090:9090"
     volumes:
       - ./prometheus.yml:/etc/prometheus/prometheus.yml
   
   grafana:
     image: grafana/grafana
     ports:
       - "3001:3000"
     environment:
       - GF_SECURITY_ADMIN_PASSWORD=admin
   ```

5. **Set Up Alerts**
   ```yaml
   # prometheus.yml
   global:
     scrape_interval: 15s
   
   scrape_configs:
     - job_name: 'app'
       static_configs:
         - targets: ['web:3000']
   
   rule_files:
     - "alert_rules.yml"
   
   alerting:
     alertmanagers:
       - static_configs:
           - targets:
             - alertmanager:9093
   ```

#### Deliverables
- [ ] Logging system implemented
- [ ] Health checks added
- [ ] Metrics collection configured
- [ ] Monitoring dashboard created
- [ ] Alerting system set up

---

### Lab 7: Final Project
**Duration**: 6-8 hours  
**Difficulty**: Beginner  
**Prerequisites**: All previous labs

#### Objectives
- Integrate all learned concepts
- Deploy a complete DevSecOps application
- Demonstrate best practices
- Create a portfolio project

#### Tasks
1. **Create Complete Application**
   - Build a full-stack application
   - Implement all security measures
   - Add comprehensive testing
   - Include monitoring and logging

2. **Deploy to Cloud**
   - Choose a cloud platform
   - Set up infrastructure
   - Deploy application
   - Configure monitoring

3. **Document Everything**
   - Create comprehensive README
   - Document all processes
   - Include troubleshooting guides
   - Add architecture diagrams

4. **Present Project**
   - Create presentation
   - Demonstrate functionality
   - Explain architecture
   - Show security measures

#### Deliverables
- [ ] Complete application deployed
- [ ] All DevSecOps practices implemented
- [ ] Comprehensive documentation
- [ ] Portfolio-ready project
- [ ] Presentation completed

## 📚 Additional Resources

### Cheat Sheets
- [Git Cheat Sheet](resources/cheat-sheets/git-cheat-sheet.md)
- [Docker Cheat Sheet](resources/cheat-sheets/docker-cheat-sheet.md)
- [Linux Commands Cheat Sheet](resources/cheat-sheets/linux-commands.md)
- [Security Best Practices](resources/cheat-sheets/security-best-practices.md)

### Troubleshooting Guides
- [Common Git Issues](resources/troubleshooting/git-troubleshooting.md)
- [Docker Problems](resources/troubleshooting/docker-troubleshooting.md)
- [CI/CD Pipeline Issues](resources/troubleshooting/cicd-troubleshooting.md)
- [Security Scanning Problems](resources/troubleshooting/security-troubleshooting.md)

### Additional Reading
- [DevSecOps Fundamentals](resources/additional-reading/devsecops-fundamentals.md)
- [Container Security](resources/additional-reading/container-security.md)
- [CI/CD Best Practices](resources/additional-reading/cicd-best-practices.md)
- [Monitoring and Observability](resources/additional-reading/monitoring-observability.md)

## 🎯 Assessment Criteria

### Lab Completion
- [ ] All labs completed successfully
- [ ] All deliverables submitted
- [ ] Code follows best practices
- [ ] Documentation is comprehensive
- [ ] Project is portfolio-ready

### Knowledge Demonstration
- [ ] Can explain DevSecOps concepts
- [ ] Can troubleshoot common issues
- [ ] Can implement security measures
- [ ] Can deploy applications
- [ ] Can monitor and maintain systems

## 🤝 Getting Help

### Support Channels
- **Documentation**: Comprehensive guides in each lab
- **Issues**: GitHub issues for lab problems
- **Discussions**: Community discussions for questions
- **Mentorship**: Connect with DevSecOps experts

### Community Resources
- **Slack**: #beginner-labs
- **Discord**: DevSecOps Learning Community
- **LinkedIn**: DevSecOps Beginners Group
- **YouTube**: DevSecOps Tutorials Channel

---

**Ready to start your DevSecOps journey?** Begin with Lab 1 and work your way through all the hands-on exercises!
