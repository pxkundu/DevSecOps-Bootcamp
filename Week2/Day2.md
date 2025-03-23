**Week 2, Day 2: Serverless with AWS Lambda - "Serverless Heist"**, building on the intermediate-to-advanced momentum from Day 1. This day will be **extensive and informative**, blending deep **AWS theory**, **DevOps theoretical knowledge**, and **practical use cases** with detailed keyword explanations rooted in AWS documentation (e.g., [AWS Lambda Developer Guide](https://docs.aws.amazon.com/lambda/latest/dg/), [AWS Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/latest/framework/)). 

The focus is on serverless architecture, event-driven design, and production-ready implementations, maintaining the out-of-the-box "Serverless Heist" twist for an engaging learning experience. 

This will match the depth of Day 1, with comprehensive sub-activities, practical steps, and real-world relevance.

---

### Week 2, Day 2: Serverless with AWS Lambda - "Serverless Heist"

#### Objective
Master **serverless computing** by designing and securing an event-driven architecture with **AWS Lambda**, deploying a CRUD API integrated with **Amazon API Gateway**, **Amazon DynamoDB**, and **Amazon SNS**, and surviving a simulated "heist" challenge to exploit and fix security flaws.

#### Duration
5-6 hours

#### Tools
- AWS Management Console, AWS CLI, Python (or Node.js), Git, Bash, Text Editor (e.g., VS Code).

#### Goal as a DevOps Engineer
- **Practical Implementation**: Automate the deployment of a serverless CRUD API, ensuring scalability, security, and observability, with event-driven triggers and production-grade configurations.
- **Focus**: Build a resilient, cost-efficient serverless application, embodying AWS and DevOps best practices like automation, shift-left security, and operational excellence.

---

### Content Breakdown

#### 1. Theory: Serverless Fundamentals, DevOps, and AWS Ecosystem (1 hour)
- **Goal**: Provide a comprehensive theoretical foundation for serverless computing, event-driven design, and DevOps principles within AWS, with detailed keyword explanations and sub-activities akin to Week 1, Day 1’s depth.
- **Materials**: Slides/video, AWS docs (e.g., [AWS Lambda Concepts](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html), [AWS DevOps Principles](https://aws.amazon.com/devops/), [Event-Driven Architecture](https://aws.amazon.com/event-driven-architecture/)).
- **Key Concepts & Keywords**:
  - **AWS Theory**:
    - **Serverless Computing**: Execute code without managing servers using **AWS Lambda**, with auto-scaling and pay-per-use billing ([Lambda How It Works](https://docs.aws.amazon.com/lambda/latest/dg/lambda-introduction.html)).
      - **Explanation**: Lambda abstracts infrastructure, running functions in response to events (e.g., HTTP requests).
    - **Event-Driven Architecture**: Trigger actions via events with **Amazon EventBridge**, **Amazon SQS**, or **Amazon SNS** ([EventBridge Concepts](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-what-is.html)).
      - **Explanation**: Decouples services, enabling asynchronous processing (e.g., SNS notifies on API calls).
    - **Scalability**: Lambda scales automatically per request, up to account limits ([Lambda Scaling](https://docs.aws.amazon.com/lambda/latest/dg/scaling.html)).
      - **Explanation**: Handles thousands of concurrent executions without manual intervention.
    - **Cost Efficiency**: Pay only for compute time (e.g., $0.20/million invocations), tracked by **Amazon CloudWatch Metrics**.
      - **Explanation**: No idle costs, ideal for variable workloads.
    - **Stateless Design**: Lambda functions are ephemeral; store state in **Amazon DynamoDB** ([DynamoDB Concepts](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.html)).
      - **Explanation**: No persistent memory between invocations, ensuring scalability.
    - **RESTful API**: Expose Lambda via **Amazon API Gateway** for HTTP endpoints ([API Gateway How It Works](https://docs.aws.amazon.com/apigateway/latest/developerguide/how-it-works.html)).
      - **Explanation**: Provides a secure, scalable API layer.
    - **AWS Shared Responsibility Model**: AWS manages Lambda runtime; you secure code, IAM, and data ([AWS Security Overview](https://docs.aws.amazon.com/whitepapers/latest/aws-overview/security.html)).
      - **Explanation**: Shared duty ensures robust security.
  - **DevOps Theoretical Knowledge**:
    - **DevOps**: Methodology uniting development and operations for rapid, reliable delivery through automation and collaboration.
    - **Key DevOps Concepts**:
      - **Automation**: Serverless reduces ops tasks (e.g., Lambda triggers).
      - **Collaboration**: Share code via Git for team alignment.
      - **Continuous Delivery**: Deploy serverless updates instantly.
      - **Observability**: Monitor with **CloudWatch Logs**, trace with **AWS X-Ray**, and audit with **AWS CloudTrail**.
      - **Shift Left**: Secure early with **AWS IAM** and **AWS KMS**.
      - **Infrastructure as Code (IaC)**: Define resources with **AWS CloudFormation**.
      - **Microservices**: Serverless enables modular, independent functions.
    - **Serverless DevOps**: Focus shifts from server management to code optimization and event orchestration.
  - **AWS Keywords**: AWS Lambda, Amazon API Gateway, Amazon DynamoDB, Amazon SNS, AWS Step Functions, Amazon CloudWatch, AWS X-Ray, AWS IAM, Amazon SQS, AWS KMS, AWS CloudTrail, Amazon EventBridge, AWS CloudFormation, Amazon S3, AWS Trusted Advisor, Operational Excellence, Cost Optimization, Security Best Practices, Scalability, Reliability, Stateless Architecture, Performance Efficiency, Continuous Delivery, AWS Shared Responsibility Model.

- **Sub-Activities**:
  1. **Serverless Computing Overview (15 min)**:
     - **Concept**: Lambda executes code without server provisioning.
     - **Keywords**: Serverless Computing, Scalability, Cost Efficiency.
     - **Details**: Pay-per-invocation (e.g., 100ms increments), scales from 0 to thousands in seconds.
     - **Action**: Open Console > Lambda > “What is AWS Lambda?”.
     - **Use Case**: Netflix uses Lambda for backend processing (e.g., encoding triggers).
     - **Why**: Reduces ops overhead, a DevOps win.
  2. **Event-Driven Architecture Basics (10 min)**:
     - **Concept**: Events trigger Lambda via EventBridge, SQS, SNS.
     - **Keywords**: Event-Driven Architecture, Amazon EventBridge, Amazon SNS.
     - **Details**: EventBridge schedules tasks (e.g., cron jobs); SNS pushes notifications.
     - **Action**: Explore EventBridge in Console.
     - **Use Case**: Notify users of new content availability (Netflix-like feature).
     - **Why**: Decouples services, enhancing resilience.
  3. **Stateless Design and Data Storage (10 min)**:
     - **Concept**: Lambda is stateless; DynamoDB persists data.
     - **Keywords**: Stateless Design, Amazon DynamoDB.
     - **Details**: DynamoDB offers NoSQL scalability (e.g., 10K writes/sec).
     - **Action**: Check DynamoDB > Tables in Console.
     - **Use Case**: Store user watch histories (Netflix-style).
     - **Why**: Ensures scalability in serverless apps.
  4. **API Exposure with API Gateway (10 min)**:
     - **Concept**: API Gateway exposes Lambda as RESTful endpoints.
     - **Keywords**: Amazon API Gateway, RESTful API.
     - **Details**: Supports HTTP methods (GET, POST), scales with traffic.
     - **Action**: View API Gateway in Console.
     - **Use Case**: Stream metadata API (e.g., movie details).
     - **Why**: Provides a secure API layer.
  5. **Security and Observability in Serverless (10 min)**:
     - **Concept**: Secure with IAM, KMS; monitor with CloudWatch, X-Ray.
     - **Keywords**: AWS IAM, AWS KMS, Amazon CloudWatch, AWS X-Ray.
     - **Details**: IAM restricts Lambda; KMS encrypts data; X-Ray traces requests.
     - **Action**: Explore IAM > Policies in Console.
     - **Use Case**: Secure user data, trace API latency (Netflix priority).
     - **Why**: DevOps demands security and visibility.
  6. **Self-Check (5 min)**:
     - **Question**: “How does statelessness benefit a streaming app?”
     - **Answer**: “It allows Lambda to scale independently, storing state in DynamoDB for persistence.”

---

#### 2. Lab: Build a Serverless CRUD API (2.5-3 hours)
- **Goal**: Deploy a production-ready serverless CRUD API with Lambda, API Gateway, DynamoDB, and SNS, automating setup with AWS CLI and CloudFormation.

##### Initial Setup with AWS CLI and Git
- **Why AWS CLI**: Automates resource creation for repeatability ([AWS CLI Setup](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html)).
- **Why Git**: Manages code versioning, enabling collaboration and pipeline integration.

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
  4. **Install Python**:
     ```bash
     sudo yum install python3 -y
     python3 --version  # Verify: Python 3.x.x
     pip3 install boto3  # AWS SDK for Python
     ```
  5. **Set Up Project**:
     ```bash
     mkdir serverless-streaming
     cd serverless-streaming
     git init
     echo "*.zip
     venv/" > .gitignore
     ```

##### Practical Implementation
- **Task 1: Create DynamoDB Table**:
  - **Command**: 
    ```bash
    aws dynamodb create-table --table-name StreamItems \
      --attribute-definitions AttributeName=id,AttributeType=S \
      --key-schema AttributeName=id,KeyType=HASH \
      --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 \
      --region us-east-1
    ```
  - **Details**: Creates a table with `id` as the primary key.
  - **Why**: Stores streaming metadata (e.g., movie IDs), a Netflix-like feature.
  - **Best Practice**: Use **On-Demand Capacity** in production for auto-scaling.

- **Task 2: Write Lambda Function**:
  - **Commands**: 
    ```bash
    nano lambda_function.py
    ```
    - **Content** (`lambda_function.py` - Production-Ready):
      ```python
      import json
      import boto3
      from uuid import uuid4
      from datetime import datetime

      dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
      sns = boto3.client('sns', region_name='us-east-1')
      table = dynamodb.Table('StreamItems')
      topic_arn = 'arn:aws:sns:us-east-1:<account-id>:StreamUpdates'

      def lambda_handler(event, context):
        try:
          http_method = event.get('httpMethod', '')
          if http_method == 'POST':
            body = json.loads(event.get('body', '{}'))
            item = {
              'id': str(uuid4()),
              'title': body.get('title', 'Untitled'),
              'timestamp': datetime.utcnow().isoformat()
            }
            table.put_item(Item=item)
            sns.publish(TopicArn=topic_arn, Message=f"Added: {item['title']}")
            return {
              'statusCode': 201,
              'headers': {'Content-Type': 'application/json'},
              'body': json.dumps(item)
            }
          elif http_method == 'GET':
            response = table.scan()
            return {
              'statusCode': 200,
              'headers': {'Content-Type': 'application/json'},
              'body': json.dumps(response['Items'])
            }
          else:
            return {
              'statusCode': 400,
              'body': json.dumps({'error': 'Method not supported'})
            }
        except Exception as e:
          print(f"Error: {str(e)}")
          return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal server error'})
          }
      ```
    - **Details**: CRUD API (POST creates items, GET lists them), notifies via SNS with error handling.
    - **Why**: Optimized for production with logging, headers, and robust error management.
    - **Best Practice**: Use environment variables for `topic_arn` in production (via SSM or Lambda env vars).

- **Task 3: Package and Deploy Lambda**:
  - **Commands**: 
    ```bash
    zip function.zip lambda_function.py
    aws lambda create-function --function-name StreamAPI \
      --runtime python3.9 \
      --handler lambda_function.lambda_handler \
      --role arn:aws:iam::<account-id>:role/LambdaRole \
      --zip-file fileb://function.zip \
      --region us-east-1
    ```
  - **Details**: Deploys Lambda with a pre-created IAM role (see Task 6).
  - **Why**: Automates serverless deployment, a DevOps practice.

- **Task 4: Set Up API Gateway**:
  - **Commands**: 
    ```bash
    aws apigateway create-rest-api --name StreamAPI --region us-east-1
    API_ID=$(aws apigateway get-rest-apis --query "items[?name=='StreamAPI'].id" --output text)
    RESOURCE_ID=$(aws apigateway get-resources --rest-api-id $API_ID --query "items[0].id" --output text)
    aws apigateway create-resource --rest-api-id $API_ID --parent-id $RESOURCE_ID --path-part stream --region us-east-1
    ITEM_RESOURCE_ID=$(aws apigateway get-resources --rest-api-id $API_ID --query "items[?pathPart=='stream'].id" --output text)
    aws apigateway put-method --rest-api-id $API_ID --resource-id $ITEM_RESOURCE_ID --http-method POST --authorization-type NONE --region us-east-1
    aws apigateway put-integration --rest-api-id $API_ID --resource-id $ITEM_RESOURCE_ID --http-method POST --type AWS_PROXY --integration-http-method POST --uri arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/arn:aws:lambda:us-east-1:<account-id>:function:StreamAPI/invocations --region us-east-1
    aws apigateway put-method --rest-api-id $API_ID --resource-id $ITEM_RESOURCE_ID --http-method GET --authorization-type NONE --region us-east-1
    aws apigateway put-integration --rest-api-id $API_ID --resource-id $ITEM_RESOURCE_ID --http-method GET --type AWS_PROXY --integration-http-method POST --uri arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/arn:aws:lambda:us-east-1:<account-id>:function:StreamAPI/invocations --region us-east-1
    aws apigateway create-deployment --rest-api-id $API_ID --stage-name prod --region us-east-1
    ```
  - **Details**: Creates a REST API with POST/GET endpoints linked to Lambda.
  - **Why**: Exposes serverless logic via HTTP, a Netflix-like API pattern.
  - **Best Practice**: Add API key or IAM auth in production.

- **Task 5: Create SNS Topic**:
  - **Command**: 
    ```bash
    aws sns create-topic --name StreamUpdates --region us-east-1
    ```
  - **Details**: Topic for event notifications (e.g., new content added).
  - **Why**: Enhances event-driven design, a Netflix feature for real-time updates.

- **Task 6: Secure with IAM and KMS**:
  - **Commands**: 
    ```bash
    aws iam create-role --role-name LambdaRole --assume-role-policy-document '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"Service":"lambda.amazonaws.com"},"Action":"sts:AssumeRole"}]}'
    aws iam put-role-policy --role-name LambdaRole --policy-name LambdaPolicy --policy-document '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Action":["logs:CreateLogGroup","logs:CreateLogStream","logs:PutLogEvents","dynamodb:PutItem","dynamodb:Scan","sns:Publish"],"Resource":"*"}]}'
    aws kms create-key --description "ServerlessKey" --region us-east-1
    KEY_ID=$(aws kms list-keys --query "Keys[0].KeyId" --output text)
    aws kms create-alias --alias-name alias/ServerlessKey --target-key-id $KEY_ID --region us-east-1
    ```
  - **Details**: IAM role grants Lambda access; KMS key encrypts data (optional for SNS in production).
  - **Why**: Enforces security best practices (least privilege, encryption).

##### 3. Chaos Twist: "Serverless Heist" (1-1.5 hours)
- **Goal**: Exploit and secure a serverless app under pressure, simulating real-world DevOps challenges.
- **Scenario**: Instructor deploys a vulnerable API (e.g., no IAM auth, unencrypted SNS); “steal” data, then secure your own.
- **Task**: 
  - Test rival API: `curl -X POST -d '{"title":"Test"}' https://<rival-api-id>.execute-api.us-east-1.amazonaws.com/prod/stream`.
  - Secure yours: Add IAM auth (`aws apigateway update-method ...`), enable KMS for SNS.
- **AWS Keywords**: Troubleshooting, Security Best Practices, AWS IAM, AWS KMS, AWS X-Ray, Scalability, Reliability.
- **Practical Use Case**: Netflix secures APIs to protect user data; this mimics that process.
- **Outcome**: Secure API endpoint, hardened against attacks.

##### 4. Wrap-Up: War Room Debrief (30-45 min)
- **Goal**: Reflect on serverless learnings and prepare for Day 3.
- **Activities**: 
  - Demo API: `curl -X POST -d '{"title":"Movie"}' https://<api-id>.execute-api.us-east-1.amazonaws.com/prod/stream`.
  - Discuss heist fixes (e.g., IAM, KMS).
  - Prep for containers (Day 3).
- **AWS Keywords**: Operational Excellence, Cost Optimization, Continuous Delivery, Performance Efficiency.
- **Practical Use Case**: Lessons apply to Netflix’s serverless encoding triggers or metadata APIs.

---

#### Key Outcomes
- **Theory Learned**: Serverless computing, event-driven design, DevOps principles (automation, observability).
- **Practical Skills**: Built a secure, scalable CRUD API with Lambda, API Gateway, DynamoDB, SNS, using CLI and IaC.

#### AWS Keywords Covered
- **AWS Lambda**: Serverless compute.
- **Amazon API Gateway**: API management.
- **Amazon DynamoDB**: NoSQL storage.
- **Amazon SNS**: Event notifications.
- **AWS Step Functions**: Orchestration (future use).
- **Amazon CloudWatch**: Logs, metrics.
- **AWS X-Ray**: Tracing.
- **AWS IAM**: Access control.
- **Amazon SQS**: Queuing (future use).
- **AWS KMS**: Encryption.
- **AWS CloudTrail**: Auditing.
- **Amazon EventBridge**: Event triggers.
- **AWS CloudFormation**: IaC.
- **Amazon S3**: Artifact storage.
- **AWS Trusted Advisor**: Best practices.
- **Operational Excellence**: Efficiency.
- **Cost Optimization**: Pay-per-use.
- **Security Best Practices**: Hardening.
- **Scalability**: Auto-scaling.
- **Reliability**: Fault tolerance.
- **Stateless Architecture**: Design principle.

---

#### Practical Use Cases
1. **Netflix Metadata API**: Serve movie details via Lambda/API Gateway, store in DynamoDB, notify via SNS.
2. **Real-Time Analytics**: Log streaming events (e.g., user plays) with Lambda, analyze with DynamoDB.
3. **Content Upload Trigger**: Lambda processes uploads from S3, notifies via SNS (Netflix encoding pipeline).

---
