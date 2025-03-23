output "s3_bucket_url" {
  value = "http://${aws_s3_bucket.website.bucket_regional_domain_name}"
}

output "cloudfront_domain" {
  value = "https://${aws_cloudfront_distribution.cdn.domain_name}"
}

output "jenkins_public_ip" {
  value = aws_instance.jenkins.public_ip
}