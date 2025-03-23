# Multi-region VPCs and EKS clusters
module "vpc" {
  for_each = var.regions
  source   = "./modules/vpc"
  region   = each.key
  env      = terraform.workspace
}

module "eks" {
  for_each = var.regions
  source   = "./modules/eks"
  region   = each.key
  env      = terraform.workspace
  vpc_id   = module.vpc[each.key].vpc_id
  subnet_ids = module.vpc[each.key].subnet_ids
}

# Jenkins instance
module "jenkins" {
  source       = "./modules/jenkins"
  region       = "us-east-1"  # Jenkins in primary region
  env          = terraform.workspace
  vpc_id       = module.vpc["us-east-1"].vpc_id
  subnet_id    = module.vpc["us-east-1"].subnet_ids[0]
  key_name     = var.key_name
}

# ECR repositories for Docker images
resource "aws_ecr_repository" "crm_services" {
  for_each = toset(["crm-api", "crm-ui", "crm-analytics"])
  name     = "${terraform.workspace}-${each.key}"
}
