Next steps:
1. Install dependencies:
   sudo apt-get install jq  # Or equivalent for your OS
2. Configure AWS credentials and kubectl:
   aws configure
   aws eks update-kubeconfig --region {{AWS_REGION}} --name {{EKS_CLUSTER_NAME}}
3. Set environment variables or provide inputs when prompted:
   export EKS_CLUSTER_NAME=<your-cluster-name>
   export AWS_REGION=us-east-1
   export SNS_TOPIC_ARN=arn:aws:sns:us-east-1:123456789012:alerts
4. Run the scan script:
   eks-status-scan-boilerplates/scripts/scan_eks_cluster.sh
5. Review the generated report at eks-status-scan-boilerplates/reports/eks_cluster_status_report.md.
6. Schedule the script using AWS Lambda or a cron job for periodic scans:
   - Package the script and dependencies.
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
           "eks:DescribeCluster",
           "ec2:DescribeInstances",
           "iam:GetRole",
           "logs:DescribeLogGroups",
           "cloudwatch:DescribeAlarms",
           "sns:Publish"
         ],
         "Resource": "*"
       }
     ]
   }
   ```
8. Optional: Install kubectl plugins for advanced security scanning:
   - kubectl-who-can: https://github.com/aquasecurity/kubectl-who-can
   - kubescape: https://github.com/armosec/kubescape
