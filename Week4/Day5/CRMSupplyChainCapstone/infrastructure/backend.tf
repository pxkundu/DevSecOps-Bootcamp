terraform {
  backend "s3" {
    bucket         = "crm-tf-state-2025"
    key            = "terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "tf-lock"
  }
}
