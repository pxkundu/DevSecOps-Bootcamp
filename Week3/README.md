# Week 3: Automate Everything - Mastering CI/CD Excellence

## Overview
Welcome to **Week 3** of our DevOps bootcamp! This week zeroes in on **CI/CD and Automation Technologies**, with a deep dive into **Jenkins** for the first three days—covering basics to advanced architectures—followed by two days exploring related CI/CD tools. Building on Week 2’s Kubernetes foundation, you’ll automate the To-Do app with real-world practices and engaging challenges.

- **Duration**: 5 days, 5-6 hours each
- **Objective**: Master Jenkins and complementary CI/CD technologies for automation excellence.
- **Tools**: Jenkins, AWS (EC2, EKS, Fargate, S3, CodePipeline, CodeBuild, Lambda), GitHub, ArgoCD, Helm, Docker, `kubectl`.

### Week 3 Content Index: CI/CD and Automation Technologies

#### Day 1: Jenkins Basics - "Pipeline Foundations"
- **Objective**: Establish a strong foundation in Jenkins CI/CD with AWS and GitHub integration.
- **Theory** (Expanded):
  - Jenkins architecture: Master vs. agent roles, plugin ecosystem, filesystem layout (e.g., `~/.jenkins`).
  - CI/CD principles: Continuous Integration (CI) vs. Continuous Deployment (CD), feedback loops, pipeline stages (source, build, test, deploy).
  - Automation benefits: Reduced manual errors, faster release cycles, consistency across environments.
  - Best practices: Pipeline as code (Jenkinsfile), version control integration, secrets management with AWS SSM, incremental builds.
  - Common pitfalls: Overloaded master, untested code in prod, lack of logging.
- **Practical** (Expanded):
  - Set up Jenkins on an AWS EC2 instance with GitHub integration.
  - Build a pipeline for the To-Do app: clone from GitHub, build Docker image, push to ECR, deploy to EKS.
  - Add unit tests (Jest) and basic logging with CloudWatch.
  - Commands for setup, pipeline execution, and troubleshooting.
- **Tools**: Jenkins, AWS EC2, GitHub, Docker, AWS ECR, EKS, AWS CloudWatch, `kubectl`.
- **Engagement**: "Build Blitz"—optimize pipeline runtime with parallel stages and share fastest time.
- **Learning Outcome**: Automate a basic CI/CD pipeline with Jenkins, AWS, and GitHub, understanding core concepts and commands.

#### Day 2: Intermediate Jenkins - "Scaling Pipelines"
- **Objective**: Scale Jenkins pipelines with multi-branch support and EC2 agents for intermediate workflows.
- **Theory** (Expanded):
  - Multi-branch pipelines: Branch-specific builds, PR validation, feature toggles.
  - Distributed builds: Static vs. dynamic agents, load balancing, agent provisioning strategies.
  - Best practices: Environment isolation (dev/staging/prod), artifact versioning in S3, rollback mechanisms, pipeline parameterization.
  - AWS integration: EC2 auto-scaling for agents, IAM roles for secure access, S3 as a durable store.
  - Scaling challenges: Agent sprawl, pipeline bottlenecks, dependency hell.
- **Practical** (Expanded):
  - Extend the To-Do app pipeline with multi-branch support (e.g., `main` vs. `dev`).
  - Configure static EC2 agents for parallel builds and tests.
  - Store build artifacts in S3, deploy to EKS with environment variables, and implement rollback.
  - Commands for agent setup, pipeline scaling, and AWS resource management.
- **Tools**: Jenkins, AWS EC2 (master + agents), GitHub, AWS S3, EKS, Docker, `kubectl`, AWS IAM.
- **Engagement**: "Agent Arena"—set up agents and race to parallelize builds across branches.
- **Learning Outcome**: Scale Jenkins pipelines with distributed builds and multi-environment support using AWS and GitHub.

#### Day 3: Advanced Jenkins - "Complex Architectures"
- **Objective**: Design complex CI/CD solutions with Jenkins, VCS, and AWS for production-grade systems.
- **Theory**:
  - Shared libraries for reusable pipeline code.
  - Dynamic agents (AWS Fargate) for cost-efficient scaling.
  - Security (e.g., Trivy scans), compliance gates, and auditability.
  - Complex architecture: multi-service, multi-region deployments.
- **Practical**:
  - Refactor the To-Do app pipeline with a shared library for build/test/deploy logic.
  - Use Fargate agents for dynamic scaling and integrate Trivy for image security scans.
  - Deploy to EKS across two AWS regions (e.g., us-east-1, us-west-2) with approval gates.
- **Tools**: Jenkins, AWS Fargate, GitHub, Trivy, AWS EKS, S3, `kubectl`.
- **Engagement**: "Security Siege"—inject a vulnerability and automate its detection/fix.
- **Learning Outcome**: Architect advanced, secure, and scalable CI/CD solutions with Jenkins.

#### Day 4: GitOps with ArgoCD - "Declarative Automation"
- **Objective**: Explore GitOps as a complementary CI/CD approach to Jenkins.
- **Theory**:
  - GitOps principles (declarative, pull-based, Git as truth).
  - ArgoCD architecture and reconciliation process.
  - Comparison with push-based CI/CD (e.g., Jenkins).
- **Practical**:
  - Deploy the To-Do app to EKS using ArgoCD.
  - Convert manifests to Helm charts and sync from GitHub.
  - Simulate and resolve deployment drift.
- **Tools**: ArgoCD, Helm, GitHub, AWS EKS, `kubectl`.
- **Engagement**: "Drift Dash"—introduce drift and race to fix it via Git PRs.
- **Learning Outcome**: Automate deployments with GitOps for consistency and scalability.

#### Day 5: Serverless CI/CD with AWS - "Cloud-Native Automation"
- **Objective**: Master serverless CI/CD using AWS-native tools.
- **Theory**:
  - Serverless CI/CD advantages (cost, simplicity) and limitations.
  - AWS CodePipeline/CodeBuild vs. Jenkins workflows.
  - Event-driven automation with Lambda and webhooks.
- **Practical**:
  - Build a serverless pipeline with CodePipeline and CodeBuild for the To-Do app.
  - Trigger builds via Lambda on GitHub events.
  - Deploy to EKS and compare with Jenkins efficiency.
- **Tools**: AWS CodePipeline, CodeBuild, Lambda, EKS, GitHub Webhooks, `kubectl`.
- **Engagement**: "Serverless Sprint"—compare build/deploy times with Jenkins.
- **Learning Outcome**: Implement lightweight, cost-effective CI/CD with serverless tools.

---

### Notes on the Plan
- **Jenkins Focus (Days 1-3)**:
  - **Day 1**: Starts with basics (pipeline as code, simple automation), ideal for onboarding to Jenkins.
  - **Day 2**: Scales up with intermediate skills (multi-branch, agents), introducing AWS depth.
  - **Day 3**: Goes advanced with complex architectures (shared libraries, dynamic agents, multi-region), reflecting enterprise needs.
- **Other CI/CD Tech (Days 4-5)**:
  - **Day 4**: Introduces GitOps with ArgoCD, a modern alternative to Jenkins’ push model.
  - **Day 5**: Explores serverless CI/CD with AWS, offering a lightweight contrast.
- **Best Practices**: Emphasizes modularity, security (e.g., Trivy), rollback, and auditability throughout.
- **Engagement**: Fun challenges (Build Blitz, Security Siege) keep it interactive and practical.
- **AWS & VCS Integration**: Ties Jenkins and other tools to GitHub and AWS (EC2, EKS, S3, Fargate) for real-world relevance.
