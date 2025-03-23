**Week 2, Day 1: CI/CD Fundamentals - "Pipeline Escape Room"**, with **AWS theory**, **DevOps theoretical knowledge**, and **key terms** related to DevOps and Version Control Systems (VCS). 

I’ll emphasize the importance of initial setup with **AWS CLI** and **basic Git commands**, focusing on today’s goal from a DevOps Engineer’s perspective. 

I tried to cover comprehensive theory, practical implementation steps, and AWS documentation references (Like, [AWS CodePipeline User Guide](https://docs.aws.amazon.com/codepipeline/latest/userguide/)).

---

### Week 2, Day 1: CI/CD Fundamentals - "Pipeline Escape Room"

#### Objective
Master **Continuous Integration (CI)** and **Continuous Deployment (CD)** by building an **AWS CodePipeline** to deploy a static website to **Amazon S3**, integrating **AWS CodeCommit** as a VCS, and debugging a complex pipeline under simulated real-world pressure. This elevates Week 1’s basics to intermediate-to-advanced DevOps practices.

#### Duration
5-6 hours

#### Tools
- AWS Management Console, AWS CLI, Git, Bash, Text Editor (e.g., nano).

#### Goal as a DevOps Engineer
- **Practical Implementation**: Automate a static website deployment pipeline across multiple stages (source, build, deploy), integrating VCS, security, monitoring, and resilience features to reflect a production-grade CI/CD workflow.
- **Focus**: Establish a secure, observable, and scalable CI/CD pipeline, embodying DevOps principles like automation, collaboration, continuous delivery, and operational excellence, while leveraging AWS services for enterprise-ready deployment.

---

##### 1. Theory: CI/CD Fundamentals, DevOps, and VCS (1 hour)
- **Goal**: Provide a comprehensive foundation for CI/CD, DevOps principles, and VCS integration within AWS, with detailed sub-activities akin to Week 1, Day 1.
- **Materials**: Slides/video, AWS docs (e.g., [AWS CodePipeline Concepts](https://docs.aws.amazon.com/codepipeline/latest/userguide/concepts.html), [AWS DevOps Principles](https://aws.amazon.com/devops/), [AWS Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/latest/framework/)).
- **Key Concepts & Keywords**:
  - **AWS Theory**:
    - **Continuous Integration (CI)**: Automate code integration and testing with **AWS CodeBuild**, ensuring rapid feedback ([CodeBuild Concepts](https://docs.aws.amazon.com/codebuild/latest/userguide/concepts.html)).
    - **Continuous Deployment (CD)**: Automate deployment to production-like environments via **AWS CodePipeline**, enabling fast releases ([CodePipeline Concepts](https://docs.aws.amazon.com/codepipeline/latest/userguide/concepts.html)).
    - **Pipeline**: Workflow of stages (Source, Build, Deploy) orchestrated by **CodePipeline**, with **Amazon S3** as an artifact store.
    - **Artifact Store**: Secure storage for build outputs using **S3**, encrypted with **AWS KMS** ([CodePipeline Artifacts](https://docs.aws.amazon.com/codepipeline/latest/userguide/artifacts.html)).
    - **Stage Transitions**: Automated or manual progression between stages, monitored by **Amazon CloudWatch Events**.
    - **Build Automation**: **CodeBuild** compiles and tests code, logging to **CloudWatch Logs** for observability.
    - **Deployment Targets**: **S3** for static sites, extensible to **AWS CodeDeploy** for EC2/Lambda.
    - **AWS Shared Responsibility Model**: AWS secures pipeline infrastructure; you manage IAM, KMS, and code security.
  - **DevOps Theoretical Knowledge**:
    - **DevOps**: Methodology uniting development and operations for rapid, reliable delivery through automation and collaboration.
    - **Key DevOps Concepts**:
      - **Automation**: Minimize manual intervention (e.g., pipeline triggers).
      - **Collaboration**: VCS enables team code sharing and review.
      - **Continuous Delivery**: Every commit is deployable, extending CI/CD.
      - **Pipeline as Code**: Define workflows in `buildspec.yml`, aligning with IaC principles.
      - **Observability**: Monitor pipeline health with **CloudWatch Metrics**, **AWS X-Ray** for tracing.
      - **Shift Left**: Integrate testing/security early (e.g., CodeBuild linting).
      - **Blue-Green Deployment**: Zero-downtime releases (future CodeDeploy context).
      - **Pipeline Maturity**: Evolve from basic builds to multi-stage, multi-environment pipelines.
    - **Version Control System (VCS)**:
      - **Definition**: Tracks code revisions (e.g., **CodeCommit**, Git).
      - **Key VCS Terms**:
        - **Repository**: Code store (e.g., `my-site`).
        - **Commit**: Code snapshot (`git commit -m "Add feature"`).
        - **Branch**: Parallel development (`git branch feature`).
        - **Merge**: Integrate changes (`git merge`).
        - **Pull Request**: Code review process in CodeCommit.
        - **Tag**: Mark release points (`git tag v1.0`).
      - **Importance**: VCS drives CI/CD by triggering pipelines on commits, ensuring versioned, auditable code.
  - **AWS Keywords**: Amazon S3, AWS CodePipeline, AWS CodeBuild, AWS CodeCommit, AWS IAM, Amazon CloudWatch, AWS KMS, AWS CloudFormation, Amazon CloudWatch Events, Elastic Load Balancing, AWS CLI, AWS CodeDeploy, Amazon CodeStar, AWS X-Ray, AWS Systems Manager (SSM), Amazon Route 53, AWS Trusted Advisor, AWS Artifact, Continuous Delivery, Operational Excellence, AWS Shared Responsibility Model, Scalability, Reliability, Security Best Practices.

- **Sub-Activities**:
  1. **CI/CD Core Concepts (15 min)**:
     - **Concept**: CI automates code testing; CD deploys it seamlessly.
     - **Keywords**: Continuous Integration, Continuous Deployment, Pipeline.
     - **Details**: CI reduces integration bugs (CodeBuild); CD speeds releases (CodePipeline).
     - **Action**: Open Console > CodePipeline > “What is CodePipeline?”.
     - **Why**: Foundational to DevOps rapid delivery.
  2. **DevOps Principles in CI/CD (15 min)**:
     - **Concept**: Automation, collaboration, and observability drive CI/CD success.
     - **Keywords**: Automation, Collaboration, Observability, Shift Left.
     - **Details**: Automation cuts toil (pipeline triggers); observability tracks health (CloudWatch); shift left catches issues pre-deploy.
     - **Action**: Read [AWS DevOps Overview](https://aws.amazon.com/devops/what-is-devops/).
     - **Why**: Aligns dev and ops, a DevOps core tenet.
  3. **VCS Role in CI/CD (10 min)**:
     - **Concept**: VCS (CodeCommit) integrates code changes into pipelines.
     - **Keywords**: Repository, Commit, Branch, Merge, Pull Request.
     - **Details**: Commits trigger CodePipeline; branches enable parallel dev.
     - **Action**: Explore CodeCommit in Console.
     - **Why**: VCS is the CI/CD entry point, enabling collaboration.
  4. **AWS Security and Monitoring (10 min)**:
     - **Concept**: Secure pipelines with IAM, KMS; monitor with CloudWatch, X-Ray.
     - **Keywords**: AWS IAM, AWS KMS, Amazon CloudWatch, AWS X-Ray.
     - **Details**: IAM restricts access; KMS encrypts artifacts; X-Ray traces execution.
     - **Action**: Check IAM > Policies in Console.
     - **Why**: Security and observability are DevOps must-haves.
  5. **Pipeline Ecosystem (10 min)**:
     - **Concept**: Broaden CI/CD with CodeDeploy, CodeStar, SSM.
     - **Keywords**: AWS CodeDeploy, Amazon CodeStar, AWS Systems Manager.
     - **Details**: CodeDeploy extends to EC2; CodeStar unifies tools; SSM manages configs.
     - **Action**: View CodeStar in Console.
     - **Why**: Shows CI/CD’s role in AWS ecosystem.
  6. **Self-Check (5 min)**:
     - **Question**: “How does CodePipeline enforce operational excellence?”
     - **Answer**: “It automates stages, reduces errors, and logs via CloudWatch.”

##### 2. Lab: Build a CI/CD Pipeline (2.5-3 hours)
- **Goal**: Automate a static website deployment pipeline with VCS, build, and deploy stages, integrating security, monitoring, and IaC elements.

###### Initial Setup with AWS CLI and Git
- **Why AWS CLI**: Provides programmatic control, enabling automation and repeatability ([AWS CLI Setup](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html)).
- **Why Git**: Core VCS tool for CodeCommit, driving CI/CD triggers and collaboration.

- **Setup Steps**:
  1. **Install AWS CLI**:
     - **Command**: `curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"; unzip awscliv2.zip; sudo ./aws/install`
     - **Why**: Ensures CLI availability.
     - **Verify**: `aws --version`.
  2. **Configure AWS CLI**:
     - **Command**: `aws configure`
     - **Details**: Input Access Key ID, Secret Key, region (`us-east-1`), format (`json`).
     - **Why**: Authenticates CLI for AWS operations.
     - **Verify**: `aws sts get-caller-identity`.
  3. **Install Git**:
     - **Command**: `sudo yum install git -y`
     - **Why**: Enables CodeCommit interaction.
     - **Verify**: `git --version`.
  4. **Configure Git for CodeCommit**:
     - **Commands**: 
       ```bash
       git config --global credential.helper '!aws codecommit credential-helper $@'
       git config --global credential.UseHttpPath true
       git config --global user.name "Your Name"
       git config --global user.email "your@email.com"
       ```
     - **Why**: Links Git to CodeCommit via IAM, sets commit identity.

###### Practical Implementation
- **Task 1: Create a CodeCommit Repository**:
  - **Command**: `aws codecommit create-repository --repository-name my-site --region us-east-1 --tags Key=Project,Value=PipelineDemo`
  - **Details**: Creates a VCS repo, tagged for cost tracking.
  - **Why**: Centralizes code, triggers pipeline on commits.

- **Task 2: Push Initial Code**:
  - **Commands**:
    ```bash
    git clone https://git-codecommit.us-east-1.amazonaws.com/v1/repos/my-site
    cd my-site
    echo "<h1>CI/CD Pipeline Demo</h1><p>Deployed with AWS</p>" > index.html
    echo "version: 0.2
    phases:
      pre_build:
        commands:
          - echo 'Starting build...' > build.log
      build:
        commands:
          - echo 'Validating HTML...' >> build.log
          - cat index.html >> build.log
      post_build:
        commands:
          - echo 'Build complete' >> build.log
    artifacts:
      files:
        - index.html
        - build.log" > buildspec.yml
    git add .
    git commit -m "Initial site commit"
    git push origin master
    ```
  - **Details**: `buildspec.yml` defines CI steps (pre-build, build, post-build).
  - **Why**: Commit initiates CI/CD, a DevOps automation cornerstone.

- **Task 3: Set Up IAM Roles and Policies**:
  - **Commands**:
    ```bash
    aws iam create-role --role-name CodeBuildRole --assume-role-policy-document '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"Service":"codebuild.amazonaws.com"},"Action":"sts:AssumeRole"}]}'
    aws iam put-role-policy --role-name CodeBuildRole --policy-name BuildPolicy --policy-document '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Action":["s3:PutObject","s3:GetObject","logs:CreateLogGroup","logs:CreateLogStream","logs:PutLogEvents"],"Resource":"*"}]}'
    aws iam create-role --role-name CodePipelineRole --assume-role-policy-document '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"Service":"codepipeline.amazonaws.com"},"Action":"sts:AssumeRole"}]}'
    aws iam put-role-policy --role-name CodePipelineRole --policy-name PipelinePolicy --policy-document '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Action":["s3:*","codebuild:*","codecommit:*","cloudwatch:*"],"Resource":"*"}]}'
    ```
  - **Details**: Custom policies grant specific permissions to S3, CodeBuild, CloudWatch.
  - **Why**: Enforces least privilege, a DevOps security best practice.

- **Task 4: Configure S3 Bucket**:
  - **Commands**: 
    ```bash
    BUCKET_NAME="my-site-bucket-$(date +%s)"
    aws s3 mb s3://$BUCKET_NAME --region us-east-1
    aws s3 website s3://$BUCKET_NAME --index-document index.html
    aws s3api put-bucket-policy --bucket $BUCKET_NAME --policy '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":"*","Action":"s3:GetObject","Resource":"arn:aws:s3:::'$BUCKET_NAME'/*"}]}'
    ```
  - **Details**: Unique bucket name, static hosting, public access.
  - **Why**: S3 provides scalable, cost-effective hosting.

- **Task 5: Create CodeBuild Project**:
  - **Command**: 
    ```bash
    aws codebuild create-project --name my-build \
      --source '{"type":"CODECOMMIT","location":"https://git-codecommit.us-east-1.amazonaws.com/v1/repos/my-site"}' \
      --artifacts '{"type":"S3","location":"'$BUCKET_NAME'"}' \
      --environment '{"type":"LINUX_CONTAINER","image":"aws/codebuild/standard:5.0","computeType":"BUILD_GENERAL1_SMALL"}' \
      --service-role arn:aws:iam::$(aws sts get-caller-identity --query Account --output text):role/CodeBuildRole \
      --logs-config '{"cloudWatchLogs":{"status":"ENABLED","groupName":"my-build-logs","streamName":"build"}}'
    ```
  - **Details**: Builds artifacts, logs to CloudWatch for observability.
  - **Why**: CI validates code quality, a DevOps gate.

- **Task 6: Set Up CodePipeline with CloudFormation Option**:
  - **Command**: 
    ```bash
    nano pipeline.json
    ```
    - **Content**:
      ```json
      {
        "pipeline": {
          "name": "my-pipeline",
          "roleArn": "arn:aws:iam::$(aws sts get-caller-identity --query Account --output text):role/CodePipelineRole",
          "artifactStore": {"type": "S3", "location": "'$BUCKET_NAME'"},
          "stages": [
            {"name": "Source", "actions": [{"name": "Source", "actionTypeId": {"category": "Source", "owner": "AWS", "provider": "CodeCommit", "version": "1"}, "outputArtifacts": [{"name": "SourceOutput"}], "configuration": {"BranchName": "master", "RepositoryName": "my-site"}}]},
            {"name": "Build", "actions": [{"name": "Build", "actionTypeId": {"category": "Build", "owner": "AWS", "provider": "CodeBuild", "version": "1"}, "inputArtifacts": [{"name": "SourceOutput"}], "outputArtifacts": [{"name": "BuildOutput"}], "configuration": {"ProjectName": "my-build"}}]},
            {"name": "Deploy", "actions": [{"name": "Deploy", "actionTypeId": {"category": "Deploy", "owner": "AWS", "provider": "S3", "version": "1"}, "inputArtifacts": [{"name": "BuildOutput"}], "configuration": {"BucketName": "'$BUCKET_NAME'", "Extract": "true"}}]}
          ]
        }
      }
      ```
    - **Run**: `aws codepipeline create-pipeline --cli-input-json file://pipeline.json`
  - **Details**: Automates stages, could use CloudFormation for IaC.
  - **Why**: CD ensures rapid, reliable deployment.

- **Outcome**: Site live at `http://$BUCKET_NAME.s3-website-us-east-1.amazonaws.com`.

##### 3. Chaos Twist: "Escape Room Challenge" (1-1.5 hours)
- **Goal**: Debug a broken pipeline under pressure, reinforcing DevOps troubleshooting skills.
- **Scenario**: Instructor injects failures (e.g., IAM policy denies S3, KMS key missing, CloudWatch log group deleted).
- **Task**:
  - Check status: `aws codepipeline get-pipeline-state --name my-pipeline`.
  - View logs: `aws logs tail /aws/codebuild/my-build-logs`.
  - Fix IAM: `aws iam put-role-policy --role-name CodeBuildRole --policy-name S3Access --policy-document '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Action":"s3:*","Resource":"arn:aws:s3:::my-site-bucket-$(date +%s)/*"}]}'`.
  - **Why**: Simulates real-world pipeline issues, testing observability and resilience.
- **AWS Keywords**: Troubleshooting, IAM Policies, CloudWatch Logs, AWS CLI, Operational Excellence, Continuous Improvement.
- **Outcome**: Pipeline restored, site deployed.

##### 4. Wrap-Up: War Room Debrief (30-45 min)
- **Goal**: Reflect and solidify CI/CD and DevOps learnings.
- **Activities**:
  - Demo: Visit `http://<s3-bucket-endpoint>`.
  - Discuss: Share chaos fixes (e.g., IAM, logs).
  - Plan: Prep for serverless (Day 2).
- **AWS Keywords**: AWS Shared Responsibility Model, Cost Efficiency, Continuous Delivery, Automation Benefits.

---

#### Key Outcomes
- **Theory**: Deep understanding of CI/CD, DevOps principles (automation, observability), and VCS role.
- **Practical**: Built a secure, monitored CI/CD pipeline with CodePipeline, CodeBuild, and S3, using AWS CLI and Git.

#### AWS Keywords Covered
- **Amazon S3**: Static hosting, artifact store.
- **AWS CodePipeline**: Pipeline orchestration.
- **AWS CodeBuild**: CI automation.
- **AWS CodeCommit**: VCS integration.
- **AWS IAM**: Security roles/policies.
- **Amazon CloudWatch**: Logs, events, metrics.
- **AWS KMS**: Encryption (potential artifact security).
- **AWS CloudFormation**: IaC option.
- **Amazon CloudWatch Events**: Stage triggers.
- **Elastic Load Balancing**: Scalability context.
- **AWS CLI**: Automation tool.
- **Continuous Delivery**: Deployment readiness.
- **Operational Excellence**: Pipeline efficiency.
- **AWS Shared Responsibility Model**: Security split.
- **AWS Artifact**: Build outputs.
- **AWS Trusted Advisor**: Best practice checks.

---

##### 4. Wrap-Up: War Room Debrief (30-45 min)
- **Goal**: Reflect on CI/CD and DevOps learnings.
- **Activities**: Demo site, discuss chaos fixes, prep for Day 2.
- **AWS Keywords**: AWS Shared Responsibility Model, Cost Efficiency, Continuous Delivery, Scalability.

---

### Top 5 Real-World CI/CD Pipeline Implementation Ideas with GitHub for Fortune 100 Companies on AWS

**five real-world, complex CI/CD pipeline ideas** tailored for Fortune 100 companies (e.g., Amazon, Microsoft, Google), using **GitHub** instead of CodeCommit, based on AWS DevOps scenarios. These reflect practices seen in large-scale enterprises, inspired by AWS documentation (e.g., [AWS CodePipeline User Guide](https://docs.aws.amazon.com/codepipeline/latest/userguide/)) and industry trends (e.g., microservices, multi-region deployments). No implementation steps yet—just high-level ideas:

1. **Multi-Region Microservices Deployment for E-Commerce (e.g., Amazon)**:
   - **What**: A CI/CD pipeline deploys a microservices-based e-commerce platform (e.g., product catalog, checkout) across multiple AWS regions (us-east-1, eu-west-1) using **AWS CodePipeline**, **AWS CodeBuild**, and **Amazon ECS Fargate**.
   - **How**: GitHub triggers pipelines on pull requests; CodeBuild runs tests (unit, integration), builds Docker images, and pushes to **Amazon ECR**. CodePipeline deploys to ECS clusters behind **Application Load Balancers (ALBs)** with **Amazon Route 53** for geo-routing.
   - **Key Features**: Multi-stage pipeline (test, staging, prod), canary deployments via **AWS CodeDeploy**, **Amazon CloudWatch** for monitoring, **AWS WAF** for security.

2. **Global Content Delivery for Media Streaming (e.g., Netflix)**:
   - **What**: Pipeline deploys a media streaming app’s static assets (e.g., UI) to **Amazon S3** and APIs to **AWS Lambda**, integrated with **Amazon CloudFront** for global CDN.
   - **How**: GitHub Actions initiates CodePipeline; CodeBuild lints/tests frontend (React) and backend (Node.js), packages artifacts. Pipeline stages deploy to S3 (static) and Lambda (API), with **CloudFront** caching and **AWS X-Ray** tracing.
   - **Key Features**: Multi-environment (dev, prod), **AWS KMS** encryption, **Amazon Route 53** latency-based routing, **CloudWatch Alarms** for latency spikes.

3. **Enterprise-Scale Financial App with Compliance (e.g., JPMorgan Chase)**:
   - **What**: CI/CD pipeline deploys a financial app to **Amazon EKS**, ensuring compliance with audits and encryption.
   - **How**: GitHub PRs trigger CodePipeline; CodeBuild runs security scans (e.g., Trivy), builds Helm charts, pushes to **ECR**. Pipeline deploys to EKS with **AWS Load Balancer Controller**, uses **Amazon RDS** for data, audited by **AWS CloudTrail**.
   - **Key Features**: Blue-green deployment via **CodeDeploy**, **AWS Secrets Manager** for credentials, **AWS WAF** for protection, **CloudWatch Container Insights** for observability.

4. **AI/ML Model Deployment for Healthcare (e.g., UnitedHealth Group)**:
   - **What**: Pipeline deploys an AI/ML model (e.g., patient diagnosis) to **AWS SageMaker**, integrated with a web app on **Amazon EC2**.
   - **How**: GitHub commits trigger CodePipeline; CodeBuild trains/tests models, builds web app Docker images. Pipeline deploys models to SageMaker endpoints and app to EC2 via **CodeDeploy**, with **Amazon Route 53** DNS.
   - **Key Features**: Multi-stage (train, test, deploy), **AWS Step Functions** for orchestration, **Amazon CloudWatch** for model metrics, **AWS KMS** for data encryption.

5. **Global Supply Chain Management (e.g., Walmart)**:
   - **What**: Pipeline deploys a supply chain app with microservices on **AWS ECS** and a frontend on **Amazon S3**, optimized for multi-region resilience.
   - **How**: GitHub Actions kicks off CodePipeline; CodeBuild tests/builds microservices (Node.js) and frontend (React), pushes to **ECR**. Pipeline deploys to ECS with **ALB**, frontend to S3 with **CloudFront**, uses **Amazon Aurora** for DB.
   - **Key Features**: Multi-region failover with **Route 53**, **AWS Auto Scaling** for ECS, **AWS WAF** for security, **CloudWatch Logs** for real-time tracking.

---
