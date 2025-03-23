#!/bin/bash
aws iam update-role --role-name JenkinsSlaveRole --description "Updated role for ECR access"
aws iam put-role-policy --role-name JenkinsSlaveRole --policy-name JenkinsSlavePolicy --policy-document '{
  "Version": "2012-10-17",
  "Statement": [
    {"Effect": "Allow", "Action": ["ecr:Get*", "ecr:Batch*", "ecr:Describe*", "ecr:PutImage", "ecr:InitiateLayerUpload", "ecr:UploadLayerPart", "ecr:CompleteLayerUpload"], "Resource": "arn:aws:ecr:us-east-1:<account-id>:repository/task-*"},
    {"Effect": "Allow", "Action": "ecr:GetAuthorizationToken", "Resource": "*"},
    {"Effect": "Allow", "Action": ["s3:PutObject", "s3:GetObject"], "Resource": "arn:aws:s3:::<your-bucket>/*"},
    {"Effect": "Allow", "Action": "secretsmanager:GetSecretValue", "Resource": "arn:aws:secretsmanager:us-east-1:<account-id>:secret:github-token-*"},
    {"Effect": "Allow", "Action": "logs:PutLogEvents", "Resource": "arn:aws:logs:us-east-1:<account-id>:log-group:JenkinsLogs:*"}
  ]
}'
