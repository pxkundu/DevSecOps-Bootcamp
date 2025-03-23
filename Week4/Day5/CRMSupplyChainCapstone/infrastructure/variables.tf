variable "regions" {
  description = "Map of regions with CIDR blocks"
  type        = map(object({
    cidr = string
  }))
  default = {
    "us-east-1" = { cidr = "10.0.0.0/16" }
    "eu-west-1" = { cidr = "10.1.0.0/16" }
  }
}

variable "instance_type" {
  description = "EKS node instance type"
  type        = string
  default     = "t3.medium"
}

variable "node_count" {
  description = "Number of EKS nodes per region"
  type        = number
  default     = 2
}
