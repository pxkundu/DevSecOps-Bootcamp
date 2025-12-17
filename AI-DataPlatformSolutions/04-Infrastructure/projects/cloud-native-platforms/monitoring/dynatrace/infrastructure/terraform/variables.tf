# =============================================================================
# Dynatrace AWS Serverless Monitoring - Variables
# =============================================================================

# -----------------------------------------------------------------------------
# AWS Configuration
# -----------------------------------------------------------------------------

variable "aws_region" {
  description = "AWS region for deployment"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment name (dev, staging, production)"
  type        = string
  default     = "dev"

  validation {
    condition     = contains(["dev", "staging", "production"], var.environment)
    error_message = "Environment must be one of: dev, staging, production."
  }
}

variable "vpc_id" {
  description = "VPC ID for ActiveGate and Lambda VPC deployment (optional)"
  type        = string
  default     = ""
}

variable "private_subnet_ids" {
  description = "List of private subnet IDs for ActiveGate deployment"
  type        = list(string)
  default     = []
}

# -----------------------------------------------------------------------------
# Dynatrace Configuration
# -----------------------------------------------------------------------------

variable "dynatrace_tenant_url" {
  description = "Dynatrace tenant URL (e.g., https://abc12345.live.dynatrace.com)"
  type        = string
  sensitive   = true

  validation {
    condition     = can(regex("^https://.*\\.dynatrace\\.com$", var.dynatrace_tenant_url))
    error_message = "Dynatrace tenant URL must be in format https://<tenant>.live.dynatrace.com"
  }
}

variable "dynatrace_tenant_id" {
  description = "Dynatrace tenant ID (extracted from URL)"
  type        = string
  sensitive   = true
}

variable "dynatrace_api_token" {
  description = "Dynatrace API token for configuration"
  type        = string
  sensitive   = true
}

variable "dynatrace_paas_token" {
  description = "Dynatrace PaaS token for OneAgent/Extension"
  type        = string
  sensitive   = true
}

variable "dynatrace_external_id" {
  description = "External ID for cross-account IAM role assumption"
  type        = string
  sensitive   = true
}

variable "dynatrace_layer_version" {
  description = "Version of the Dynatrace Lambda Layer to use"
  type        = number
  default     = 1
}

# -----------------------------------------------------------------------------
# Deployment Options
# -----------------------------------------------------------------------------

variable "deploy_activegate" {
  description = "Whether to deploy an ActiveGate instance"
  type        = bool
  default     = false
}

variable "configure_dynatrace_integration" {
  description = "Whether to configure Dynatrace AWS integration via API"
  type        = bool
  default     = true
}

variable "monitor_tagged_only" {
  description = "Only monitor resources with specific tags"
  type        = bool
  default     = false
}

variable "tags_to_monitor" {
  description = "Tags required for monitoring (when monitor_tagged_only is true)"
  type = list(object({
    key   = string
    value = string
  }))
  default = [
    {
      key   = "Monitoring"
      value = "dynatrace"
    }
  ]
}

# -----------------------------------------------------------------------------
# ActiveGate Configuration (if deployed)
# -----------------------------------------------------------------------------

variable "activegate_instance_type" {
  description = "EC2 instance type for ActiveGate"
  type        = string
  default     = "t3.medium"
}

variable "activegate_volume_size" {
  description = "EBS volume size for ActiveGate in GB"
  type        = number
  default     = 50
}

# -----------------------------------------------------------------------------
# Monitoring Services
# -----------------------------------------------------------------------------

variable "monitor_lambda" {
  description = "Enable Lambda monitoring"
  type        = bool
  default     = true
}

variable "monitor_api_gateway" {
  description = "Enable API Gateway monitoring"
  type        = bool
  default     = true
}

variable "monitor_dynamodb" {
  description = "Enable DynamoDB monitoring"
  type        = bool
  default     = true
}

variable "monitor_sqs" {
  description = "Enable SQS monitoring"
  type        = bool
  default     = true
}

variable "monitor_sns" {
  description = "Enable SNS monitoring"
  type        = bool
  default     = true
}

variable "monitor_step_functions" {
  description = "Enable Step Functions monitoring"
  type        = bool
  default     = true
}

variable "monitor_s3" {
  description = "Enable S3 monitoring (can generate many metrics)"
  type        = bool
  default     = false
}

# -----------------------------------------------------------------------------
# Alerting Configuration
# -----------------------------------------------------------------------------

variable "alerting_email" {
  description = "Email address for alert notifications"
  type        = string
  default     = ""
}

variable "slack_webhook_url" {
  description = "Slack webhook URL for notifications"
  type        = string
  default     = ""
  sensitive   = true
}

variable "pagerduty_service_key" {
  description = "PagerDuty service integration key"
  type        = string
  default     = ""
  sensitive   = true
}

# -----------------------------------------------------------------------------
# Common Tags
# -----------------------------------------------------------------------------

variable "additional_tags" {
  description = "Additional tags to apply to all resources"
  type        = map(string)
  default     = {}
}

