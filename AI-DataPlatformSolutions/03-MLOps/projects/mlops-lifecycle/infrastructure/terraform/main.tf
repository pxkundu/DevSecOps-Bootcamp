# ============================================================================
# MLOps Platform Infrastructure - Main Configuration
# ============================================================================

terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.20"
    }
    helm = {
      source  = "hashicorp/helm"
      version = "~> 2.10"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.5"
    }
  }

  backend "s3" {
    bucket         = "mlops-platform-terraform-state"
    key            = "mlops-platform/terraform.tfstate"
    region         = "us-west-2"
    encrypt        = true
    dynamodb_table = "mlops-platform-terraform-locks"
  }
}

# ============================================================================
# PROVIDERS CONFIGURATION
# ============================================================================

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = "MLOps Platform"
      Environment = var.environment
      ManagedBy   = "Terraform"
      Owner       = var.owner
      CostCenter  = var.cost_center
    }
  }
}

provider "kubernetes" {
  host                   = module.eks.cluster_endpoint
  cluster_ca_certificate = base64decode(module.eks.cluster_certificate_authority_data)

  exec {
    api_version = "client.authentication.k8s.io/v1beta1"
    command     = "aws"
    args        = ["eks", "get-token", "--cluster-name", module.eks.cluster_name]
  }
}

provider "helm" {
  kubernetes {
    host                   = module.eks.cluster_endpoint
    cluster_ca_certificate = base64decode(module.eks.cluster_certificate_authority_data)

    exec {
      api_version = "client.authentication.k8s.io/v1beta1"
      command     = "aws"
      args        = ["eks", "get-token", "--cluster-name", module.eks.cluster_name]
    }
  }
}

# ============================================================================
# DATA SOURCES
# ============================================================================

data "aws_availability_zones" "available" {
  filter {
    name   = "opt-in-status"
    values = ["opt-in-not-required"]
  }
}

data "aws_caller_identity" "current" {}

data "aws_region" "current" {}

# ============================================================================
# RANDOM RESOURCES
# ============================================================================

resource "random_string" "suffix" {
  length  = 8
  special = false
  upper   = false
}

# ============================================================================
# LOCAL VALUES
# ============================================================================

locals {
  name_prefix = "${var.project_name}-${var.environment}"
  
  azs = slice(data.aws_availability_zones.available.names, 0, 3)
  
  vpc_cidr = var.vpc_cidr
  
  private_subnets = [
    cidrsubnet(local.vpc_cidr, 8, 1),
    cidrsubnet(local.vpc_cidr, 8, 2),
    cidrsubnet(local.vpc_cidr, 8, 3),
  ]
  
  public_subnets = [
    cidrsubnet(local.vpc_cidr, 8, 101),
    cidrsubnet(local.vpc_cidr, 8, 102),
    cidrsubnet(local.vpc_cidr, 8, 103),
  ]
  
  database_subnets = [
    cidrsubnet(local.vpc_cidr, 8, 201),
    cidrsubnet(local.vpc_cidr, 8, 202),
    cidrsubnet(local.vpc_cidr, 8, 203),
  ]

  common_tags = {
    Project     = var.project_name
    Environment = var.environment
    Terraform   = "true"
    Owner       = var.owner
  }
}

# ============================================================================
# VPC MODULE
# ============================================================================

module "vpc" {
  source = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"

  name = "${local.name_prefix}-vpc"
  cidr = local.vpc_cidr

  azs              = local.azs
  private_subnets  = local.private_subnets
  public_subnets   = local.public_subnets
  database_subnets = local.database_subnets

  enable_nat_gateway     = true
  single_nat_gateway     = var.environment == "dev" ? true : false
  enable_vpn_gateway     = false
  enable_dns_hostnames   = true
  enable_dns_support     = true

  create_database_subnet_group = true
  create_database_subnet_route_table = true

  # Kubernetes specific tags
  public_subnet_tags = {
    "kubernetes.io/role/elb" = "1"
    "kubernetes.io/cluster/${local.name_prefix}-eks" = "owned"
  }

  private_subnet_tags = {
    "kubernetes.io/role/internal-elb" = "1"
    "kubernetes.io/cluster/${local.name_prefix}-eks" = "owned"
  }

  tags = local.common_tags
}

# ============================================================================
# EKS CLUSTER
# ============================================================================

module "eks" {
  source = "terraform-aws-modules/eks/aws"
  version = "~> 19.15"

  cluster_name    = "${local.name_prefix}-eks"
  cluster_version = var.kubernetes_version

  vpc_id                         = module.vpc.vpc_id
  subnet_ids                     = module.vpc.private_subnets
  cluster_endpoint_public_access = true
  cluster_endpoint_private_access = true

  cluster_addons = {
    coredns = {
      most_recent = true
    }
    kube-proxy = {
      most_recent = true
    }
    vpc-cni = {
      most_recent = true
    }
    aws-ebs-csi-driver = {
      most_recent = true
    }
  }

  # Node groups
  eks_managed_node_groups = {
    general = {
      name           = "general"
      instance_types = var.eks_node_instance_types
      
      min_size     = var.eks_node_group_min_size
      max_size     = var.eks_node_group_max_size
      desired_size = var.eks_node_group_desired_size

      disk_size = 50
      ami_type  = "AL2_x86_64"
      
      labels = {
        role = "general"
      }
      
      taints = []
      
      update_config = {
        max_unavailable_percentage = 33
      }
    }

    mlops = {
      name           = "mlops"
      instance_types = var.eks_mlops_instance_types
      
      min_size     = 1
      max_size     = 10
      desired_size = 2

      disk_size = 100
      ami_type  = "AL2_x86_64"
      
      labels = {
        role = "mlops"
        "node.kubernetes.io/workload" = "mlops"
      }
      
      taints = [
        {
          key    = "mlops"
          value  = "true"
          effect = "NO_SCHEDULE"
        }
      ]
    }

    gpu = {
      name           = "gpu"
      instance_types = ["g4dn.xlarge"]
      
      min_size     = 0
      max_size     = 5
      desired_size = 0

      disk_size = 100
      ami_type  = "AL2_x86_64_GPU"
      
      labels = {
        role = "gpu"
        "node.kubernetes.io/accelerator" = "nvidia-tesla-t4"
      }
      
      taints = [
        {
          key    = "gpu"
          value  = "true"
          effect = "NO_SCHEDULE"
        }
      ]
    }
  }

  # Allow worker nodes to join cluster
  node_security_group_additional_rules = {
    ingress_self_all = {
      description = "Node to node all ports/protocols"
      protocol    = "-1"
      from_port   = 0
      to_port     = 0
      type        = "ingress"
      self        = true
    }
  }

  tags = local.common_tags
}

# ============================================================================
# RDS DATABASE (MLflow Backend Store)
# ============================================================================

resource "aws_db_subnet_group" "mlops" {
  name       = "${local.name_prefix}-db-subnet-group"
  subnet_ids = module.vpc.database_subnets

  tags = merge(local.common_tags, {
    Name = "${local.name_prefix}-db-subnet-group"
  })
}

resource "aws_security_group" "rds" {
  name_prefix = "${local.name_prefix}-rds-"
  vpc_id      = module.vpc.vpc_id

  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = [module.vpc.vpc_cidr]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(local.common_tags, {
    Name = "${local.name_prefix}-rds-sg"
  })
}

resource "random_password" "db_password" {
  length  = 16
  special = true
}

resource "aws_db_instance" "mlops" {
  identifier = "${local.name_prefix}-mlops-db"

  engine         = "postgres"
  engine_version = "15.3"
  instance_class = var.rds_instance_class

  allocated_storage     = var.rds_allocated_storage
  max_allocated_storage = var.rds_max_allocated_storage
  storage_type          = "gp3"
  storage_encrypted     = true

  db_name  = "mlops"
  username = "mlops"
  password = random_password.db_password.result

  vpc_security_group_ids = [aws_security_group.rds.id]
  db_subnet_group_name   = aws_db_subnet_group.mlops.name

  backup_retention_period = var.environment == "prod" ? 7 : 1
  backup_window          = "03:00-04:00"
  maintenance_window     = "Sun:04:00-Sun:05:00"

  skip_final_snapshot       = var.environment != "prod"
  final_snapshot_identifier = var.environment == "prod" ? "${local.name_prefix}-final-snapshot-${formatdate("YYYY-MM-DD-hhmm", timestamp())}" : null
  deletion_protection       = var.environment == "prod"

  performance_insights_enabled = true
  monitoring_interval         = 60

  tags = merge(local.common_tags, {
    Name = "${local.name_prefix}-mlops-db"
  })
}

# ============================================================================
# ELASTICACHE REDIS (Feature Store Online Storage)
# ============================================================================

resource "aws_elasticache_subnet_group" "mlops" {
  name       = "${local.name_prefix}-redis-subnet-group"
  subnet_ids = module.vpc.private_subnets

  tags = merge(local.common_tags, {
    Name = "${local.name_prefix}-redis-subnet-group"
  })
}

resource "aws_security_group" "redis" {
  name_prefix = "${local.name_prefix}-redis-"
  vpc_id      = module.vpc.vpc_id

  ingress {
    from_port   = 6379
    to_port     = 6379
    protocol    = "tcp"
    cidr_blocks = [module.vpc.vpc_cidr]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(local.common_tags, {
    Name = "${local.name_prefix}-redis-sg"
  })
}

resource "aws_elasticache_replication_group" "mlops" {
  replication_group_id         = "${local.name_prefix}-redis"
  description                  = "Redis cluster for MLOps feature store"

  node_type                   = var.redis_node_type
  port                        = 6379
  parameter_group_name        = "default.redis7"

  num_cache_clusters          = var.redis_num_cache_nodes
  automatic_failover_enabled  = var.redis_num_cache_nodes > 1
  multi_az_enabled           = var.redis_num_cache_nodes > 1

  subnet_group_name          = aws_elasticache_subnet_group.mlops.name
  security_group_ids         = [aws_security_group.redis.id]

  at_rest_encryption_enabled = true
  transit_encryption_enabled = true

  maintenance_window         = "sun:05:00-sun:09:00"
  snapshot_retention_limit   = var.environment == "prod" ? 5 : 1
  snapshot_window           = "03:00-05:00"

  tags = local.common_tags
}

# ============================================================================
# S3 BUCKETS
# ============================================================================

# MLflow Artifacts Bucket
resource "aws_s3_bucket" "mlflow_artifacts" {
  bucket = "${local.name_prefix}-mlflow-artifacts-${random_string.suffix.result}"

  tags = merge(local.common_tags, {
    Name = "${local.name_prefix}-mlflow-artifacts"
    Purpose = "MLflow Artifacts Storage"
  })
}

resource "aws_s3_bucket_versioning" "mlflow_artifacts" {
  bucket = aws_s3_bucket.mlflow_artifacts.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "mlflow_artifacts" {
  bucket = aws_s3_bucket.mlflow_artifacts.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "mlflow_artifacts" {
  bucket = aws_s3_bucket.mlflow_artifacts.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Data Lake Bucket
resource "aws_s3_bucket" "data_lake" {
  bucket = "${local.name_prefix}-data-lake-${random_string.suffix.result}"

  tags = merge(local.common_tags, {
    Name = "${local.name_prefix}-data-lake"
    Purpose = "Data Lake Storage"
  })
}

resource "aws_s3_bucket_versioning" "data_lake" {
  bucket = aws_s3_bucket.data_lake.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "data_lake" {
  bucket = aws_s3_bucket.data_lake.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "data_lake" {
  bucket = aws_s3_bucket.data_lake.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Model Registry Bucket
resource "aws_s3_bucket" "model_registry" {
  bucket = "${local.name_prefix}-model-registry-${random_string.suffix.result}"

  tags = merge(local.common_tags, {
    Name = "${local.name_prefix}-model-registry"
    Purpose = "Model Registry Storage"
  })
}

resource "aws_s3_bucket_versioning" "model_registry" {
  bucket = aws_s3_bucket.model_registry.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "model_registry" {
  bucket = aws_s3_bucket.model_registry.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# ============================================================================
# IAM ROLES AND POLICIES
# ============================================================================

# EKS Service Account Role for MLflow
data "aws_iam_policy_document" "mlflow_assume_role_policy" {
  statement {
    actions = ["sts:AssumeRoleWithWebIdentity"]
    effect  = "Allow"

    condition {
      test     = "StringEquals"
      variable = "${replace(module.eks.cluster_oidc_issuer_url, "https://", "")}:sub"
      values   = ["system:serviceaccount:mlops:mlflow"]
    }

    principals {
      identifiers = [module.eks.oidc_provider_arn]
      type        = "Federated"
    }
  }
}

resource "aws_iam_role" "mlflow" {
  assume_role_policy = data.aws_iam_policy_document.mlflow_assume_role_policy.json
  name               = "${local.name_prefix}-mlflow-role"

  tags = local.common_tags
}

resource "aws_iam_policy" "mlflow_s3_access" {
  name = "${local.name_prefix}-mlflow-s3-access"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject",
          "s3:ListBucket"
        ]
        Resource = [
          aws_s3_bucket.mlflow_artifacts.arn,
          "${aws_s3_bucket.mlflow_artifacts.arn}/*",
          aws_s3_bucket.model_registry.arn,
          "${aws_s3_bucket.model_registry.arn}/*"
        ]
      }
    ]
  })

  tags = local.common_tags
}

resource "aws_iam_role_policy_attachment" "mlflow_s3_access" {
  policy_arn = aws_iam_policy.mlflow_s3_access.arn
  role       = aws_iam_role.mlflow.name
}

# ============================================================================
# SECRETS MANAGER
# ============================================================================

resource "aws_secretsmanager_secret" "mlops_secrets" {
  name = "${local.name_prefix}-mlops-secrets"

  tags = merge(local.common_tags, {
    Name = "${local.name_prefix}-mlops-secrets"
  })
}

resource "aws_secretsmanager_secret_version" "mlops_secrets" {
  secret_id = aws_secretsmanager_secret.mlops_secrets.id
  secret_string = jsonencode({
    database_url = "postgresql://${aws_db_instance.mlops.username}:${random_password.db_password.result}@${aws_db_instance.mlops.endpoint}/${aws_db_instance.mlops.db_name}"
    database_host = aws_db_instance.mlops.address
    database_port = aws_db_instance.mlops.port
    database_name = aws_db_instance.mlops.db_name
    database_username = aws_db_instance.mlops.username
    database_password = random_password.db_password.result
    redis_endpoint = aws_elasticache_replication_group.mlops.primary_endpoint_address
    redis_port = aws_elasticache_replication_group.mlops.port
    mlflow_artifacts_bucket = aws_s3_bucket.mlflow_artifacts.bucket
    data_lake_bucket = aws_s3_bucket.data_lake.bucket
    model_registry_bucket = aws_s3_bucket.model_registry.bucket
  })
}

# ============================================================================
# APPLICATION LOAD BALANCER
# ============================================================================

resource "aws_security_group" "alb" {
  name_prefix = "${local.name_prefix}-alb-"
  vpc_id      = module.vpc.vpc_id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(local.common_tags, {
    Name = "${local.name_prefix}-alb-sg"
  })
}

resource "aws_lb" "mlops" {
  name               = "${local.name_prefix}-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = module.vpc.public_subnets

  enable_deletion_protection = var.environment == "prod"

  tags = merge(local.common_tags, {
    Name = "${local.name_prefix}-alb"
  })
}

# ============================================================================
# MONITORING AND LOGGING
# ============================================================================

# CloudWatch Log Groups
resource "aws_cloudwatch_log_group" "eks_cluster" {
  name              = "/aws/eks/${module.eks.cluster_name}/cluster"
  retention_in_days = var.cloudwatch_retention_days

  tags = local.common_tags
}

resource "aws_cloudwatch_log_group" "mlops_application" {
  name              = "/aws/mlops/${local.name_prefix}/application"
  retention_in_days = var.cloudwatch_retention_days

  tags = local.common_tags
}

# ============================================================================
# OUTPUTS
# ============================================================================

output "vpc_id" {
  description = "VPC ID"
  value       = module.vpc.vpc_id
}

output "private_subnets" {
  description = "Private subnet IDs"
  value       = module.vpc.private_subnets
}

output "public_subnets" {
  description = "Public subnet IDs"
  value       = module.vpc.public_subnets
}

output "eks_cluster_id" {
  description = "EKS cluster ID"
  value       = module.eks.cluster_id
}

output "eks_cluster_arn" {
  description = "EKS cluster ARN"
  value       = module.eks.cluster_arn
}

output "eks_cluster_endpoint" {
  description = "EKS cluster endpoint"
  value       = module.eks.cluster_endpoint
}

output "eks_cluster_name" {
  description = "EKS cluster name"
  value       = module.eks.cluster_name
}

output "rds_endpoint" {
  description = "RDS instance endpoint"
  value       = aws_db_instance.mlops.endpoint
  sensitive   = true
}

output "redis_endpoint" {
  description = "Redis cluster endpoint"
  value       = aws_elasticache_replication_group.mlops.primary_endpoint_address
  sensitive   = true
}

output "mlflow_artifacts_bucket" {
  description = "MLflow artifacts S3 bucket name"
  value       = aws_s3_bucket.mlflow_artifacts.bucket
}

output "data_lake_bucket" {
  description = "Data lake S3 bucket name"
  value       = aws_s3_bucket.data_lake.bucket
}

output "model_registry_bucket" {
  description = "Model registry S3 bucket name"
  value       = aws_s3_bucket.model_registry.bucket
}

output "secrets_manager_arn" {
  description = "Secrets Manager ARN for MLOps secrets"
  value       = aws_secretsmanager_secret.mlops_secrets.arn
}

output "load_balancer_dns" {
  description = "Load balancer DNS name"
  value       = aws_lb.mlops.dns_name
}

output "mlflow_service_account_role_arn" {
  description = "MLflow service account IAM role ARN"
  value       = aws_iam_role.mlflow.arn
}
