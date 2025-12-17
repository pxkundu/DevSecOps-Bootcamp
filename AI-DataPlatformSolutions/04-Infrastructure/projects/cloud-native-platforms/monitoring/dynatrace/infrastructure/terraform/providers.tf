# =============================================================================
# Dynatrace AWS Serverless Monitoring - Provider Configuration
# =============================================================================

# -----------------------------------------------------------------------------
# Terraform Settings
# -----------------------------------------------------------------------------

terraform {
  required_version = ">= 1.0.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }

    dynatrace = {
      source  = "dynatrace-oss/dynatrace"
      version = "~> 1.0"
    }

    random = {
      source  = "hashicorp/random"
      version = "~> 3.0"
    }

    null = {
      source  = "hashicorp/null"
      version = "~> 3.0"
    }
  }
}

# -----------------------------------------------------------------------------
# AWS Provider - Default Region
# -----------------------------------------------------------------------------

provider "aws" {
  region = var.aws_region

  # Default tags applied to all resources
  default_tags {
    tags = merge(
      {
        Project       = "dynatrace-monitoring"
        Environment   = var.environment
        ManagedBy     = "terraform"
        CostCenter    = "platform-engineering"
        Owner         = "devops-team"
        Application   = "serverless-monitoring"
        CreatedDate   = timestamp()
      },
      var.additional_tags
    )
  }
}

# -----------------------------------------------------------------------------
# AWS Provider - US East 1 (for global resources like IAM)
# -----------------------------------------------------------------------------

provider "aws" {
  alias  = "us_east_1"
  region = "us-east-1"

  default_tags {
    tags = merge(
      {
        Project       = "dynatrace-monitoring"
        Environment   = var.environment
        ManagedBy     = "terraform"
      },
      var.additional_tags
    )
  }
}

# -----------------------------------------------------------------------------
# Dynatrace Provider
# -----------------------------------------------------------------------------

provider "dynatrace" {
  # Dynatrace environment URL
  dt_env_url = var.dynatrace_tenant_url

  # API token with required permissions
  dt_api_token = var.dynatrace_api_token

  # Optional: Configure client timeout
  # client_timeout = 300
}

# -----------------------------------------------------------------------------
# Random Provider (for generating unique IDs)
# -----------------------------------------------------------------------------

provider "random" {}

# -----------------------------------------------------------------------------
# Null Provider (for local-exec and triggers)
# -----------------------------------------------------------------------------

provider "null" {}

