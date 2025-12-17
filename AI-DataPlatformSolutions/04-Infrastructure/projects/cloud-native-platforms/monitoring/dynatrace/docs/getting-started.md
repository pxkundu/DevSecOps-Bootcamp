# 🚀 Getting Started with Dynatrace AWS Serverless Monitoring

## 📋 Prerequisites

Before you begin, ensure you have the following:

### Required Accounts & Access
- [ ] **Dynatrace Environment**: SaaS or Managed (trial available at [dynatrace.com](https://www.dynatrace.com/trial/))
- [ ] **AWS Account**: With admin access or appropriate IAM permissions
- [ ] **Git**: For cloning this repository

### Required Tools
```bash
# Check tool versions
aws --version          # >= 2.0
terraform --version    # >= 1.0
python3 --version      # >= 3.9
jq --version           # >= 1.6
curl --version         # any recent version
```

### Required Dynatrace API Tokens

You'll need two API tokens with specific permissions:

#### 1. API Token (for configuration)
```
Permissions required:
- Read configuration
- Write configuration
- Access problem and event feed, metrics (v2)
- Read metrics
- Ingest metrics
- Read SLO
- Write SLO
- Read synthetic locations
- Create and read synthetic monitors
- Write synthetic monitors
```

#### 2. PaaS Token (for OneAgent/Extension)
```
Permissions required:
- PaaS integration - Installer download
```

## 🔧 Step 1: Environment Setup

### 1.1 Clone the Repository

```bash
git clone <repository-url>
cd cloud-native-platforms/monitoring/dynatrace
```

### 1.2 Set Environment Variables

Create a `.env` file (don't commit this!):

```bash
# Dynatrace Configuration
export DT_TENANT_URL="https://your-tenant-id.live.dynatrace.com"
export DT_API_TOKEN="dt0c01.XXXXXXXXXXXXXXXXXXXXXX.YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY"
export DT_PAAS_TOKEN="dt0c01.XXXXXXXXXXXXXXXXXXXXXX.ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ"

# AWS Configuration
export AWS_REGION="us-east-1"
export AWS_ACCOUNT_ID="123456789012"
export ENVIRONMENT="dev"  # dev, staging, production

# Optional: AWS Profile
export AWS_PROFILE="your-profile"

# Load variables
source .env
```

### 1.3 Verify Connectivity

```bash
# Test Dynatrace API access
curl -s -X GET "${DT_TENANT_URL}/api/v2/entities" \
  -H "Authorization: Api-Token ${DT_API_TOKEN}" \
  -H "Content-Type: application/json" | jq '.totalCount'

# Expected: A number (entities count)

# Test AWS access
aws sts get-caller-identity
# Expected: Your AWS account information
```

## 📡 Step 2: Configure AWS Integration

### 2.1 Create IAM Role for Dynatrace

The AWS integration requires an IAM role that Dynatrace can assume:

```bash
cd infrastructure/terraform
terraform init
terraform apply -target=module.dynatrace_iam_role \
  -var="dynatrace_external_id=YOUR_EXTERNAL_ID"
```

Alternatively, use CloudFormation:

```bash
aws cloudformation create-stack \
  --stack-name dynatrace-monitoring-role \
  --template-body file://infrastructure/cloudformation/dynatrace-iam-role.yaml \
  --parameters ParameterKey=ExternalId,ParameterValue=YOUR_EXTERNAL_ID \
  --capabilities CAPABILITY_NAMED_IAM
```

### 2.2 Configure AWS Integration in Dynatrace

1. Navigate to **Settings** → **Cloud and virtualization** → **AWS**
2. Click **Connect new instance**
3. Enter:
   - **Connection name**: `production-serverless` (or your preferred name)
   - **IAM Role ARN**: The ARN from step 2.1
   - **Your AWS Account ID**: Your 12-digit AWS account ID
   - **External ID**: The external ID you used in step 2.1
4. Select services to monitor:
   - ✅ Lambda
   - ✅ API Gateway
   - ✅ DynamoDB
   - ✅ SQS
   - ✅ SNS
   - ✅ Step Functions
   - ✅ S3 (optional, can generate many metrics)
5. Click **Connect**

### 2.3 Verify AWS Integration

Wait 5-10 minutes, then verify in Dynatrace:

1. Go to **Infrastructure** → **AWS**
2. You should see your AWS account listed
3. Check **Technologies & Processes** for discovered Lambda functions

## 🔌 Step 3: Deploy Lambda Extension

### 3.1 Get the Dynatrace Lambda Layer ARN

The layer ARN varies by region. Find your region's ARN:

```bash
# Get layer ARN for your region
# Format: arn:aws:lambda:REGION:725887861453:layer:Dynatrace_OneAgent_1_277_27_20240221-135729:1

# Current regions and latest versions available at:
# https://www.dynatrace.com/support/help/setup-and-configuration/setup-on-container-platforms/aws/deploy-oneagent-as-lambda-extension
```

### 3.2 Configure Lambda Functions

#### Option A: Using Environment Variables

Add these environment variables to your Lambda functions:

```bash
# Required
DT_TENANT="your-tenant-id"           # Just the ID, not full URL
DT_CLUSTER_ID="-1"                    # -1 for SaaS, cluster ID for Managed
DT_CONNECTION_BASE_URL="https://your-tenant-id.live.dynatrace.com"
DT_CONNECTION_AUTH_TOKEN="dt0c01.XX.YY"  # Your PaaS token

# Optional (but recommended)
AWS_LAMBDA_EXEC_WRAPPER="/opt/dynatrace"
DT_OPEN_TELEMETRY_ENABLE_INTEGRATION="true"
DT_LOGLEVELCON="info"
```

#### Option B: Using AWS Secrets Manager

Store credentials securely:

```bash
# Create secret
aws secretsmanager create-secret \
  --name "dynatrace/lambda-extension" \
  --secret-string '{
    "DT_TENANT": "your-tenant-id",
    "DT_CONNECTION_BASE_URL": "https://your-tenant-id.live.dynatrace.com",
    "DT_CONNECTION_AUTH_TOKEN": "dt0c01.XX.YY"
  }'

# Reference in Lambda (add IAM permissions first)
DT_CONNECTION_AUTH_TOKEN="sm://dynatrace/lambda-extension:DT_CONNECTION_AUTH_TOKEN"
```

### 3.3 Deploy Extension to Lambda Functions

#### Using Terraform

```hcl
# In your Lambda Terraform configuration
resource "aws_lambda_function" "example" {
  function_name = "my-monitored-function"
  runtime       = "python3.11"
  handler       = "handler.lambda_handler"
  
  # Add Dynatrace layer
  layers = [
    "arn:aws:lambda:${var.aws_region}:725887861453:layer:Dynatrace_OneAgent:${var.dt_layer_version}"
  ]
  
  environment {
    variables = {
      DT_TENANT                    = var.dynatrace_tenant
      DT_CLUSTER_ID                = "-1"
      DT_CONNECTION_BASE_URL       = var.dynatrace_url
      DT_CONNECTION_AUTH_TOKEN     = var.dynatrace_paas_token
      AWS_LAMBDA_EXEC_WRAPPER      = "/opt/dynatrace"
    }
  }
}
```

#### Using Serverless Framework

```yaml
# serverless.yaml
service: my-serverless-app

provider:
  name: aws
  runtime: python3.11
  region: us-east-1

custom:
  dynatrace:
    tenant: ${env:DT_TENANT}
    connectionUrl: ${env:DT_CONNECTION_BASE_URL}
    authToken: ${env:DT_CONNECTION_AUTH_TOKEN}

functions:
  hello:
    handler: handler.hello
    layers:
      - arn:aws:lambda:${self:provider.region}:725887861453:layer:Dynatrace_OneAgent:1
    environment:
      DT_TENANT: ${self:custom.dynatrace.tenant}
      DT_CLUSTER_ID: "-1"
      DT_CONNECTION_BASE_URL: ${self:custom.dynatrace.connectionUrl}
      DT_CONNECTION_AUTH_TOKEN: ${self:custom.dynatrace.authToken}
      AWS_LAMBDA_EXEC_WRAPPER: /opt/dynatrace
```

#### Using AWS SAM

```yaml
# template.yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31

Globals:
  Function:
    Layers:
      - !Sub arn:aws:lambda:${AWS::Region}:725887861453:layer:Dynatrace_OneAgent:1
    Environment:
      Variables:
        DT_TENANT: !Ref DynatraceTenant
        DT_CLUSTER_ID: "-1"
        DT_CONNECTION_BASE_URL: !Ref DynatraceUrl
        AWS_LAMBDA_EXEC_WRAPPER: /opt/dynatrace

Parameters:
  DynatraceTenant:
    Type: String
  DynatraceUrl:
    Type: String

Resources:
  MyFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: index.handler
      Runtime: python3.11
```

### 3.4 Verify Lambda Extension

1. Invoke your Lambda function
2. Check CloudWatch Logs for Dynatrace extension output:
   ```
   [dynatrace] Dynatrace Lambda extension started
   [dynatrace] Connected to Dynatrace cluster
   ```
3. In Dynatrace, go to **Services** and look for your Lambda function

## 📊 Step 4: Configure Dashboards

### 4.1 Import Pre-built Dashboards

Use the provided dashboard definitions:

```bash
# Import Lambda overview dashboard
curl -X POST "${DT_TENANT_URL}/api/config/v1/dashboards" \
  -H "Authorization: Api-Token ${DT_API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d @dashboards/lambda-overview.json

# Import API Gateway dashboard
curl -X POST "${DT_TENANT_URL}/api/config/v1/dashboards" \
  -H "Authorization: Api-Token ${DT_API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d @dashboards/api-gateway-metrics.json
```

### 4.2 Create Custom Dashboard (Optional)

1. Navigate to **Dashboards** in Dynatrace
2. Click **Create dashboard**
3. Add tiles for:
   - Lambda invocations (timeseries)
   - Error rates (timeseries)
   - Cold start percentage (single value)
   - P95 duration (timeseries)
   - Top 10 slowest functions (table)

## 🚨 Step 5: Configure Alerting

### 5.1 Create Alerting Profile

```bash
# Create alerting profile
curl -X POST "${DT_TENANT_URL}/api/config/v1/alertingProfiles" \
  -H "Authorization: Api-Token ${DT_API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d @configuration/dynatrace-api/alerting-profiles.json
```

### 5.2 Configure Notification Channels

#### Slack Integration

1. Create a Slack App with incoming webhook
2. Configure in Dynatrace:
   ```bash
   curl -X POST "${DT_TENANT_URL}/api/config/v1/notifications" \
     -H "Authorization: Api-Token ${DT_API_TOKEN}" \
     -H "Content-Type: application/json" \
     -d @alerting/notification-integrations/slack.json
   ```

#### PagerDuty Integration

1. Get your PagerDuty service integration key
2. Configure in Dynatrace:
   ```bash
   curl -X POST "${DT_TENANT_URL}/api/config/v1/notifications" \
     -H "Authorization: Api-Token ${DT_API_TOKEN}" \
     -H "Content-Type: application/json" \
     -d @alerting/notification-integrations/pagerduty.json
   ```

## ✅ Step 6: Validation Checklist

Run the validation script:

```bash
./automation/scripts/validate-setup.sh
```

Or manually verify:

### AWS Integration
- [ ] AWS integration shows as "Connected" in Dynatrace
- [ ] CloudWatch metrics are being collected
- [ ] AWS services appear in Infrastructure view

### Lambda Monitoring
- [ ] Lambda functions appear in Services view
- [ ] Distributed traces are being captured
- [ ] Custom metrics are visible (if configured)
- [ ] Cold starts are being detected

### Dashboards
- [ ] Lambda overview dashboard loads correctly
- [ ] Metrics are populating in charts
- [ ] Filters work as expected

### Alerting
- [ ] Test alert fires correctly
- [ ] Notifications reach configured channels
- [ ] Alert routing works as expected

## 🎉 Next Steps

Congratulations! You have a working Dynatrace monitoring setup. Here's what to do next:

1. **Expand Coverage**: Add the Lambda extension to more functions
2. **Customize Dashboards**: Create team-specific views
3. **Configure SLOs**: Define service level objectives
4. **Set Up Synthetic Monitoring**: Proactive availability testing
5. **Implement Custom Metrics**: Track business KPIs

## 🆘 Troubleshooting

### Common Issues

#### Lambda extension not connecting
```bash
# Check CloudWatch Logs for errors
aws logs filter-log-events \
  --log-group-name "/aws/lambda/your-function" \
  --filter-pattern "dynatrace"
```

#### No AWS metrics in Dynatrace
- Verify IAM role permissions
- Check external ID matches
- Wait 10-15 minutes for initial data

#### Traces not appearing
- Verify `AWS_LAMBDA_EXEC_WRAPPER` is set
- Check PaaS token has correct permissions
- Ensure function is being invoked

See [Troubleshooting Guide](troubleshooting.md) for more solutions.

## 📚 Additional Resources

- [Dynatrace Documentation](https://www.dynatrace.com/support/help/)
- [AWS Lambda Best Practices](https://docs.aws.amazon.com/lambda/latest/operatorguide/best-practices.html)
- [Dynatrace API Reference](https://www.dynatrace.com/support/help/dynatrace-api)
- [Configuration Guide](configuration-guide.md)
- [Best Practices](best-practices.md)

