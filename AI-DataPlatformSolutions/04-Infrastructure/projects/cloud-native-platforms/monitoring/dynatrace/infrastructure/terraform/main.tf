# =============================================================================
# Dynatrace AWS Serverless Monitoring - Main Terraform Configuration
# =============================================================================

terraform {
  required_version = ">= 1.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    dynatrace = {
      source  = "dynatrace-oss/dynatrace"
      version = "~> 1.0"
    }
  }

  backend "s3" {
    # Configure in environment-specific tfvars
    # bucket         = "your-terraform-state-bucket"
    # key            = "dynatrace/monitoring/terraform.tfstate"
    # region         = "us-east-1"
    # encrypt        = true
    # dynamodb_table = "terraform-state-lock"
  }
}

# =============================================================================
# Providers
# =============================================================================

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = "dynatrace-monitoring"
      Environment = var.environment
      ManagedBy   = "terraform"
    }
  }
}

provider "dynatrace" {
  dt_env_url   = var.dynatrace_tenant_url
  dt_api_token = var.dynatrace_api_token
}

# =============================================================================
# Data Sources
# =============================================================================

data "aws_caller_identity" "current" {}
data "aws_region" "current" {}

data "aws_vpc" "selected" {
  count = var.vpc_id != "" ? 1 : 0
  id    = var.vpc_id
}

data "aws_subnets" "private" {
  count = var.vpc_id != "" ? 1 : 0
  
  filter {
    name   = "vpc-id"
    values = [var.vpc_id]
  }
  
  filter {
    name   = "tag:Tier"
    values = ["private"]
  }
}

# =============================================================================
# KMS Key for Secrets Encryption
# =============================================================================

resource "aws_kms_key" "dynatrace_secrets" {
  description             = "KMS key for Dynatrace secrets encryption"
  deletion_window_in_days = 30
  enable_key_rotation     = true

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "Enable IAM User Permissions"
        Effect = "Allow"
        Principal = {
          AWS = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:root"
        }
        Action   = "kms:*"
        Resource = "*"
      },
      {
        Sid    = "Allow Lambda to decrypt"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
        Action = [
          "kms:Decrypt",
          "kms:DescribeKey"
        ]
        Resource = "*"
        Condition = {
          StringEquals = {
            "kms:CallerAccount" = data.aws_caller_identity.current.account_id
          }
        }
      }
    ]
  })

  tags = {
    Name = "dynatrace-secrets-key"
  }
}

resource "aws_kms_alias" "dynatrace_secrets" {
  name          = "alias/dynatrace-secrets"
  target_key_id = aws_kms_key.dynatrace_secrets.key_id
}

# =============================================================================
# Secrets Manager for Dynatrace Credentials
# =============================================================================

resource "aws_secretsmanager_secret" "dynatrace_credentials" {
  name        = "dynatrace/${var.environment}/credentials"
  description = "Dynatrace monitoring credentials"
  kms_key_id  = aws_kms_key.dynatrace_secrets.arn

  tags = {
    Name = "dynatrace-credentials"
  }
}

resource "aws_secretsmanager_secret_version" "dynatrace_credentials" {
  secret_id = aws_secretsmanager_secret.dynatrace_credentials.id
  secret_string = jsonencode({
    tenant_url         = var.dynatrace_tenant_url
    api_token          = var.dynatrace_api_token
    paas_token         = var.dynatrace_paas_token
    tenant_id          = var.dynatrace_tenant_id
    connection_base_url = var.dynatrace_tenant_url
  })
}

# =============================================================================
# IAM Role for Dynatrace AWS Integration
# =============================================================================

resource "aws_iam_role" "dynatrace_monitoring" {
  name        = "dynatrace-monitoring-role-${var.environment}"
  description = "IAM role for Dynatrace AWS monitoring integration"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          AWS = "arn:aws:iam::509560245411:root"  # Dynatrace AWS Account
        }
        Action = "sts:AssumeRole"
        Condition = {
          StringEquals = {
            "sts:ExternalId" = var.dynatrace_external_id
          }
        }
      }
    ]
  })

  tags = {
    Name = "dynatrace-monitoring-role"
  }
}

resource "aws_iam_role_policy" "dynatrace_monitoring" {
  name = "dynatrace-monitoring-policy"
  role = aws_iam_role.dynatrace_monitoring.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "CloudWatchMetrics"
        Effect = "Allow"
        Action = [
          "cloudwatch:GetMetricStatistics",
          "cloudwatch:ListMetrics",
          "cloudwatch:GetMetricData"
        ]
        Resource = "*"
      },
      {
        Sid    = "ResourceDiscovery"
        Effect = "Allow"
        Action = [
          "tag:GetResources",
          "tag:GetTagKeys",
          "tag:GetTagValues"
        ]
        Resource = "*"
      },
      {
        Sid    = "LambdaDiscovery"
        Effect = "Allow"
        Action = [
          "lambda:ListFunctions",
          "lambda:ListTags",
          "lambda:GetFunctionConfiguration"
        ]
        Resource = "*"
      },
      {
        Sid    = "DynamoDBDiscovery"
        Effect = "Allow"
        Action = [
          "dynamodb:ListTables",
          "dynamodb:DescribeTable",
          "dynamodb:ListTagsOfResource"
        ]
        Resource = "*"
      },
      {
        Sid    = "SQSDiscovery"
        Effect = "Allow"
        Action = [
          "sqs:ListQueues",
          "sqs:GetQueueAttributes",
          "sqs:ListQueueTags"
        ]
        Resource = "*"
      },
      {
        Sid    = "SNSDiscovery"
        Effect = "Allow"
        Action = [
          "sns:ListTopics",
          "sns:GetTopicAttributes",
          "sns:ListTagsForResource"
        ]
        Resource = "*"
      },
      {
        Sid    = "APIGatewayDiscovery"
        Effect = "Allow"
        Action = [
          "apigateway:GET"
        ]
        Resource = "arn:aws:apigateway:*::/*"
      },
      {
        Sid    = "StepFunctionsDiscovery"
        Effect = "Allow"
        Action = [
          "states:ListStateMachines",
          "states:DescribeStateMachine",
          "states:ListTagsForResource"
        ]
        Resource = "*"
      },
      {
        Sid    = "S3Discovery"
        Effect = "Allow"
        Action = [
          "s3:ListAllMyBuckets",
          "s3:GetBucketLocation",
          "s3:GetBucketTagging"
        ]
        Resource = "*"
      }
    ]
  })
}

# =============================================================================
# IAM Role for Lambda Extension
# =============================================================================

resource "aws_iam_role" "lambda_monitoring" {
  name        = "lambda-dynatrace-monitoring-${var.environment}"
  description = "IAM role for Lambda functions with Dynatrace monitoring"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })

  tags = {
    Name = "lambda-dynatrace-monitoring"
  }
}

resource "aws_iam_role_policy" "lambda_monitoring" {
  name = "lambda-monitoring-policy"
  role = aws_iam_role.lambda_monitoring.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "SecretsAccess"
        Effect = "Allow"
        Action = [
          "secretsmanager:GetSecretValue"
        ]
        Resource = aws_secretsmanager_secret.dynatrace_credentials.arn
      },
      {
        Sid    = "KMSDecrypt"
        Effect = "Allow"
        Action = [
          "kms:Decrypt"
        ]
        Resource = aws_kms_key.dynatrace_secrets.arn
      },
      {
        Sid    = "CloudWatchLogs"
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  role       = aws_iam_role.lambda_monitoring.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy_attachment" "lambda_vpc_access" {
  count      = var.vpc_id != "" ? 1 : 0
  role       = aws_iam_role.lambda_monitoring.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole"
}

# =============================================================================
# Security Groups (if VPC deployment)
# =============================================================================

resource "aws_security_group" "activegate" {
  count       = var.deploy_activegate && var.vpc_id != "" ? 1 : 0
  name        = "dynatrace-activegate-${var.environment}"
  description = "Security group for Dynatrace ActiveGate"
  vpc_id      = var.vpc_id

  # Inbound from Lambda functions
  ingress {
    from_port       = 9999
    to_port         = 9999
    protocol        = "tcp"
    cidr_blocks     = [data.aws_vpc.selected[0].cidr_block]
    description     = "ActiveGate communication from VPC"
  }

  # Outbound to Dynatrace SaaS
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

resource "aws_security_group" "lambda" {
  count       = var.vpc_id != "" ? 1 : 0
  name        = "dynatrace-lambda-${var.environment}"
  description = "Security group for Lambda functions with Dynatrace"
  vpc_id      = var.vpc_id

  # Outbound HTTPS
  egress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "HTTPS outbound"
  }

  # Outbound to ActiveGate (if deployed)
  dynamic "egress" {
    for_each = var.deploy_activegate ? [1] : []
    content {
      from_port       = 9999
      to_port         = 9999
      protocol        = "tcp"
      security_groups = [aws_security_group.activegate[0].id]
      description     = "To ActiveGate"
    }
  }

  tags = {
    Name = "dynatrace-lambda-sg"
  }
}

# =============================================================================
# CloudWatch Log Group for Dynatrace Audit
# =============================================================================

resource "aws_cloudwatch_log_group" "dynatrace_audit" {
  name              = "/dynatrace/audit-logs"
  retention_in_days = 90

  tags = {
    Name = "dynatrace-audit-logs"
  }
}

# =============================================================================
# SSM Parameters for Lambda Extension Configuration
# =============================================================================

resource "aws_ssm_parameter" "dynatrace_layer_arn" {
  name        = "/dynatrace/${var.environment}/lambda-layer-arn"
  description = "Dynatrace Lambda Layer ARN for this region"
  type        = "String"
  value       = "arn:aws:lambda:${data.aws_region.current.name}:725887861453:layer:Dynatrace_OneAgent:${var.dynatrace_layer_version}"

  tags = {
    Name = "dynatrace-layer-arn"
  }
}

resource "aws_ssm_parameter" "dynatrace_tenant" {
  name        = "/dynatrace/${var.environment}/tenant-id"
  description = "Dynatrace Tenant ID"
  type        = "String"
  value       = var.dynatrace_tenant_id

  tags = {
    Name = "dynatrace-tenant-id"
  }
}

# =============================================================================
# Dynatrace AWS Integration (using Dynatrace provider)
# =============================================================================

resource "dynatrace_aws_credentials" "main" {
  count = var.configure_dynatrace_integration ? 1 : 0

  label             = "${var.environment}-serverless"
  partition_type    = "AWS_DEFAULT"
  tagged_only       = var.monitor_tagged_only
  authentication_data {
    account_id  = data.aws_caller_identity.current.account_id
    iam_role    = aws_iam_role.dynatrace_monitoring.arn
    external_id = var.dynatrace_external_id
  }

  depends_on = [aws_iam_role_policy.dynatrace_monitoring]
}

# =============================================================================
# Outputs
# =============================================================================

output "dynatrace_role_arn" {
  description = "ARN of the IAM role for Dynatrace AWS integration"
  value       = aws_iam_role.dynatrace_monitoring.arn
}

output "lambda_role_arn" {
  description = "ARN of the IAM role for Lambda functions"
  value       = aws_iam_role.lambda_monitoring.arn
}

output "secrets_arn" {
  description = "ARN of the Secrets Manager secret"
  value       = aws_secretsmanager_secret.dynatrace_credentials.arn
}

output "lambda_layer_arn" {
  description = "ARN of the Dynatrace Lambda Layer"
  value       = aws_ssm_parameter.dynatrace_layer_arn.value
}

output "activegate_security_group_id" {
  description = "Security group ID for ActiveGate"
  value       = var.deploy_activegate && var.vpc_id != "" ? aws_security_group.activegate[0].id : null
}

output "lambda_security_group_id" {
  description = "Security group ID for Lambda functions"
  value       = var.vpc_id != "" ? aws_security_group.lambda[0].id : null
}

