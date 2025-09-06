# Variables for E-Commerce Data Platform Infrastructure

variable "aws_region" {
  description = "AWS region for resources"
  type        = string
  default     = "us-west-2"
}

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
  default     = "dev"
  
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

variable "project_name" {
  description = "Name of the project"
  type        = string
  default     = "ecommerce-data-platform"
}

variable "owner" {
  description = "Owner of the resources"
  type        = string
  default     = "data-engineering-team"
}

# Network Configuration
variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "availability_zones" {
  description = "Availability zones"
  type        = list(string)
  default     = ["us-west-2a", "us-west-2b", "us-west-2c"]
}

variable "private_subnet_cidrs" {
  description = "CIDR blocks for private subnets"
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
}

variable "public_subnet_cidrs" {
  description = "CIDR blocks for public subnets"
  type        = list(string)
  default     = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]
}

# RDS Configuration
variable "postgres_version" {
  description = "PostgreSQL version"
  type        = string
  default     = "15.3"
}

variable "rds_instance_type" {
  description = "RDS instance type"
  type        = string
  default     = "db.t3.medium"
}

variable "rds_allocated_storage" {
  description = "RDS allocated storage in GB"
  type        = number
  default     = 100
}

variable "rds_max_allocated_storage" {
  description = "RDS maximum allocated storage in GB"
  type        = number
  default     = 1000
}

variable "database_name" {
  description = "Database name"
  type        = string
  default     = "ecommerce_platform"
}

variable "database_username" {
  description = "Database username"
  type        = string
  default     = "dataadmin"
}

variable "database_password" {
  description = "Database password"
  type        = string
  sensitive   = true
  default     = "ChangeMePlease123!"
}

variable "backup_retention_period" {
  description = "Database backup retention period in days"
  type        = number
  default     = 7
}

# EKS Configuration
variable "kubernetes_version" {
  description = "Kubernetes version"
  type        = string
  default     = "1.27"
}

variable "eks_node_instance_type" {
  description = "EKS node instance type"
  type        = string
  default     = "m5.large"
}

variable "eks_min_nodes" {
  description = "Minimum number of EKS nodes"
  type        = number
  default     = 1
}

variable "eks_max_nodes" {
  description = "Maximum number of EKS nodes"
  type        = number
  default     = 10
}

variable "eks_desired_nodes" {
  description = "Desired number of EKS nodes"
  type        = number
  default     = 3
}

# MSK Configuration
variable "kafka_version" {
  description = "Kafka version"
  type        = string
  default     = "2.8.1"
}

variable "msk_instance_type" {
  description = "MSK instance type"
  type        = string
  default     = "kafka.m5.large"
}

variable "msk_volume_size" {
  description = "MSK EBS volume size in GB"
  type        = number
  default     = 100
}

# Redis Configuration
variable "redis_node_type" {
  description = "Redis node type"
  type        = string
  default     = "cache.t3.micro"
}

variable "redis_num_nodes" {
  description = "Number of Redis nodes"
  type        = number
  default     = 2
}

# Data Configuration
variable "data_retention_days" {
  description = "Data retention period in days"
  type        = number
  default     = 2555  # ~7 years
}

variable "log_retention_days" {
  description = "Log retention period in days"
  type        = number
  default     = 30
}

# EMR Configuration
variable "emr_release_label" {
  description = "EMR release label"
  type        = string
  default     = "emr-6.10.0"
}

variable "emr_master_instance_type" {
  description = "EMR master instance type"
  type        = string
  default     = "m5.xlarge"
}

variable "emr_core_instance_type" {
  description = "EMR core instance type"
  type        = string
  default     = "m5.large"
}

variable "emr_core_instance_count" {
  description = "Number of EMR core instances"
  type        = number
  default     = 2
}

# Monitoring Configuration
variable "enable_detailed_monitoring" {
  description = "Enable detailed monitoring"
  type        = bool
  default     = true
}

variable "cloudwatch_dashboard_enabled" {
  description = "Enable CloudWatch dashboard"
  type        = bool
  default     = true
}

# Security Configuration
variable "enable_encryption" {
  description = "Enable encryption for all services"
  type        = bool
  default     = true
}

variable "allowed_cidr_blocks" {
  description = "CIDR blocks allowed to access resources"
  type        = list(string)
  default     = ["0.0.0.0/0"]  # Restrict this in production
}

# Cost Management
variable "auto_scaling_enabled" {
  description = "Enable auto scaling for cost optimization"
  type        = bool
  default     = true
}

variable "spot_instances_enabled" {
  description = "Use spot instances where possible"
  type        = bool
  default     = false  # Enable for dev/staging
}

# Tagging
variable "additional_tags" {
  description = "Additional tags to apply to resources"
  type        = map(string)
  default     = {}
}
