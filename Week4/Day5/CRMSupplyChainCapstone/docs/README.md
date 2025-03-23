# CRM-Integrated Global Supply Chain System

## What is This Project?
This capstone project is a multi-region, production-grade application integrating a **Customer Relationship Management (CRM)** system with a **Global Supply Chain Management System**. Built as part of a Week 4, Day 5 DevOps bootcamp, it simulates a real-world enterprise solution for managing customer orders and supply chain operations (e.g., inventory, logistics) across North America (`us-east-1`) and Europe (`eu-west-1`). The system leverages **Terraform** for infrastructure, **Kubernetes (EKS)** for orchestration, **Docker** for containerization, and **Jenkins** for CI/CD automation, all hosted on AWS.

### High-Level Ideas
- **Unified System**: Combines CRM (customer orders, analytics) with supply chain (inventory, shipping) for seamless business operations.
- **Multi-Region**: Ensures low-latency access and resilience with failover between `us-east-1` and `eu-west-1`.
- **DevSecOps**: Embeds security, automation, and observability best practices.
- **Cost Optimization**: Balances performance and budget (~$60-70/month AWS spend) for learning and scalability.

## How It is Designed?
The project is architected in **five phases** to ensure clarity and success:
1. **Design (Phase 1)**: Blueprint for multi-region infra (EKS, VPCs, RDS, S3, ECR) using Terraform, reusing Day 2’s CRM setup.
2. **Backend (Phase 2)**: Microservices for CRM (`crm-api`) and supply chain (`inventory-service`, `logistics-service`, `order-service`).
3. **Frontend (Phase 3)**: User interfaces (`crm-ui`, `tracking-ui`) for customer and supply chain interaction.
4. **Core Features (Phase 4)**: Integration (e.g., order-to-inventory sync), Kubernetes deployments, and Ingress routing.
5. **Delivery (Phase 5)**: Jenkins pipeline, DevSecOps practices, and automated testing.

### Key Design Components
- **Infrastructure**: 
  - EKS clusters (2 t3.medium nodes per region) with modular VPCs (1 NAT Gateway/region).
  - RDS (t3.micro, single-AZ) in `us-east-1` for shared data.
  - S3 (Standard-IA) and DynamoDB for Terraform state.
  - ECR with lifecycle policies for 8 microservices.
- **Microservices**: 8 Dockerized services (CRM: 3, Supply Chain: 5) deployed on EKS with namespaces (`crm-us`, `supply-eu`).
- **CI/CD**: Jenkins pipeline builds, pushes to ECR, and deploys with zero-downtime rolling updates.

## Why This Solution?
- **Reuse**: Extends Day 2’s CRM infra, minimizing rework and cost, akin to Amazon’s IaC efficiency.
- **Multi-Region**: Mimics Walmart’s global supply chain reach, ensuring resilience and low latency.
- **Cost Efficiency**: t3 instances, single-AZ RDS, and lifecycle policies keep AWS spend low (~$60-70/month), ideal for learning and scaling.
- **Terraform + Kubernetes**: Industry-standard combo for IaC and orchestration, used by DHL for logistics systems.
- **DevSecOps**: Security (IAM, encryption), modularity, and automation reflect enterprise priorities.

## Why Industry Standard?
- **Modular IaC**: Terraform modules (e.g., `vpc`, `eks`) mirror Amazon’s reusable infra patterns.
- **Microservices**: Service isolation (e.g., `inventory-service`) aligns with Walmart’s architecture.
- **Multi-Region Resilience**: Failover design matches DHL’s logistics uptime needs.
- **GitOps**: Jenkins pipeline triggered by Git commits reflects modern CI/CD (e.g., Netflix).
- **Security**: Least-privilege IAM and RBAC prep meet compliance (SOC 2, GDPR), a Fortune 100 must.

## Learning Benefits
This project teaches best practices for key DevOps technologies:
- **Terraform**: Modular IaC, remote state management, cost optimization.
- **Kubernetes**: Deployments, Services, Ingress, HPA, multi-region orchestration.
- **Docker**: Containerization for microservices, image lifecycle management.
- **Jenkins**: Pipeline as Code, GitOps, zero-downtime deployments.
- **AWS**: EKS, RDS, S3, ECR in a production-like setup.
- **DevSecOps**: Security (encryption, IAM), observability prep, and automated testing.

By building this, learners gain hands-on experience with enterprise-grade workflows, preparing for roles at companies like Walmart, Amazon, or DHL.

## Project Folder Structure
```
CRMSupplyChainCapstone/
├── docs/                       # Documentation
│   ├── architecture.md         # System architecture overview
│   └── README.md              # Project setup and usage
├── infrastructure/             # Terraform IaC
│   ├── main.tf                # Root configuration
│   ├── variables.tf           # Input variables
│   ├── outputs.tf             # Output values
│   ├── backend.tf             # Remote state config
│   ├── terraform.tfvars       # Variable overrides (gitignored)
│   └── modules/               # Reusable Terraform modules
│       ├── vpc/               # VPC module
│       │   ├── main.tf
│       │   ├── variables.tf
│       │   └── outputs.tf
│       ├── eks/               # EKS module
│       │   ├── main.tf
│       │   ├── variables.tf
│       │   └── outputs.tf
│       └── rds/               # RDS module
│           ├── main.tf
│           ├── variables.tf
│           └── outputs.tf
├── services/                   # Microservices code
│   ├── crm-api/               # CRM API service
│   │   ├── Dockerfile
│   │   ├── app.js
│   │   └── package.json
│   ├── crm-ui/                # CRM UI service
│   │   ├── Dockerfile
│   │   ├── app.js
│   │   └── package.json
│   ├── crm-analytics/         # CRM analytics service
│   │   ├── Dockerfile
│   │   ├── app.js
│   │   └── package.json
│   ├── inventory-service/     # Supply chain inventory service
│   │   ├── Dockerfile
│   │   ├── app.js
│   │   └── package.json
│   ├── logistics-service/     # Supply chain logistics service
│   │   ├── Dockerfile
│   │   ├── app.js
│   │   └── package.json
│   ├── order-service/         # Supply chain order service
│   │   ├── Dockerfile
│   │   ├── app.js
│   │   └── package.json
│   ├── analytics-service/     # Supply chain analytics service
│   │   ├── Dockerfile
│   │   ├── app.js
│   │   └── package.json
│   └── api-gateway/           # NGINX API gateway
│       ├── Dockerfile
│       ├── nginx.conf
│       └── entrypoint.sh
├── kubernetes/                 # Kubernetes manifests
│   ├── crm/                   # CRM K8s resources
│   │   ├── deployment.yaml
│   │   └── service.yaml
│   ├── supply-chain/          # Supply chain K8s resources
│   │   ├── inventory-deployment.yaml
│   │   ├── inventory-service.yaml
│   │   ├── logistics-deployment.yaml
│   │   ├── logistics-service.yaml
│   │   ├── order-deployment.yaml
│   │   ├── order-service.yaml
│   │   ├── analytics-deployment.yaml
│   │   └── analytics-service.yaml
│   └── ingress/               # Ingress configuration
│       └── ingress.yaml
├── pipeline/                   # CI/CD configuration
│   ├── Jenkinsfile            # Jenkins pipeline
│   └── scripts/               # Helper scripts
│       ├── build.sh
│       ├── deploy.sh
│       └── test.sh
├── tests/                      # Automated tests
│   ├── integration/           # Integration tests
│   │   └── test-order-flow.sh
│   └── unit/                  # Unit tests
│       └── test-services.sh
├── .gitignore                 # Git ignore file
└── .dockerignore              # Docker ignore file
```
---

## Next Steps
- **Phase 1**: Implement infrastructure in `infrastructure/` using Terraform.
- Follow the 5-phase plan to build, deploy, and test the system.

This project is your gateway to mastering enterprise DevOps—start exploring!

---

### Explanation
- **What**: Clearly defines the project’s scope and purpose, tying CRM and supply chain together.
- **How**: Outlines the 5-phase design and key components, providing a high-level roadmap.
- **Why**: Justifies choices with cost, efficiency, and industry relevance, grounding decisions in real-world needs.
- **Industry Standard**: Links to Fortune 100 practices (modularity, resilience, security) for credibility.
- **Learning**: Highlights skill-building opportunities, making it educational and practical.
- **Folder Structure**: Matches the script from the previous response, ensuring consistency.

