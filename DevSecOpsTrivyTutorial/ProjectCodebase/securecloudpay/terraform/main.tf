provider "aws" {
  region = "us-west-2"
}

resource "aws_s3_bucket" "insecure_bucket" {
  bucket = "securecloudpay-dev"
  acl    = "public-read"
}
