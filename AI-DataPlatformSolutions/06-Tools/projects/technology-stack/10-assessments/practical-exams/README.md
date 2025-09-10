# Practical Exams - Hands-On Assessment

## 🎯 Overview
This section provides practical exams to assess your DevSecOps skills through hands-on scenarios. These exams test real-world problem-solving abilities and practical implementation skills.

## 📁 Directory Structure

```
practical-exams/
├── README.md
├── exam-01-infrastructure-setup/
├── exam-02-cicd-pipeline/
├── exam-03-security-implementation/
├── exam-04-monitoring-setup/
├── exam-05-disaster-recovery/
└── scoring-rubrics/
```

## 🧪 Practical Exam Scenarios

### Exam 1: Infrastructure Setup
**Duration**: 3 hours  
**Difficulty**: Intermediate  
**Scenario**: Set up a complete DevSecOps infrastructure

#### Requirements
- Create a VPC with public and private subnets
- Deploy an EKS cluster with worker nodes
- Set up a RDS database with encryption
- Configure security groups and NACLs
- Implement monitoring and logging

#### Deliverables
- [ ] Infrastructure code (Terraform/CloudFormation)
- [ ] Working Kubernetes cluster
- [ ] Database with proper security
- [ ] Monitoring dashboard
- [ ] Documentation

#### Scoring Criteria
- **Infrastructure (40%)**: Proper resource creation and configuration
- **Security (30%)**: Security groups, encryption, access controls
- **Monitoring (20%)**: Logging, metrics, alerting setup
- **Documentation (10%)**: Clear documentation and comments

---

### Exam 2: CI/CD Pipeline
**Duration**: 4 hours  
**Difficulty**: Intermediate  
**Scenario**: Build a complete CI/CD pipeline with security integration

#### Requirements
- Create a multi-stage pipeline (build, test, security, deploy)
- Integrate SAST and DAST scanning
- Implement automated testing
- Set up deployment to multiple environments
- Configure rollback procedures

#### Deliverables
- [ ] Pipeline configuration files
- [ ] Security scanning integration
- [ ] Automated testing setup
- [ ] Deployment scripts
- [ ] Pipeline documentation

#### Scoring Criteria
- **Pipeline Design (35%)**: Proper stage configuration and flow
- **Security Integration (30%)**: Security scanning and compliance
- **Testing (20%)**: Unit, integration, and security tests
- **Deployment (15%)**: Multi-environment deployment and rollback

---

### Exam 3: Security Implementation
**Duration**: 3 hours  
**Difficulty**: Advanced  
**Scenario**: Implement comprehensive security measures

#### Requirements
- Set up secrets management (Vault/AWS Secrets Manager)
- Configure RBAC and network policies
- Implement container security scanning
- Set up runtime security monitoring
- Configure compliance scanning

#### Deliverables
- [ ] Secrets management setup
- [ ] Security policies and RBAC
- [ ] Container security configuration
- [ ] Runtime monitoring setup
- [ ] Compliance reports

#### Scoring Criteria
- **Secrets Management (25%)**: Proper secret storage and access
- **Access Control (25%)**: RBAC and network policies
- **Container Security (25%)**: Image scanning and runtime protection
- **Compliance (25%)**: Security scanning and compliance reporting

---

### Exam 4: Monitoring Setup
**Duration**: 3 hours  
**Difficulty**: Intermediate  
**Scenario**: Set up comprehensive monitoring and observability

#### Requirements
- Deploy Prometheus and Grafana
- Configure application metrics collection
- Set up distributed tracing (Jaeger)
- Implement log aggregation (ELK stack)
- Configure alerting and incident response

#### Deliverables
- [ ] Monitoring stack deployment
- [ ] Metrics collection configuration
- [ ] Tracing setup
- [ ] Log aggregation system
- [ ] Alerting rules and dashboards

#### Scoring Criteria
- **Metrics Collection (30%)**: Prometheus configuration and targets
- **Visualization (25%)**: Grafana dashboards and charts
- **Tracing (20%)**: Distributed tracing setup
- **Logging (15%)**: Log aggregation and analysis
- **Alerting (10%)**: Alert rules and notification setup

---

### Exam 5: Disaster Recovery
**Duration**: 4 hours  
**Difficulty**: Advanced  
**Scenario**: Implement disaster recovery and business continuity

#### Requirements
- Set up automated backups
- Configure cross-region replication
- Implement failover procedures
- Test disaster recovery scenarios
- Document recovery procedures

#### Deliverables
- [ ] Backup automation
- [ ] Cross-region setup
- [ ] Failover procedures
- [ ] Recovery testing results
- [ ] DR documentation

#### Scoring Criteria
- **Backup Strategy (30%)**: Automated backup configuration
- **Replication (25%)**: Cross-region data replication
- **Failover (25%)**: Automated failover procedures
- **Testing (20%)**: DR testing and validation

## 📊 Scoring Rubrics

### Infrastructure Setup Rubric
| Criteria | Excellent (4) | Good (3) | Satisfactory (2) | Needs Improvement (1) |
|----------|---------------|----------|------------------|----------------------|
| Resource Creation | All resources created correctly | Most resources correct | Some issues | Multiple errors |
| Security Configuration | Comprehensive security | Good security measures | Basic security | Security gaps |
| Monitoring Setup | Full monitoring stack | Good monitoring | Basic monitoring | Limited monitoring |
| Documentation | Clear and complete | Good documentation | Basic documentation | Poor documentation |

### CI/CD Pipeline Rubric
| Criteria | Excellent (4) | Good (3) | Satisfactory (2) | Needs Improvement (1) |
|----------|---------------|----------|------------------|----------------------|
| Pipeline Design | Well-structured pipeline | Good structure | Basic structure | Poor structure |
| Security Integration | Comprehensive security | Good security | Basic security | Limited security |
| Testing | Complete test suite | Good testing | Basic testing | Limited testing |
| Deployment | Multi-environment | Good deployment | Basic deployment | Limited deployment |

## 🎯 Exam Preparation

### Study Materials
- [Infrastructure as Code Best Practices](study-materials/iac-best-practices.md)
- [CI/CD Pipeline Patterns](study-materials/cicd-patterns.md)
- [Security Implementation Guide](study-materials/security-guide.md)
- [Monitoring and Observability](study-materials/monitoring-guide.md)

### Practice Scenarios
- [Infrastructure Setup Practice](practice/infrastructure-practice.md)
- [Pipeline Development Practice](practice/pipeline-practice.md)
- [Security Implementation Practice](practice/security-practice.md)
- [Monitoring Setup Practice](practice/monitoring-practice.md)

### Tools and Resources
- [Required Tools List](tools/required-tools.md)
- [Reference Documentation](tools/reference-docs.md)
- [Sample Solutions](tools/sample-solutions.md)
- [Troubleshooting Guide](tools/troubleshooting.md)

## 📋 Exam Guidelines

### Before the Exam
- Ensure all required tools are installed
- Set up your development environment
- Review the exam requirements
- Prepare your workspace

### During the Exam
- Read all requirements carefully
- Plan your approach before starting
- Document your work as you go
- Test your solutions thoroughly
- Ask questions if anything is unclear

### After the Exam
- Review your deliverables
- Ensure all requirements are met
- Check your documentation
- Submit your work on time

## 🏆 Certification Path

### Exam Progression
1. **Infrastructure Setup** → Foundation level
2. **CI/CD Pipeline** → Intermediate level
3. **Security Implementation** → Advanced level
4. **Monitoring Setup** → Intermediate level
5. **Disaster Recovery** → Advanced level

### Certification Requirements
- Pass all 5 practical exams
- Achieve minimum 70% score on each exam
- Complete all deliverables
- Submit comprehensive documentation

---

**Ready to test your DevSecOps skills?** Start with Exam 1 and work your way through all the practical assessments!
