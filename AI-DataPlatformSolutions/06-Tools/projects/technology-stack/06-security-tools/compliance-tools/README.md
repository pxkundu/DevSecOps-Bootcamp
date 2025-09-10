# Compliance Tools - Security Compliance Management

## 📋 Overview
Compliance tools help organizations meet regulatory requirements and security standards. This section covers tools for automated compliance checking, policy enforcement, and audit management.

## 📁 Directory Structure

```
compliance-tools/
├── README.md
├── policy-as-code/
│   ├── opa-policies/
│   ├── rego-scripts/
│   └── compliance-frameworks/
├── audit-tools/
│   ├── compliance-scanners/
│   └── audit-reports/
└── frameworks/
    ├── nist/
    ├── cis/
    └── pci-dss/
```

## 🛠️ Policy as Code Tools

### 1. Open Policy Agent (OPA)
```rego
# policy-as-code/opa-policies/kubernetes-security.rego
package kubernetes.admission

deny[msg] {
    input.request.kind.kind == "Pod"
    not input.request.object.spec.securityContext.runAsNonRoot
    msg := "Containers must run as non-root"
}

deny[msg] {
    input.request.kind.kind == "Pod"
    input.request.object.spec.containers[_].securityContext.privileged == true
    msg := "Privileged containers are not allowed"
}

deny[msg] {
    input.request.kind.kind == "Pod"
    not input.request.object.spec.containers[_].securityContext.readOnlyRootFilesystem
    msg := "Containers must have read-only root filesystem"
}
```

### 2. OPA Gatekeeper
```yaml
# policy-as-code/opa-policies/constraint-template.yaml
apiVersion: templates.gatekeeper.sh/v1beta1
kind: ConstraintTemplate
metadata:
  name: k8srequiredlabels
spec:
  crd:
    spec:
      names:
        kind: K8sRequiredLabels
      validation:
        properties:
          labels:
            type: array
            items:
              type: string
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package k8srequiredlabels
        
        violation[{"msg": msg}] {
          required := input.parameters.labels
          provided := input.review.object.metadata.labels
          missing := required[_]
          not provided[missing]
          msg := sprintf("Missing required label: %v", [missing])
        }
```

## 🔍 Compliance Scanners

### 1. CIS Kubernetes Benchmark
```bash
#!/bin/bash
# audit-tools/compliance-scanners/cis-k8s-scan.sh

# Install kube-bench
curl -L https://github.com/aquasecurity/kube-bench/releases/download/v0.6.15/kube-bench_0.6.15_linux_amd64.tar.gz | tar -xz

# Run CIS Kubernetes benchmark
./kube-bench run --targets master,node,etcd,policies

# Generate compliance report
./kube-bench run --targets master,node,etcd,policies --json > cis-report.json
```

### 2. NIST Compliance Scanner
```yaml
# audit-tools/compliance-scanners/nist-scanner.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: nist-scanner-config
data:
  scanner.yaml: |
    nist:
      framework: "NIST-CSF"
      controls:
        - id: "PR.AC-1"
          description: "Identities and credentials are issued, managed, verified, revoked, and audited"
          checks:
            - name: "rbac-enabled"
              type: "kubernetes"
              resource: "rbac"
            - name: "service-accounts"
              type: "kubernetes"
              resource: "serviceaccounts"
        - id: "PR.DS-1"
          description: "Data-at-rest is protected"
          checks:
            - name: "encryption-at-rest"
              type: "kubernetes"
              resource: "secrets"
```

## 📊 Compliance Frameworks

### 1. NIST Cybersecurity Framework
```yaml
# frameworks/nist/nist-csf.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: nist-csf-config
data:
  framework.yaml: |
    nist_csf:
      identify:
        - asset_management
        - business_environment
        - governance
        - risk_assessment
        - risk_management_strategy
      protect:
        - identity_management
        - protective_technology
        - awareness_training
        - data_security
        - maintenance
      detect:
        - anomalies_events
        - continuous_monitoring
        - detection_processes
      respond:
        - response_planning
        - communications
        - analysis
        - mitigation
        - improvements
      recover:
        - recovery_planning
        - improvements
        - communications
```

### 2. CIS Controls
```yaml
# frameworks/cis/cis-controls.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: cis-controls-config
data:
  controls.yaml: |
    cis_controls:
      basic:
        - control_1: "Inventory and Control of Enterprise Assets"
        - control_2: "Inventory and Control of Software Assets"
        - control_3: "Data Protection"
        - control_4: "Secure Configuration of Enterprise Assets"
        - control_5: "Account Management"
      foundational:
        - control_6: "Access Control Management"
        - control_7: "Continuous Vulnerability Management"
        - control_8: "Audit Log Management"
        - control_9: "Email and Web Browser Protections"
        - control_10: "Malware Defenses"
```

## 🚀 Automation Scripts

### 1. Compliance Check Script
```bash
#!/bin/bash
# scripts/compliance-check.sh

set -e

echo "Running compliance checks..."

# Run OPA policies
echo "Checking OPA policies..."
kubectl get pods -o yaml | conftest test -

# Run CIS benchmark
echo "Running CIS Kubernetes benchmark..."
kube-bench run --targets master,node,etcd,policies

# Run NIST compliance scan
echo "Running NIST compliance scan..."
nist-scanner run --framework nist-csf

# Generate compliance report
echo "Generating compliance report..."
compliance-report generate --output compliance-report.html

echo "Compliance checks completed"
```

### 2. Policy Enforcement Script
```bash
#!/bin/bash
# scripts/enforce-policies.sh

echo "Enforcing compliance policies..."

# Install OPA Gatekeeper
kubectl apply -f https://raw.githubusercontent.com/open-policy-agent/gatekeeper/release-3.14/deploy/gatekeeper.yaml

# Apply constraint templates
kubectl apply -f policy-as-code/opa-policies/constraint-templates/

# Apply constraints
kubectl apply -f policy-as-code/opa-policies/constraints/

# Verify policy enforcement
kubectl get constraints

echo "Policy enforcement completed"
```

## 📋 Best Practices

### 1. Policy Development
- Write clear, testable policies
- Use version control for policies
- Implement policy testing
- Regular policy reviews

### 2. Compliance Management
- Automate compliance checking
- Regular compliance audits
- Document compliance status
- Implement remediation workflows

### 3. Framework Implementation
- Choose appropriate frameworks
- Map controls to requirements
- Implement continuous monitoring
- Regular framework updates

---

**Ready to master compliance tools?** Start with OPA policies and work your way up to comprehensive compliance automation!
