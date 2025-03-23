# GitOps Security Best Practices

Notes on securing GitOps workflows for Task Manager.

## Key Principles
- **Least Privilege**: IAM roles scoped to ECR push/pull.
- **Secrets Management**: AWS Secrets Manager for all creds.
- **Immutable Artifacts**: ECR updates post-deploy with tags.
- **GitOps Security**: Encrypted Git access, RBAC, drift detection.
- **Auditability**: CloudTrail, Git, and ArgoCD logs.
