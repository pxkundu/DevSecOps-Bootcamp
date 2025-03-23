provider "aws" {
  region = "us-east-1"  # Default region for Terraform operations
}

# Multi-region VPCs
module "vpc" {
  source   = "./modules/vpc"
  for_each = var.regions
  region   = each.key
  cidr     = each.value.cidr
}

# Multi-region EKS clusters
module "eks" {
  source     = "./modules/eks"
  for_each   = var.regions
  region     = each.key
  vpc_id     = module.vpc[each.key].vpc_id
  subnet_ids = module.vpc[each.key].private_subnet_ids
}

# RDS in us-east-1 only
module "rds" {
  source         = "./modules/rds"
  vpc_id         = module.vpc["us-east-1"].vpc_id
  subnet_ids     = module.vpc["us-east-1"].private_subnet_ids
  db_name        = "crm_supply_db"
  instance_class = "db.t3.micro"
}

# ECR repositories for all microservices
resource "aws_ecr_repository" "services" {
  for_each = toset([
    "crm-api", "crm-ui", "crm-analytics",
    "inventory-service", "logistics-service", "order-service",
    "analytics-service", "api-gateway"
  ])
  name = "supplychain-crm/${each.key}"
}
