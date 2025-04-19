variable "region" {
  default = "us-east-1"
}

variable "vpc_id" {
  description = "VPC ID for EKS"
}

variable "subnet_ids" {
  description = "Subnet IDs for EKS (3 AZs)"
  type        = list(string)
}
