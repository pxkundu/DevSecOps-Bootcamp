# DevSecOps-Bootcamp 🚀

A comprehensive 6-week DevSecOps bootcamp with step-by-step instructions, hands-on projects, and real-world simulations. This bootcamp blends foundational learning with chaos engineering, gamification, and practical implementation to prepare intermediate AWS DevOps and Cloud Engineers for real-world challenges.

## 📚 Complete Learning Path Index

### 🗓️ **Week 1: Core AWS Foundations with Chaos Engineering**
**Goal**: Build AWS basics with controlled chaos to spark engagement and resilience.

#### Day 1: AWS Basics Refresher
- **Duration**: 4-5 hours
- **Objective**: Set up foundational AWS resources and recover from simulated failures
- **Tools**: AWS Console, AWS CLI
- **Activities**: VPC creation, EC2 deployment, web server setup, chaos recovery
- **Chaos Twist**: "Power Outage" - subnet termination and recovery
- **Resources**: [Day 1 Guide](Week1/Day1.md)

#### Day 2: Storage and Databases
- **Duration**: 4-5 hours
- **Objective**: Deploy S3 and RDS with competitive gamification
- **Tools**: AWS Console, MySQL Workbench
- **Activities**: S3 static site, RDS MySQL, database operations
- **Gamified Twist**: Speed race for fastest deployment
- **Resources**: [Day 2 Guide](Week1/Day2.md)

#### Day 3: Networking Deep Dive
- **Duration**: 4-5 hours
- **Objective**: Build multi-tier VPC and handle simulated attacks
- **Tools**: AWS Console
- **Activities**: Multi-tier VPC, NAT Gateways, route tables
- **Chaos Twist**: "DDoS" - security group modifications
- **Resources**: [Day 3 Guide](Week1/Day3.md)

#### Day 4: Intro to Scripting
- **Duration**: 4-5 hours
- **Objective**: Automate EC2 setup with scripted failures
- **Tools**: AWS CLI, Bash
- **Activities**: AWS CLI automation, EC2 provisioning scripts
- **Chaos Twist**: Script failures and debugging
- **Resources**: [Day 4 Guide](Week1/Day4.md)

#### Day 5: Mini-Project
- **Duration**: 5-6 hours
- **Objective**: Deploy web app with last-minute requirements
- **Tools**: AWS Console, AWS CLI
- **Activities**: Web application deployment, S3 integration
- **Chaos Twist**: "CEO Tweet" - emergency status page
- **Resources**: [Day 5 Guide](Week1/Day5/README.md)
  - [Project Details](Week1/Day5/Day5.md)
  - [Best Practices](Week1/Day5/BestPractices.md)
  - [NodeJS Project](Week1/Day5/NodeJSprojectWithInEC2server.md)
  - [PHP Project](Week1/Day5/PHPprojectWithInEC2server.md)
  - [WordPress CMS Project](Week1/Day5/WPCMSprojectWithInEC2server.md)

**Week 1 Resources**: [Overview](Week1/README.md) | [Topics](Week1/Topics/)

---

### 🗓️ **Week 2: Infrastructure as Code and Containers**
**Goal**: Master IaC tools and containerization with competitive challenges.

#### Day 1: CloudFormation Basics
- **Duration**: 4-5 hours
- **Objective**: Write templates, deploy EC2 + RDS, fix random errors
- **Tools**: AWS CloudFormation, AWS Console
- **Activities**: Template creation, stack deployment, error resolution
- **Chaos Twist**: Random template errors and fixes
- **Resources**: [Day 1 Guide](Week2/Day1.md)

#### Day 2: Terraform Introduction
- **Duration**: 4-5 hours
- **Objective**: Rebuild Day 1 stack, race against peers
- **Tools**: Terraform, AWS CLI
- **Activities**: Terraform configuration, state management
- **Gamified Twist**: Speed competition for fastest deployment
- **Resources**: [Day 2 Guide](Week2/Day2.md)

#### Day 3: Docker Fundamentals
- **Duration**: 4-5 hours
- **Objective**: Build/run containers, solve escape room challenges
- **Tools**: Docker, Docker Compose
- **Activities**: Container creation, image management, networking
- **Chaos Twist**: Container escape room challenges
- **Resources**: [Day 3 Guide](Week2/Day3.md)

#### Day 4: Containers on ECS
- **Duration**: 4-5 hours
- **Objective**: Deploy to Fargate, scale after traffic spikes
- **Tools**: AWS ECS, Fargate
- **Activities**: ECS cluster setup, service deployment, auto-scaling
- **Chaos Twist**: Traffic spike simulation
- **Resources**: [Day 4 Guide](Week2/Day4/Day4.md)
  - [EKS Implementation](Week2/Day4/Day4onEKS.md)

#### Day 5: Mini-Hackathon
- **Duration**: 5-6 hours
- **Objective**: IaC + ECS app, recover from Chaos Monkey
- **Tools**: Terraform, ECS, AWS CLI
- **Activities**: Complete application deployment, chaos testing
- **Chaos Twist**: Chaos Monkey attacks
- **Resources**: [Day 5 Guide](Week2/Day5/README.md)
  - [Project Details](Week2/Day5/Day5.md)
  - [JPMC with Kubernetes](Week2/Day5/JPMCwithKube.md)
  - [Top 5 Companies Using Kubernetes](Week2/Day5/Top5companiesUsinfKube.md)

**Week 2 Resources**: [Overview](Week2/README.md) | [Topics](Week2/Topics/)

---

### 🗓️ **Week 3: CI/CD and Serverless with Incident Drills**
**Goal**: Master CI/CD pipelines and serverless with real incident scenarios.

#### Day 1: CI/CD Basics
- **Duration**: 4-5 hours
- **Objective**: GitHub Actions pipeline, rollback bad commits
- **Tools**: GitHub Actions, Git
- **Activities**: Pipeline creation, automated testing, rollback procedures
- **Chaos Twist**: Bad commit deployment and recovery
- **Resources**: [Day 1 Guide](Week3/Day1.md)

#### Day 2: AWS CodeSuite
- **Duration**: 4-5 hours
- **Objective**: CodePipeline for ECS, fix production outages
- **Tools**: AWS CodePipeline, CodeBuild, CodeDeploy
- **Activities**: Multi-stage pipeline, ECS deployment
- **Chaos Twist**: Production outage simulation
- **Resources**: [Day 2 Guide](Week3/Day2.md)

#### Day 3: Serverless Foundations
- **Duration**: 4-5 hours
- **Objective**: Lambda API, secure from rival "hacks"
- **Tools**: AWS Lambda, API Gateway
- **Activities**: Serverless function creation, API development
- **Chaos Twist**: Security breach simulation
- **Resources**: [Day 3 Guide](Week3/Day3/README.md)
  - [Pipeline Library](Week3/Day3/week3-day3/pipeline-lib/README.md)
  - [Task Manager](Week3/Day3/week3-day3/task-manager/README.md)

#### Day 4: Pipeline Under Pressure
- **Duration**: 4-5 hours
- **Objective**: Multi-stage deploy, add features mid-build
- **Tools**: Jenkins, GitOps
- **Activities**: Advanced pipeline configuration, GitOps implementation
- **Chaos Twist**: Mid-build requirement changes
- **Resources**: [Day 4 Guide](Week3/Day4/README.md)
  - [Pipeline Library](Week3/Day4/week3-day4/pipeline-lib/README.md)
  - [Task Manager GitOps](Week3/Day4/week3-day4/task-manager-gitops/README.md)

#### Day 5: Incident Showdown
- **Duration**: 5-6 hours
- **Objective**: Fix cascading failures, write post-mortems
- **Tools**: Jenkins, AWS CLI
- **Activities**: Incident response, failure recovery, documentation
- **Chaos Twist**: Cascading system failures
- **Resources**: [Day 5 Guide](Week3/Day5/Day5.md)
  - [Jenkins Master-Slave Automation](Week3/Day5/JenkinsMasterSlaveAutomation/README.md)

**Week 3 Resources**: [Overview](Week3/README.md) | [Topics](Week3/Topics/)

---

### 🗓️ **Week 4: Scalability and Monitoring with Chaos**
**Goal**: Build scalable systems with comprehensive monitoring and chaos testing.

#### Day 1: Load Balancing
- **Duration**: 4-5 hours
- **Objective**: ALB setup, tune for traffic surges
- **Tools**: AWS ALB, EC2, Terraform
- **Activities**: Load balancer configuration, health checks, traffic distribution
- **Chaos Twist**: Traffic surge simulation
- **Resources**: [Day 1 Guide](Week4/Day1/README.md)
  - [Static Website Terraform Jenkins](Week4/Day1/StaticWebsiteTerraformJenkins/README.md)

#### Day 2: Autoscaling
- **Duration**: 4-5 hours
- **Objective**: Add autoscaling, recover terminated instances
- **Tools**: AWS Auto Scaling, CloudWatch
- **Activities**: Auto-scaling group configuration, policy management
- **Chaos Twist**: Instance termination and recovery
- **Resources**: [Day 2 Guide](Week4/Day2/README.md)
  - [Advanced Topics Project](Week4/Day2/ProjectWithAdvanceTopics/README.md)
  - [CRM Terraform Jenkins](Week4/Day2/ProjectWithAdvanceTopics/CRMTerraformJenkins/README.md)

#### Day 3: CloudWatch Monitoring
- **Duration**: 4-5 hours
- **Objective**: Monitor ECS, solve performance mysteries
- **Tools**: CloudWatch, X-Ray, ECS
- **Activities**: Metric collection, alarm configuration, performance analysis
- **Chaos Twist**: Performance mystery investigation
- **Resources**: [Day 3 Guide](Week4/Day3/README.md)
  - [Message Encoder Decoder K8s](Week4/Day3/MessageEncoderDecoderK8s/README.md)

#### Day 4: EKS Introduction
- **Duration**: 4-5 hours
- **Objective**: Deploy to EKS, heal crashed pods
- **Tools**: AWS EKS, kubectl
- **Activities**: EKS cluster setup, pod deployment, troubleshooting
- **Chaos Twist**: Pod crash simulation
- **Resources**: [Day 4 Guide](Week4/Day4/README.md)

#### Day 5: Resilience Rally
- **Duration**: 5-6 hours
- **Objective**: Scalable app, survive chaos tests
- **Tools**: EKS, Terraform, Jenkins
- **Activities**: Complete application deployment, chaos engineering
- **Chaos Twist**: Multi-system failure simulation
- **Resources**: [Day 5 Guide](Week4/Day5/README.md)
  - [CRM Supply Chain Capstone](Week4/Day5/CRMSupplyChainCapstone/README.md)
  - [Capstone Documentation](Week4/Day5/CRMSupplyChainCapstone/docs/README.md)
  - [Project Implementation Plan](Week4/Day5/ProjectImplementationPlan/README.md)
    - [Phase 1](Week4/Day5/ProjectImplementationPlan/Phase1/README.md)
    - [Phase 2](Week4/Day5/ProjectImplementationPlan/Phase2/README.md)
    - [Phase 3](Week4/Day5/ProjectImplementationPlan/Phase3/README.md)
    - [Phase 4](Week4/Day5/ProjectImplementationPlan/Phase4/README.md)
    - [Phase 5](Week4/Day5/ProjectImplementationPlan/Phase5/README.md)

**Week 4 Resources**: [Overview](Week4/README.md) | [Topics](Week4/Topics/)

---

### 🗓️ **Week 5: Security, Cost, and Troubleshooting**
**Goal**: Master security practices, cost optimization, and advanced troubleshooting.

#### Day 1: Security Basics
- **Duration**: 4-5 hours
- **Objective**: Encrypt S3/RDS, fix exposed buckets
- **Tools**: AWS KMS, IAM, Security Hub
- **Activities**: Data encryption, access control, security assessment
- **Chaos Twist**: Security breach simulation
- **Resources**: [Day 1 Guide](Week5/Day1/README.md)

#### Day 2: Disaster Recovery
- **Duration**: 4-5 hours
- **Objective**: Multi-AZ RDS, failover after outages
- **Tools**: AWS RDS, Route 53, CloudFormation
- **Activities**: DR strategy implementation, failover testing
- **Chaos Twist**: Availability zone failure simulation
- **Resources**: [Day 2 Guide](Week5/Day2/README.md)

#### Day 3: Cost Optimization
- **Duration**: 4-5 hours
- **Objective**: Cut costs, avoid overspending penalties
- **Tools**: AWS Cost Explorer, Trusted Advisor
- **Activities**: Cost analysis, optimization strategies, budget management
- **Chaos Twist**: Budget constraint challenges
- **Resources**: [Day 3 Guide](Week5/Day3/README.md)

#### Day 4: Advanced Troubleshooting
- **Duration**: 4-5 hours
- **Objective**: Debug with X-Ray, solve complex issues
- **Tools**: AWS X-Ray, CloudWatch Logs, Systems Manager
- **Activities**: Distributed tracing, log analysis, system diagnostics
- **Chaos Twist**: Complex failure scenarios
- **Resources**: [Day 4 Guide](Week5/Day4/README.md)

#### Day 5: Security Mini-Project
- **Duration**: 5-6 hours
- **Objective**: Secure app with DR, pass peer audit
- **Tools**: All Week 5 tools
- **Activities**: Complete secure application, security audit
- **Chaos Twist**: Peer security review
- **Resources**: [Day 5 Guide](Week5/Day5/README.md)

**Week 5 Resources**: [Overview](Week5/README.md)

---

### 🗓️ **Week 6: Capstone and Real-World Crunch**
**Goal**: Synthesize all learning into a comprehensive capstone project.

#### Day 1: Capstone Kickoff
- **Duration**: 7-8 hours
- **Objective**: Plan microservices, adapt to tool changes
- **Tools**: Architecture planning, EKS, CI/CD tools
- **Activities**: Microservices design, tool selection, adaptation
- **Chaos Twist**: Mid-plan tool swapping
- **Resources**: [Day 1 Guide](Week6/Day1/README.md)

#### Day 2: Build and Automate
- **Duration**: 7-8 hours
- **Objective**: CI/CD + EKS, scale for DDoS attacks
- **Tools**: EKS, GitHub Actions, AWS Shield
- **Activities**: Platform deployment, automation, scaling
- **Chaos Twist**: DDoS attack simulation
- **Resources**: [Day 2 Guide](Week6/Day2/README.md)

#### Day 3: Secure and Monitor
- **Duration**: 7-8 hours
- **Objective**: Add encryption/alarms, pass penetration tests
- **Tools**: AWS KMS, CloudWatch, OWASP ZAP
- **Activities**: Security implementation, monitoring setup, security testing
- **Chaos Twist**: Penetration testing challenges
- **Resources**: [Day 3 Guide](Week6/Day3/README.md)

#### Day 4: Chaos Crunch
- **Duration**: 7-8 hours
- **Objective**: Survive outages/spikes, write runbooks
- **Tools**: Chaos engineering tools, monitoring systems
- **Activities**: Chaos testing, incident response, documentation
- **Chaos Twist**: Multi-system failure simulation
- **Resources**: [Day 4 Guide](Week6/Day4/README.md)

#### Day 5: Production Push
- **Duration**: 7-8 hours
- **Objective**: Deploy to production, present to executives
- **Tools**: All learned tools and techniques
- **Activities**: Production deployment, presentation, evaluation
- **Chaos Twist**: Executive review pressure
- **Resources**: [Day 5 Guide](Week6/Day5/README.md)

**Week 6 Resources**: [Overview](Week6/README.md) | [Plan](Week6/Plan.md) | [Kubernetes Plan](Week6/KubernetesPlan.md) | [Best Practices](Week6/BestPractices.md)
- [Capstone Project](Week6/CapstoneProject/)
- [Learning Kubernetes Project](Week6/LearningKubeProject/)

---

## 🛠️ **Additional Learning Resources**

### 🔐 **DevSecOps Tools & Tutorials**
- [DevSecOps Tools](DevSecOpsTools/) - Comprehensive tooling guide
- [DevSecOps Trivy Tutorial](DevSecOpsTrivyTutorial/) - Complete Trivy security scanning guide
  - [Part 1-10 Tutorial Series](DevSecOpsTrivyTutorial/learningTrivy_Part1.md)
  - [Project Codebase](DevSecOpsTrivyTutorial/ProjectCodebase/)
- [DevSecOps Automation](DevSecOpsAutomation/) - Kubernetes and Istio automation scripts
  - [Kubernetes Setup Scripts](DevSecOpsAutomation/KubernetesMasterWorkerSetup/)
  - [Istio Bookinfo Deployment](DevSecOpsAutomation/istio-bookinfo/)
  - [Kubernetes Manifests](DevSecOpsAutomation/manifests/)

### 🚀 **AWS DevOps Boilerplates**
- [AWS DevOps Boilerplates](DevSecOpsBoilerplates/aws-devops-boilerplates/) - Production-ready templates
  - CloudFormation, Terraform, Docker, ECS, Lambda, EKS
  - IAM, CloudWatch, Secrets Management
- [AWS Testing Boilerplates](DevSecOpsBoilerplates/aws-testing-boilerplates/) - Testing frameworks
- [AWS Security Testing](DevSecOpsBoilerplates/aws-security-testing-boilerplates/) - Security testing templates
- [AWS Cost Audit](DevSecOpsBoilerplates/aws-cost-audit-boilerplates/) - Cost optimization tools
- [EKS Status Scanner](DevSecOpsBoilerplates/eks-status-scan-boilerplates/) - EKS monitoring tools

### 🤖 **AI & Data Platform Solutions**
- [Enterprise AI-Data Platform](AI-DataPlatformSolutions/) - Comprehensive AI/ML platform guide
  - [Foundation & Architecture](AI-DataPlatformSolutions/01-Foundation/)
  - [Data Engineering](AI-DataPlatformSolutions/02-DataEngineering/)
  - [MLOps](AI-DataPlatformSolutions/03-MLOps/)
  - [Infrastructure & DevOps](AI-DataPlatformSolutions/04-Infrastructure/)
  - [Security & Compliance](AI-DataPlatformSolutions/05-Security/)
  - [Tools & Technologies](AI-DataPlatformSolutions/06-Tools/)
  - [Implementation Examples](AI-DataPlatformSolutions/07-Examples/)
  - [Best Practices](AI-DataPlatformSolutions/08-BestPractices/)

### 🧪 **Software Quality Assurance (SQA)**
- [SQA Knowledge Hub](SQA-KnowHow/) - Comprehensive QA learning resources
  - [SQA Manual Testing](SQA-KnowHow/SQA-Manual-Testing/) - Manual testing methodologies
  - [SQA Automation Testing](SQA-KnowHow/SQA-Automation-Testing/) - Automated testing frameworks
    - [Selenium Learning Project](SQA-KnowHow/SQA-Automation-Testing/SQA-Automation-Testing-Selenium-Learning-Project.md)
    - [Cypress Learning Project](SQA-KnowHow/SQA-Automation-Testing/SQA-Automation-Testing-Cypress-Learning-Project.md)
    - [Advanced Concepts](SQA-KnowHow/SQA-Automation-Testing/SQA-Automation-Testing-Advance-Concepts.md)
    - [Framework Comparison](SQA-KnowHow/SQA-Automation-Testing/SQA-Automation-Testing-Framework-Comparison.md)

### 📊 **AWS DevOps Boilerplates (Root Level)**
- [S3 Management Scripts](aws-devops-boilerplates/s3/) - S3 bucket management and cleanup

---

## 🎯 **Learning Objectives & Outcomes**

### **By Week 6, You Will Be Able To:**
- ✅ Design and deploy scalable microservices architectures
- ✅ Implement comprehensive CI/CD pipelines with multiple tools
- ✅ Secure applications using industry best practices
- ✅ Monitor and troubleshoot complex distributed systems
- ✅ Handle real-world incidents and chaos scenarios
- ✅ Optimize costs and implement disaster recovery
- ✅ Present technical solutions to stakeholders
- ✅ Work effectively in DevSecOps teams

### **Key Skills Developed:**
- **AWS Services**: EC2, S3, RDS, VPC, ECS, EKS, Lambda, CloudWatch
- **Infrastructure as Code**: Terraform, CloudFormation
- **Containerization**: Docker, ECS, EKS, Istio
- **CI/CD**: Jenkins, GitHub Actions, AWS CodeSuite
- **Security**: IAM, KMS, Security Hub, penetration testing
- **Monitoring**: CloudWatch, X-Ray, logging, alerting
- **Chaos Engineering**: Failure simulation, incident response
- **Cost Optimization**: Budget management, resource optimization

---

## 🚀 **Getting Started**

### **Prerequisites:**
- Basic understanding of cloud computing concepts
- Familiarity with Linux command line
- AWS account (free tier recommended)
- Local development environment setup

### **Recommended Learning Path:**
1. **Start with Week 1** - Build AWS foundations
2. **Progress sequentially** through each week
3. **Complete all hands-on projects** in each day
4. **Practice chaos scenarios** to build resilience
5. **Document your learning** and create a portfolio
6. **Participate in peer reviews** and discussions

### **Time Commitment:**
- **Per Day**: 4-8 hours (depending on week)
- **Per Week**: 20-40 hours
- **Total Bootcamp**: 120-240 hours over 6 weeks

---

## 🤝 **Support & Community**

### **Learning Resources:**
- Daily war rooms and mentor hotlines
- Peer collaboration and code reviews
- Real-world scenario simulations
- Comprehensive documentation and examples

### **Tools & Technologies:**
- All necessary tools provided or guided installation
- Cloud-based development environments available
- Comprehensive boilerplates and templates
- Security testing and monitoring tools

---

## 📝 **Notes**

- **Chaos Engineering**: Controlled failure simulation to build resilience
- **Gamification**: Competitive elements to enhance engagement
- **Real-World Focus**: Practical scenarios and industry best practices
- **Hands-On Learning**: 60% practical implementation, 40% theory
- **Continuous Improvement**: Regular updates and community contributions

---

*Prepared by Partha Sarathi Kundu for the DevSecOps Bootcamp project - A comprehensive journey from AWS basics to enterprise DevSecOps mastery.*

## 📄 **License**
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.