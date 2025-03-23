## Week 4, Day 5: Capstone Project - Global Supply Chain Management System

### Overview
- Build a multi-region supply chain system using Terraform and Kubernetes.
- Integrate Docker, Jenkins, GitHub, and AWS for automation and deployment.

### Objectives
- Provision multi-region infra with Terraform.
- Deploy supply chain microservices on EKS with Kubernetes.
- Automate via Jenkins pipeline from GitHub.

### Time Allocation
- **Planning & Review**: 1 hour
- **Implementation**: 2 hours
- **Total**: 3 hours

### Plan
1. **Infrastructure Setup (Terraform)**:
   - Provision EKS clusters in `us-east-1` and `eu-west-1`.
   - Use modules for VPCs, EKS, and state management (S3 backend).
2. **Application Development**:
   - Microservices: `inventory-api`, `tracking-ui`, `logistics-worker`.
   - Dockerize each component.
3. **Kubernetes Deployment**:
   - Deploy microservices to EKS with Deployments and Services.
   - Use namespaces (`prod-us`, `prod-eu`) for isolation.
4. **CI/CD Pipeline (Jenkins)**:
   - Build Docker images, push to ECR, apply Terraform and K8s manifests.
   - Trigger on GitHub commits.
5. **Verification**:
   - Test supply chain functionality (e.g., track inventory across regions).
   - Validate scalability and resilience.

### Tools
- Terraform, Kubernetes (EKS), Docker, Jenkins, GitHub, AWS.

### Deliverables
- Running supply chain system.
- Automated pipeline documentation.

---

This brief plan aligns with Week 4’s progression—Terraform (Days 1-2), Kubernetes (Days 3-4)—and caps it with a practical, industry-relevant project.