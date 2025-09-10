# Intermediate Hands-On Labs - DevSecOps Advanced Practices

## 🚀 Overview
This section provides intermediate-level hands-on labs for DevSecOps practitioners who want to advance their skills. These labs focus on advanced concepts, enterprise patterns, and real-world scenarios.

## 📁 Directory Structure

```
intermediate/
├── README.md
├── lab-01-multi-cloud-setup/
├── lab-02-advanced-cicd/
├── lab-03-container-security/
├── lab-04-infrastructure-automation/
├── lab-05-monitoring-observability/
├── lab-06-compliance-automation/
└── lab-07-disaster-recovery/
```

## 🎯 Learning Objectives

By the end of these intermediate labs, you will be able to:
- Implement multi-cloud DevSecOps strategies
- Build advanced CI/CD pipelines with security integration
- Implement comprehensive container security
- Automate infrastructure provisioning and management
- Set up enterprise-grade monitoring and observability
- Implement compliance automation and governance
- Design and implement disaster recovery strategies

## 🛠️ Lab Prerequisites

### Required Knowledge
- Basic DevSecOps concepts
- Experience with Docker and Kubernetes
- Understanding of CI/CD pipelines
- Basic cloud platform knowledge
- Security fundamentals

### Required Tools
- Docker and Kubernetes
- Terraform or CloudFormation
- CI/CD platform (Jenkins, GitLab CI, or GitHub Actions)
- Cloud accounts (AWS, Azure, or GCP)
- Monitoring tools (Prometheus, Grafana)
- Security scanning tools

## 🧪 Hands-On Labs

### Lab 1: Multi-Cloud Setup
**Duration**: 4-6 hours  
**Difficulty**: Intermediate  
**Prerequisites**: Basic cloud knowledge

#### Objectives
- Set up infrastructure across multiple cloud providers
- Implement cross-cloud networking
- Configure unified monitoring and logging
- Establish security policies across clouds

#### Tasks
1. **AWS Infrastructure Setup**
   ```bash
   # Create AWS VPC and EKS cluster
   terraform init
   terraform plan -var-file="aws/terraform.tfvars"
   terraform apply -var-file="aws/terraform.tfvars"
   ```

2. **Azure Infrastructure Setup**
   ```bash
   # Create Azure VNet and AKS cluster
   az login
   az group create --name devsecops-rg --location westus2
   az aks create --resource-group devsecops-rg --name devsecops-aks
   ```

3. **Cross-Cloud Networking**
   ```bash
   # Set up VPN connections between clouds
   aws ec2 create-vpn-connection --type ipsec.1 --customer-gateway-id cgw-12345678
   az network vpn-gateway create --resource-group devsecops-rg --name vpn-gateway
   ```

4. **Unified Monitoring**
   ```yaml
   # Deploy Prometheus across clouds
   helm install prometheus prometheus-community/kube-prometheus-stack \
     --namespace monitoring \
     --create-namespace \
     --values values/multi-cloud-prometheus.yaml
   ```

#### Deliverables
- [ ] Multi-cloud infrastructure deployed
- [ ] Cross-cloud networking configured
- [ ] Unified monitoring setup
- [ ] Security policies implemented

---

### Lab 2: Advanced CI/CD
**Duration**: 6-8 hours  
**Difficulty**: Intermediate  
**Prerequisites**: Basic CI/CD knowledge

#### Objectives
- Build advanced CI/CD pipelines with security integration
- Implement automated testing and quality gates
- Set up deployment strategies (blue-green, canary)
- Integrate security scanning and compliance checks

#### Tasks
1. **Pipeline Configuration**
   ```yaml
   # .gitlab-ci.yml - Advanced pipeline
   stages:
     - build
     - test
     - security
     - deploy-staging
     - deploy-production
   
   variables:
     DOCKER_IMAGE: $CI_REGISTRY_IMAGE
     DOCKER_TAG: $CI_COMMIT_SHA
   
   build:
     stage: build
     script:
       - docker build -t $DOCKER_IMAGE:$DOCKER_TAG .
       - docker push $DOCKER_IMAGE:$DOCKER_TAG
   
   security:
     stage: security
     script:
       - trivy image $DOCKER_IMAGE:$DOCKER_TAG
       - sonar-scanner -Dsonar.projectKey=myapp
   
   deploy-staging:
     stage: deploy-staging
     script:
       - kubectl apply -f k8s/staging/
       - kubectl rollout status deployment/myapp-staging
   
   deploy-production:
     stage: deploy-production
     script:
       - kubectl apply -f k8s/production/
       - kubectl rollout status deployment/myapp-production
     when: manual
   ```

2. **Quality Gates**
   ```bash
   # Implement quality gates
   # Code coverage check
   if [ $(coverage) -lt 80 ]; then
     echo "Code coverage below threshold"
     exit 1
   fi
   
   # Security scan check
   if [ $(vulnerabilities) -gt 0 ]; then
     echo "Security vulnerabilities found"
     exit 1
   fi
   ```

3. **Deployment Strategies**
   ```yaml
   # Blue-Green deployment
   apiVersion: argoproj.io/v1alpha1
   kind: Rollout
   metadata:
     name: myapp-rollout
   spec:
     replicas: 5
     strategy:
       blueGreen:
         activeService: myapp-active
         previewService: myapp-preview
         autoPromotionEnabled: false
   ```

#### Deliverables
- [ ] Advanced CI/CD pipeline implemented
- [ ] Quality gates configured
- [ ] Deployment strategies working
- [ ] Security integration complete

---

### Lab 3: Container Security
**Duration**: 5-7 hours  
**Difficulty**: Intermediate  
**Prerequisites**: Docker and Kubernetes knowledge

#### Objectives
- Implement comprehensive container security
- Set up runtime security monitoring
- Configure network policies and RBAC
- Implement secrets management

#### Tasks
1. **Container Image Security**
   ```dockerfile
   # Secure Dockerfile
   FROM node:18-alpine AS base
   
   # Create non-root user
   RUN addgroup -g 1001 -S nodejs
   RUN adduser -S nextjs -u 1001
   
   # Install security updates
   RUN apk update && apk upgrade
   
   # Copy application
   COPY --chown=nextjs:nodejs . .
   
   # Switch to non-root user
   USER nextjs
   
   # Expose port
   EXPOSE 3000
   
   # Health check
   HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
     CMD curl -f http://localhost:3000/health || exit 1
   ```

2. **Runtime Security**
   ```yaml
   # Falco configuration
   apiVersion: v1
   kind: ConfigMap
   metadata:
     name: falco-config
   data:
     falco.yaml: |
       rules_file:
         - /etc/falco/falco_rules.yaml
         - /etc/falco/falco_rules.local.yaml
       json_output: true
       json_include_output_property: true
   ```

3. **Network Policies**
   ```yaml
   # Network policy
   apiVersion: networking.k8s.io/v1
   kind: NetworkPolicy
   metadata:
     name: myapp-network-policy
   spec:
     podSelector:
       matchLabels:
         app: myapp
     policyTypes:
     - Ingress
     - Egress
     ingress:
     - from:
       - namespaceSelector:
           matchLabels:
             name: frontend
       ports:
       - protocol: TCP
         port: 3000
   ```

#### Deliverables
- [ ] Container security implemented
- [ ] Runtime monitoring configured
- [ ] Network policies working
- [ ] Secrets management setup

---

### Lab 4: Infrastructure Automation
**Duration**: 6-8 hours  
**Difficulty**: Intermediate  
**Prerequisites**: Terraform or CloudFormation knowledge

#### Objectives
- Automate infrastructure provisioning
- Implement infrastructure as code best practices
- Set up automated testing for infrastructure
- Configure drift detection and remediation

#### Tasks
1. **Terraform Modules**
   ```hcl
   # modules/vpc/main.tf
   resource "aws_vpc" "main" {
     cidr_block           = var.cidr_block
     enable_dns_hostnames = true
     enable_dns_support   = true
     
     tags = merge(var.tags, {
       Name = "${var.name}-vpc"
     })
   }
   
   resource "aws_internet_gateway" "main" {
     vpc_id = aws_vpc.main.id
     
     tags = merge(var.tags, {
       Name = "${var.name}-igw"
     })
   }
   ```

2. **Infrastructure Testing**
   ```bash
   # Terratest for infrastructure testing
   go test -v -timeout 30m -run TestVPC
   ```

3. **Drift Detection**
   ```yaml
   # GitHub Actions workflow for drift detection
   name: Infrastructure Drift Detection
   on:
     schedule:
       - cron: '0 2 * * *'  # Daily at 2 AM
   
   jobs:
     drift-detection:
       runs-on: ubuntu-latest
       steps:
       - uses: actions/checkout@v3
       - name: Terraform Plan
         run: terraform plan -detailed-exitcode
         continue-on-error: true
   ```

#### Deliverables
- [ ] Infrastructure automation implemented
- [ ] Modules created and tested
- [ ] Drift detection configured
- [ ] Best practices followed

---

### Lab 5: Monitoring & Observability
**Duration**: 5-7 hours  
**Difficulty**: Intermediate  
**Prerequisites**: Basic monitoring knowledge

#### Objectives
- Set up comprehensive monitoring and observability
- Implement distributed tracing
- Configure alerting and incident response
- Set up log aggregation and analysis

#### Tasks
1. **Prometheus & Grafana Setup**
   ```yaml
   # Prometheus configuration
   global:
     scrape_interval: 15s
     evaluation_interval: 15s
   
   rule_files:
     - "rules/*.yml"
   
   scrape_configs:
     - job_name: 'kubernetes-pods'
       kubernetes_sd_configs:
         - role: pod
   ```

2. **Distributed Tracing**
   ```yaml
   # Jaeger configuration
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: jaeger
   spec:
     replicas: 1
     selector:
       matchLabels:
         app: jaeger
     template:
       metadata:
         labels:
           app: jaeger
       spec:
         containers:
         - name: jaeger
           image: jaegertracing/all-in-one:latest
           ports:
           - containerPort: 16686
   ```

3. **ELK Stack Setup**
   ```yaml
   # Elasticsearch configuration
   apiVersion: apps/v1
   kind: StatefulSet
   metadata:
     name: elasticsearch
   spec:
     serviceName: elasticsearch
     replicas: 3
     selector:
       matchLabels:
         app: elasticsearch
   ```

#### Deliverables
- [ ] Monitoring stack deployed
- [ ] Distributed tracing configured
- [ ] Log aggregation working
- [ ] Alerting setup complete

---

### Lab 6: Compliance Automation
**Duration**: 4-6 hours  
**Difficulty**: Intermediate  
**Prerequisites**: Security and compliance knowledge

#### Objectives
- Implement automated compliance checking
- Set up policy as code
- Configure audit logging and reporting
- Implement automated remediation

#### Tasks
1. **OPA Policies**
   ```rego
   # OPA policy for compliance
   package kubernetes.admission
   
   deny[msg] {
       input.request.kind.kind == "Pod"
       not input.request.object.spec.securityContext.runAsNonRoot
       msg := "Containers must run as non-root"
   }
   ```

2. **Compliance Scanning**
   ```bash
   # CIS Kubernetes benchmark
   kubectl-bench run --targets master,node,etcd,policies
   ```

3. **Audit Logging**
   ```yaml
   # Audit policy
   apiVersion: audit.k8s.io/v1
   kind: Policy
   rules:
   - level: Metadata
     resources:
     - group: ""
       resources: ["secrets"]
   ```

#### Deliverables
- [ ] Compliance automation implemented
- [ ] Policy as code configured
- [ ] Audit logging working
- [ ] Automated remediation setup

---

### Lab 7: Disaster Recovery
**Duration**: 6-8 hours  
**Difficulty**: Intermediate  
**Prerequisites**: Infrastructure and backup knowledge

#### Objectives
- Design and implement disaster recovery strategies
- Set up automated backups
- Configure cross-region replication
- Implement failover procedures

#### Tasks
1. **Backup Strategy**
   ```bash
   # Velero backup configuration
   velero install \
     --provider aws \
     --plugins velero/velero-plugin-for-aws:v1.0.0 \
     --bucket velero-backups \
     --secret-file ./credentials-velero
   ```

2. **Cross-Region Replication**
   ```yaml
   # Cross-region replication
   apiVersion: v1
   kind: ConfigMap
   metadata:
     name: velero-config
   data:
     backup-location-config: |
       region: us-west-2
       s3ForcePathStyle: true
       s3Url: https://s3.us-west-2.amazonaws.com
   ```

3. **Failover Testing**
   ```bash
   # Disaster recovery testing
   kubectl create namespace dr-test
   velero backup create dr-test-backup --include-namespaces dr-test
   ```

#### Deliverables
- [ ] Disaster recovery strategy implemented
- [ ] Automated backups configured
- [ ] Cross-region replication working
- [ ] Failover procedures tested

## 📚 Additional Resources

### Study Materials
- [Advanced DevSecOps Patterns](study-materials/advanced-patterns.md)
- [Enterprise Security Practices](study-materials/enterprise-security.md)
- [Multi-Cloud Strategies](study-materials/multi-cloud-strategies.md)
- [Compliance Frameworks](study-materials/compliance-frameworks.md)

### Tools and Technologies
- [Terraform Advanced](tools/terraform-advanced.md)
- [Kubernetes Security](tools/kubernetes-security.md)
- [Monitoring Stack](tools/monitoring-stack.md)
- [Security Tools](tools/security-tools.md)

---

**Ready to advance your DevSecOps skills?** Start with Lab 1 and work your way through all the intermediate-level exercises!
