# =============================================================================
# Dynatrace AWS Serverless Monitoring - Outputs
# =============================================================================

# -----------------------------------------------------------------------------
# IAM Outputs
# -----------------------------------------------------------------------------

output "iam_role_arn" {
  description = "ARN of the IAM role for Dynatrace AWS integration"
  value       = aws_iam_role.dynatrace_monitoring.arn
}

output "iam_role_name" {
  description = "Name of the IAM role for Dynatrace AWS integration"
  value       = aws_iam_role.dynatrace_monitoring.name
}

output "lambda_execution_role_arn" {
  description = "ARN of the IAM role for Lambda functions with Dynatrace"
  value       = aws_iam_role.lambda_monitoring.arn
}

output "lambda_execution_role_name" {
  description = "Name of the IAM role for Lambda functions"
  value       = aws_iam_role.lambda_monitoring.name
}

# -----------------------------------------------------------------------------
# Secrets Outputs
# -----------------------------------------------------------------------------

output "secrets_manager_secret_arn" {
  description = "ARN of the Secrets Manager secret containing Dynatrace credentials"
  value       = aws_secretsmanager_secret.dynatrace_credentials.arn
}

output "secrets_manager_secret_name" {
  description = "Name of the Secrets Manager secret"
  value       = aws_secretsmanager_secret.dynatrace_credentials.name
}

output "kms_key_arn" {
  description = "ARN of the KMS key for secrets encryption"
  value       = aws_kms_key.dynatrace_secrets.arn
}

output "kms_key_alias" {
  description = "Alias of the KMS key"
  value       = aws_kms_alias.dynatrace_secrets.name
}

# -----------------------------------------------------------------------------
# Lambda Extension Outputs
# -----------------------------------------------------------------------------

output "dynatrace_lambda_layer_arn" {
  description = "ARN of the Dynatrace Lambda Layer for this region"
  value       = aws_ssm_parameter.dynatrace_layer_arn.value
}

output "lambda_environment_variables" {
  description = "Environment variables to add to Lambda functions"
  value = {
    DT_TENANT                = var.dynatrace_tenant_id
    DT_CLUSTER_ID            = "-1"
    DT_CONNECTION_BASE_URL   = var.dynatrace_tenant_url
    AWS_LAMBDA_EXEC_WRAPPER  = "/opt/dynatrace"
    # Note: DT_CONNECTION_AUTH_TOKEN should be retrieved from Secrets Manager
  }
}

output "lambda_layer_configuration" {
  description = "Lambda layer configuration for Terraform"
  value = {
    layer_arn = aws_ssm_parameter.dynatrace_layer_arn.value
  }
}

# -----------------------------------------------------------------------------
# SSM Parameter Outputs
# -----------------------------------------------------------------------------

output "ssm_parameter_layer_arn" {
  description = "SSM Parameter path for Dynatrace Layer ARN"
  value       = aws_ssm_parameter.dynatrace_layer_arn.name
}

output "ssm_parameter_tenant_id" {
  description = "SSM Parameter path for Dynatrace Tenant ID"
  value       = aws_ssm_parameter.dynatrace_tenant.name
}

# -----------------------------------------------------------------------------
# Security Group Outputs (VPC deployment)
# -----------------------------------------------------------------------------

output "activegate_security_group" {
  description = "Security group details for ActiveGate"
  value = var.deploy_activegate && var.vpc_id != "" ? {
    id   = aws_security_group.activegate[0].id
    name = aws_security_group.activegate[0].name
  } : null
}

output "lambda_security_group" {
  description = "Security group details for Lambda functions"
  value = var.vpc_id != "" ? {
    id   = aws_security_group.lambda[0].id
    name = aws_security_group.lambda[0].name
  } : null
}

# -----------------------------------------------------------------------------
# CloudWatch Outputs
# -----------------------------------------------------------------------------

output "audit_log_group_name" {
  description = "CloudWatch Log Group for Dynatrace audit logs"
  value       = aws_cloudwatch_log_group.dynatrace_audit.name
}

output "audit_log_group_arn" {
  description = "ARN of the CloudWatch Log Group for audit logs"
  value       = aws_cloudwatch_log_group.dynatrace_audit.arn
}

# -----------------------------------------------------------------------------
# Integration Configuration Outputs
# -----------------------------------------------------------------------------

output "dynatrace_integration_config" {
  description = "Configuration to use in Dynatrace AWS integration setup"
  value = {
    iam_role_arn   = aws_iam_role.dynatrace_monitoring.arn
    external_id    = var.dynatrace_external_id
    aws_account_id = data.aws_caller_identity.current.account_id
    aws_region     = data.aws_region.current.name
  }
  sensitive = true
}

# -----------------------------------------------------------------------------
# Deployment Summary
# -----------------------------------------------------------------------------

output "deployment_summary" {
  description = "Summary of the Dynatrace monitoring deployment"
  value = {
    environment        = var.environment
    region             = data.aws_region.current.name
    account_id         = data.aws_caller_identity.current.account_id
    vpc_deployed       = var.vpc_id != ""
    activegate_enabled = var.deploy_activegate
    services_monitored = {
      lambda         = var.monitor_lambda
      api_gateway    = var.monitor_api_gateway
      dynamodb       = var.monitor_dynamodb
      sqs            = var.monitor_sqs
      sns            = var.monitor_sns
      step_functions = var.monitor_step_functions
      s3             = var.monitor_s3
    }
  }
}

