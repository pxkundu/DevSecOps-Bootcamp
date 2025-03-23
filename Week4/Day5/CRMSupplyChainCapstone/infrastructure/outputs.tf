output "eks_endpoints" {
  value = { for region, eks in module.eks : region => eks.cluster_endpoint }
}

output "rds_endpoint" {
  value = module.rds.rds_endpoint
}
