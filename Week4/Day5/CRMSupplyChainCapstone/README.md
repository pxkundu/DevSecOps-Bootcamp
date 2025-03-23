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
│   ├── CONFIG-README-FRONTEND.md  # Phase 3: Frontend setup guide (new)
│   └── README.md               # Project setup and usage
├── infrastructure/             # Terraform IaC (placeholder for Phase 5)
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
│   ├── crm-api/               # CRM API service (Phase 2 placeholder)
│   │   ├── Dockerfile
│   │   ├── app.js
│   │   └── package.json
│   ├── crm-ui/                # CRM UI service (Phase 3)
│   │   ├── Dockerfile         # Phase 3: Docker config
│   │   ├── app.js             # Phase 3: Express app
│   │   ├── package.json       # Phase 3: Dependencies
│   │   ├── views/             # Phase 3: EJS templates
│   │   │   ├── index.ejs      # Phase 3: Dashboard
│   │   │   ├── order-details.ejs  # Phase 3: Order details
│   │   │   └── partials/      # Phase 3: Reusable components
│   │   │       └── order-table.ejs  # Phase 3: Order table
│   │   └── public/            # Phase 3: Static assets
│   │       ├── styles.css     # Phase 3: CSS
│   │       └── script.js      # Phase 3: Client-side JS
│   ├── crm-analytics/         # CRM analytics service (Phase 2 placeholder)
│   │   ├── Dockerfile
│   │   ├── app.js
│   │   └── package.json
│   ├── inventory-service/     # Supply chain inventory service (Phase 2 placeholder)
│   │   ├── Dockerfile
│   │   ├── app.js
│   │   └── package.json
│   ├── logistics-service/     # Supply chain logistics service (Phase 2 placeholder)
│   │   ├── Dockerfile
│   │   ├── app.js
│   │   └── package.json
│   ├── order-service/         # Supply chain order service (Phase 2 placeholder)
│   │   ├── Dockerfile
│   │   ├── app.js
│   │   └── package.json
│   ├── analytics-service/     # Supply chain analytics service (Phase 2 placeholder)
│   │   ├── Dockerfile
│   │   ├── app.js
│   │   └── package.json
│   └── api-gateway/           # NGINX API gateway (Phase 2 placeholder)
│       ├── Dockerfile
│       ├── nginx.conf
│       └── entrypoint.sh
├── kubernetes/                 # Kubernetes manifests
│   ├── crm/                   # CRM K8s resources
│   │   ├── deployment.yaml    # Original placeholder (empty)
│   │   ├── service.yaml       # Original placeholder (empty)
│   │   ├── crm-ui-deployment.yaml       # Phase 4: CRM UI deployment
│   │   ├── crm-ui-service.yaml          # Phase 4: CRM UI service
│   │   ├── crm-api-deployment.yaml      # Phase 4: CRM API deployment
│   │   ├── crm-api-service.yaml         # Phase 4: CRM API service
│   │   ├── order-service-deployment.yaml  # Phase 4: Order service deployment
│   │   ├── order-service-service.yaml    # Phase 4: Order service
│   │   ├── crm-analytics-deployment.yaml  # Phase 4: CRM analytics deployment
│   │   └── crm-analytics-service.yaml    # Phase 4: CRM analytics service
│   ├── supply-chain/          # Supply chain K8s resources
│   │   ├── inventory-deployment.yaml     # Phase 4: Inventory deployment (updated from placeholder)
│   │   ├── inventory-service.yaml        # Phase 4: Inventory service (updated from placeholder)
│   │   ├── logistics-deployment.yaml     # Phase 4: Logistics deployment (updated from placeholder)
│   │   ├── logistics-service.yaml        # Phase 4: Logistics service (updated from placeholder)
│   │   ├── order-deployment.yaml         # Phase 4: Order deployment (updated from placeholder)
│   │   ├── order-service.yaml            # Phase 4: Order service (updated from placeholder)
│   │   ├── analytics-deployment.yaml     # Phase 4: Analytics deployment (updated from placeholder)
│   │   ├── analytics-service.yaml        # Phase 4: Analytics service (updated from placeholder)
│   │   ├── tracking-ui-deployment.yaml   # Phase 4: Tracking UI deployment
│   │   ├── tracking-ui-service.yaml      # Phase 4: Tracking UI service
│   │   └── analytics-service-hpa.yaml    # Phase 4: HPA for analytics-service
│   └── ingress/               # Ingress configuration
│       └── ingress.yaml       # Phase 4: NGINX Ingress (updated from placeholder)
├── pipeline/                   # CI/CD configuration (placeholder for Phase 5)
│   ├── Jenkinsfile            # Jenkins pipeline
│   └── scripts/               # Helper scripts
│       ├── build.sh
│       ├── deploy.sh
│       └── test.sh
├── tests/                      # Automated tests (placeholder)
│   ├── integration/           # Integration tests
│   │   └── test-order-flow.sh
│   └── unit/                  # Unit tests
│       └── test-services.sh
├── .gitignore                 # Git ignore file (updated in Phase 3/4)
└── .dockerignore              # Docker ignore file (updated in Phase 3/4)
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

