provider "aws" {
  region = var.region
}

module "eks" {
  source          = "terraform-aws-modules/eks/aws"
  cluster_name    = "ecomm-cluster"
  cluster_version = "1.29"
  vpc_id          = var.vpc_id
  subnet_ids      = var.subnet_ids
  node_groups = {
    ng1 = {
      instance_types = ["t4g.medium"]
      min_size       = 2
      max_size       = 4
      desired_size   = 2
    }
  }
}

# Simplified Karpenter setup (requires additional IAM and Helm setup in practice)
resource "aws_eks_addon" "karpenter" {
  cluster_name = module.eks.cluster_id
  addon_name   = "karpenter"
}
