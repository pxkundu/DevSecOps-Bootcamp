# =============================================================================
# Dynatrace AWS Serverless Monitoring - Production Environment
# =============================================================================

# -----------------------------------------------------------------------------
# AWS Configuration
# -----------------------------------------------------------------------------
aws_region  = "us-east-1"
environment = "production"

# VPC Configuration (set to your VPC ID if using VPC Lambda/ActiveGate)
# vpc_id = "vpc-xxxxxxxxx"
# private_subnet_ids = ["subnet-aaaa", "subnet-bbbb"]

# -----------------------------------------------------------------------------
# Dynatrace Configuration
# IMPORTANT: Use environment variables or Terraform Cloud variables for secrets
# Do NOT commit actual tokens to version control
# -----------------------------------------------------------------------------

# Example: Set via environment variables
# export TF_VAR_dynatrace_tenant_url="https://abc12345.live.dynatrace.com"
# export TF_VAR_dynatrace_tenant_id="abc12345"
# export TF_VAR_dynatrace_api_token="dt0c01.XXX.YYY"
# export TF_VAR_dynatrace_paas_token="dt0c01.XXX.ZZZ"
# export TF_VAR_dynatrace_external_id="unique-external-id"

dynatrace_layer_version = 1

# -----------------------------------------------------------------------------
# Deployment Options
# -----------------------------------------------------------------------------
deploy_activegate               = false
configure_dynatrace_integration = true
monitor_tagged_only             = false

# Monitoring scope
monitor_lambda         = true
monitor_api_gateway    = true
monitor_dynamodb       = true
monitor_sqs            = true
monitor_sns            = true
monitor_step_functions = true
monitor_s3             = false  # Can generate many metrics

# -----------------------------------------------------------------------------
# Alerting Configuration
# -----------------------------------------------------------------------------
# alerting_email        = "platform-team@company.com"
# slack_webhook_url     = "https://hooks.slack.com/services/XXX/YYY/ZZZ"
# pagerduty_service_key = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# -----------------------------------------------------------------------------
# Additional Tags
# -----------------------------------------------------------------------------
additional_tags = {
  CostCenter  = "platform-engineering"
  Team        = "devops"
  Criticality = "high"
}

