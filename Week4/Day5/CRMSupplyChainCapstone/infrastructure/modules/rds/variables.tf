variable "vpc_id" {}
variable "subnet_ids" {}
variable "db_name" {}
variable "db_username" {}
variable "db_password" { sensitive = true }
variable "encryption" {}
