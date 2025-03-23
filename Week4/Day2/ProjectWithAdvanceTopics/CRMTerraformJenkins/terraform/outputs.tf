output "eks_cluster_endpoints" {
  value = { for region, eks in module.eks : region => eks.cluster_endpoint }
}

output "jenkins_public_ip" {
  value = module.jenkins.jenkins_public_ip
}

output "ecr_repositories" {
  value = { for repo in aws_ecr_repository.crm_services : repo.name => repo.repository_url }
}
