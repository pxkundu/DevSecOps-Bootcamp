Next steps:
1. Install dependencies for generate_cost_audit.py:
   pip install boto3
2. Configure AWS credentials (AWS CLI or environment variables).
3. Replace placeholders in reports/cost_audit_report.md (e.g., {{AWS_REGION}}, {{SNS_TOPIC_ARN}}) or set environment variables:
   export AWS_REGION=us-east-1
   export SNS_TOPIC_ARN=arn:aws:sns:us-east-1:123456789012:alerts
4. Run the audit script to generate the report:
   python3 aws-cost-audit-boilerplates/scripts/generate_cost_audit.py
5. Review the generated report at aws-cost-audit-boilerplates/reports/cost_audit_report.md.
6. Schedule the script using AWS Lambda and EventBridge for periodic audits:
   - Package the Python script with dependencies.
   - Create a Lambda function with the IAM role below.
   - Set a daily EventBridge rule to trigger the Lambda function.
7. IAM role for Lambda (if scheduled):
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Action": [
           "ec2:DescribeInstances",
           "rds:DescribeDBInstances",
           "s3:ListAllMyBuckets",
           "lambda:ListFunctions",
           "dynamodb:ListTables",
           "dynamodb:DescribeTable",
           "ce:GetCostAndUsage",
           "sns:Publish"
         ],
         "Resource": "*"
       }
     ]
   }
   ```

   ---

*Prepared by {Partha Sarathi Kundu} on April 19, 2025, for the AWS Boilerplate writing project.*