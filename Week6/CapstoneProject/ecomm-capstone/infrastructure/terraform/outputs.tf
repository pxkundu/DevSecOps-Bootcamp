output "cluster_endpoint" {
  value = module.eks.cluster_endpoint
}

output "alb_url" {
  value = "<ALB_DNS_NAME>" # Replace with actual ALB DNS after apply
}
