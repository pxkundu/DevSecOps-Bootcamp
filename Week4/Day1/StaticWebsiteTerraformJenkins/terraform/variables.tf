variable "bucket_name" {
  description = "Name of the S3 bucket"
  type        = string
  default     = "my-static-website-2025"  # Replace with unique name
}

variable "region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "key_name" {
  description = "EC2 key pair name"
  type        = string
  default     = "my-key"  # Replace with your key pair
}