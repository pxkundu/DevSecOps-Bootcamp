### Week 2, Day 3: Containers on AWS ECS - "Container Siege"

#### Objective
Master **container orchestration** by deploying a microservices-based application on **Amazon ECS (Fargate)** with **Amazon ECR**, integrating **Application Load Balancer (ALB)** and **Amazon Route 53** for traffic management, and defending against a simulated "siege" (e.g., traffic spikes, container failures) to ensure resilience and scalability.

#### Duration
5-6 hours

#### Tools
- AWS Management Console, AWS CLI, Docker, Git, Bash, Text Editor (e.g., VS Code).

#### Goal as a DevOps Engineer
- **Practical Implementation**: Automate the deployment of a multi-container app (e.g., frontend and API) on ECS Fargate, leveraging Docker, ECR, and ALB, with production-grade security, scalability, and observability.
- **Focus**: Build a resilient, scalable microservices architecture, embodying AWS and DevOps best practices like automation, continuous deployment, and fault tolerance, tailored for real-world applications.

---

### Content Breakdown

#### 1. Theory: Containerization, Microservices, and AWS ECS Ecosystem (1 hour)
- **Goal**: Establish a comprehensive theoretical foundation for containers, microservices, and ECS, with detailed keyword explanations and real-world context, matching the depth of previous days.
- **Materials**: Slides/video, AWS docs (e.g., [ECS Concepts](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/Welcome.html), [AWS DevOps Principles](https://aws.amazon.com/devops/), [Microservices on AWS](https://aws.amazon.com/microservices/)).
- **Key Concepts & Keywords**:
  - **AWS Theory**:
    - **Containerization**: Package applications with dependencies using **Docker** and deploy via **Amazon ECS** ([ECS Container Basics](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/docker-basics.html)).
      - **Explanation**: Containers ensure consistency across dev, test, and prod environments.
    - **Microservices**: Independent, loosely coupled services managed by **ECS** ([Microservices Architecture](https://aws.amazon.com/microservices/)).
      - **Explanation**: Breaks monolithic apps into scalable, modular components (e.g., Netflix’s API services).
    - **Service Discovery**: Route traffic to services with **Amazon Route 53** and **Application Load Balancer (ALB)** ([Route 53 Concepts](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/Welcome.html)).
      - **Explanation**: DNS and load balancing ensure service availability.
    - **Load Balancing**: Distribute traffic across containers with **ALB** ([ALB How It Works](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/introduction.html)).
      - **Explanation**: Balances load, improves fault tolerance.
    - **Fault Tolerance**: **AWS Auto Scaling** adjusts container count based on demand ([ECS Auto Scaling](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/service-auto-scaling.html)).
      - **Explanation**: Ensures availability during traffic spikes.
    - **Container Registry**: **Amazon ECR** stores Docker images securely ([ECR Concepts](https://docs.aws.amazon.com/AmazonECR/latest/userguide/what-is-ecr.html)).
      - **Explanation**: Centralized image management with encryption.
    - **Serverless Containers**: **Amazon ECS Fargate** runs containers without managing EC2 instances ([Fargate Overview](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/AWS_Fargate.html)).
      - **Explanation**: Simplifies ops, scales per task.
    - **AWS Shared Responsibility Model**: AWS secures ECS infrastructure; you manage container security and configs.
      - **Explanation**: Shared duty ensures robust deployments.
  - **DevOps Theoretical Knowledge**:
    - **DevOps**: Culture of automation, collaboration, and continuous improvement for rapid, reliable delivery.
    - **Key DevOps Concepts**:
      - **Automation**: ECS tasks deploy via pipelines (e.g., CodePipeline).
      - **Collaboration**: Git manages container code across teams.
      - **Continuous Deployment**: Deploy updates seamlessly with ECS.
      - **Observability**: Monitor with **Amazon CloudWatch**, trace with **AWS X-Ray**.
      - **Shift Left**: Test containers early (e.g., Docker builds in CI).
      - **Infrastructure as Code (IaC)**: Define ECS with **AWS CloudFormation**.
      - **Resilience**: Auto-scaling and load balancing ensure uptime.
      - **Microservices Adoption**: Modular design aligns with DevOps agility.
  - **AWS Keywords**: Amazon ECS, Amazon Fargate, Amazon ECR, Application Load Balancer, Amazon Route 53, Amazon CloudWatch, AWS IAM, Amazon VPC, AWS Auto Scaling, AWS KMS, AWS CloudFormation, Amazon EFS, AWS X-Ray, Amazon S3, AWS Trusted Advisor, Operational Excellence, Reliability, Scalability, Performance Efficiency, Security Best Practices, Cost Optimization, Continuous Deployment, AWS Shared Responsibility Model, Microservices Architecture, Container Orchestration.

- **Sub-Activities**:
  1. **Containerization Basics (15 min)**:
     - **Concept**: Docker packages apps; ECS orchestrates them.
     - **Keywords**: Containerization, Docker, Amazon ECS.
     - **Details**: Containers include app, libs, and runtime (e.g., Node.js in a container).
     - **Action**: Open Console > ECS > “What is Amazon ECS?”.
     - **Use Case**: Netflix uses containers for encoding services.
     - **Why**: Ensures portability, a DevOps enabler.
  2. **Microservices Architecture (10 min)**:
     - **Concept**: Break apps into independent services with ECS.
     - **Keywords**: Microservices, Amazon ECS.
     - **Details**: Each service (e.g., UI, API) scales separately.
     - **Action**: Read [Microservices on AWS](https://aws.amazon.com/microservices/).
     - **Use Case**: Netflix’s microservices handle streaming, billing separately.
     - **Why**: Enhances scalability, aligns with DevOps modularity.
  3. **Service Discovery and Load Balancing (10 min)**:
     - **Concept**: Route 53 and ALB direct traffic to ECS services.
     - **Keywords**: Service Discovery, Amazon Route 53, Application Load Balancer.
     - **Details**: Route 53 resolves DNS; ALB balances container load.
     - **Action**: Explore Route 53 in Console.
     - **Use Case**: Netflix routes global users to nearest streaming servers.
     - **Why**: Ensures availability and performance.
  4. **Fault Tolerance and Auto Scaling (10 min)**:
     - **Concept**: Auto Scaling adjusts ECS tasks dynamically.
     - **Keywords**: Fault Tolerance, AWS Auto Scaling.
     - **Details**: Scales based on CPU/memory metrics (e.g., 70% threshold).
     - **Action**: Check ECS > Clusters in Console.
     - **Use Case**: Netflix scales during peak streaming hours (e.g., weekends).
     - **Why**: Maintains reliability, a DevOps priority.
  5. **Security and Observability in Containers (10 min)**:
     - **Concept**: Secure with IAM, KMS; monitor with CloudWatch, X-Ray.
     - **Keywords**: AWS IAM, AWS KMS, Amazon CloudWatch, AWS X-Ray.
     - **Details**: IAM restricts ECS; KMS encrypts EFS; X-Ray traces requests.
     - **Action**: View IAM > Roles in Console.
     - **Use Case**: Netflix secures containerized APIs, monitors latency.
     - **Why**: DevOps demands security and visibility.
  6. **Self-Check (5 min)**:
     - **Question**: “How does Fargate differ from EC2 in ECS?”
     - **Answer**: “Fargate abstracts server management; EC2 requires manual EC2 config.”

---

#### 2. Lab: Deploy a Microservices App on ECS Fargate (2.5-3 hours)
- **Goal**: Deploy a production-ready microservices app (React frontend, Node.js API) on ECS Fargate, automating setup with Docker, ECR, and CloudFormation.

##### Initial Setup with AWS CLI, Docker, and Git
- **Why AWS CLI**: Automates ECS, ECR, and ALB creation for repeatability ([AWS CLI Setup](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html)).
- **Why Docker**: Builds and runs containers, essential for ECS ([Docker Basics](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/docker-basics.html)).
- **Why Git**: Manages microservices code, enabling collaboration.

- **Setup Steps**:
  1. **Install AWS CLI**:
     ```bash
     curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
     unzip awscliv2.zip
     sudo ./aws/install
     aws --version  # Verify: aws-cli/2.x.x
     ```
  2. **Configure AWS CLI**:
     ```bash
     aws configure
     # Access Key ID, Secret Key, us-east-1, json
     aws sts get-caller-identity  # Verify account
     ```
  3. **Install Git**:
     ```bash
     sudo yum install git -y
     git --version  # Verify: git version 2.x.x
     ```
  4. **Install Docker**:
     ```bash
     sudo yum install docker -y
     sudo systemctl start docker
     sudo usermod -aG docker ec2-user  # Avoid sudo for docker commands
     docker --version  # Verify: Docker version 20.x.x
     ```
  5. **Install Node.js**:
     ```bash
     curl -sL https://rpm.nodesource.com/setup_20.x | sudo bash -
     sudo yum install -y nodejs
     node -v  # Verify: v20.x.x
     ```
  6. **Set Up Project**:
     ```bash
     mkdir ecs-streaming
     cd ecs-streaming
     git init
     echo "node_modules/
     *.zip
     build/" > .gitignore
     ```

##### Practical Implementation
- **Folder Structure**:
  ```
  ecs-streaming/
  ├── frontend/                # React frontend
  │   ├── src/
  │   │   ├── App.js          # Main component
  │   │   ├── App.css         # Styling
  │   │   └── index.js        # Entry point
  │   ├── public/
  │   │   └── index.html      # HTML template
  │   ├── Dockerfile          # Docker config
  │   ├── package.json        # Dependencies
  │   └── nginx.conf          # Nginx config
  ├── api/                    # Node.js API
  │   ├── index.js           # API logic
  │   ├── Dockerfile         # Docker config
  │   └── package.json       # Dependencies
  ├── infra/                  # IaC
  │   └── ecs-stack.yml      # CloudFormation template
  └── README.md              # Docs
  ```

- **Task 1: Create Frontend Container (React)**:
  - **Commands**: 
    ```bash
    cd frontend
    npx create-react-app .
    nano src/App.js
    ```
    - **Content** (`src/App.js` - Production-Ready):
      ```javascript
      import React, { useState, useEffect } from 'react';
      import './App.css';

      function App() {
        const [status, setStatus] = useState('Loading...');
        useEffect(() => {
          fetch('http://<alb-dns>/api/status', { method: 'GET' })
            .then(res => res.json())
            .then(data => setStatus(data.message))
            .catch(err => setStatus('Error: ' + err.message));
        }, []);

        return (
          <div className="App">
            <h1>Streaming Frontend</h1>
            <p>Status: {status}</p>
          </div>
        );
      }

      export default App;
      ```
    - **Details**: Fetches API status, displays dynamically.
    - **Why**: Optimized with error handling, minimal dependencies.

  - **Commands (continued)**:
    ```bash
    nano Dockerfile
    ```
    - **Content** (`Dockerfile` - Optimized):
      ```dockerfile
      FROM node:20-alpine AS builder
      WORKDIR /app
      COPY package*.json ./
      RUN npm ci --production
      COPY . .
      RUN npm run build

      FROM nginx:alpine
      COPY --from=builder /app/build /usr/share/nginx/html
      COPY nginx.conf /etc/nginx/conf.d/default.conf
      EXPOSE 80
      CMD ["nginx", "-g", "daemon off;"]
      ```
    - **Details**: Multi-stage build reduces image size, uses Nginx for static serving.
    - **Why**: Production-ready with lightweight base images.

    ```bash
    nano nginx.conf
    ```
    - **Content** (`nginx.conf`):
      ```nginx
      server {
          listen 80;
          server_name localhost;
          location / {
              root /usr/share/nginx/html;
              index index.html;
              try_files $uri $uri/ /index.html;  # SPA routing
          }
      }
      ```
    - **Details**: Configures Nginx for single-page app (SPA) routing.
    - **Why**: Ensures React routing works in production.

  - **Build and Test**:
    ```bash
    docker build -t streaming-frontend .
    docker run -p 80:80 streaming-frontend
    # Test locally: http://localhost
    ```

- **Task 2: Create API Container (Node.js)**:
  - **Commands**: 
    ```bash
    cd ../api
    npm init -y
    npm install express
    nano index.js
    ```
    - **Content** (`index.js` - Production-Ready):
      ```javascript
      const express = require('express');
      const app = express();
      const port = process.env.PORT || 3000;

      app.use(express.json());
      app.get('/api/status', (req, res) => {
        res.status(200).json({ message: 'API is running', timestamp: new Date().toISOString() });
      });

      app.listen(port, () => {
        console.log(`API running on port ${port}`);
      });
      ```
    - **Details**: Simple status API with Express, configurable port.
    - **Why**: Optimized for production with minimal footprint, logging.

  - **Commands (continued)**:
    ```bash
    nano Dockerfile
    ```
    - **Content** (`Dockerfile` - Optimized):
      ```dockerfile
      FROM node:20-alpine
      WORKDIR /app
      COPY package*.json ./
      RUN npm ci --production
      COPY . .
      EXPOSE 3000
      CMD ["node", "index.js"]
      ```
    - **Details**: Lightweight image, production dependencies only.
    - **Why**: Ensures fast startup, small size for ECS.

  - **Build and Test**:
    ```bash
    docker build -t streaming-api .
    docker run -p 3000:3000 streaming-api
    # Test locally: curl http://localhost:3000/api/status
    ```

- **Task 3: Push Images to Amazon ECR**:
  - **Commands**: 
    ```bash
    aws ecr create-repository --repository-name streaming-frontend --region us-east-1
    aws ecr create-repository --repository-name streaming-api --region us-east-1
    aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com
    docker tag streaming-frontend:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/streaming-frontend:latest
    docker tag streaming-api:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/streaming-api:latest
    docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/streaming-frontend:latest
    docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/streaming-api:latest
    ```
  - **Details**: Creates ECR repos, tags/pushes images.
  - **Why**: Centralized, secure image storage, a DevOps best practice.

- **Task 4: Deploy with ECS Fargate and CloudFormation**:
  - **Commands**: 
    ```bash
    cd ../infra
    nano ecs-stack.yml
    ```
    - **Content** (`ecs-stack.yml` - Production-Ready):
      ```yaml
      AWSTemplateFormatVersion: '2010-09-09'
      Resources:
        VPC:
          Type: AWS::EC2::VPC
          Properties:
            CidrBlock: 10.0.0.0/16
            EnableDnsHostnames: true
            EnableDnsSupport: true
        PublicSubnet1:
          Type: AWS::EC2::Subnet
          Properties:
            VpcId: !Ref VPC
            CidrBlock: 10.0.1.0/24
            AvailabilityZone: us-east-1a
        PublicSubnet2:
          Type: AWS::EC2::Subnet
          Properties:
            VpcId: !Ref VPC
            CidrBlock: 10.0.2.0/24
            AvailabilityZone: us-east-1b
        InternetGateway:
          Type: AWS::EC2::InternetGateway
        AttachGateway:
          Type: AWS::EC2::VPCGatewayAttachment
          Properties:
            VpcId: !Ref VPC
            InternetGatewayId: !Ref InternetGateway
        RouteTable:
          Type: AWS::EC2::RouteTable
          Properties:
            VpcId: !Ref VPC
        Route:
          Type: AWS::EC2::Route
          Properties:
            RouteTableId: !Ref RouteTable
            DestinationCidrBlock: 0.0.0.0/0
            GatewayId: !Ref InternetGateway
        SubnetRouteTableAssociation1:
          Type: AWS::EC2::SubnetRouteTableAssociation
          Properties:
            SubnetId: !Ref PublicSubnet1
            RouteTableId: !Ref RouteTable
        SubnetRouteTableAssociation2:
          Type: AWS::EC2::SubnetRouteTableAssociation
          Properties:
            SubnetId: !Ref PublicSubnet2
            RouteTableId: !Ref RouteTable
        ECSCluster:
          Type: AWS::ECS::Cluster
          Properties:
            ClusterName: StreamingCluster
        ECSExecutionRole:
          Type: AWS::IAM::Role
          Properties:
            AssumeRolePolicyDocument:
              Version: '2012-10-17'
              Statement:
                - Effect: Allow
                  Principal:
                    Service: ecs-tasks.amazonaws.com
                  Action: sts:AssumeRole
            ManagedPolicyArns:
              - arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy
        ECSTaskRole:
          Type: AWS::IAM::Role
          Properties:
            AssumeRolePolicyDocument:
              Version: '2012-10-17'
              Statement:
                - Effect: Allow
                  Principal:
                    Service: ecs-tasks.amazonaws.com
                  Action: sts:AssumeRole
            Policies:
              - PolicyName: TaskPolicy
                PolicyDocument:
                  Version: '2012-10-17'
                  Statement:
                    - Effect: Allow
                      Action:
                        - logs:CreateLogGroup
                        - logs:CreateLogStream
                        - logs:PutLogEvents
                      Resource: '*'
        FrontendTaskDefinition:
          Type: AWS::ECS::TaskDefinition
          Properties:
            Family: StreamingFrontend
            ExecutionRoleArn: !GetAtt ECSExecutionRole.Arn
            TaskRoleArn: !GetAtt ECSTaskRole.Arn
            NetworkMode: awsvpc
            RequiresCompatibilities:
              - FARGATE
            Cpu: '256'
            Memory: '512'
            ContainerDefinitions:
              - Name: frontend
                Image: !Sub <account-id>.dkr.ecr.us-east-1.amazonaws.com/streaming-frontend:latest
                PortMappings:
                  - ContainerPort: 80
                LogConfiguration:
                  LogDriver: awslogs
                  Options:
                    awslogs-group: /ecs/StreamingFrontend
                    awslogs-region: us-east-1
                    awslogs-stream-prefix: frontend
        APITaskDefinition:
          Type: AWS::ECS::TaskDefinition
          Properties:
            Family: StreamingAPI
            ExecutionRoleArn: !GetAtt ECSExecutionRole.Arn
            TaskRoleArn: !GetAtt ECSTaskRole.Arn
            NetworkMode: awsvpc
            RequiresCompatibilities:
              - FARGATE
            Cpu: '256'
            Memory: '512'
            ContainerDefinitions:
              - Name: api
                Image: !Sub <account-id>.dkr.ecr.us-east-1.amazonaws.com/streaming-api:latest
                PortMappings:
                  - ContainerPort: 3000
                LogConfiguration:
                  LogDriver: awslogs
                  Options:
                    awslogs-group: /ecs/StreamingAPI
                    awslogs-region: us-east-1
                    awslogs-stream-prefix: api
        ALB:
          Type: AWS::ElasticLoadBalancingV2::LoadBalancer
          Properties:
            Subnets:
              - !Ref PublicSubnet1
              - !Ref PublicSubnet2
            SecurityGroups:
              - !Ref ALBSecurityGroup
        ALBSecurityGroup:
          Type: AWS::EC2::SecurityGroup
          Properties:
            VpcId: !Ref VPC
            GroupDescription: ALB Security Group
            SecurityGroupIngress:
              - IpProtocol: tcp
                FromPort: 80
                ToPort: 80
                CidrIp: 0.0.0.0/0
        TargetGroupFrontend:
          Type: AWS::ElasticLoadBalancingV2::TargetGroup
          Properties:
            VpcId: !Ref VPC
            Port: 80
            Protocol: HTTP
            TargetType: ip
            HealthCheckPath: /
        TargetGroupAPI:
          Type: AWS::ElasticLoadBalancingV2::TargetGroup
          Properties:
            VpcId: !Ref VPC
            Port: 3000
            Protocol: HTTP
            TargetType: ip
            HealthCheckPath: /api/status
        Listener:
          Type: AWS::ElasticLoadBalancingV2::Listener
          Properties:
            LoadBalancerArn: !Ref ALB
            Port: 80
            Protocol: HTTP
            DefaultActions:
              - Type: forward
                TargetGroupArn: !Ref TargetGroupFrontend
        ListenerRuleAPI:
          Type: AWS::ElasticLoadBalancingV2::ListenerRule
          Properties:
            ListenerArn: !Ref Listener
            Priority: 1
            Conditions:
              - Field: path-pattern
                Values: ["/api/*"]
            Actions:
              - Type: forward
                TargetGroupArn: !Ref TargetGroupAPI
        FrontendService:
          Type: AWS::ECS::Service
          Properties:
            Cluster: !Ref ECSCluster
            ServiceName: FrontendService
            TaskDefinition: !Ref FrontendTaskDefinition
            DesiredCount: 2
            LaunchType: FARGATE
            NetworkConfiguration:
              AwsvpcConfiguration:
                Subnets:
                  - !Ref PublicSubnet1
                  - !Ref PublicSubnet2
                SecurityGroups:
                  - !Ref ServiceSecurityGroup
                AssignPublicIp: ENABLED
            LoadBalancers:
              - TargetGroupArn: !Ref TargetGroupFrontend
                ContainerName: frontend
                ContainerPort: 80
        APIService:
          Type: AWS::ECS::Service
          Properties:
            Cluster: !Ref ECSCluster
            ServiceName: APIService
            TaskDefinition: !Ref APITaskDefinition
            DesiredCount: 2
            LaunchType: FARGATE
            NetworkConfiguration:
              AwsvpcConfiguration:
                Subnets:
                  - !Ref PublicSubnet1
                  - !Ref PublicSubnet2
                SecurityGroups:
                  - !Ref ServiceSecurityGroup
                AssignPublicIp: ENABLED
            LoadBalancers:
              - TargetGroupArn: !Ref TargetGroupAPI
                ContainerName: api
                ContainerPort: 3000
        ServiceSecurityGroup:
          Type: AWS::EC2::SecurityGroup
          Properties:
            VpcId: !Ref VPC
            GroupDescription: ECS Service Security Group
            SecurityGroupIngress:
              - IpProtocol: tcp
                FromPort: 80
                ToPort: 80
                SourceSecurityGroupId: !Ref ALBSecurityGroup
              - IpProtocol: tcp
                FromPort: 3000
                ToPort: 3000
                SourceSecurityGroupId: !Ref ALBSecurityGroup
        AutoScalingTarget:
          Type: AWS::ApplicationAutoScaling::Target
          Properties:
            MaxCapacity: 10
            MinCapacity: 2
            ResourceId: !Sub service/${ECSCluster}/${APIService.Name}
            ScalableDimension: ecs:service:DesiredCount
            ServiceNamespace: ecs
        AutoScalingPolicy:
          Type: AWS::ApplicationAutoScaling::ScalingPolicy
          Properties:
            PolicyName: APIScalingPolicy
            PolicyType: TargetTrackingScaling
            ScalingTargetId: !Ref AutoScalingTarget
            TargetTrackingScalingPolicyConfiguration:
              TargetValue: 70.0
              PredefinedMetricSpecification:
                PredefinedMetricType: ECSServiceAverageCPUUtilization
      Outputs:
        ALBDNSName:
          Value: !GetAtt ALB.DNSName
      ```
    - **Details**: Defines VPC, ECS cluster, Fargate tasks, ALB, auto-scaling, and security groups.
    - **Why**: IaC ensures consistency, a DevOps best practice.

  - **Deploy CloudFormation**:
    ```bash
    aws cloudformation create-stack --stack-name ECSStreamingStack \
      --template-body file://ecs-stack.yml \
      --capabilities CAPABILITY_NAMED_IAM \
      --region us-east-1
    aws cloudformation wait stack-create-complete --stack-name ECSStreamingStack
    ALB_DNS=$(aws cloudformation describe-stacks --stack-name ECSStreamingStack --query "Stacks[0].Outputs[?OutputKey=='ALBDNSName'].OutputValue" --output text)
    ```

- **Task 5: Test and Verify**:
  - **Commands**: 
    ```bash
    curl http://$ALB_DNS  # Frontend
    curl http://$ALB_DNS/api/status  # API
    aws logs tail /ecs/StreamingFrontend  # Frontend logs
    aws logs tail /ecs/StreamingAPI  # API logs
    ```
  - **Details**: Verifies frontend and API accessibility via ALB.
  - **Why**: Ensures deployment success, reflects Netflix’s service uptime.

##### 3. Chaos Twist: "Container Siege" (1-1.5 hours)
- **Goal**: Defend against a simulated siege (e.g., traffic spike, container failure), reinforcing DevOps resilience skills.
- **Scenario**: Instructor increases traffic (e.g., via `ab -n 1000 -c 100 http://$ALB_DNS/`) or stops containers (ECS > Stop Task).
- **Task**: 
  - Monitor: `aws cloudwatch get-metric-statistics --namespace AWS/ECS --metric-name CPUUtilization --dimensions Name=ClusterName,Value=StreamingCluster --start-time $(date -u -d "5 minutes ago" +%s) --end-time $(date -u +%s) --period 60 --statistics Average`.
  - Scale: Verify Auto Scaling adjusts (ECS > Services > APIService > Desired Count).
  - Recover: Restart failed tasks if needed (ECS > Tasks > Run New Task).
- **AWS Keywords**: Troubleshooting, Reliability, AWS Auto Scaling, Amazon CloudWatch, Scalability, Operational Excellence.
- **Practical Use Case**: Netflix handles peak streaming loads (e.g., new season drops).
- **Outcome**: App withstands siege, auto-scales, and recovers.

##### 4. Wrap-Up: War Room Debrief (30-45 min)
- **Goal**: Reflect on container learnings and prepare for Day 4.
- **Activities**: 
  - Demo: Visit `http://$ALB_DNS` and `/api/status`.
  - Discuss siege fixes (e.g., scaling, logs).
  - Prep for Kubernetes (Day 4).
- **AWS Keywords**: Operational Excellence, Performance Efficiency, Cost Optimization, Reliability.
- **Practical Use Case**: Lessons apply to Netflix’s containerized streaming APIs.

---

#### Key Outcomes
- **Theory Learned**: Containerization, microservices, fault tolerance, DevOps resilience.
- **Practical Skills**: Deployed a microservices app on ECS Fargate with ALB, Route 53-ready, auto-scaling enabled.

#### AWS Keywords Covered
- **Amazon ECS**: Container orchestration.
- **Amazon Fargate**: Serverless containers.
- **Amazon ECR**: Container registry.
- **Application Load Balancer**: Traffic distribution.
- **Amazon Route 53**: DNS (future use).
- **Amazon CloudWatch**: Monitoring/logs.
- **AWS IAM**: Access control.
- **Amazon VPC**: Network isolation.
- **AWS Auto Scaling**: Dynamic scaling.
- **AWS KMS**: Encryption (future use).
- **AWS CloudFormation**: IaC.
- **Amazon EFS**: Shared storage (future use).
- **AWS X-Ray**: Tracing (future use).
- **Amazon S3**: Artifact storage (future use).
- **AWS Trusted Advisor**: Best practices.
- **Operational Excellence**: Efficiency.
- **Reliability**: Fault tolerance.
- **Scalability**: Auto-scaling.
- **Performance Efficiency**: Optimized resources.
- **Security Best Practices**: Hardening.
- **Cost Optimization**: Fargate efficiency.
- **Continuous Deployment**: Pipeline-ready.

---

#### Practical Use Cases
1. **Netflix Streaming Service**: Deploy UI and API microservices on ECS, scale with viewer demand.
2. **E-Commerce Checkout**: Run frontend and payment API on ECS, balance load with ALB.
3. **Real-Time Analytics**: Process streaming data with ECS containers, store in EFS.

---
