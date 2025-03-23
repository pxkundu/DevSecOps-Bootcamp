variable "regions" {
  description = "Map of regions for deployment"
  type        = map(string)
  default     = {
    "us-east-1" = "use1"
    "eu-west-1" = "euw1"
  }
}

variable "key_name" {
  description = "EC2 key pair name"
  type        = string
  default     = "my-key"  # Replace with your key pair
}

variable "bucket_name" {
  description = "S3 bucket for Terraform state"
  type        = string
  default     = "crm-tf-state-2025"  # Must be unique
}
