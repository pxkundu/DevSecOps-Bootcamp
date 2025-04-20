#!/bin/bash

# Script to generate new AWS DevOps boilerplate files non-interactively

# Define root directory
ROOT_DIR="aws-devops-boilerplates"

# Check if directory already exists
if [ -d "$ROOT_DIR" ]; then
  echo "Warning: Directory $ROOT_DIR already exists. Overwriting specified files."
else
  # Create root directory and subdirectories
  mkdir -p "$ROOT_DIR"/{cloudformation,docker,codepipeline,ecs,lambda,terraform,iam,cloudwatch,secrets,eks} || {
    echo "Error: Failed to create directory structure."
    exit 1
  }
fi

# Verify write permissions
if [ ! -w "$ROOT_DIR" ]; then
  echo "Error: No write permissions for $ROOT_DIR."
  exit 1
fi

# Create cloudformation/rds-instance.yml
cat << 'EOF' > "$ROOT_DIR/cloudformation/rds-instance.yml"
AWSTemplateFormatVersion: '2010-09-09'
Description: RDS PostgreSQL instance with encryption. Replace {{AWS_REGION}} and {{SNS_TOPIC_ARN}} before deployment.
Resources:
  RDSDatabase:
    Type: AWS::RDS::DBInstance
    Properties:
      DBInstanceIdentifier: my-postgres-db
      Engine: postgres
      EngineVersion: '13.7'
      DBInstanceClass: db.t3.micro
      AllocatedStorage: 20
      StorageEncrypted: true
      MasterUsername: admin
      MasterUserPassword: '{{DB_PASSWORD}}'  # Replace with your password or use Secrets Manager
      VPCSecurityGroups:
        - !Ref DBSecurityGroup
      DBSubnetGroupName: !Ref DBSubnetGroup
      MultiAZ: false
      BackupRetentionPeriod: 7
      EnablePerformanceInsights: true
  DBSubnetGroup:
    Type: AWS::RDS::DBSubnetGroup
    Properties:
      DBSubnetGroupDescription: Subnet group for RDS
      SubnetIds:
        - '{{SUBNET_ID_1}}'  # Replace with your private subnet ID
        - '{{SUBNET_ID_2}}'  # Replace with another private subnet ID
  DBSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: Security group for RDS
      VpcId: '{{VPC_ID}}'  # Replace with your VPC ID
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 5432
          ToPort: 5432
          CidrIp: 10.0.0.0/16
EOF

# Create cloudformation/dynamodb-table.yml
cat << 'EOF' > "$ROOT_DIR/cloudformation/dynamodb-table.yml"
AWSTemplateFormatVersion: '2010-09-09'
Description: DynamoDB table with auto-scaling. Replace {{TABLE_NAME}} before deployment.
Resources:
  DynamoDBTable:
    Type: AWS::DynamoDB::Table
    Properties:
      TableName: '{{TABLE_NAME}}'  # Replace with your table name (e.g., my-app-table)
      AttributeDefinitions:
        - AttributeName: id
          AttributeType: S
      KeySchema:
        - AttributeName: id
          KeyType: HASH
      BillingMode: PAY_PER_REQUEST
      PointInTimeRecoverySpecification:
        PointInTimeRecoveryEnabled: true
  ReadScaling:
    Type: AWS::ApplicationAutoScaling::ScalableTarget
    Properties:
      MaxCapacity: 100
      MinCapacity: 10
      ResourceId: !Sub table/${DynamoDBTable}
      ScalableDimension: dynamodb:table:ReadCapacityUnits
      ServiceNamespace: dynamodb
EOF

# Create docker/python-dockerfile
cat << 'EOF' > "$ROOT_DIR/docker/python-dockerfile"
# Build stage
FROM python:3.9-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt
COPY . .

# Run stage
FROM python:3.9-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
RUN useradd -m appuser && chown -R appuser /app
USER appuser
EXPOSE 5000
ENV PATH=/root/.local/bin:$PATH
CMD ["python", "app.py"]
EOF

# Create docker/docker-compose.yml
cat << 'EOF' > "$ROOT_DIR/docker/docker-compose.yml"
version: '3.8'
services:
  app:
    build:
      context: .
      dockerfile: python-dockerfile
    ports:
      - "5000:5000"
    environment:
      - REDIS_HOST=redis
    depends_on:
      - redis
  redis:
    image: redis:6.2-alpine
    ports:
      - "6379:6379"
EOF

# Create codepipeline/serverless-pipeline.yml
cat << 'EOF' > "$ROOT_DIR/codepipeline/serverless-pipeline.yml"
Resources:
  Pipeline:
    Type: AWS::CodePipeline::Pipeline
    Properties:
      RoleArn: !GetAtt PipelineRole.Arn
      Stages:
        - Name: Source
          Actions:
            - Name: SourceAction
              ActionTypeId:
                Category: Source
                Owner: AWS
                Provider: CodeCommit
                Version: '1'
              Configuration:
                RepositoryName: '{{REPO_NAME}}'  # Replace with your CodeCommit repository name
                BranchName: main
        - Name: Build
          Actions:
            - Name: BuildAction
              ActionTypeId:
                Category: Build
                Owner: AWS
                Provider: CodeBuild
                Version: '1'
              Configuration:
                ProjectName: '{{BUILD_PROJECT_NAME}}'  # Replace with your CodeBuild project name
        - Name: Deploy
          Actions:
            - Name: DeployAction
              ActionTypeId:
                Category: Deploy
                Owner: AWS
                Provider: CloudFormation
                Version: '1'
              Configuration:
                StackName: ServerlessAppStack
                TemplatePath: BuildArtifact::sam-template.yml
EOF

# Create codepipeline/blue-green-pipeline.yml
cat << 'EOF' > "$ROOT_DIR/codepipeline/blue-green-pipeline.yml"
Resources:
  Pipeline:
    Type: AWS::CodePipeline::Pipeline
    Properties:
      RoleArn: !GetAtt PipelineRole.Arn
      Stages:
        - Name: Source
          Actions:
            - Name: SourceAction
              ActionTypeId:
                Category: Source
                Owner: AWS
                Provider: CodeCommit
                Version: '1'
              Configuration:
                RepositoryName: '{{REPO_NAME}}'  # Replace with your CodeCommit repository name
                BranchName: main
        - Name: Build
          Actions:
            - Name: BuildAction
              ActionTypeId:
                Category: Build
                Owner: AWS
                Provider: CodeBuild
                Version: '1'
              Configuration:
                ProjectName: '{{BUILD_PROJECT_NAME}}'  # Replace with your CodeBuild project name
        - Name: Deploy
          Actions:
            - Name: BlueGreenDeploy
              ActionTypeId:
                Category: Deploy
                Owner: AWS
                Provider: CodeDeployToECS
                Version: '1'
              Configuration:
                ApplicationName: '{{CODEDEPLOY_APP_NAME}}'  # Replace with your CodeDeploy application name
                DeploymentGroupName: '{{CODEDEPLOY_GROUP_NAME}}'  # Replace with your deployment group name
                TaskDefinitionTemplateArtifact: BuildArtifact
                AppSpecTemplateArtifact: BuildArtifact
EOF

# Create ecs/service-definition.json
cat << 'EOF' > "$ROOT_DIR/ecs/service-definition.json"
{
  "cluster": "{{ECS_CLUSTER_NAME}}",  # Replace with your ECS cluster name
  "serviceName": "{{ECS_SERVICE_NAME}}",  # Replace with your ECS service name
  "taskDefinition": "{{TASK_DEFINITION_ARN}}",  # Replace with your task definition ARN
  "desiredCount": 2,
  "launchType": "FARGATE",
  "networkConfiguration": {
    "awsvpcConfiguration": {
      "subnets": ["{{SUBNET_ID_1}}", "{{SUBNET_ID_2}}"],  # Replace with your subnet IDs
      "securityGroups": ["{{SECURITY_GROUP_ID}}"],  # Replace with your security group ID
      "assignPublicIp": "ENABLED"
    }
  },
  "loadBalancers": [
    {
      "targetGroupArn": "{{TARGET_GROUP_ARN}}",  # Replace with your ALB target group ARN
      "containerName": "my-app",
      "containerPort": 5000
    }
  ]
}
EOF

# Create ecs/alb-config.yml
cat << 'EOF' > "$ROOT_DIR/ecs/alb-config.yml"
Resources:
  ApplicationLoadBalancer:
    Type: AWS::ElasticLoadBalancingV2::LoadBalancer
    Properties:
      Subnets:
        - '{{SUBNET_ID_1}}'  # Replace with your public subnet ID
        - '{{SUBNET_ID_2}}'  # Replace with another public subnet ID
      SecurityGroups:
        - '{{SECURITY_GROUP_ID}}'  # Replace with your security group ID
      Scheme: internet-facing
      Type: application
  TargetGroup:
    Type: AWS::ElasticLoadBalancingV2::TargetGroup
    Properties:
      VpcId: '{{VPC_ID}}'  # Replace with your VPC ID
      Port: 5000
      Protocol: HTTP
      HealthCheckPath: /health
      TargetType: ip
  Listener:
    Type: AWS::ElasticLoadBalancingV2::Listener
    Properties:
      LoadBalancerArn: !Ref ApplicationLoadBalancer
      Port: 80
      Protocol: HTTP
      DefaultActions:
        - Type: forward
          TargetGroupArn: !Ref TargetGroup
EOF

# Create lambda/log-retention.yml
cat << 'EOF' > "$ROOT_DIR/lambda/log-retention.yml"
Resources:
  LogRetentionFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: LogRetentionManager
      Handler: index.handler
      Role: !GetAtt LambdaExecutionRole.Arn
      Code:
        ZipFile: |
          import json
          import boto3
          import os

          def get_input(prompt):
              try:
                  return os.environ.get(prompt) or input(f"Enter {prompt}: ")
              except EOFError:
                  raise ValueError(f"{prompt} not provided")

          def lambda_handler(event, context):
              region = get_input('AWS_REGION')
              sns_topic_arn = get_input('SNS_TOPIC_ARN')
              logs = boto3.client('logs', region_name=region)
              sns = boto3.client('sns', region_name=region)
              log_groups = logs.describe_log_groups()['logGroups']
              for group in log_groups:
                  group_name = group['logGroupName']
                  if 'retentionInDays' not in group or group['retentionInDays'] != 30:
                      logs.put_retention_policy(logGroupName=group_name, retentionInDays=30)
                      sns.publish(
                          TopicArn=sns_topic_arn,
                          Message=f"Set retention to 30 days for log group {group_name}"
                      )
              return {'statusCode': 200, 'body': json.dumps('Log retention updated')}
      Runtime: python3.9
      Timeout: 60
      Environment:
        Variables:
          AWS_REGION: '{{AWS_REGION}}'  # Replace with your AWS region
          SNS_TOPIC_ARN: '{{SNS_TOPIC_ARN}}'  # Replace with your SNS Topic ARN
  LambdaExecutionRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: lambda.amazonaws.com
            Action: sts:AssumeRole
      Policies:
        - PolicyName: LogRetentionPolicy
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Effect: Allow
                Action:
                  - logs:DescribeLogGroups
                  - logs:PutRetentionPolicy
                Resource: '*'
              - Effect: Allow
                Action: sns:Publish
                Resource: '{{SNS_TOPIC_ARN}}'  # Replace with your SNS Topic ARN
EOF

# Create lambda/dynamodb-backup.yml
cat << 'EOF' > "$ROOT_DIR/lambda/dynamodb-backup.yml"
Resources:
  BackupFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: DynamoDBBackup
      Handler: index.handler
      Role: !GetAtt LambdaExecutionRole.Arn
      Code:
        ZipFile: |
          import json
          import boto3
          import os
          from datetime import datetime

          def get_input(prompt):
              try:
                  return os.environ.get(prompt) or input(f"Enter {prompt}: ")
              except EOFError:
                  raise ValueError(f"{prompt} not provided")

          def lambda_handler(event, context):
              table_name = get_input('TABLE_NAME')
              sns_topic_arn = get_input('SNS_TOPIC_ARN')
              dynamodb = boto3.client('dynamodb')
              sns = boto3.client('sns')
              backup_name = f"{table_name}-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
              dynamodb.create_backup(TableName=table_name, BackupName=backup_name)
              sns.publish(
                  TopicArn=sns_topic_arn,
                  Message=f"Backup {backup_name} created for table {table_name}"
              )
              return {'statusCode': 200, 'body': json.dumps('Backup complete')}
      Runtime: python3.9
      Timeout: 60
      Environment:
        Variables:
          TABLE_NAME: '{{TABLE_NAME}}'  # Replace with your DynamoDB table name
          SNS_TOPIC_ARN: '{{SNS_TOPIC_ARN}}'  # Replace with your SNS Topic ARN
  LambdaExecutionRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: lambda.amazonaws.com
            Action: sts:AssumeRole
      Policies:
        - PolicyName: DynamoDBBackupPolicy
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Effect: Allow
                Action:
                  - dynamodb:CreateBackup
                  - dynamodb:DescribeTable
                Resource: '*'
              - Effect: Allow
                Action: sns:Publish
                Resource: '{{SNS_TOPIC_ARN}}'  # Replace with your SNS Topic ARN
  ScheduleRule:
    Type: AWS::Events::Rule
    Properties:
      Description: Weekly DynamoDB backup
      ScheduleExpression: rate(7 days)
      Targets:
        - Arn: !GetAtt BackupFunction.Arn
          Id: BackupFunctionTarget
  PermissionForEvents:
    Type: AWS::Lambda::Permission
    Properties:
      FunctionName: !Ref BackupFunction
      Action: lambda:InvokeFunction
      Principal: events.amazonaws.com
      SourceArn: !GetAtt ScheduleRule.Arn
EOF

# Create terraform/lambda-function.tf
cat << 'EOF' > "$ROOT_DIR/terraform/lambda-function.tf"
resource "aws_lambda_function" "s3_processor" {
  function_name = "{{LAMBDA_FUNCTION_NAME}}"  # Replace with your Lambda function name
  runtime       = "python3.9"
  handler       = "index.handler"
  role          = aws_iam_role.lambda_role.arn
  filename      = "lambda.zip"
  source_code_hash = filebase64sha256("lambda.zip")
}

resource "aws_lambda_permission" "s3_trigger" {
  statement_id  = "AllowExecutionFromS3"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.s3_processor.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = "arn:aws:s3:::{{S3_BUCKET_NAME}}"  # Replace with your S3 bucket name
}

resource "aws_s3_bucket_notification" "bucket_notification" {
  bucket = "{{S3_BUCKET_NAME}}"  # Replace with your S3 bucket name
  lambda_function {
    lambda_function_arn = aws_lambda_function.s3_processor.arn
    events              = ["s3:ObjectCreated:*"]
  }
}

resource "aws_iam_role" "lambda_role" {
  name = "lambda_s3_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy" "lambda_policy" {
  name = "lambda_s3_policy"
  role = aws_iam_role.lambda_role.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:ListBucket"
        ]
        Resource = [
          "arn:aws:s3:::{{S3_BUCKET_NAME}}",
          "arn:aws:s3:::{{S3_BUCKET_NAME}}/*"
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "*"
      }
    ]
  })
}
EOF

# Create terraform/kms-key.tf
cat << 'EOF' > "$ROOT_DIR/terraform/kms-key.tf"
resource "aws_kms_key" "custom_key" {
  description             = "KMS key for encryption"
  enable_key_rotation     = true
  deletion_window_in_days = 10
}

resource "aws_kms_alias" "key_alias" {
  name          = "alias/{{KMS_ALIAS}}"  # Replace with your KMS alias (e.g., my-key)
  target_key_id = aws_kms_key.custom_key.key_id
}
EOF

# Create iam/codebuild-role.json
cat << 'EOF' > "$ROOT_DIR/iam/codebuild-role.json"
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::{{S3_BUCKET_NAME}}",  # Replace with your S3 bucket name
        "arn:aws:s3:::{{S3_BUCKET_NAME}}/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "ecr:GetAuthorizationToken",
        "ecr:BatchCheckLayerAvailability",
        "ecr:GetDownloadUrlForLayer",
        "ecr:BatchGetImage",
        "ecr:PutImage",
        "ecr:InitiateLayerUpload",
        "ecr:UploadLayerPart",
        "ecr:CompleteLayerUpload"
      ],
      "Resource": "*"
    }
  ]
}
EOF

# Create iam/ssm-access-policy.json
cat << 'EOF' > "$ROOT_DIR/iam/ssm-access-policy.json"
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ssm:GetParameter",
        "ssm:GetParameters",
        "ssm:GetParametersByPath"
      ],
      "Resource": "arn:aws:ssm:{{AWS_REGION}}:*:parameter/{{SSM_PARAMETER_PATH}}"  # Replace with your region and parameter path (e.g., /my-app/*)
    }
  ]
}
EOF

# Create cloudwatch/rds-alarms.yml
cat << 'EOF' > "$ROOT_DIR/cloudwatch/rds-alarms.yml"
Resources:
  CPUAlarm:
    Type: AWS::CloudWatch::Alarm
    Properties:
      AlarmDescription: "Alarm if RDS CPU exceeds 80%"
      Namespace: AWS/RDS
      MetricName: CPUUtilization
      Dimensions:
        - Name: DBInstanceIdentifier
          Value: '{{RDS_INSTANCE_ID}}'  # Replace with your RDS instance ID
      Statistic: Average
      Period: 300
      EvaluationPeriods: 2
      Threshold: 80
      ComparisonOperator: GreaterThanThreshold
      AlarmActions:
        - '{{SNS_TOPIC_ARN}}'  # Replace with your SNS Topic ARN
  StorageAlarm:
    Type: AWS::CloudWatch::Alarm
    Properties:
      AlarmDescription: "Alarm if RDS storage is below 10%"
      Namespace: AWS/RDS
      MetricName: FreeStorageSpace
      Dimensions:
        - Name: DBInstanceIdentifier
          Value: '{{RDS_INSTANCE_ID}}'  # Replace with your RDS instance ID
      Statistic: Average
      Period: 300
      EvaluationPeriods: 2
      Threshold: 10
      ComparisonOperator: LessThanThreshold
      AlarmActions:
        - '{{SNS_TOPIC_ARN}}'  # Replace with your SNS Topic ARN
EOF

# Create cloudwatch/api-latency-alarm.yml
cat << 'EOF' > "$ROOT_DIR/cloudwatch/api-latency-alarm.yml"
Resources:
  LatencyAlarm:
    Type: AWS::CloudWatch::Alarm
    Properties:
      AlarmDescription: "Alarm if API Gateway latency exceeds 500ms"
      Namespace: AWS/ApiGateway
      MetricName: Latency
      Dimensions:
        - Name: ApiName
          Value: '{{API_ID}}'  # Replace with your API Gateway ID or name
      Statistic: Average
      Period: 60
      EvaluationPeriods: 2
      Threshold: 0.5
      ComparisonOperator: GreaterThanThreshold
      AlarmActions:
        - '{{SNS_TOPIC_ARN}}'  # Replace with your SNS Topic ARN
EOF

# Create secrets/kms-encrypted-secret.yml
cat << 'EOF' > "$ROOT_DIR/secrets/kms-encrypted-secret.yml"
Resources:
  Secret:
    Type: AWS::SecretsManager::Secret
    Properties:
      Name: my-app-secret
      Description: Application credentials
      KmsKeyId: '{{KMS_KEY_ARN}}'  # Replace with your KMS key ARN
      SecretString: '{"username":"app_user","password":"initial"}'
EOF

# Create secrets/secret-rotation-policy.json
cat << 'EOF' > "$ROOT_DIR/secrets/secret-rotation-policy.json"
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "secretsmanager:RotateSecret",
        "secretsmanager:GetSecretValue",
        "secretsmanager:UpdateSecret",
        "secretsmanager:DescribeSecret"
      ],
      "Resource": "{{SECRETS_MANAGER_ARN}}"  # Replace with your Secrets Manager ARN
    },
    {
      "Effect": "Allow",
      "Action": [
        "kms:GenerateDataKey",
        "kms:Decrypt"
      ],
      "Resource": "{{KMS_KEY_ARN}}"  # Replace with your KMS key ARN
    }
  ]
}
EOF

# Create eks/node-group.tf
cat << 'EOF' > "$ROOT_DIR/eks/node-group.tf"
resource "aws_eks_node_group" "node_group" {
  cluster_name    = "{{EKS_CLUSTER_NAME}}"  # Replace with your EKS cluster name
  node_group_name = "main-node-group"
  node_role_arn   = aws_iam_role.node_role.arn
  subnet_ids      = {{SUBNET_IDS}}  # Replace with your subnet IDs (e.g., ["subnet-123", "subnet-456"])
  scaling_config {
    desired_size = 2
    max_size     = 4
    min_size     = 1
  }
}

resource "aws_iam_role" "node_role" {
  name = "eks-node-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "node_policy" {
  role       = aws_iam_role.node_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy"
}
EOF

# Create eks/cluster-autoscaler.yml
cat << 'EOF' > "$ROOT_DIR/eks/cluster-autoscaler.yml"
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cluster-autoscaler
  namespace: kube-system
spec:
  replicas: 1
  selector:
    matchLabels:
      app: cluster-autoscaler
  template:
    metadata:
      labels:
        app: cluster-autoscaler
    spec:
      containers:
        - name: cluster-autoscaler
          image: k8s.gcr.io/autoscaling/cluster-autoscaler:v1.21.0
          env:
            - name: AWS_REGION
              value: '{{AWS_REGION}}'  # Replace with your AWS region
            - name: CLUSTER_NAME
              value: '{{EKS_CLUSTER_NAME}}'  # Replace with your EKS cluster name
EOF

# Verify file creation
FILES=(
  "$ROOT_DIR/cloudformation/rds-instance.yml"
  "$ROOT_DIR/cloudformation/dynamodb-table.yml"
  "$ROOT_DIR/docker/python-dockerfile"
  "$ROOT_DIR/docker/docker-compose.yml"
  "$ROOT_DIR/codepipeline/serverless-pipeline.yml"
  "$ROOT_DIR/codepipeline/blue-green-pipeline.yml"
  "$ROOT_DIR/ecs/service-definition.json"
  "$ROOT_DIR/ecs/alb-config.yml"
  "$ROOT_DIR/lambda/log-retention.yml"
  "$ROOT_DIR/lambda/dynamodb-backup.yml"
  "$ROOT_DIR/terraform/lambda-function.tf"
  "$ROOT_DIR/terraform/kms-key.tf"
  "$ROOT_DIR/iam/codebuild-role.json"
  "$ROOT_DIR/iam/ssm-access-policy.json"
  "$ROOT_DIR/cloudwatch/rds-alarms.yml"
  "$ROOT_DIR/cloudwatch/api-latency-alarm.yml"
  "$ROOT_DIR/secrets/kms-encrypted-secret.yml"
  "$ROOT_DIR/secrets/secret-rotation-policy.json"
  "$ROOT_DIR/eks/node-group.tf"
  "$ROOT_DIR/eks/cluster-autoscaler.yml"
)

for file in "${FILES[@]}"; do
  if [ ! -f "$file" ]; then
    echo "Error: Failed to create $file."
    exit 1
  fi
done

echo "AWS DevOps boilerplate files created successfully in $ROOT_DIR/"
echo "Next steps:"
echo "1. Replace placeholders (e.g., {{SNS_TOPIC_ARN}}, {{AWS_REGION}}, {{TABLE_NAME}}) in the templates with your values."
echo "2. Deploy CloudFormation templates using AWS CLI:"
echo "   aws cloudformation deploy --template-file $ROOT_DIR/cloudformation/rds-instance.yml --stack-name RDSInstance --capabilities CAPABILITY_IAM"
echo "   aws cloudformation deploy --template-file $ROOT_DIR/lambda/log-retention.yml --stack-name LogRetention --capabilities CAPABILITY_IAM"
echo "3. Apply Terraform modules:"
echo "   cd $ROOT_DIR/terraform && terraform init && terraform apply"
echo "4. Set environment variables for Lambda functions (e.g., SNS_TOPIC_ARN, TABLE_NAME) or enter values when prompted at runtime."
echo "5. For CodePipeline, set repository and project names via AWS CLI or CodePipeline settings."
echo "6. Ensure RDS, DynamoDB, Secrets Manager, and EKS are enabled in your account."
echo "7. Push to GitHub: Initialize a repo, add files, and share with the community."
exit 0
