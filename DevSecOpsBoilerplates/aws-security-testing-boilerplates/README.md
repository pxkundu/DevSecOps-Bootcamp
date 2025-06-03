Next steps:
1. Replace placeholders ({{SNS_TOPIC_ARN}}, {{AWS_REGION}}, {{REPO_URL}}, {{EKS_CLUSTER_NAME}}) in the templates with your values.
2. Deploy templates using AWS CLI:
   aws cloudformation deploy --template-file aws-security-testing-boilerplates/cloudformation/iam-policy-audit.yml --stack-name IAMPolicyAudit --capabilities CAPABILITY_IAM
   aws cloudformation deploy --template-file aws-security-testing-boilerplates/cloudformation/kms-key-audit.yml --stack-name KMSKeyAudit --capabilities CAPABILITY_IAM
   aws cloudformation deploy --template-file aws-security-testing-boilerplates/codebuild/code-vuln-scan.yml --stack-name CodeVulnScan --capabilities CAPABILITY_IAM
   aws cloudformation deploy --template-file aws-security-testing-boilerplates/codebuild/infra-vuln-scan.yml --stack-name InfraVulnScan --capabilities CAPABILITY_IAM
   aws cloudformation deploy --template-file aws-security-testing-boilerplates/lambda/secrets-exposure-scan.yml --stack-name SecretsExposure --capabilities CAPABILITY_IAM
   aws cloudformation deploy --template-file aws-security-testing-boilerplates/lambda/ebs-encryption-check.yml --stack-name EBSEncryptionCheck --capabilities CAPABILITY_IAM
   aws cloudformation deploy --template-file aws-security-testing-boilerplates/cloudwatch/guardduty-alarm.yml --stack-name GuardDutyAlarm --capabilities CAPABILITY_IAM
   aws cloudformation deploy --template-file aws-security-testing-boilerplates/cloudwatch/config-rule-alarm.yml --stack-name ConfigRuleAlarm --capabilities CAPABILITY_IAM
   aws cloudformation deploy --template-file aws-security-testing-boilerplates/eks/pod-security-scan.yml --stack-name PodSecurityScan --capabilities CAPABILITY_IAM
   aws cloudformation deploy --template-file aws-security-testing-boilerplates/eks/cluster-config-scan.yml --stack-name ClusterConfigScan --capabilities CAPABILITY_IAM
3. Set environment variables for Lambda functions (e.g., SNS_TOPIC_ARN, AWS_REGION) or enter values when prompted at runtime.
4. For code-vuln-scan.yml and infra-vuln-scan.yml, set REPO_URL or S3_BUCKET_NAME via CodeBuild environment variables or AWS CLI.
5. Ensure GuardDuty, AWS Config, and EKS are enabled in your account.

---

*Prepared by {Partha Sarathi Kundu} on April 19, 2025, for the AWS Boilerplate writing project.*