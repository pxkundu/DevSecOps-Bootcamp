variable "region" {
  default = "us-east-1"
}

variable "vpc_cidr" {
  default = "10.0.0.0/16"
}

variable "cluster_name" {
  default = "crm-supply-eks"
}

variable "db_password" {
  sensitive = true
}
