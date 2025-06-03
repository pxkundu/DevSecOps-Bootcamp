resource "aws_eks_node_group" "node_group" {
  cluster_name    = "{{EKS_CLUSTER_NAME}}"  # Replace with your EKS cluster name
  node_group_name = "main-node-group"
  node_role_arn   = aws_iam_role.node_role.arn
  subnet_ids      = {{SUBNET_IDS}}  # Replace with your subnet IDs (e.g., ["subnet-123", "subnet-456"])
  scaling_config {
    desired_size = 2
    max_size     = 4
    min_size     = 1
  }
}

resource "aws_iam_role" "node_role" {
  name = "eks-node-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "node_policy" {
  role       = aws_iam_role.node_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy"
}
