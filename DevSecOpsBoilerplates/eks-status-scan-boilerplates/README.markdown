# EKS Cluster Status Scanner

## What is This Script?

The EKS Cluster Status Scanner is a Bash script (`scan_eks_cluster.sh`) that scans an Amazon Elastic Kubernetes Service (EKS) cluster to provide a comprehensive status report. It collects critical information about the cluster's configuration, resources, security posture, and operational health, generating a Markdown report (`eks_cluster_status_report.md`) with structured tables and actionable insights. The script is designed for **DevSecOps professionals** to monitor, troubleshoot, and optimize EKS clusters.

### Key Features

- **Cluster Overview**: Reports cluster version, endpoint accessibility, authentication mode, and status.
- **Node Status**: Details node count, instance types, and health issues.
- **Pod Status**: Summarizes pod count, namespaces, and failed pods.
- **Networking**: Lists VPC, subnets, and security groups.
- **Security**: Evaluates IAM roles, RBAC policies, and network policies.
- **Logging and Monitoring**: Checks CloudWatch/CloudTrail integration and logging configuration.
- **Critical Issues**: Identifies misconfigurations, security risks, and performance bottlenecks.
- **Recommendations**: Provides actionable steps to address issues (e.g., disable public endpoints, enable network policies).
- **Interactive Mode**: Prompts for inputs (cluster name, region, SNS topic) with validation and confirmation.
- **Automation-Ready**: Supports non-interactive execution via environment variables for CI/CD or scheduled runs.

### Output

The script generates a Markdown report in `eks-status-scan-boilerplates/reports/eks_cluster_status_report.md`, formatted as tables for easy sharing (e.g., GitHub, Confluence). Example report snippet:

```markdown
# EKS Cluster Status Report

**Generated on**: 2025-04-19 23:23:00 UTC

**Cluster Name**: my-eks-cluster

**Region**: us-east-1

## Cluster Overview
| Attribute | Value | Status | Notes |
|-----------|-------|--------|-------|
| Version | 1.27 | OK | Upgrade if outdated |
| Endpoint Public Access | true | Warning | Disable if not needed |

## Critical Issues
- Public endpoint enabled for cluster my-eks-cluster.
- No network policies detected.

## Recommendations
- Disable public endpoint or restrict access using security groups.
- Implement network policies to restrict pod communication.
```

### Directory Structure

```
eks-status-scan-boilerplates/
├── scripts/
│   ├── scan_eks_cluster.sh
├── reports/
│   ├── eks_cluster_status_report.md
```

## Why Use This Script?

This script is essential for DevSecOps teams managing EKS clusters because it:

- **Enhances Visibility**: Provides a holistic view of cluster health, from nodes to security configurations.
- **Improves Security**: Detects vulnerabilities like public endpoints, missing network policies, or overly permissive RBAC roles.
- **Boosts Operational Efficiency**: Identifies failed pods, unhealthy nodes, and logging gaps, enabling proactive fixes.
- **Supports Compliance**: Helps audit configurations for compliance with best practices (e.g., least privilege, logging enabled).
- **Saves Time**: Automates manual checks, delivering a shareable report in minutes.
- **Enables Automation**: Designed for integration with CI/CD pipelines, Lambda, or cron jobs for continuous monitoring.
- **Empowers Teams**: Offers actionable recommendations, making it accessible to developers, security engineers, and operators.

### Use Cases

- **Troubleshooting**: Diagnose why pods are failing or nodes are unhealthy.
- **Security Audits**: Identify misconfigurations like public endpoints or missing network policies.
- **Cost Optimization**: Highlight oversized nodes or underutilized resources.
- **Compliance Checks**: Verify logging and monitoring for audit requirements.
- **Daily Operations**: Monitor cluster health as part of DevSecOps workflows.

## How to Use the Script

### Prerequisites

- **AWS CLI**: Installed and configured with credentials (`aws configure`).

- **kubectl**: Installed and configured to access the EKS cluster (`aws eks update-kubeconfig`).

- **jq**: For JSON parsing (`sudo apt-get install jq` or equivalent).

- **AWS Permissions**: IAM role with:

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

- **Optional Tools**: `kubectl-who-can` or `kubescape` for advanced RBAC and pod security analysis.

### Setup

1. **Generate the Script**:

   - Save and run the generator script (`generate_eks_status_scan_boilerplates_interactive.sh`):

     ```bash
     chmod +x generate_eks_status_scan_boilerplates_interactive.sh
     ./generate_eks_status_scan_boilerplates_interactive.sh
     ```

   - This creates the `eks-status-scan-boilerplates` directory with `scan_eks_cluster.sh` and a report template.

2. **Install Dependencies**:

   ```bash
   sudo apt-get install jq  # For Ubuntu/Debian
   sudo yum install jq      # For Amazon Linux/CentOS
   ```

3. **Configure AWS and kubectl**:

   ```bash
   aws configure
   aws eks update-kubeconfig --region us-east-1 --name my-eks-cluster
   ```

### Running the Script

The script runs in **interactive mode** by default, prompting for inputs with validation and confirmation.

1. **Run Interactively**:

   ```bash
   eks-status-scan-boilerplates/scripts/scan_eks_cluster.sh
   ```

   - Example interaction:

     ```
     Please provide the following details for the EKS cluster scan:
     Enter EKS_CLUSTER_NAME: my-eks-cluster
     Enter AWS_REGION: us-east-1
     Enter SNS_TOPIC_ARN (or press Enter to skip): arn:aws:sns:us-east-1:123456789012:alerts
     
     You entered:
     EKS_CLUSTER_NAME: my-eks-cluster
     AWS_REGION: us-east-1
     SNS_TOPIC_ARN: arn:aws:sns:us-east-1:123456789012:alerts
     Are these correct? (y/n): y
     Configuring kubectl...
     Scanning cluster overview...
     EKS cluster status scan complete. Report generated at eks-status-scan-boilerplates/reports/eks_cluster_status_report.md.
     ```

2. **Run Non-Interactively** (for automation):

   - Set environment variables:

     ```bash
     export EKS_CLUSTER_NAME=my-eks-cluster
     export AWS_REGION=us-east-1
     export SNS_TOPIC_ARN=arn:aws:sns:us-east-1:123456789012:alerts
     ```

   - Run the script:

     ```bash
     eks-status-scan-boilerplates/scripts/scan_eks_cluster.sh
     ```

3. **Review the Report**:

   - Open `eks-status-scan-boilerplates/reports/eks_cluster_status_report.md` in a Markdown viewer (e.g., GitHub, VS Code).

### Scheduling Periodic Scans

To run the script periodically (e.g., daily), use AWS Lambda or a cron job:

1. **Lambda Setup**:

   - Package the script with dependencies:

     ```bash
     mkdir lambda_package
     cp eks-status-scan-boilerplates/scripts/scan_eks_cluster.sh lambda_package/
     # Add jq and kubectl binaries (requires custom runtime)
     cd lambda_package
     zip -r ../eks_scan_lambda.zip .
     ```

   - Create a Lambda function:

     ```bash
     aws lambda create-function --function-name EKSScan --runtime provided.al2 --role arn:aws:iam::123456789012:role/lambda-eks-scan-role --handler scan_eks_cluster.sh --zip-file fileb://eks_scan_lambda.zip
     ```

   - Set environment variables in Lambda:

     ```bash
     aws lambda update-function-configuration --function-name EKSScan --environment "Variables={EKS_CLUSTER_NAME=my-eks-cluster,AWS_REGION=us-east-1,SNS_TOPIC_ARN=arn:aws:sns:us-east-1:123456789012:alerts}"
     ```

   - Schedule with EventBridge:

     ```bash
     aws events put-rule --name DailyEKSScan --schedule-expression "rate(1 day)"
     aws events put-targets --rule DailyEKSScan --targets "Id=1,Arn=arn:aws:lambda:us-east-1:123456789012:function:EKSScan"
     aws lambda add-permission --function-name EKSScan --statement-id eventbridge --action lambda:InvokeFunction --principal events.amazonaws.com --source-arn arn:aws:events:us-east-1:123456789012:rule/DailyEKSScan
     ```

2. **Cron Job Setup**:

   - Add to crontab:

     ```bash
     crontab -e
     0 0 * * * EKS_CLUSTER_NAME=my-eks-cluster AWS_REGION=us-east-1 SNS_TOPIC_ARN=arn:aws:sns:us-east-1:123456789012:alerts /path/to/scan_eks_cluster.sh
     ```

### Sharing the Script

- Push to GitHub for collaboration:

  ```bash
  cd eks-status-scan-boilerplates
  git init
  git add .
  git commit -m "Add EKS cluster status scanner"
  git remote add origin <your-repo-url>
  git push -u origin main
  ```

- Include this `README.md` and a `LICENSE` (e.g., MIT) to make it community-friendly.

## How Does the Script Work?

### Workflow

1. **Prerequisite Check**:

   - Verifies `aws`, `kubectl`, and `jq` are installed.
   - Ensures AWS credentials are valid (`aws sts get-caller-identity`).

2. **Input Collection**:

   - Prompts for `EKS_CLUSTER_NAME`, `AWS_REGION`, and `SNS_TOPIC_ARN` (optional).
   - Validates inputs and confirms with the user.
   - Checks if the cluster exists (`aws eks describe-cluster`).

3. **Cluster Scanning**:

   - Configures `kubectl` (`aws eks update-kubeconfig`).
   - Queries cluster details (`aws eks describe-cluster`).
   - Collects node, pod, networking, security, and logging data using `kubectl` and AWS CLI.
   - Identifies issues (e.g., public endpoints, failed pods) and generates recommendations.

4. **Report Generation**:

   - Writes a Markdown report with tables for each section (Cluster Overview, Node Status, etc.).
   - Lists critical issues and recommendations in bullet points.

5. **Notifications**:

   - Sends SNS notifications for critical issues if `SNS_TOPIC_ARN` is provided.

### Technical Details

- **Tools Used**: AWS CLI (`eks`, `ec2`, `iam`, `logs`, `cloudwatch`, `sns`), `kubectl`, `jq`.
- **Data Sources**:
  - EKS API: Cluster configuration, VPC settings, logging status.
  - Kubernetes API: Nodes, pods, RBAC roles, network policies.
  - CloudWatch: Alarms for EKS metrics.
- **Error Handling**: Gracefully handles missing tools, invalid inputs, and API failures.
- **Security**: Uses least privilege IAM permissions; avoids storing sensitive data in the report.

## What Information Does It Provide?

The script collects and reports:

- **Cluster Overview**: Version, endpoint accessibility, authentication mode, status.
- **Node Status**: Count, instance types, unhealthy nodes.
- **Pod Status**: Count, namespaces, failed or crashing pods.
- **Networking**: VPC ID, subnets, security groups.
- **Security**: OIDC provider, RBAC role count, network policy usage.
- **Logging and Monitoring**: Control plane logging, CloudWatch alarms.
- **Issues and Recommendations**: Critical findings (e.g., "No network policies detected") with fixes (e.g., "Implement network policies").

### Critical Issues Detected

- Public cluster endpoints (security risk).
- Insecure authentication modes (e.g., not `API_AND_CONFIG_MAP`).
- Unhealthy nodes or failed pods (operational issues).
- Missing network policies (security gap).
- Disabled logging (compliance issue).
- Excessive RBAC roles (potential privilege escalation).

### DevSecOps Insights

- **Security**: Flags misconfigurations and suggests tools like `kubescape` for pod security.
- **Operations**: Highlights resource bottlenecks and node health issues.
- **Development**: Identifies failing pods for debugging.
- **Compliance**: Ensures logging and monitoring for auditability.

## Why Is This Information Useful?

- **Security Engineers**: Detect and fix vulnerabilities (e.g., public endpoints, missing network policies).
- **DevOps Engineers**: Troubleshoot node and pod issues, optimize resource usage.
- **Developers**: Debug application failures by identifying crashing pods.
- **Compliance Teams**: Verify logging and monitoring for regulatory requirements.
- **Managers**: Gain a high-level view of cluster health and risks via the Markdown report.

## How to Extend the Script

### Add More Checks

- **Storage Usage**: Scan persistent volume claims (`kubectl describe pvc`).

- **Cost Analysis**: Integrate AWS Cost Explorer for EKS-related costs.

- **Compliance Frameworks**: Use `kubescape` to check against NSA-CISA or MITRE ATT&CK.

  ```bash
  kubescape scan --submit
  ```

### Integrate with Tools

- **Prometheus**: Add node and pod metrics via a Prometheus endpoint.

- **Kubectl Plugins**:

  - `kubectl-who-can` for RBAC analysis:

    ```bash
    kubectl who-can create pods --all-namespaces
    ```

  - `kubescape` for pod security:

    ```bash
    curl -s https://raw.githubusercontent.com/armosec/kubescape/master/install.sh | /bin/bash
    ```

### Customize Output

- **JSON Output**: Modify `write_report` to generate JSON for API integration.

- **Slack Notifications**: Replace SNS with a Slack webhook:

  ```bash
  curl -X POST -H 'Content-type: application/json' --data "{\"text\":\"EKS Issues: ${ISSUES[*]}\"}" <slack-webhook-url>
  ```

## Troubleshooting

### Common Issues

- **"AWS CLI not installed"**:
  - Install AWS CLI: `pip install awscli`
  - Verify: `aws --version`
- **"Cluster not found"**:
  - Check cluster name and region: `aws eks list-clusters --region us-east-1`
  - Update kubeconfig: `aws eks update-kubeconfig --region us-east-1 --name my-eks-cluster`
- **"Failed to send SNS notification"**:
  - Verify SNS topic: `aws sns list-topics --region us-east-1`
  - Create topic: `aws sns create-topic --name alerts --region us-east-1`
- **Report not generated**:
  - Check permissions: `chmod u+w eks-status-scan-boilerplates/reports`
  - Verify disk space: `df -h .`

### Debugging

- Run with debug mode:

  ```bash
  bash -x eks-status-scan-boilerplates/scripts/scan_eks_cluster.sh
  ```

- Check kubectl connectivity:

  ```bash
  kubectl cluster-info
  ```

- Validate AWS credentials:

  ```bash
  aws sts get-caller-identity
  ```

## Limitations

- **Storage Metrics**: Doesn’t scan persistent volume usage (extend with `kubectl describe pvc`).
- **Detailed Metrics**: Lacks CPU/memory utilization (integrate with Prometheus or CloudWatch Container Insights).
- **IAM Permissions**: Broad permissions for simplicity; scope to specific resources in production (e.g., `arn:aws:eks:*:123456789012:cluster/*`).
- **Lambda Compatibility**: Requires custom runtime for bash scripts with `kubectl` and `jq`.

## Contributing

- Fork the repository and submit pull requests for new features or bug fixes.
- Suggest enhancements (e.g., additional checks, output formats) via GitHub issues.
- Share your use cases to improve the script for the community.

## License

MIT License - Feel free to use, modify, and distribute.

## Contact

For questions or feedback, open an issue on the GitHub repository or contact your DevSecOps team.

---

*Prepared by {Partha Sarathi Kundu} on April 19, 2025, for the EKS Cluster Status Scanner project.*