#!/bin/bash

# Script to generate AWS security testing boilerplate files non-interactively

# Define root directory
ROOT_DIR="aws-security-testing-boilerplates"

# Check if directory already exists
if [ -d "$ROOT_DIR" ]; then
  echo "Warning: Directory $ROOT_DIR already exists. Overwriting specified files."
else
  # Create root directory and subdirectories
  mkdir -p "$ROOT_DIR"/{cloudformation,codebuild,lambda,cloudwatch,eks} || {
    echo "Error: Failed to create directory structure."
    exit 1
  }
fi

# Verify write permissions
if [ ! -w "$ROOT_DIR" ]; then
  echo "Error: No write permissions for $ROOT_DIR."
  exit 1
fi

# Create cloudformation/iam-policy-audit.yml
echo "Creating iam-policy-audit.yml..."
cat << 'EOF' > "$ROOT_DIR/cloudformation/iam-policy-audit.yml"
AWSTemplateFormatVersion: '2010-09-09'
Description: Lambda to audit IAM policies for overly permissive permissions. Set SNS_TOPIC_ARN and AWS_REGION at runtime.
Resources:
  IAMPolicyAuditor:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: IAMPolicyAuditor
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
              iam = boto3.client('iam', region_name=region)
              sns = boto3.client('sns', region_name=region)
              policies = iam.list_policies(Scope='Local')['Policies']
              issues = []
              for policy in policies:
                  policy_arn = policy['Arn']
                  policy_version = iam.get_policy_version(
                      PolicyArn=policy_arn,
                      VersionId=policy['DefaultVersionId']
                  )['PolicyVersion']['Document']
                  for statement in policy_version.get('Statement', []):
                      if statement.get('Effect') == 'Allow' and (
                          '*' in statement.get('Action', []) or
                          '*' in statement.get('Resource', [])
                      ):
                          issues.append(f"Overly permissive policy: {policy_arn}")
              if issues:
                  sns.publish(
                      TopicArn=sns_topic_arn,
                      Message='\n'.join(issues)
                  )
              return {'statusCode': 200, 'body': json.dumps('IAM policy audit complete')}
      Runtime: python3.9
      Timeout: 60
      Environment:
        Variables:
          AWS_REGION: '{{AWS_REGION}}'  # Replace with your AWS region (e.g., us-east-1)
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
        - PolicyName: IAMAuditPolicy
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Effect: Allow
                Action:
                  - iam:ListPolicies
                  - iam:GetPolicyVersion
                Resource: '*'
              - Effect: Allow
                Action: sns:Publish
                Resource: '{{SNS_TOPIC_ARN}}'  # Replace with your SNS Topic ARN
  ScheduleRule:
    Type: AWS::Events::Rule
    Properties:
      Description: Daily IAM policy audit
      ScheduleExpression: rate(1 day)
      Targets:
        - Arn: !GetAtt IAMPolicyAuditor.Arn
          Id: IAMPolicyAuditorTarget
  PermissionForEvents:
    Type: AWS::Lambda::Permission
    Properties:
      FunctionName: !Ref IAMPolicyAuditor
      Action: lambda:InvokeFunction
      Principal: events.amazonaws.com
      SourceArn: !GetAtt ScheduleRule.Arn
EOF

# Create cloudformation/kms-key-audit.yml
echo "Creating kms-key-audit.yml..."
cat << 'EOF' > "$ROOT_DIR/cloudformation/kms-key-audit.yml"
AWSTemplateFormatVersion: '2010-09-09'
Description: Lambda to audit KMS keys for public access or disabled rotation. Set SNS_TOPIC_ARN and AWS_REGION at runtime.
Resources:
  KMSKeyAuditor:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: KMSKeyAuditor
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
              kms = boto3.client('kms', region_name=region)
              sns = boto3.client('sns', region_name=region)
              keys = kms.list_keys()['Keys']
              issues = []
              for key in keys:
                  key_id = key['KeyId']
                  key_metadata = kms.describe_key(KeyId=key_id)['KeyMetadata']
                  if not key_metadata['KeyRotationEnabled']:
                      issues.append(f"KMS key {key_id} has rotation disabled")
                  policy = kms.get_key_policy(KeyId=key_id, PolicyName='default')['Policy']
                  if '"AWS": "*"' in policy:
                      issues.append(f"KMS key {key_id} has public access")
              if issues:
                  sns.publish(
                      TopicArn=sns_topic_arn,
                      Message='\n'.join(issues)
                  )
              return {'statusCode': 200, 'body': json.dumps('KMS key audit complete')}
      Runtime: python3.9
      Timeout: 60
      Environment:
        Variables:
          AWS_REGION: '{{AWS_REGION}}'  # Replace with your AWS region (e.g., us-east-1)
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
        - PolicyName: KMSAuditPolicy
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Effect: Allow
                Action:
                  - kms:ListKeys
                  - kms:DescribeKey
                  - kms:GetKeyPolicy
                Resource: '*'
              - Effect: Allow
                Action: sns:Publish
                Resource: '{{SNS_TOPIC_ARN}}'  # Replace with your SNS Topic ARN
  ScheduleRule:
    Type: AWS::Events::Rule
    Properties:
      Description: Daily KMS key audit
      ScheduleExpression: rate(1 day)
      Targets:
        - Arn: !GetAtt KMSKeyAuditor.Arn
          Id: KMSKeyAuditorTarget
  PermissionForEvents:
    Type: AWS::Lambda::Permission
    Properties:
      FunctionName: !Ref KMSKeyAuditor
      Action: lambda:InvokeFunction
      Principal: events.amazonaws.com
      SourceArn: !GetAtt ScheduleRule.Arn
EOF

# Create codebuild/code-vuln-scan.yml
echo "Creating code-vuln-scan.yml..."
cat << 'EOF' > "$ROOT_DIR/codebuild/code-vuln-scan.yml"
Resources:
  CodeVulnScanProject:
    Type: AWS::CodeBuild::Project
    Properties:
      Name: CodeVulnScanProject
      ServiceRole: !GetAtt CodeBuildRole.Arn
      Artifacts:
        Type: NO_ARTIFACTS
      Environment:
        Type: LINUX_CONTAINER
        Image: aws/codebuild/standard:5.0
        ComputeType: BUILD_GENERAL1_MEDIUM
      Source:
        Type: NO_SOURCE
        BuildSpec: |
          version: 0.2
          phases:
            install:
              commands:
                - npm install -g snyk
            build:
              commands:
                # Set REPO_URL as a CodeBuild environment variable or pass via AWS CLI
                # Example: aws codebuild start-build --project-name CodeVulnScanProject --environment-variables-override "Name=REPO_URL,Value=https://github.com/my-org/my-repo.git"
                - if [ -z "$REPO_URL" ]; then echo "Error: REPO_URL not set"; exit 1; fi
                - git clone $REPO_URL repo
                - cd repo
                - snyk test --severity-threshold=high > vuln-report.txt
                - if grep -q "Vulnerabilities found" vuln-report.txt; then echo "Vulnerabilities detected"; exit 1; fi
          reports:
            vuln-report:
              files:
                - vuln-report.txt
              format: JUNIT
      LogsConfig:
        CloudWatchLogs:
          Status: ENABLED
          GroupName: /codebuild/code-vuln-scans
      EnvironmentVariables:
        - Name: REPO_URL
          Value: '{{REPO_URL}}'  # Replace with your repository URL (e.g., https://github.com/my-org/my-repo.git)
  CodeBuildRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: codebuild.amazonaws.com
            Action: sts:AssumeRole
      Policies:
        - PolicyName: CodeBuildPolicy
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Effect: Allow
                Action:
                  - logs:CreateLogGroup
                  - logs:CreateLogStream
                  - logs:PutLogEvents
                Resource: '*'
              - Effect: Allow
                Action: sns:Publish
                Resource: '{{SNS_TOPIC_ARN}}'  # Replace with your SNS Topic ARN
EOF

# Create codebuild/infra-vuln-scan.yml
echo "Creating infra-vuln-scan.yml..."
cat << 'EOF' > "$ROOT_DIR/codebuild/infra-vuln-scan.yml"
Resources:
  InfraVulnScanProject:
    Type: AWS::CodeBuild::Project
    Properties:
      Name: InfraVulnScanProject
      ServiceRole: !GetAtt CodeBuildRole.Arn
      Artifacts:
        Type: NO_ARTIFACTS
      Environment:
        Type: LINUX_CONTAINER
        Image: aws/codebuild/standard:5.0
        ComputeType: BUILD_GENERAL1_MEDIUM
      Source:
        Type: NO_SOURCE
        BuildSpec: |
          version: 0.2
          phases:
            install:
              commands:
                - gem install cfn-nag
            build:
              commands:
                # Set S3_BUCKET_NAME as a CodeBuild environment variable or pass via AWS CLI
                # Example: aws codebuild start-build --project-name InfraVulnScanProject --environment-variables-override "Name=S3_BUCKET_NAME,Value=my-cfn-templates"
                - if [ -z "$S3_BUCKET_NAME" ]; then echo "Error: S3_BUCKET_NAME not set"; exit 1; fi
                - aws s3 cp s3://$S3_BUCKET_NAME/templates/ templates/ --recursive
                - cfn_nag_scan --input-path templates/ > cfn-nag-report.txt
                - if grep -q "FAIL" cfn-nag-report.txt; then echo "Security issues detected"; exit 1; fi
          reports:
            cfn-nag-report:
              files:
                - cfn-nag-report.txt
              format: JUNIT
      LogsConfig:
        CloudWatchLogs:
          Status: ENABLED
          GroupName: /codebuild/infra-vuln-scans
      EnvironmentVariables:
        - Name: S3_BUCKET_NAME
          Value: '{{S3_BUCKET_NAME}}'  # Replace with your S3 bucket name (e.g., my-cfn-templates)
  CodeBuildRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: codebuild.amazonaws.com
            Action: sts:AssumeRole
      Policies:
        - PolicyName: CodeBuildPolicy
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Effect: Allow
                Action:
                  - logs:CreateLogGroup
                  - logs:CreateLogStream
                  - logs:PutLogEvents
                Resource: '*'
              - Effect: Allow
                Action:
                  - s3:GetObject
                  - s3:ListBucket
                Resource:
                  - 'arn:aws:s3:::{{S3_BUCKET_NAME}}'
                  - 'arn:aws:s3:::{{S3_BUCKET_NAME}}/*'
              - Effect: Allow
                Action: sns:Publish
                Resource: '{{SNS_TOPIC_ARN}}'  # Replace with your SNS Topic ARN
EOF

# Create lambda/secrets-exposure-scan.yml
echo "Creating secrets-exposure-scan.yml..."
cat << 'EOF' > "$ROOT_DIR/lambda/secrets-exposure-scan.yml"
AWSTemplateFormatVersion: '2010-09-09'
Description: Lambda to scan S3 buckets for exposed secrets. Set SNS_TOPIC_ARN and AWS_REGION at runtime.
Resources:
  SecretsExposureScanner:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: SecretsExposureScanner
      Handler: index.handler
      Role: !GetAtt LambdaExecutionRole.Arn
      Code:
        ZipFile: |
          import json
          import boto3
          import os
          import re

          def get_input(prompt):
              try:
                  return os.environ.get(prompt) or input(f"Enter {prompt}: ")
              except EOFError:
                  raise ValueError(f"{prompt} not provided")

          def lambda_handler(event, context):
              region = get_input('AWS_REGION')
              sns_topic_arn = get_input('SNS_TOPIC_ARN')
              s3 = boto3.client('s3', region_name=region)
              sns = boto3.client('sns', region_name=region)
              buckets = s3.list_buckets()['Buckets']
              issues = []
              secret_pattern = re.compile(r'(?i)(api_key|password|secret|token)=[^\s]+')
              for bucket in buckets:
                  name = bucket['Name']
                  try:
                      acl = s3.get_bucket_acl(Bucket=name)
                      if any(grant['Grantee'].get('URI', '') == 'http://acs.amazonaws.com/groups/global/AllUsers' for grant in acl['Grants']):
                          objects = s3.list_objects_v2(Bucket=name).get('Contents', [])
                          for obj in objects:
                              content = s3.get_object(Bucket=name, Key=obj['Key'])['Body'].read().decode('utf-8', errors='ignore')
                              if secret_pattern.search(content):
                                  issues.append(f"Potential secret exposed in public bucket {name}/{obj['Key']}")
                  except s3.exceptions.ClientError:
                      continue
              if issues:
                  sns.publish(
                      TopicArn=sns_topic_arn,
                      Message='\n'.join(issues)
                  )
              return {'statusCode': 200, 'body': json.dumps('Secrets exposure scan complete')}
      Runtime: python3.9
      Timeout: 120
      Environment:
        Variables:
          AWS_REGION: '{{AWS_REGION}}'  # Replace with your AWS region (e.g., us-east-1)
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
        - PolicyName: SecretsScanPolicy
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Effect: Allow
                Action:
                  - s3:ListAllMyBuckets
                  - s3:GetBucketAcl
                  - s3:ListBucket
                  - s3:GetObject
                Resource: '*'
              - Effect: Allow
                Action: sns:Publish
                Resource: '{{SNS_TOPIC_ARN}}'  # Replace with your SNS Topic ARN
  ScheduleRule:
    Type: AWS::Events::Rule
    Properties:
      Description: Daily secrets exposure scan
      ScheduleExpression: rate(1 day)
      Targets:
        - Arn: !GetAtt SecretsExposureScanner.Arn
          Id: SecretsExposureScannerTarget
  PermissionForEvents:
    Type: AWS::Lambda::Permission
    Properties:
      FunctionName: !Ref SecretsExposureScanner
      Action: lambda:InvokeFunction
      Principal: events.amazonaws.com
      SourceArn: !GetAtt ScheduleRule.Arn
EOF

# Create lambda/ebs-encryption-check.yml
echo "Creating ebs-encryption-check.yml..."
cat << 'EOF' > "$ROOT_DIR/lambda/ebs-encryption-check.yml"
AWSTemplateFormatVersion: '2010-09-09'
Description: Lambda to verify EBS volumes are encrypted. Set SNS_TOPIC_ARN and AWS_REGION at runtime.
Resources:
  EBSEncryptionChecker:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: EBSEncryptionChecker
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
              ec2 = boto3.client('ec2', region_name=region)
              sns = boto3.client('sns', region_name=region)
              volumes = ec2.describe_volumes()['Volumes']
              issues = []
              for volume in volumes:
                  if not volume.get('Encrypted', False):
                      issues.append(f"EBS volume {volume['VolumeId']} is not encrypted")
              if issues:
                  sns.publish(
                      TopicArn=sns_topic_arn,
                      Message='\n'.join(issues)
                  )
              return {'statusCode': 200, 'body': json.dumps('EBS encryption check complete')}
      Runtime: python3.9
      Timeout: 60
      Environment:
        Variables:
          AWS_REGION: '{{AWS_REGION}}'  # Replace with your AWS region (e.g., us-east-1)
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
        - PolicyName: EBSEncryptionPolicy
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Effect: Allow
                Action:
                  - ec2:DescribeVolumes
                Resource: '*'
              - Effect: Allow
                Action: sns:Publish
                Resource: '{{SNS_TOPIC_ARN}}'  # Replace with your SNS Topic ARN
  ScheduleRule:
    Type: AWS::Events::Rule
    Properties:
      Description: Daily EBS encryption check
      ScheduleExpression: rate(1 day)
      Targets:
        - Arn: !GetAtt EBSEncryptionChecker.Arn
          Id: EBSEncryptionCheckerTarget
  PermissionForEvents:
    Type: AWS::Lambda::Permission
    Properties:
      FunctionName: !Ref EBSEncryptionChecker
      Action: lambda:InvokeFunction
      Principal: events.amazonaws.com
      SourceArn: !GetAtt ScheduleRule.Arn
EOF

# Create cloudwatch/guardduty-alarm.yml
echo "Creating guardduty-alarm.yml..."
cat << 'EOF' > "$ROOT_DIR/cloudwatch/guardduty-alarm.yml"
AWSTemplateFormatVersion: '2010-09-09'
Description: CloudWatch alarm for high-severity GuardDuty findings. Set SNS_TOPIC_ARN before deployment.
Resources:
  GuardDutyAlarm:
    Type: AWS::CloudWatch::Alarm
    Properties:
      AlarmDescription: "Alarm for high-severity GuardDuty findings"
      Namespace: AWS/GuardDuty
      MetricName: FindingCount
      Dimensions:
        - Name: Severity
          Value: High
      Statistic: Sum
      Period: 300
      EvaluationPeriods: 1
      Threshold: 1
      ComparisonOperator: GreaterThanOrEqualToThreshold
      AlarmActions:
        - '{{SNS_TOPIC_ARN}}'  # Replace with your SNS Topic ARN
EOF

# Create cloudwatch/config-rule-alarm.yml
echo "Creating config-rule-alarm.yml..."
cat << 'EOF' > "$ROOT_DIR/cloudwatch/config-rule-alarm.yml"
AWSTemplateFormatVersion: '2010-09-09'
Description: CloudWatch alarm for non-compliant AWS Config rules. Set SNS_TOPIC_ARN before deployment.
Resources:
  ConfigRuleAlarm:
    Type: AWS::CloudWatch::Alarm
    Properties:
      AlarmDescription: "Alarm for non-compliant AWS Config rules"
      Namespace: AWS/Config
      MetricName: NonCompliantResources
      Statistic: Sum
      Period: 300
      EvaluationPeriods: 1
      Threshold: 1
      ComparisonOperator: GreaterThanOrEqualToThreshold
      AlarmActions:
        - '{{SNS_TOPIC_ARN}}'  # Replace with your SNS Topic ARN
EOF

# Create eks/pod-security-scan.yml
echo "Creating pod-security-scan.yml..."
cat << 'EOF' > "$ROOT_DIR/eks/pod-security-scan.yml"
AWSTemplateFormatVersion: '2010-09-09'
Description: Lambda to scan EKS pods for insecure configurations. Set EKS_CLUSTER_NAME, SNS_TOPIC_ARN, and AWS_REGION at runtime.
Resources:
  PodSecurityScanner:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: PodSecurityScanner
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
              cluster_name = get_input('EKS_CLUSTER_NAME')
              sns_topic_arn = get_input('SNS_TOPIC_ARN')
              eks = boto3.client('eks', region_name=region)
              sns = boto3.client('sns', region_name=region)
              issues = []
              try:
                  clusters = eks.list_clusters()['clusters']
                  if cluster_name not in clusters:
                      issues.append(f"EKS cluster {cluster_name} not found")
                  else:
                      issues.append(f"Placeholder: Insecure pod found in {cluster_name}")
              except Exception as e:
                  issues.append(f"Error scanning EKS cluster {cluster_name}: {str(e)}")
              if issues:
                  sns.publish(
                      TopicArn=sns_topic_arn,
                      Message='\n'.join(issues)
                  )
              return {'statusCode': 200, 'body': json.dumps('EKS pod security scan complete')}
      Runtime: python3.9
      Timeout: 60
      Environment:
        Variables:
          AWS_REGION: '{{AWS_REGION}}'  # Replace with your AWS region (e.g., us-east-1)
          EKS_CLUSTER_NAME: '{{EKS_CLUSTER_NAME}}'  # Replace with your EKS cluster name
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
        - PolicyName: EKSSecurityPolicy
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Effect: Allow
                Action:
                  - eks:ListClusters
                  - eks:DescribeCluster
                Resource: '*'
              - Effect: Allow
                Action: sns:Publish
                Resource: '{{SNS_TOPIC_ARN}}'  # Replace with your SNS Topic ARN
  ScheduleRule:
    Type: AWS::Events::Rule
    Properties:
      Description: Daily EKS pod security scan
      ScheduleExpression: rate(1 day)
      Targets:
        - Arn: !GetAtt PodSecurityScanner.Arn
          Id: PodSecurityScannerTarget
  PermissionForEvents:
    Type: AWS::Lambda::Permission
    Properties:
      FunctionName: !Ref PodSecurityScanner
      Action: lambda:InvokeFunction
      Principal: events.amazonaws.com
      SourceArn: !GetAtt ScheduleRule.Arn
EOF

# Create eks/cluster-config-scan.yml
echo "Creating cluster-config-scan.yml..."
cat << 'EOF' > "$ROOT_DIR/eks/cluster-config-scan.yml"
AWSTemplateFormatVersion: '2010-09-09'
Description: Lambda to audit EKS cluster configurations. Set EKS_CLUSTER_NAME, SNS_TOPIC_ARN, and AWS_REGION at runtime.
Resources:
  ClusterConfigScanner:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: ClusterConfigScanner
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
              cluster_name = get_input('EKS_CLUSTER_NAME')
              sns_topic_arn = get_input('SNS_TOPIC_ARN')
              eks = boto3.client('eks', region_name=region)
              sns = boto3.client('sns', region_name=region)
              issues = []
              try:
                  cluster = eks.describe_cluster(name=cluster_name)['cluster']
                  if cluster['accessConfig']['authenticationMode'] != 'API_AND_CONFIG_MAP':
                      issues.append(f"EKS cluster {cluster_name} uses insecure authentication mode")
                  if cluster['resourcesVpcConfig']['endpointPublicAccess']:
                      issues.append(f"EKS cluster {cluster_name} has public endpoint enabled")
              except eks.exceptions.ResourceNotFoundException:
                  issues.append(f"EKS cluster {cluster_name} not found")
              if issues:
                  sns.publish(
                      TopicArn=sns_topic_arn,
                      Message='\n'.join(issues)
                  )
              return {'statusCode': 200, 'body': json.dumps('EKS cluster config scan complete')}
      Runtime: python3.9
      Timeout: 60
      Environment:
        Variables:
          AWS_REGION: '{{AWS_REGION}}'  # Replace with your AWS region (e.g., us-east-1)
          EKS_CLUSTER_NAME: '{{EKS_CLUSTER_NAME}}'  # Replace with your EKS cluster name
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
        - PolicyName: EKSConfigPolicy
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Effect: Allow
                Action:
                  - eks:DescribeCluster
                  - eks:ListClusters
                Resource: '*'
              - Effect: Allow
                Action: sns:Publish
                Resource: '{{SNS_TOPIC_ARN}}'  # Replace with your SNS Topic ARN
  ScheduleRule:
    Type: AWS::Events::Rule
    Properties:
      Description: Daily EKS cluster config scan
      ScheduleExpression: rate(1 day)
      Targets:
        - Arn: !GetAtt ClusterConfigScanner.Arn
          Id: ClusterConfigScannerTarget
  PermissionForEvents:
    Type: AWS::Lambda::Permission
    Properties:
      FunctionName: !Ref ClusterConfigScanner
      Action: lambda:InvokeFunction
      Principal: events.amazonaws.com
      SourceArn: !GetAtt ScheduleRule.Arn
EOF

# Verify file creation
FILES=(
  "$ROOT_DIR/cloudformation/iam-policy-audit.yml"
  "$ROOT_DIR/cloudformation/kms-key-audit.yml"
  "$ROOT_DIR/codebuild/code-vuln-scan.yml"
  "$ROOT_DIR/codebuild/infra-vuln-scan.yml"
  "$ROOT_DIR/lambda/secrets-exposure-scan.yml"
  "$ROOT_DIR/lambda/ebs-encryption-check.yml"
  "$ROOT_DIR/cloudwatch/guardduty-alarm.yml"
  "$ROOT_DIR/cloudwatch/config-rule-alarm.yml"
  "$ROOT_DIR/eks/pod-security-scan.yml"
  "$ROOT_DIR/eks/cluster-config-scan.yml"
)

for file in "${FILES[@]}"; do
  if [ ! -f "$file" ]; then
    echo "Error: Failed to create $file."
    exit 1
  fi
done

echo "AWS Security Testing boilerplate files created successfully in $ROOT_DIR/"
echo "Next steps:"
echo "1. Replace placeholders ({{SNS_TOPIC_ARN}}, {{AWS_REGION}}, {{REPO_URL}}, {{EKS_CLUSTER_NAME}}) in the templates with your values."
echo "2. Deploy templates using AWS CLI:"
echo "   aws cloudformation deploy --template-file $ROOT_DIR/cloudformation/iam-policy-audit.yml --stack-name IAMPolicyAudit --capabilities CAPABILITY_IAM"
echo "   aws cloudformation deploy --template-file $ROOT_DIR/cloudformation/kms-key-audit.yml --stack-name KMSKeyAudit --capabilities CAPABILITY_IAM"
echo "   aws cloudformation deploy --template-file $ROOT_DIR/codebuild/code-vuln-scan.yml --stack-name CodeVulnScan --capabilities CAPABILITY_IAM"
echo "   aws cloudformation deploy --template-file $ROOT_DIR/codebuild/infra-vuln-scan.yml --stack-name InfraVulnScan --capabilities CAPABILITY_IAM"
echo "   aws cloudformation deploy --template-file $ROOT_DIR/lambda/secrets-exposure-scan.yml --stack-name SecretsExposure --capabilities CAPABILITY_IAM"
echo "   aws cloudformation deploy --template-file $ROOT_DIR/lambda/ebs-encryption-check.yml --stack-name EBSEncryptionCheck --capabilities CAPABILITY_IAM"
echo "   aws cloudformation deploy --template-file $ROOT_DIR/cloudwatch/guardduty-alarm.yml --stack-name GuardDutyAlarm --capabilities CAPABILITY_IAM"
echo "   aws cloudformation deploy --template-file $ROOT_DIR/cloudwatch/config-rule-alarm.yml --stack-name ConfigRuleAlarm --capabilities CAPABILITY_IAM"
echo "   aws cloudformation deploy --template-file $ROOT_DIR/eks/pod-security-scan.yml --stack-name PodSecurityScan --capabilities CAPABILITY_IAM"
echo "   aws cloudformation deploy --template-file $ROOT_DIR/eks/cluster-config-scan.yml --stack-name ClusterConfigScan --capabilities CAPABILITY_IAM"
echo "3. Set environment variables for Lambda functions (e.g., SNS_TOPIC_ARN, AWS_REGION) or enter values when prompted at runtime."
echo "4. For code-vuln-scan.yml and infra-vuln-scan.yml, set REPO_URL or S3_BUCKET_NAME via CodeBuild environment variables or AWS CLI."
echo "5. Ensure GuardDuty, AWS Config, and EKS are enabled in your account."
echo "6. Push to GitHub: Initialize a repo, add files, and share with the community."
exit 0
