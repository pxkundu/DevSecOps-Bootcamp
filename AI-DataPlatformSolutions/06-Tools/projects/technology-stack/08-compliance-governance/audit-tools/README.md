# Audit Tools - Compliance and Governance

## 🔍 Overview
Audit tools help organizations maintain compliance, track changes, and ensure governance across their DevSecOps infrastructure and applications.

## 📁 Directory Structure

```
audit-tools/
├── README.md
├── aws-audit/
│   ├── configs/
│   └── scripts/
├── azure-audit/
│   ├── configs/
│   └── scripts/
├── kubernetes-audit/
│   ├── policies/
│   └── scripts/
└── compliance-frameworks/
    ├── nist/
    ├── cis/
    └── pci-dss/
```

## 🛠️ AWS Audit Tools

### 1. AWS Config Rules
```yaml
# aws-audit/configs/config-rules.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: aws-config-rules
data:
  config-rules.yaml: |
    rules:
      - name: "s3-bucket-public-read-prohibited"
        description: "Checks that S3 buckets do not allow public read access"
        source:
          owner: AWS
          sourceIdentifier: S3_BUCKET_PUBLIC_READ_PROHIBITED
      
      - name: "rds-storage-encrypted"
        description: "Checks that RDS instances are encrypted"
        source:
          owner: AWS
          sourceIdentifier: RDS_STORAGE_ENCRYPTED
      
      - name: "ec2-instance-no-public-ip"
        description: "Checks that EC2 instances do not have public IPs"
        source:
          owner: AWS
          sourceIdentifier: EC2_INSTANCE_NO_PUBLIC_IP
```

### 2. AWS Audit Script
```bash
#!/bin/bash
# aws-audit/scripts/aws-audit.sh

echo "Running AWS compliance audit..."

# Check S3 bucket encryption
echo "Checking S3 bucket encryption..."
aws s3api list-buckets --query 'Buckets[].Name' --output text | while read bucket; do
  encryption=$(aws s3api get-bucket-encryption --bucket $bucket 2>/dev/null)
  if [ $? -ne 0 ]; then
    echo "❌ Bucket $bucket is not encrypted"
  else
    echo "✅ Bucket $bucket is encrypted"
  fi
done

# Check RDS encryption
echo "Checking RDS encryption..."
aws rds describe-db-instances --query 'DBInstances[?StorageEncrypted==`false`].DBInstanceIdentifier' --output text
if [ $? -eq 0 ]; then
  echo "❌ Unencrypted RDS instances found"
else
  echo "✅ All RDS instances are encrypted"
fi

# Check IAM policies
echo "Checking IAM policies..."
aws iam list-policies --query 'Policies[?PolicyName==`AdministratorAccess`]' --output text
if [ $? -eq 0 ]; then
  echo "❌ Administrator access policy found"
else
  echo "✅ No administrator access policy found"
fi

echo "AWS audit completed"
```

## 🔧 Azure Audit Tools

### 1. Azure Policy Definitions
```json
{
  "properties": {
    "displayName": "Require encryption on storage accounts",
    "description": "This policy ensures that storage accounts use encryption",
    "policyRule": {
      "if": {
        "allOf": [
          {
            "field": "type",
            "equals": "Microsoft.Storage/storageAccounts"
          },
          {
            "field": "Microsoft.Storage/storageAccounts/encryption.services.blob.enabled",
            "equals": "false"
          }
        ]
      },
      "then": {
        "effect": "deny"
      }
    }
  }
}
```

### 2. Azure Audit Script
```bash
#!/bin/bash
# azure-audit/scripts/azure-audit.sh

echo "Running Azure compliance audit..."

# Check storage account encryption
echo "Checking storage account encryption..."
az storage account list --query '[?encryption.services.blob.enabled==`false`].name' --output tsv
if [ $? -eq 0 ]; then
  echo "❌ Unencrypted storage accounts found"
else
  echo "✅ All storage accounts are encrypted"
fi

# Check virtual machine encryption
echo "Checking VM encryption..."
az vm encryption show --ids $(az vm list --query '[].id' --output tsv) --query 'disks[?encryptionSettings==null].name' --output tsv
if [ $? -eq 0 ]; then
  echo "❌ Unencrypted VMs found"
else
  echo "✅ All VMs are encrypted"
fi

# Check network security groups
echo "Checking network security groups..."
az network nsg list --query '[?securityRules[?access==`Allow` && direction==`Inbound` && sourceAddressPrefix==`*`]].name' --output tsv
if [ $? -eq 0 ]; then
  echo "❌ NSGs with open access found"
else
  echo "✅ No NSGs with open access found"
fi

echo "Azure audit completed"
```

## ☸️ Kubernetes Audit Tools

### 1. Kubernetes Audit Policy
```yaml
# kubernetes-audit/policies/audit-policy.yaml
apiVersion: audit.k8s.io/v1
kind: Policy
rules:
- level: Metadata
  namespaces: ["kube-system"]
  resources:
  - group: ""
    resources: ["secrets"]
- level: RequestResponse
  namespaces: ["default"]
  resources:
  - group: ""
    resources: ["pods", "services"]
- level: Request
  resources:
  - group: "apps"
    resources: ["deployments", "replicasets"]
- level: Metadata
  resources:
  - group: ""
    resources: ["configmaps", "secrets"]
```

### 2. Kubernetes Audit Script
```bash
#!/bin/bash
# kubernetes-audit/scripts/k8s-audit.sh

echo "Running Kubernetes compliance audit..."

# Check RBAC
echo "Checking RBAC configuration..."
kubectl get clusterroles --no-headers | wc -l
if [ $(kubectl get clusterroles --no-headers | wc -l) -lt 10 ]; then
  echo "❌ Insufficient RBAC roles configured"
else
  echo "✅ RBAC properly configured"
fi

# Check network policies
echo "Checking network policies..."
kubectl get networkpolicies --all-namespaces --no-headers | wc -l
if [ $(kubectl get networkpolicies --all-namespaces --no-headers | wc -l) -eq 0 ]; then
  echo "❌ No network policies found"
else
  echo "✅ Network policies configured"
fi

# Check pod security
echo "Checking pod security..."
kubectl get pods --all-namespaces -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.securityContext.runAsNonRoot}{"\n"}{end}' | grep -v true
if [ $? -eq 0 ]; then
  echo "❌ Pods running as root found"
else
  echo "✅ All pods running as non-root"
fi

# Check secrets
echo "Checking secrets..."
kubectl get secrets --all-namespaces --no-headers | wc -l
if [ $(kubectl get secrets --all-namespaces --no-headers | wc -l) -eq 0 ]; then
  echo "❌ No secrets found"
else
  echo "✅ Secrets properly configured"
fi

echo "Kubernetes audit completed"
```

## 📊 Compliance Frameworks

### 1. NIST Compliance
```yaml
# compliance-frameworks/nist/nist-compliance.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: nist-compliance
data:
  nist-csf.yaml: |
    nist_csf:
      identify:
        - asset_management:
            controls:
              - id: "ID.AM-1"
                description: "Physical devices and systems within the organization are inventoried"
                status: "implemented"
              - id: "ID.AM-2"
                description: "Software platforms and applications within the organization are inventoried"
                status: "implemented"
        - business_environment:
            controls:
              - id: "ID.BE-1"
                description: "The organization's role in the supply chain is identified and communicated"
                status: "implemented"
      protect:
        - identity_management:
            controls:
              - id: "PR.AC-1"
                description: "Identities and credentials are issued, managed, verified, revoked, and audited"
                status: "implemented"
```

### 2. CIS Compliance
```yaml
# compliance-frameworks/cis/cis-compliance.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: cis-compliance
data:
  cis-controls.yaml: |
    cis_controls:
      basic:
        - control_1:
            title: "Inventory and Control of Enterprise Assets"
            description: "Actively manage all enterprise assets"
            status: "implemented"
        - control_2:
            title: "Inventory and Control of Software Assets"
            description: "Actively manage all software on the network"
            status: "implemented"
      foundational:
        - control_6:
            title: "Access Control Management"
            description: "Use access control lists to manage access to data"
            status: "implemented"
```

## 🚀 Deployment Scripts

### 1. Install Audit Tools
```bash
#!/bin/bash
# scripts/install-audit-tools.sh

echo "Installing audit tools..."

# Install kube-bench
curl -L https://github.com/aquasecurity/kube-bench/releases/download/v0.6.15/kube-bench_0.6.15_linux_amd64.tar.gz | tar -xz

# Install kube-hunter
pip install kube-hunter

# Install kube-score
curl -L https://github.com/zegl/kube-score/releases/download/v1.16.1/kube-score_1.16.1_linux_amd64.tar.gz | tar -xz

echo "Audit tools installation completed"
```

### 2. Run Compliance Audit
```bash
#!/bin/bash
# scripts/run-compliance-audit.sh

echo "Running comprehensive compliance audit..."

# Run kube-bench
echo "Running Kubernetes CIS benchmark..."
./kube-bench run --targets master,node,etcd,policies

# Run kube-hunter
echo "Running Kubernetes security scan..."
kube-hunter --remote <cluster-ip>

# Run kube-score
echo "Running Kubernetes configuration analysis..."
kube-score score k8s-manifests/

# Run cloud provider audits
if [ "$CLOUD_PROVIDER" = "aws" ]; then
  ./aws-audit/scripts/aws-audit.sh
elif [ "$CLOUD_PROVIDER" = "azure" ]; then
  ./azure-audit/scripts/azure-audit.sh
fi

echo "Compliance audit completed"
```

## 📋 Best Practices

### 1. Audit Strategy
- Implement continuous auditing
- Use automated compliance checking
- Regular audit reviews
- Document audit findings

### 2. Compliance Management
- Map controls to requirements
- Implement remediation workflows
- Track compliance status
- Regular compliance reporting

### 3. Governance
- Establish audit policies
- Define compliance standards
- Implement access controls
- Regular governance reviews

---

**Ready to master audit tools?** Start with basic compliance checking and work your way up to comprehensive governance!
