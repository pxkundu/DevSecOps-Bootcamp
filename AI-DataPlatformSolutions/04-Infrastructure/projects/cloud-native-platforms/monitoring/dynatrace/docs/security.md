# 🔐 Security Guide

## 📋 Overview

This guide covers security considerations, best practices, and compliance requirements for the Dynatrace AWS Serverless monitoring solution.

## 🏛️ Security Architecture

```mermaid
graph TB
    subgraph "AWS Account"
        subgraph "VPC"
            subgraph "Private Subnet"
                AG[ActiveGate EC2/ECS]
                Lambda[Lambda Functions]
            end
            subgraph "Public Subnet"
                NAT[NAT Gateway]
            end
        end
        
        SM[Secrets Manager]
        IAM[IAM Roles]
        KMS[KMS Keys]
        CW[CloudWatch]
    end
    
    subgraph "Dynatrace Platform"
        DT[Dynatrace SaaS]
        API[Dynatrace API]
    end
    
    Lambda -->|Extension| AG
    AG -->|HTTPS 443| NAT
    NAT -->|Encrypted| DT
    SM -->|Credentials| Lambda
    IAM -->|Permissions| AG
    KMS -->|Encryption| SM
    CW -->|Metrics| DT
    
    style SM fill:#f9f,stroke:#333
    style KMS fill:#f9f,stroke:#333
    style IAM fill:#ff9,stroke:#333
```

## 🔑 Credential Management

### Token Types and Usage

```mermaid
flowchart LR
    subgraph "Token Types"
        API[API Token]
        PAAS[PaaS Token]
        DATA[Data Ingest Token]
    end
    
    subgraph "Usage"
        CONFIG[Configuration API]
        AGENT[OneAgent/Extension]
        METRICS[Metrics Ingestion]
    end
    
    API --> CONFIG
    PAAS --> AGENT
    DATA --> METRICS
```

### Secrets Manager Integration

```bash
# Create secret with encryption
aws secretsmanager create-secret \
  --name "dynatrace/production/credentials" \
  --description "Dynatrace monitoring credentials" \
  --kms-key-id alias/dynatrace-secrets \
  --secret-string '{
    "api_token": "dt0c01.XXXXXX.YYYYYYYY",
    "paas_token": "dt0c01.XXXXXX.ZZZZZZZZ",
    "tenant_url": "https://abc12345.live.dynatrace.com"
  }'
```

### Token Rotation Policy

```mermaid
sequenceDiagram
    participant Rotation as Rotation Lambda
    participant SM as Secrets Manager
    participant DT as Dynatrace API
    participant Config as Configuration
    
    Rotation->>SM: Get current secret
    Rotation->>DT: Create new token
    DT-->>Rotation: New token value
    Rotation->>SM: Update secret (AWSPENDING)
    Rotation->>Config: Test new token
    Config-->>Rotation: Validation success
    Rotation->>SM: Finish rotation (AWSCURRENT)
    Rotation->>DT: Revoke old token
```

**Rotation Lambda Implementation:**

```python
import boto3
import requests
import json

def lambda_handler(event, context):
    """Rotate Dynatrace API token."""
    secret_id = event['SecretId']
    step = event['Step']
    
    sm_client = boto3.client('secretsmanager')
    
    if step == 'createSecret':
        create_new_token(sm_client, secret_id, event['ClientRequestToken'])
    elif step == 'setSecret':
        # Token already set in Dynatrace during create
        pass
    elif step == 'testSecret':
        test_token(sm_client, secret_id, event['ClientRequestToken'])
    elif step == 'finishSecret':
        finish_rotation(sm_client, secret_id, event['ClientRequestToken'])

def create_new_token(sm_client, secret_id, token):
    """Create new Dynatrace token."""
    current = sm_client.get_secret_value(SecretId=secret_id)
    secret_dict = json.loads(current['SecretString'])
    
    # Create new token via Dynatrace API
    response = requests.post(
        f"{secret_dict['tenant_url']}/api/v2/apiTokens",
        headers={"Authorization": f"Api-Token {secret_dict['api_token']}"},
        json={
            "name": f"rotated-{token[:8]}",
            "scopes": ["metrics.ingest", "entities.read"]
        }
    )
    new_token = response.json()['token']
    
    # Store as pending
    secret_dict['api_token'] = new_token
    sm_client.put_secret_value(
        SecretId=secret_id,
        ClientRequestToken=token,
        SecretString=json.dumps(secret_dict),
        VersionStages=['AWSPENDING']
    )
```

## 🛡️ IAM Security

### Principle of Least Privilege

```mermaid
graph TB
    subgraph "IAM Role Hierarchy"
        Admin[Admin Role]
        Deploy[Deployment Role]
        Monitor[Monitoring Role]
        Read[Read-Only Role]
    end
    
    subgraph "Permissions"
        Full[Full Access]
        Write[Write Config]
        Metrics[Read Metrics]
        View[View Only]
    end
    
    Admin --> Full
    Deploy --> Write
    Monitor --> Metrics
    Read --> View
    
    style Admin fill:#f00,stroke:#333
    style Deploy fill:#ff0,stroke:#333
    style Monitor fill:#0f0,stroke:#333
    style Read fill:#0ff,stroke:#333
```

### Dynatrace AWS Role Policy

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DynatraceCloudWatchAccess",
      "Effect": "Allow",
      "Action": [
        "cloudwatch:GetMetricStatistics",
        "cloudwatch:ListMetrics",
        "cloudwatch:GetMetricData"
      ],
      "Resource": "*",
      "Condition": {
        "StringEquals": {
          "aws:RequestedRegion": [
            "us-east-1",
            "us-west-2",
            "eu-west-1"
          ]
        }
      }
    },
    {
      "Sid": "DynatraceResourceDiscovery",
      "Effect": "Allow",
      "Action": [
        "tag:GetResources",
        "lambda:ListFunctions",
        "lambda:ListTags",
        "dynamodb:ListTables",
        "dynamodb:DescribeTable",
        "sqs:ListQueues",
        "sqs:GetQueueAttributes",
        "sns:ListTopics"
      ],
      "Resource": "*"
    },
    {
      "Sid": "DenyDestructiveActions",
      "Effect": "Deny",
      "Action": [
        "lambda:DeleteFunction",
        "dynamodb:DeleteTable",
        "sqs:DeleteQueue",
        "sns:DeleteTopic"
      ],
      "Resource": "*"
    }
  ]
}
```

### Trust Policy with External ID

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::509560245411:root"
      },
      "Action": "sts:AssumeRole",
      "Condition": {
        "StringEquals": {
          "sts:ExternalId": "YOUR_UNIQUE_EXTERNAL_ID"
        }
      }
    }
  ]
}
```

## 🔒 Data Protection

### Data Flow Security

```mermaid
flowchart LR
    subgraph "Source"
        Lambda[Lambda Function]
        API[API Gateway]
    end
    
    subgraph "Transport"
        TLS[TLS 1.3]
    end
    
    subgraph "Destination"
        DT[Dynatrace]
    end
    
    subgraph "Protection"
        Mask[Data Masking]
        Encrypt[Encryption]
    end
    
    Lambda -->|Traces/Logs| Mask
    API -->|Metrics| Mask
    Mask --> Encrypt
    Encrypt --> TLS
    TLS --> DT
```

### Data Masking Configuration

```json
{
  "sensitiveDataMasking": {
    "enabled": true,
    "rules": [
      {
        "name": "Credit Card Numbers",
        "pattern": "\\b(?:\\d{4}[- ]?){3}\\d{4}\\b",
        "replacement": "****-****-****-****",
        "applyTo": ["logs", "request_attributes"]
      },
      {
        "name": "Social Security Numbers",
        "pattern": "\\b\\d{3}-\\d{2}-\\d{4}\\b",
        "replacement": "***-**-****",
        "applyTo": ["logs", "request_attributes"]
      },
      {
        "name": "Email Addresses",
        "pattern": "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}",
        "replacement": "***@***.***",
        "applyTo": ["logs"]
      },
      {
        "name": "API Keys",
        "pattern": "(?i)(api[_-]?key|apikey)[\"']?\\s*[:=]\\s*[\"']?([\\w-]+)",
        "replacement": "$1=***REDACTED***",
        "applyTo": ["logs", "request_attributes"]
      }
    ]
  }
}
```

### Encryption Standards

| Data State | Encryption Method | Key Management |
|------------|-------------------|----------------|
| At Rest (AWS) | AES-256 | AWS KMS |
| In Transit | TLS 1.3 | Certificate Manager |
| At Rest (Dynatrace) | AES-256 | Dynatrace Managed Keys |
| Secrets | AES-256 | Customer Managed KMS |

## 🌐 Network Security

### Network Architecture

```mermaid
graph TB
    subgraph "Internet"
        DT[Dynatrace SaaS]
    end
    
    subgraph "AWS VPC"
        subgraph "Public Subnet"
            IGW[Internet Gateway]
            NAT[NAT Gateway]
        end
        
        subgraph "Private Subnet A"
            Lambda1[Lambda VPC]
            AG[ActiveGate]
        end
        
        subgraph "Private Subnet B"
            Lambda2[Lambda VPC]
        end
    end
    
    DT <-->|HTTPS 443| IGW
    IGW --> NAT
    NAT --> Lambda1
    NAT --> Lambda2
    Lambda1 --> AG
    Lambda2 --> AG
    AG --> NAT
```

### Security Group Configuration

```hcl
# ActiveGate Security Group
resource "aws_security_group" "activegate" {
  name        = "dynatrace-activegate-sg"
  description = "Security group for Dynatrace ActiveGate"
  vpc_id      = var.vpc_id

  # Inbound from Lambda functions
  ingress {
    from_port       = 9999
    to_port         = 9999
    protocol        = "tcp"
    security_groups = [aws_security_group.lambda.id]
    description     = "ActiveGate communication port"
  }

  # Outbound to Dynatrace
  egress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "HTTPS to Dynatrace SaaS"
  }

  tags = {
    Name = "dynatrace-activegate-sg"
  }
}

# Lambda Security Group
resource "aws_security_group" "lambda" {
  name        = "dynatrace-lambda-sg"
  description = "Security group for Lambda functions"
  vpc_id      = var.vpc_id

  # Outbound to ActiveGate
  egress {
    from_port       = 9999
    to_port         = 9999
    protocol        = "tcp"
    security_groups = [aws_security_group.activegate.id]
    description     = "To ActiveGate"
  }

  # Outbound HTTPS (for functions not using ActiveGate)
  egress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "HTTPS outbound"
  }
}
```

### VPC Endpoints (Optional)

```hcl
# For enhanced security, use VPC endpoints
resource "aws_vpc_endpoint" "secrets_manager" {
  vpc_id              = var.vpc_id
  service_name        = "com.amazonaws.${var.region}.secretsmanager"
  vpc_endpoint_type   = "Interface"
  subnet_ids          = var.private_subnet_ids
  security_group_ids  = [aws_security_group.vpc_endpoints.id]
  private_dns_enabled = true
}

resource "aws_vpc_endpoint" "cloudwatch" {
  vpc_id              = var.vpc_id
  service_name        = "com.amazonaws.${var.region}.monitoring"
  vpc_endpoint_type   = "Interface"
  subnet_ids          = var.private_subnet_ids
  security_group_ids  = [aws_security_group.vpc_endpoints.id]
  private_dns_enabled = true
}
```

## 📋 Compliance

### Compliance Framework Mapping

```mermaid
graph LR
    subgraph "Compliance Frameworks"
        SOC2[SOC 2 Type II]
        ISO[ISO 27001]
        GDPR[GDPR]
        HIPAA[HIPAA]
        PCI[PCI DSS]
    end
    
    subgraph "Controls"
        AC[Access Control]
        AU[Audit Logging]
        EN[Encryption]
        DM[Data Masking]
        RM[Retention Mgmt]
    end
    
    SOC2 --> AC
    SOC2 --> AU
    ISO --> EN
    GDPR --> DM
    GDPR --> RM
    HIPAA --> EN
    HIPAA --> AC
    PCI --> EN
    PCI --> DM
```

### Audit Logging

```python
# Audit logging for Dynatrace configuration changes
import json
import boto3
from datetime import datetime

def log_config_change(change_type, resource, user, details):
    """Log configuration changes to CloudWatch."""
    logs_client = boto3.client('logs')
    
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "change_type": change_type,
        "resource": resource,
        "user": user,
        "details": details,
        "source": "dynatrace-monitoring"
    }
    
    logs_client.put_log_events(
        logGroupName="/dynatrace/audit-logs",
        logStreamName=datetime.utcnow().strftime("%Y/%m/%d"),
        logEvents=[{
            "timestamp": int(datetime.utcnow().timestamp() * 1000),
            "message": json.dumps(log_entry)
        }]
    )
```

### Data Retention Policy

```yaml
data_retention:
  metrics:
    high_resolution: 7 days    # 1-minute granularity
    standard: 35 days          # 5-minute granularity
    aggregated: 3 years        # 1-hour granularity
    
  traces:
    detailed: 35 days
    service_flow: 35 days
    
  logs:
    raw: 35 days
    indexed: 90 days
    
  session_replay:
    recordings: 35 days
    
  problems:
    open: indefinite
    closed: 365 days
```

## 🔍 Security Monitoring

### Security Alerts

```json
{
  "securityAlerts": [
    {
      "name": "Failed Authentication Spike",
      "description": "Alert when authentication failures spike",
      "metricSelector": "builtin:security.authentication.failures",
      "threshold": 100,
      "timeframe": "5m",
      "severity": "HIGH"
    },
    {
      "name": "Unusual API Access Pattern",
      "description": "Detect anomalous API access",
      "type": "ANOMALY_DETECTION",
      "baseline": "ADAPTIVE",
      "sensitivity": "HIGH"
    },
    {
      "name": "Token Usage from New Location",
      "description": "API token used from unfamiliar IP",
      "type": "GEOLOCATION_CHANGE",
      "severity": "MEDIUM"
    }
  ]
}
```

### Security Dashboard

```mermaid
graph TB
    subgraph "Security Dashboard"
        subgraph "Authentication"
            A1[Login Success Rate]
            A2[Failed Attempts]
            A3[MFA Usage]
        end
        
        subgraph "Access Patterns"
            B1[API Calls by User]
            B2[Geographic Distribution]
            B3[Time-based Patterns]
        end
        
        subgraph "Data Protection"
            C1[Encryption Status]
            C2[Masking Applied]
            C3[Data Exports]
        end
        
        subgraph "Compliance"
            D1[Policy Violations]
            D2[Audit Log Status]
            D3[Certificate Expiry]
        end
    end
```

## ✅ Security Checklist

### Pre-Deployment

```markdown
## Security Checklist - Pre-Deployment

### Credential Management
- [ ] API tokens stored in Secrets Manager
- [ ] PaaS tokens have minimal required scopes
- [ ] Token rotation policy configured
- [ ] KMS key created for secret encryption

### IAM Configuration
- [ ] Dedicated IAM role for Dynatrace
- [ ] External ID configured for cross-account access
- [ ] Least privilege permissions applied
- [ ] Resource-based conditions where possible

### Network Security
- [ ] ActiveGate in private subnet
- [ ] Security groups configured correctly
- [ ] VPC endpoints for AWS services (optional)
- [ ] TLS 1.2+ enforced

### Data Protection
- [ ] Sensitive data masking rules configured
- [ ] PII handling documented
- [ ] Data retention policies set
- [ ] Encryption at rest enabled
```

### Ongoing Operations

```markdown
## Security Checklist - Ongoing

### Monthly Reviews
- [ ] Review IAM role permissions
- [ ] Audit API token usage
- [ ] Check for unused tokens
- [ ] Review security alerts

### Quarterly Reviews
- [ ] Penetration testing results
- [ ] Compliance audit preparation
- [ ] Security training updates
- [ ] Disaster recovery testing

### Annual Reviews
- [ ] Full security assessment
- [ ] Policy updates
- [ ] Third-party security audit
- [ ] Compliance certification renewal
```

## 📚 References

- [Dynatrace Security Whitepaper](https://www.dynatrace.com/support/help/reference/security/)
- [AWS Security Best Practices](https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/)
- [OWASP Serverless Top 10](https://owasp.org/www-project-serverless-top-10/)
- [CIS AWS Foundations Benchmark](https://www.cisecurity.org/benchmark/amazon_web_services)

