# Policy Enforcement - Automated Security Policies

## 🛡️ Overview
Policy enforcement tools automatically apply and enforce security policies across infrastructure and applications. This section covers tools for implementing policy as code and automated enforcement.

## 📁 Directory Structure

```
policy-enforcement/
├── README.md
├── opa-gatekeeper/
│   ├── constraint-templates/
│   ├── constraints/
│   └── policies/
├── kyverno/
│   ├── policies/
│   └── cluster-policies/
├── falco/
│   ├── rules/
│   └── configurations/
└── scripts/
    ├── deploy-policies.sh
    └── test-policies.sh
```

## 🛠️ OPA Gatekeeper Implementation

### 1. Constraint Templates
```yaml
# opa-gatekeeper/constraint-templates/required-labels.yaml
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

### 2. Constraints
```yaml
# opa-gatekeeper/constraints/required-labels-constraint.yaml
apiVersion: config.gatekeeper.sh/v1beta1
kind: K8sRequiredLabels
metadata:
  name: required-labels
spec:
  match:
    kinds:
      - apiGroups: ["apps"]
        kinds: ["Deployment"]
  parameters:
    labels: ["app", "version", "environment"]
```

### 3. Security Policies
```yaml
# opa-gatekeeper/policies/security-policies.yaml
apiVersion: templates.gatekeeper.sh/v1beta1
kind: ConstraintTemplate
metadata:
  name: k8ssecuritypolicy
spec:
  crd:
    spec:
      names:
        kind: K8sSecurityPolicy
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package k8ssecuritypolicy
        
        violation[{"msg": msg}] {
          input.review.object.kind == "Pod"
          container := input.review.object.spec.containers[_]
          not container.securityContext.runAsNonRoot
          msg := "Containers must run as non-root"
        }
        
        violation[{"msg": msg}] {
          input.review.object.kind == "Pod"
          container := input.review.object.spec.containers[_]
          container.securityContext.privileged == true
          msg := "Privileged containers are not allowed"
        }
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
```

### 2. Network Policies
```yaml
# kyverno/policies/network-policy.yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: network-policy
spec:
  validationFailureAction: enforce
  background: true
  rules:
  - name: require-network-policy
    match:
      any:
      - resources:
          kinds:
          - Namespace
    validate:
      message: "Namespaces must have NetworkPolicy"
      pattern:
        metadata:
          annotations:
            "net.beta.kubernetes.io/network-policy": "true"
```

## 🔍 Falco Runtime Security

### 1. Falco Rules
```yaml
# falco/rules/security-rules.yaml
- rule: Terminal shell in container
  desc: Notice shell activity in container
  condition: >
    spawned_process and container and
    shell_procs and proc.tty != 0
  output: >
    Shell spawned in container (user=%user.name user_loginuid=%user.loginuid %container.info
    shell=%proc.name parent=%proc.pname cmdline=%proc.cmdline terminal=%proc.tty container_id=%container.id image=%container.image.repository)
  priority: WARNING
  tags: [container, shell, mitre_execution]

- rule: Write to root directory
  desc: Detect writes to root directory
  condition: >
    open_write and
    fd.name startswith / and
    fd.name != /tmp and
    fd.name != /var/tmp and
    fd.name != /dev and
    fd.name != /proc and
    fd.name != /sys
  output: >
    Write to root directory (user=%user.name command=%proc.cmdline file=%fd.name)
  priority: WARNING
  tags: [filesystem, mitre_persistence]
```

### 2. Falco Configuration
```yaml
# falco/configurations/falco-config.yaml
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
    http_output:
      enabled: true
      url: "http://falco-webhook:8080/webhook"
    grpc:
      enabled: true
      bind_address: "0.0.0.0:5060"
```

## 🚀 Deployment Scripts

### 1. Deploy Policies Script
```bash
#!/bin/bash
# scripts/deploy-policies.sh

set -e

echo "Deploying policy enforcement tools..."

# Install OPA Gatekeeper
echo "Installing OPA Gatekeeper..."
kubectl apply -f https://raw.githubusercontent.com/open-policy-agent/gatekeeper/release-3.14/deploy/gatekeeper.yaml

# Wait for Gatekeeper to be ready
kubectl wait --for=condition=ready pod -l control-plane=controller-manager -n gatekeeper-system --timeout=300s

# Install Kyverno
echo "Installing Kyverno..."
kubectl create -f https://github.com/kyverno/kyverno/releases/download/v1.10.0/install.yaml

# Wait for Kyverno to be ready
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=kyverno -n kyverno --timeout=300s

# Install Falco
echo "Installing Falco..."
helm repo add falcosecurity https://falcosecurity.github.io/charts
helm install falco falcosecurity/falco --namespace falco --create-namespace

# Apply constraint templates
echo "Applying OPA Gatekeeper constraint templates..."
kubectl apply -f opa-gatekeeper/constraint-templates/

# Apply constraints
echo "Applying OPA Gatekeeper constraints..."
kubectl apply -f opa-gatekeeper/constraints/

# Apply Kyverno policies
echo "Applying Kyverno policies..."
kubectl apply -f kyverno/cluster-policies/

# Apply Falco rules
echo "Applying Falco rules..."
kubectl apply -f falco/rules/

echo "Policy enforcement deployment completed"
```

### 2. Test Policies Script
```bash
#!/bin/bash
# scripts/test-policies.sh

echo "Testing policy enforcement..."

# Test OPA Gatekeeper
echo "Testing OPA Gatekeeper constraints..."
kubectl get constraints

# Test Kyverno policies
echo "Testing Kyverno policies..."
kubectl get clusterpolicies

# Test Falco
echo "Testing Falco..."
kubectl get pods -n falco

# Test policy violations
echo "Testing policy violations..."
kubectl apply -f test-pods/privileged-pod.yaml || echo "Expected: Privileged pod rejected"

echo "Policy testing completed"
```

## 📋 Best Practices

### 1. Policy Development
- Write clear, testable policies
- Use version control for policies
- Implement policy testing
- Regular policy reviews

### 2. Enforcement Strategy
- Start with warning mode
- Gradually move to enforcement
- Monitor policy violations
- Implement remediation workflows

### 3. Runtime Security
- Monitor container behavior
- Detect anomalous activities
- Implement alerting
- Regular rule updates

---

**Ready to master policy enforcement?** Start with OPA Gatekeeper and work your way up to comprehensive runtime security!
