# ============================================================================
# VARIABLES - MLOps Platform Infrastructure
# ============================================================================

# ============================================================================
# GENERAL CONFIGURATION
# ============================================================================

variable "project_name" {
  description = "Name of the MLOps project"
  type        = string
  default     = "mlops-platform"
}

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
  default     = "dev"
  
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be one of: dev, staging, prod."
  }
}

variable "owner" {
  description = "Owner of the resources"
  type        = string
  default     = "mlops-team"
}

variable "cost_center" {
  description = "Cost center for billing"
  type        = string
  default     = "ml-engineering"
}

# ============================================================================
# AWS CONFIGURATION
# ============================================================================

variable "aws_region" {
  description = "AWS region for resources"
  type        = string
  default     = "us-west-2"
}

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

# ============================================================================
# EKS CONFIGURATION
# ============================================================================

variable "kubernetes_version" {
  description = "Kubernetes version for EKS cluster"
  type        = string
  default     = "1.27"
}

variable "eks_node_instance_types" {
  description = "Instance types for general EKS node group"
  type        = list(string)
  default     = ["t3.medium"]
}

variable "eks_mlops_instance_types" {
  description = "Instance types for MLOps workload node group"
  type        = list(string)
  default     = ["c5.xlarge", "c5.2xlarge"]
}

variable "eks_node_group_min_size" {
  description = "Minimum size of EKS node group"
  type        = number
  default     = 1
}

variable "eks_node_group_max_size" {
  description = "Maximum size of EKS node group"
  type        = number
  default     = 10
}

variable "eks_node_group_desired_size" {
  description = "Desired size of EKS node group"
  type        = number
  default     = 2
}

# ============================================================================
# RDS CONFIGURATION
# ============================================================================

variable "rds_instance_class" {
  description = "RDS instance class for MLflow backend store"
  type        = string
  default     = "db.t3.micro"
}

variable "rds_allocated_storage" {
  description = "Allocated storage for RDS instance (GB)"
  type        = number
  default     = 20
}

variable "rds_max_allocated_storage" {
  description = "Maximum allocated storage for RDS instance (GB)"
  type        = number
  default     = 100
}

# ============================================================================
# REDIS CONFIGURATION
# ============================================================================

variable "redis_node_type" {
  description = "ElastiCache Redis node type"
  type        = string
  default     = "cache.t3.micro"
}

variable "redis_num_cache_nodes" {
  description = "Number of cache nodes in Redis cluster"
  type        = number
  default     = 1
}

# ============================================================================
# MONITORING CONFIGURATION
# ============================================================================

variable "cloudwatch_retention_days" {
  description = "CloudWatch logs retention period in days"
  type        = number
  default     = 14
}

variable "enable_container_insights" {
  description = "Enable CloudWatch Container Insights for EKS"
  type        = bool
  default     = true
}

# ============================================================================
# MLOPS SPECIFIC CONFIGURATION
# ============================================================================

variable "mlflow_artifact_store_type" {
  description = "Type of artifact store for MLflow (s3, gcs, azure)"
  type        = string
  default     = "s3"
}

variable "enable_gpu_nodes" {
  description = "Enable GPU nodes for training workloads"
  type        = bool
  default     = false
}

variable "gpu_node_instance_types" {
  description = "Instance types for GPU node group"
  type        = list(string)
  default     = ["g4dn.xlarge", "g4dn.2xlarge"]
}

variable "enable_spot_instances" {
  description = "Enable spot instances for cost optimization"
  type        = bool
  default     = false
}

variable "spot_instance_types" {
  description = "Instance types for spot instances"
  type        = list(string)
  default     = ["c5.large", "c5.xlarge", "c5.2xlarge", "m5.large", "m5.xlarge"]
}

# ============================================================================
# FEATURE STORE CONFIGURATION
# ============================================================================

variable "feast_registry_type" {
  description = "Type of registry for Feast feature store (sql, gcs, s3)"
  type        = string
  default     = "sql"
}

variable "feast_online_store_type" {
  description = "Type of online store for Feast (redis, dynamodb)"
  type        = string
  default     = "redis"
}

variable "feast_offline_store_type" {
  description = "Type of offline store for Feast (postgres, snowflake, bigquery)"
  type        = string
  default     = "postgres"
}

# ============================================================================
# SECURITY CONFIGURATION
# ============================================================================

variable "enable_encryption_at_rest" {
  description = "Enable encryption at rest for all storage"
  type        = bool
  default     = true
}

variable "enable_encryption_in_transit" {
  description = "Enable encryption in transit"
  type        = bool
  default     = true
}

variable "allowed_cidr_blocks" {
  description = "CIDR blocks allowed to access the infrastructure"
  type        = list(string)
  default     = ["0.0.0.0/0"]  # Restrict this in production
}

variable "enable_private_endpoints" {
  description = "Enable VPC endpoints for AWS services"
  type        = bool
  default     = true
}

# ============================================================================
# BACKUP AND DISASTER RECOVERY
# ============================================================================

variable "backup_retention_period" {
  description = "Backup retention period in days"
  type        = number
  default     = 7
}

variable "enable_multi_az" {
  description = "Enable Multi-AZ deployment for RDS"
  type        = bool
  default     = false
}

variable "enable_cross_region_backup" {
  description = "Enable cross-region backup"
  type        = bool
  default     = false
}

# ============================================================================
# AUTOSCALING CONFIGURATION
# ============================================================================

variable "enable_cluster_autoscaler" {
  description = "Enable cluster autoscaler for EKS"
  type        = bool
  default     = true
}

variable "enable_horizontal_pod_autoscaler" {
  description = "Enable horizontal pod autoscaler"
  type        = bool
  default     = true
}

variable "enable_vertical_pod_autoscaler" {
  description = "Enable vertical pod autoscaler"
  type        = bool
  default     = false
}

# ============================================================================
# NETWORKING CONFIGURATION
# ============================================================================

variable "enable_nat_gateway" {
  description = "Enable NAT Gateway for private subnets"
  type        = bool
  default     = true
}

variable "single_nat_gateway" {
  description = "Use single NAT Gateway (cost optimization for dev)"
  type        = bool
  default     = true
}

variable "enable_flow_logs" {
  description = "Enable VPC Flow Logs"
  type        = bool
  default     = false
}

# ============================================================================
# DOMAIN AND DNS CONFIGURATION
# ============================================================================

variable "domain_name" {
  description = "Domain name for MLOps platform"
  type        = string
  default     = ""
}

variable "create_route53_zone" {
  description = "Create Route53 hosted zone"
  type        = bool
  default     = false
}

variable "ssl_certificate_arn" {
  description = "ARN of SSL certificate for HTTPS"
  type        = string
  default     = ""
}

# ============================================================================
# MODEL SERVING CONFIGURATION
# ============================================================================

variable "model_serving_replicas" {
  description = "Number of replicas for model serving"
  type        = number
  default     = 2
}

variable "model_serving_cpu_request" {
  description = "CPU request for model serving pods"
  type        = string
  default     = "100m"
}

variable "model_serving_memory_request" {
  description = "Memory request for model serving pods"
  type        = string
  default     = "256Mi"
}

variable "model_serving_cpu_limit" {
  description = "CPU limit for model serving pods"
  type        = string
  default     = "1000m"
}

variable "model_serving_memory_limit" {
  description = "Memory limit for model serving pods"
  type        = string
  default     = "2Gi"
}

# ============================================================================
# DATA LAKE CONFIGURATION
# ============================================================================

variable "data_lake_storage_class" {
  description = "Storage class for data lake (STANDARD, STANDARD_IA, GLACIER)"
  type        = string
  default     = "STANDARD"
}

variable "enable_data_lake_versioning" {
  description = "Enable versioning for data lake bucket"
  type        = bool
  default     = true
}

variable "data_lake_lifecycle_enabled" {
  description = "Enable lifecycle policies for data lake"
  type        = bool
  default     = true
}

# ============================================================================
# OBSERVABILITY CONFIGURATION
# ============================================================================

variable "enable_prometheus" {
  description = "Enable Prometheus monitoring"
  type        = bool
  default     = true
}

variable "enable_grafana" {
  description = "Enable Grafana dashboards"
  type        = bool
  default     = true
}

variable "enable_jaeger" {
  description = "Enable Jaeger distributed tracing"
  type        = bool
  default     = false
}

variable "enable_elasticsearch" {
  description = "Enable Elasticsearch for logging"
  type        = bool
  default     = false
}

variable "enable_fluentd" {
  description = "Enable Fluentd for log aggregation"
  type        = bool
  default     = true
}

# ============================================================================
# MLOPS PLATFORM VERSIONS
# ============================================================================

variable "mlflow_version" {
  description = "MLflow version to deploy"
  type        = string
  default     = "2.7.1"
}

variable "feast_version" {
  description = "Feast version to deploy"
  type        = string
  default     = "0.32.0"
}

variable "kubeflow_version" {
  description = "Kubeflow version to deploy"
  type        = string
  default     = "1.7.0"
}

variable "seldon_core_version" {
  description = "Seldon Core version for model serving"
  type        = string
  default     = "1.17.0"
}

# ============================================================================
# COMPLIANCE AND GOVERNANCE
# ============================================================================

variable "enable_audit_logging" {
  description = "Enable audit logging for compliance"
  type        = bool
  default     = true
}

variable "enable_resource_tagging" {
  description = "Enable comprehensive resource tagging"
  type        = bool
  default     = true
}

variable "compliance_framework" {
  description = "Compliance framework to follow (SOC2, GDPR, HIPAA)"
  type        = string
  default     = "SOC2"
}

variable "data_residency_region" {
  description = "Region for data residency requirements"
  type        = string
  default     = ""
}

# ============================================================================
# DISASTER RECOVERY
# ============================================================================

variable "enable_disaster_recovery" {
  description = "Enable disaster recovery setup"
  type        = bool
  default     = false
}

variable "dr_region" {
  description = "Disaster recovery region"
  type        = string
  default     = "us-east-1"
}

variable "rpo_hours" {
  description = "Recovery Point Objective in hours"
  type        = number
  default     = 24
}

variable "rto_hours" {
  description = "Recovery Time Objective in hours"  
  type        = number
  default     = 4
}

# ============================================================================
# COST OPTIMIZATION
# ============================================================================

variable "enable_cost_optimization" {
  description = "Enable cost optimization features"
  type        = bool
  default     = true
}

variable "reserved_instance_percentage" {
  description = "Percentage of reserved instances to use"
  type        = number
  default     = 50
}

variable "enable_automatic_shutdown" {
  description = "Enable automatic shutdown for dev environments"
  type        = bool
  default     = false
}

variable "shutdown_schedule" {
  description = "Cron schedule for automatic shutdown"
  type        = string
  default     = "0 22 * * 1-5"  # 10 PM on weekdays
}

variable "startup_schedule" {
  description = "Cron schedule for automatic startup"
  type        = string
  default     = "0 8 * * 1-5"   # 8 AM on weekdays
}

# ============================================================================
# DEVELOPMENT CONFIGURATION
# ============================================================================

variable "enable_development_tools" {
  description = "Enable development tools (JupyterLab, VS Code Server)"
  type        = bool
  default     = true
}

variable "jupyter_instance_type" {
  description = "Instance type for JupyterLab"
  type        = string
  default     = "t3.medium"
}

variable "enable_notebook_scheduling" {
  description = "Enable notebook scheduling with Papermill"
  type        = bool
  default     = false
}

# ============================================================================
# EXTERNAL INTEGRATIONS
# ============================================================================

variable "slack_webhook_url" {
  description = "Slack webhook URL for notifications"
  type        = string
  default     = ""
  sensitive   = true
}

variable "pagerduty_service_key" {
  description = "PagerDuty service key for alerts"
  type        = string
  default     = ""
  sensitive   = true
}

variable "datadog_api_key" {
  description = "Datadog API key for monitoring"
  type        = string
  default     = ""
  sensitive   = true
}

variable "github_org" {
  description = "GitHub organization for CI/CD integration"
  type        = string
  default     = ""
}

variable "github_repo" {
  description = "GitHub repository for CI/CD integration"
  type        = string
  default     = ""
}

# ============================================================================
# ADVANCED FEATURES
# ============================================================================

variable "enable_model_explainability" {
  description = "Enable model explainability tools (SHAP, LIME)"
  type        = bool
  default     = true
}

variable "enable_automl" {
  description = "Enable AutoML capabilities"
  type        = bool
  default     = false
}

variable "enable_federated_learning" {
  description = "Enable federated learning infrastructure"
  type        = bool
  default     = false
}

variable "enable_edge_deployment" {
  description = "Enable edge deployment capabilities"
  type        = bool
  default     = false
}

variable "enable_model_compression" {
  description = "Enable model compression and optimization"
  type        = bool
  default     = true
}

# ============================================================================
# EXPERIMENTAL FEATURES
# ============================================================================

variable "enable_quantum_ml" {
  description = "Enable quantum ML infrastructure (experimental)"
  type        = bool
  default     = false
}

variable "enable_neuromorphic_computing" {
  description = "Enable neuromorphic computing support (experimental)"
  type        = bool
  default     = false
}

variable "enable_synthetic_data" {
  description = "Enable synthetic data generation capabilities"
  type        = bool
  default     = false
}
