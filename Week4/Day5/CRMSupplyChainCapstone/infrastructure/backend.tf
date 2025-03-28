terraform {
  backend "s3" {
    bucket         = "<your-s3-bucket>"
    key            = "terraform/state"
    region         = "us-east-1"
    dynamodb_table = "terraform-locks"
  }
}
