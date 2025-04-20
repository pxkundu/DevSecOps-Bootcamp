module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 18.0"
  cluster_name    = "{{EKS_CLUSTER_NAME}}"  # Replace with your EKS cluster name
  cluster_version = "1.21"
  vpc_id          = "{{VPC_ID}}"  # Replace with your VPC ID
  subnets         = {{SUBNET_IDS}}  # Replace with your subnet IDs (e.g., ["subnet-123", "subnet-456"])
  node_groups = {
    eks_nodes = {
      desired_capacity = 2
      max_capacity     = 3
      min_capacity     = 1
      instance_type    = "t3.medium"
    }
  }
}
