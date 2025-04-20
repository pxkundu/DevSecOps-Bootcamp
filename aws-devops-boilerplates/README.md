# AWS DevOps Boilerplates

A collection of reusable AWS DevOps templates following best practices for security, scalability, and automation.

## Structure
- **cloudformation/**: CloudFormation templates (e.g., VPC, cost budgets).
- **docker/**: Dockerfiles and image scanning for ECS.
- **codepipeline/**: CI/CD pipelines with testing stages.
- **ecs/**: ECS task definitions and auto-scaling policies.
- **lambda/**: SAM templates and error monitoring for serverless apps.
- **terraform/**: Terraform modules (e.g., S3, backups).
- **iam/**: IAM roles and MFA enforcement.
- **cloudwatch/**: Alarms for EC2 and ALB performance.
- **secrets/**: Secrets Manager integration and rotation.
- **eks/**: EKS cluster setup and pod security policies.

## Usage
1. Clone the repo
2. Customize templates as needed (e.g., update ARNs, regions).
3. Deploy using AWS CLI, Terraform, or AWS Console.

## Prerequisites
- AWS CLI
- Terraform (for terraform/*)
- Docker (for docker/*)
- GitHub Actions (for docker/image-scan.yml)

## Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License
MIT License. See [LICENSE](LICENSE).

---

*Prepared by {Partha Sarathi Kundu} on April 19, 2025, for the AWS Boilerplate writing project.*