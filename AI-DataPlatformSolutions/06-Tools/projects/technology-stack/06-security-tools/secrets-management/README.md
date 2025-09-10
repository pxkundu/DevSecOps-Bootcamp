# Secrets Management - Secure Credential Storage

## 🔐 Overview
Secrets management is crucial for DevSecOps to securely store, manage, and distribute sensitive information like passwords, API keys, and certificates. This section covers enterprise-grade secrets management solutions.

## 📁 Directory Structure

```
secrets-management/
├── README.md
├── vault/
│   ├── policies/
│   ├── auth-methods/
│   └── secrets-engines/
├── aws-secrets-manager/
│   ├── policies/
│   └── scripts/
├── azure-key-vault/
│   ├── policies/
│   └── scripts/
└── kubernetes-secrets/
    ├── sealed-secrets/
    └── external-secrets/
```

## 🛠️ HashiCorp Vault Implementation

### 1. Vault Configuration
```hcl
# vault/config/vault.hcl
storage "file" {
  path = "/vault/file"
}

listener "tcp" {
  address     = "0.0.0.0:8200"
  tls_disable = 1
}

api_addr = "http://0.0.0.0:8200"
ui = true
```

### 2. Vault Policies
```hcl
# vault/policies/app-policy.hcl
path "secret/data/myapp/*" {
  capabilities = ["read"]
}

path "secret/data/myapp/database" {
  capabilities = ["read", "update"]
}

path "pki/issue/myapp" {
  capabilities = ["create", "update"]
}
```

### 3. Vault Scripts
```bash
#!/bin/bash
# vault/scripts/setup-vault.sh

# Initialize Vault
vault operator init -key-shares=5 -key-threshold=3

# Unseal Vault
vault operator unseal <unseal-key-1>
vault operator unseal <unseal-key-2>
vault operator unseal <unseal-key-3>

# Enable secrets engine
vault secrets enable -path=secret kv-v2

# Create policy
vault policy write myapp-policy vault/policies/app-policy.hcl

# Enable auth method
vault auth enable kubernetes
```

## 🔑 AWS Secrets Manager

### 1. Secrets Creation
```bash
#!/bin/bash
# aws-secrets-manager/scripts/create-secret.sh

# Create database secret
aws secretsmanager create-secret \
    --name "myapp/database" \
    --description "Database credentials for MyApp" \
    --secret-string '{"username":"admin","password":"securepassword","host":"db.example.com","port":"5432"}'

# Create API key secret
aws secretsmanager create-secret \
    --name "myapp/api-key" \
    --description "API key for MyApp" \
    --secret-string "sk-1234567890abcdef"
```

### 2. IAM Policy
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "secretsmanager:GetSecretValue"
      ],
      "Resource": [
        "arn:aws:secretsmanager:us-west-2:123456789012:secret:myapp/*"
      ]
    }
  ]
}
```

## 🔐 Azure Key Vault

### 1. Key Vault Setup
```bash
#!/bin/bash
# azure-key-vault/scripts/setup-keyvault.sh

# Create resource group
az group create --name myapp-rg --location westus2

# Create key vault
az keyvault create \
    --name myapp-keyvault \
    --resource-group myapp-rg \
    --location westus2 \
    --sku standard

# Create secrets
az keyvault secret set \
    --vault-name myapp-keyvault \
    --name database-password \
    --value "securepassword"

az keyvault secret set \
    --vault-name myapp-keyvault \
    --name api-key \
    --value "sk-1234567890abcdef"
```

### 2. Access Policy
```json
{
  "properties": {
    "accessPolicies": [
      {
        "tenantId": "tenant-id",
        "objectId": "object-id",
        "permissions": {
          "keys": ["get", "list"],
          "secrets": ["get", "list"],
          "certificates": ["get", "list"]
        }
      }
    ]
  }
}
```

## ☸️ Kubernetes Secrets Management

### 1. Sealed Secrets
```yaml
# kubernetes-secrets/sealed-secrets/myapp-secret.yaml
apiVersion: bitnami.com/v1alpha1
kind: SealedSecret
metadata:
  name: myapp-secret
  namespace: default
spec:
  encryptedData:
    database-password: AgBy3i4OJSWK+PiTySYZZA9rO43cGDEQAx...
    api-key: AgBy3i4OJSWK+PiTySYZZA9rO43cGDEQAx...
  template:
    metadata:
      name: myapp-secret
      namespace: default
    type: Opaque
```

### 2. External Secrets Operator
```yaml
# kubernetes-secrets/external-secrets/secret-store.yaml
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: vault-backend
  namespace: default
spec:
  provider:
    vault:
      server: "https://vault.example.com"
      path: "secret"
      version: "v2"
      auth:
        kubernetes:
          mountPath: "kubernetes"
          role: "myapp"
```

## 📋 Best Practices

### 1. Security
- Rotate secrets regularly
- Use least privilege access
- Encrypt secrets at rest and in transit
- Audit secret access
- Implement secret scanning

### 2. Management
- Use centralized secret management
- Implement backup and recovery
- Monitor secret usage
- Automate secret rotation
- Document secret policies

### 3. Integration
- Integrate with CI/CD pipelines
- Use service accounts for applications
- Implement secret injection
- Monitor secret health
- Plan for disaster recovery

---

**Ready to master secrets management?** Start with Vault setup and work your way up to enterprise-grade secret management!
