# Custom Nginx Helm Chart

This Helm chart deploys an Nginx web server with configurable replicas, service, and ingress.

## Prerequisites
- Kubernetes 1.19+
- Helm 3.0+
- An ingress controller (e.g., nginx-ingress) if ingress is enabled

## Installation
```bash
helm install custom-nginx ./helm-charts/custom-nginx -n partha-app-ns
```

## Values
| Key                | Description                  | Default             |
|--------------------|------------------------------|---------------------|
| replicaCount      | Number of replicas           | 2                   |
| image.repository  | Nginx image repository       | nginx               |
| image.tag         | Nginx image tag              | 1.25                |
| service.type      | Service type                 | ClusterIP           |
| ingress.enabled   | Enable ingress               | true                |
| ingress.host      | Ingress hostname             | nginx.example.com   |

## Contributing
Fork the repo, make changes, and submit a PR to https://github.com/yourusername/your-repo.
