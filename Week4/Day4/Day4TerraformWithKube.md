## Week 4, Day 4: Advanced Kubernetes with Terraform (Enhanced CRM Project)

### Overview
Day 4 now leverages Terraform to provision and manage Kubernetes resources on EKS, enhancing the CRM Platform with advanced K8s features. You’ll secure, scale, and optimize the `crm-api`, `crm-ui`, and `crm-analytics` microservices, integrating Terraform for infrastructure as code (IaC) and Kubernetes for orchestration. This reflects Fortune 100 practices where IaC and container orchestration converge for scalability, security, and team collaboration.

### Learning Objectives
- Combine Terraform and Kubernetes for end-to-end IaC and orchestration.
- Implement Ingress, HPA, ConfigMaps, Secrets, and RBAC on the CRM app.
- Apply Fortune 100 best practices for multi-team, production-grade deployments.
- Simulate a real-world CRM use case (e.g., Salesforce-like system).

### Prerequisites
- Day 2’s `CRMTerraformJenkins` project (EKS clusters, ECR images).
- Day 3’s Kubernetes basics (`kubectl`, EKS setup).
- Tools: Terraform, `kubectl`, Helm, AWS CLI, Jenkins.

### Time Allocation
- **Theory**: 2 hours
- **Practical**: 2 hours
- **Total**: 4 hours

---

### Theoretical Explanation

#### Key Concepts & Keywords
1. **Terraform + Kubernetes Integration**:
   - **Definition**: Terraform provisions EKS clusters and K8s resources (e.g., namespaces, RBAC) via the Kubernetes provider.
   - **Why**: Ensures reproducible infra and app states, aligning IaC with orchestration.
   - **Components**: `kubernetes` provider, `aws_eks_cluster` resource.

2. **Ingress**:
   - **Definition**: Routes external traffic to CRM Services (e.g., `crm-api`, `crm-ui`).
   - **Terraform**: Defines `kubernetes_ingress_v1` resources.
   - **Why**: Centralizes traffic management, reduces AWS LoadBalancer costs.

3. **Horizontal Pod Autoscaling (HPA)**:
   - **Definition**: Scales CRM Pods based on CPU/memory metrics.
   - **Terraform**: `kubernetes_horizontal_pod_autoscaler_v2`.
   - **Why**: Handles peak CRM usage (e.g., sales campaigns).

4. **ConfigMap**:
   - **Definition**: Stores CRM config (e.g., API endpoints, timeouts).
   - **Terraform**: `kubernetes_config_map`.
   - **Why**: Separates config from code, enabling dynamic updates.

5. **Secret**:
   - **Definition**: Secures CRM sensitive data (e.g., DB creds).
   - **Terraform**: `kubernetes_secret`.
   - **Why**: Enhances security in multi-team setups.

6. **Role-Based Access Control (RBAC)**:
   - **Definition**: Restricts access to CRM namespaces (e.g., `dev-us`).
   - **Terraform**: `kubernetes_role`, `kubernetes_role_binding`.
   - **Why**: Enforces least privilege for infra, app, and security teams.

7. **Helm Charts**:
   - **Definition**: Packages CRM K8s manifests for templated deployments.
   - **Why**: Simplifies complex rollouts, standard in Fortune 100.

#### Fortune 100 Best Practices
- **IaC + Orchestration**: Terraform provisions EKS, K8s manages workloads.
- **Multi-Team**: RBAC isolates namespaces (e.g., `dev-us` for devs, `prod-us` for ops).
- **Scalability**: HPA and Ingress optimize resource use and traffic.
- **Security**: Secrets encrypted, RBAC audited, Ingress with TLS.
- **Governance**: Terraform state in S3, Helm charts versioned in GitHub.

#### Why This Matters
- **Consistency**: Terraform ensures infra matches K8s desired state.
- **Scalability**: HPA and Ingress handle millions of CRM users.
- **Collaboration**: RBAC and namespaces support 100s of engineers.
- **Compliance**: Secrets and audit trails meet SOC 2, GDPR.

---

### Practical Use Cases & Real-World Applications

#### Practical Activity Plan
- **Objective**: Enhance the CRM Platform (`CRMTerraformJenkins`) with advanced K8s on EKS.
- **Setup**: Extend Day 2’s Terraform config and Day 3’s EKS deployment.
- **Tasks**:
  1. Update Terraform for K8s resources (Ingress, HPA, ConfigMap, Secret, RBAC).
  2. Deploy CRM microservices with Helm.
  3. Integrate with Jenkins pipeline for CI/CD.
- **Outcome**: A scalable, secure CRM on EKS, Fortune 100-ready.

#### Fortune 100 Use Case: Salesforce CRM Global Deployment
- **Scenario**: Salesforce deploys its CRM across `us-east-1` and `eu-west-1` for 10M users.
- **Context**: Multi-team (infra, app, security), high traffic, strict compliance.
- **Theoretical Application**:
  - **Terraform**: Provisions EKS, namespaces (`prod-us`, `prod-eu`).
  - **Ingress**: Routes `crm.salesforce.com` to `crm-ui`, `/api` to `crm-api`.
  - **HPA**: Scales `crm-api` from 5 to 50 Pods at 70% CPU.
  - **ConfigMap**: Stores API rate limits.
  - **Secret**: Holds Salesforce API keys.
  - **RBAC**: Grants devs `read-only` in `dev-us`, ops `full` in `prod-us`.
- **Practical Workflow**:
  - Terraform (`k8s.tf`):
    ```hcl
    provider "kubernetes" {
      host                   = module.eks["us-east-1"].cluster_endpoint
      cluster_ca_certificate = base64decode(module.eks["us-east-1"].cluster_ca)
      exec {
        api_version = "client.authentication.k8s.io/v1beta1"
        command     = "aws"
        args        = ["eks", "get-token", "--cluster-name", "dev-us-crm-us-east-1"]
      }
    }

    resource "kubernetes_namespace" "crm" {
      metadata {
        name = "dev-us"
      }
    }

    resource "kubernetes_config_map" "crm_config" {
      metadata {
        name      = "crm-config"
        namespace = "dev-us"
      }
      data = {
        "api_rate_limit" = "1000"
      }
    }

    resource "kubernetes_secret" "crm_secret" {
      metadata {
        name      = "crm-secret"
        namespace = "dev-us"
      }
      data = {
        "api_key" = base64encode("salesforce123")
      }
    }

    resource "kubernetes_ingress_v1" "crm_ingress" {
      metadata {
        name      = "crm-ingress"
        namespace = "dev-us"
        annotations = {
          "nginx.ingress.kubernetes.io/rewrite-target" = "/"
        }
      }
      spec {
        ingress_class_name = "nginx"
        rule {
          host = "crm.local"
          http {
            path {
              path      = "/"
              path_type = "Prefix"
              backend {
                service {
                  name = "crm-ui-service"
                  port { number = 80 }
                }
              }
            }
            path {
              path      = "/api"
              path_type = "Prefix"
              backend {
                service {
                  name = "crm-api-service"
                  port { number = 80 }
                }
              }
            }
          }
        }
      }
    }

    resource "kubernetes_horizontal_pod_autoscaler_v2" "crm_api_hpa" {
      metadata {
        name      = "crm-api-hpa"
        namespace = "dev-us"
      }
      spec {
        scale_target_ref {
          api_version = "apps/v1"
          kind        = "Deployment"
          name        = "crm-api"
        }
        min_replicas = 2
        max_replicas = 10
        metric {
          type = "Resource"
          resource {
            name = "cpu"
            target {
              type                = "Utilization"
              average_utilization = 70
            }
          }
        }
      }
    }

    resource "kubernetes_role" "dev_access" {
      metadata {
        name      = "dev-access"
        namespace = "dev-us"
      }
      rule {
        api_groups = [""]
        resources  = ["pods", "services"]
        verbs      = ["get", "list"]
      }
    }

    resource "kubernetes_role_binding" "dev_binding" {
      metadata {
        name      = "dev-binding"
        namespace = "dev-us"
      }
      subject {
        kind      = "User"
        name      = "dev-user"
        api_group = "rbac.authorization.k8s.io"
      }
      role_ref {
        kind      = "Role"
        name      = "dev-access"
        api_group = "rbac.authorization.k8s.io"
      }
    }
    ```
  - Helm Chart (optional, simplifies deployment):
    - Install NGINX Ingress:
      ```bash
      helm install nginx-ingress ingress-nginx/ingress-nginx -n ingress-nginx --create-namespace
      ```
  - Outcome: CRM scales to 10M users, secure and team-ready.
- **DevOps Impact**: 
  - Auto-scales for sales peaks.
  - Secures customer data with RBAC/Secrets.

#### Enhanced CRM Project Implementation
- **Scenario**: Upgrade `CRMTerraformJenkins` for production.
- **Context**: Multi-team CRM on EKS with advanced K8s.
- **Practical Workflow**:
  1. **Update Terraform**:
     - Add `k8s.tf` to `terraform/` (above code).
     - Update `main.tf` Deployments/Services:
       ```hcl
       resource "kubernetes_deployment_v1" "crm_api" {
         metadata {
           name      = "crm-api"
           namespace = "dev-us"
         }
         spec {
           replicas = 2
           selector {
             match_labels = { app = "crm-api" }
           }
           template {
             metadata {
               labels = { app = "crm-api" }
             }
             spec {
               container {
                 image = "866934333672.dkr.ecr.us-east-1.amazonaws.com/dev-us-crm-api:latest"
                 name  = "crm-api"
                 port {
                   container_port = 3000
                 }
                 env {
                   name  = "API_RATE_LIMIT"
                   value_from {
                     config_map_key_ref {
                       name = "crm-config"
                       key  = "api_rate_limit"
                     }
                   }
                 }
                 env {
                   name  = "API_KEY"
                   value_from {
                     secret_key_ref {
                       name = "crm-secret"
                       key  = "api_key"
                     }
                   }
                 }
               }
             }
           }
         }
       }

       resource "kubernetes_service_v1" "crm_api_service" {
         metadata {
           name      = "crm-api-service"
           namespace = "dev-us"
         }
         spec {
           selector = { app = "crm-api" }
           port {
             port        = 80
             target_port = "3000"
           }
           type = "ClusterIP"
         }
       }
       ```
       - Repeat for `crm-ui`, `crm-analytics`.
  2. **Deploy**:
     ```bash
     cd terraform
     terraform init
     terraform apply -var="key_name=my-key"
     ```
  3. **Jenkins Pipeline**:
     - Update `Jenkinsfile`:
       ```groovy
       stage('Deploy to EKS') {
         steps {
           dir('terraform') {
             sh 'terraform init -backend-config="bucket=crm-tf-state-2025"'
             sh 'terraform workspace select ${BRANCH_NAME} || terraform workspace new ${BRANCH_NAME}'
             sh 'terraform apply -auto-approve'
           }
           sh 'kubectl apply -f k8s/ -n ${BRANCH_NAME}'
         }
       }
       ```
  - **Outcome**: CRM on EKS with Ingress, HPA, secure configs, and RBAC.

---

### Lesson Plan Details

#### Theory Session (2 hr)
- **Topics**:
  1. **Terraform + K8s Synergy (30 min)**:
     - Provisioning EKS and K8s resources.
     - State management with S3.
  2. **Ingress & HPA (40 min)**:
     - Traffic routing and auto-scaling mechanics.
     - Metrics Server integration.
  3. **ConfigMaps & Secrets (30 min)**:
     - Config vs. sensitive data management.
     - Terraform vs. YAML approaches.
  4. **RBAC & Governance (20 min)**:
     - Multi-team access control.
     - Fortune 100 compliance needs.
- **Delivery**: Slides, demo of `terraform apply` + `kubectl get ingress`.

#### Practical Session (2 hr)
- **Activity**: Deploy enhanced CRM on EKS.
- **Steps**:
  1. **Setup (20 min)**:
     - Update `CRMTerraformJenkins/terraform/` with `k8s.tf`.
     - Install Helm and NGINX Ingress (above).
  2. **Terraform Deployment (50 min)**:
     - Apply updated Terraform config.
     - Verify: `kubectl get pods -n dev-us`.
  3. **Test Scaling & Security (50 min)**:
     - Simulate load: `kubectl run -i --tty load-generator --image=busybox --restart=Never -- /bin/sh -c "while true; do wget -q -O- http://crm-api-service.dev-us.svc.cluster.local; done"`
     - Check HPA: `kubectl get hpa -n dev-us`.
     - Test RBAC: `kubectl auth can-i get pods -n dev-us --as=dev-user`.
- **Outcome**: CRM scales, routes traffic, and secures access.

---

### Assessment
- **Quiz**: 
  - How does Terraform enhance K8s deployments?
  - What’s the role of HPA in CRM scaling?
- **Hands-On**: 
  - Show Ingress routing: `curl http://crm.local/api`.
  - Verify RBAC restrictions.

---

### Fortune 100 Alignment
- **Salesforce**: Uses Terraform for EKS, K8s for CRM microservices, mirroring this setup.
- **Walmart**: Scales e-commerce with HPA, secures with RBAC, akin to our CRM.
- **Your Project**: Prepares for multi-region, team-driven CRM ops.

