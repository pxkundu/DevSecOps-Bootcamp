# Policy as Code - Automated Policy Management

## 📜 Overview
Policy as Code enables organizations to define, manage, and enforce policies using code, providing consistency, version control, and automation across infrastructure and applications.

## 📁 Directory Structure

```
policy-as-code/
├── README.md
├── opa/
│   ├── policies/
│   ├── rego/
│   └── tests/
├── kyverno/
│   ├── policies/
│   └── cluster-policies/
├── sentinel/
│   ├── policies/
│   └── imports/
└── scripts/
    ├── deploy-policies.sh
    └── test-policies.sh
```

## 🛠️ Open Policy Agent (OPA)

### 1. OPA Policies
```rego
# opa/policies/kubernetes-security.rego
package kubernetes.admission

import rego.v1

# Deny privileged containers
deny[msg] {
    input.request.kind.kind == "Pod"
    container := input.request.object.spec.containers[_]
    container.securityContext.privileged == true
    msg := "Privileged containers are not allowed"
}

# Deny containers running as root
deny[msg] {
    input.request.kind.kind == "Pod"
    container := input.request.object.spec.containers[_]
    not container.securityContext.runAsNonRoot
    msg := "Containers must run as non-root"
}

# Deny containers without resource limits
deny[msg] {
    input.request.kind.kind == "Pod"
    container := input.request.object.spec.containers[_]
    not container.resources.limits
    msg := "Containers must have resource limits"
}

# Deny containers without read-only root filesystem
deny[msg] {
    input.request.kind.kind == "Pod"
    container := input.request.object.spec.containers[_]
    not container.securityContext.readOnlyRootFilesystem
    msg := "Containers must have read-only root filesystem"
}
```

### 2. OPA Tests
```rego
# opa/tests/kubernetes-security_test.rego
package kubernetes.admission

import rego.v1

test_deny_privileged_container {
    input := {
        "request": {
            "kind": {"kind": "Pod"},
            "object": {
                "spec": {
                    "containers": [{
                        "securityContext": {"privileged": true}
                    }]
                }
            }
        }
    }
    
    count(deny) == 1
    deny[0] == "Privileged containers are not allowed"
}

test_allow_non_privileged_container {
    input := {
        "request": {
            "kind": {"kind": "Pod"},
            "object": {
                "spec": {
                    "containers": [{
                        "securityContext": {"privileged": false}
                    }]
                }
            }
        }
    }
    
    count(deny) == 0
}
```

### 3. OPA Configuration
```yaml
# opa/config/opa-config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: opa-config
data:
  opa.conf: |
    services:
      kubernetes:
        url: https://kubernetes.default.svc.cluster.local
    bundles:
      devsecops:
        service: kubernetes
        resource: /apis/policy/v1beta1/policies
    plugins:
      envoy_ext_authz_grpc:
        addr: :9191
        query: data.kubernetes.admission.deny
```

## 🔧 Kyverno Policies

### 1. Cluster Policies
```yaml
# kyverno/cluster-policies/security-policy.yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: security-policy
spec:
  validationFailureAction: enforce
  background: true
  rules:
  - name: require-non-root
    match:
      any:
      - resources:
          kinds:
          - Pod
    validate:
      message: "Containers must run as non-root"
      pattern:
        spec:
          containers:
          - name: "*"
            securityContext:
              runAsNonRoot: true
  - name: require-readonly-filesystem
    match:
      any:
      - resources:
          kinds:
          - Pod
    validate:
      message: "Containers must have read-only root filesystem"
      pattern:
        spec:
          containers:
          - name: "*"
            securityContext:
              readOnlyRootFilesystem: true
  - name: require-resource-limits
    match:
      any:
      - resources:
          kinds:
          - Pod
    validate:
      message: "Containers must have resource limits"
      pattern:
        spec:
          containers:
          - name: "*"
            resources:
              limits:
                memory: "?*"
                cpu: "?*"
```

### 2. Namespace Policies
```yaml
# kyverno/policies/namespace-policy.yaml
apiVersion: kyverno.io/v1
kind: Policy
metadata:
  name: namespace-policy
  namespace: default
spec:
  validationFailureAction: enforce
  background: true
  rules:
  - name: require-labels
    match:
      any:
      - resources:
          kinds:
          - Pod
    validate:
      message: "Pods must have required labels"
      pattern:
        metadata:
          labels:
            app: "?*"
            version: "?*"
            environment: "?*"
```

## 🏗️ Terraform Sentinel

### 1. Sentinel Policies
```javascript
// sentinel/policies/aws-security.sentinel
import "tfplan"

# Check for S3 bucket encryption
s3_buckets = filter tfplan.resource_changes as _, rc {
    rc.type is "aws_s3_bucket"
    rc.change.actions is ["create", "update"]
}

violations = filter s3_buckets as _, bucket {
    not bucket.change.after.server_side_encryption_configuration
}

main = rule {
    length(violations) is 0
}

# Check for RDS encryption
rds_instances = filter tfplan.resource_changes as _, rc {
    rc.type is "aws_db_instance"
    rc.change.actions is ["create", "update"]
}

rds_violations = filter rds_instances as _, instance {
    not instance.change.after.storage_encrypted
}

main = rule {
    length(rds_violations) is 0
}
```

### 2. Sentinel Configuration
```hcl
# sentinel/config/sentinel.hcl
policy "aws-security" {
  source = "./policies/aws-security.sentinel"
  enforcement_level = "hard-mandatory"
}

policy "azure-security" {
  source = "./policies/azure-security.sentinel"
  enforcement_level = "soft-mandatory"
}

policy "kubernetes-security" {
  source = "./policies/kubernetes-security.sentinel"
  enforcement_level = "hard-mandatory"
}
```

## 🚀 Deployment Scripts

### 1. Deploy Policies
```bash
#!/bin/bash
# scripts/deploy-policies.sh

set -e

echo "Deploying policy as code..."

# Deploy OPA
echo "Deploying OPA..."
kubectl apply -f opa/config/
kubectl apply -f opa/policies/

# Deploy Kyverno
echo "Deploying Kyverno..."
kubectl apply -f kyverno/cluster-policies/
kubectl apply -f kyverno/policies/

# Deploy Sentinel
echo "Deploying Sentinel policies..."
terraform plan -var-file="sentinel/config/sentinel.hcl"

echo "Policy deployment completed"
```

### 2. Test Policies
```bash
#!/bin/bash
# scripts/test-policies.sh

echo "Testing policy as code..."

# Test OPA policies
echo "Testing OPA policies..."
opa test opa/policies/ -v

# Test Kyverno policies
echo "Testing Kyverno policies..."
kyverno test kyverno/policies/

# Test Sentinel policies
echo "Testing Sentinel policies..."
sentinel test sentinel/policies/

echo "Policy testing completed"
```

## 📊 Policy Monitoring

### 1. Policy Violations Dashboard
```yaml
# monitoring/policy-violations.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: policy-violations-dashboard
data:
  dashboard.json: |
    {
      "dashboard": {
        "title": "Policy Violations Dashboard",
        "panels": [
          {
            "title": "Policy Violations Over Time",
            "type": "graph",
            "targets": [
              {
                "expr": "rate(policy_violations_total[5m])",
                "legendFormat": "Violations/sec"
              }
            ]
          },
          {
            "title": "Violations by Policy",
            "type": "pie",
            "targets": [
              {
                "expr": "sum by (policy) (policy_violations_total)",
                "legendFormat": "{{policy}}"
              }
            ]
          }
        ]
      }
    }
```

### 2. Policy Compliance Report
```bash
#!/bin/bash
# scripts/generate-compliance-report.sh

echo "Generating policy compliance report..."

# Generate OPA compliance report
echo "Generating OPA compliance report..."
opa eval --data opa/policies/ --format json 'data.kubernetes.admission.deny' > opa-compliance.json

# Generate Kyverno compliance report
echo "Generating Kyverno compliance report..."
kyverno test kyverno/policies/ --format json > kyverno-compliance.json

# Generate Sentinel compliance report
echo "Generating Sentinel compliance report..."
sentinel test sentinel/policies/ --format json > sentinel-compliance.json

# Generate combined report
echo "Generating combined compliance report..."
jq -s '.[0] * .[1] * .[2]' opa-compliance.json kyverno-compliance.json sentinel-compliance.json > combined-compliance.json

echo "Compliance report generated"
```

## 📋 Best Practices

### 1. Policy Development
- Write clear, testable policies
- Use version control for policies
- Implement policy testing
- Regular policy reviews

### 2. Policy Management
- Organize policies by domain
- Use consistent naming conventions
- Implement policy documentation
- Regular policy updates

### 3. Policy Enforcement
- Start with warning mode
- Gradually move to enforcement
- Monitor policy violations
- Implement remediation workflows

---

**Ready to master policy as code?** Start with OPA policies and work your way up to comprehensive policy management!
