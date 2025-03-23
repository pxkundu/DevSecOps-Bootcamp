     #!/bin/bash

# Create project root
mkdir -p CRMSupplyChainCapstone
cd CRMSupplyChainCapstone

# Documentation
mkdir -p docs
touch docs/architecture.md
touch docs/README.md

# Infrastructure (Terraform)
mkdir -p infrastructure/modules/{vpc,eks,rds}
touch infrastructure/main.tf
touch infrastructure/variables.tf
touch infrastructure/outputs.tf
touch infrastructure/backend.tf
touch infrastructure/terraform.tfvars
touch infrastructure/modules/vpc/{main.tf,variables.tf,outputs.tf}
touch infrastructure/modules/eks/{main.tf,variables.tf,outputs.tf}
touch infrastructure/modules/rds/{main.tf,variables.tf,outputs.tf}

# Services (Microservices)
mkdir -p services/{crm-api,crm-ui,crm-analytics,inventory-service,logistics-service,order-service,analytics-service,api-gateway}
touch services/crm-api/{Dockerfile,app.js,package.json}
touch services/crm-ui/{Dockerfile,app.js,package.json}
touch services/crm-analytics/{Dockerfile,app.js,package.json}
touch services/inventory-service/{Dockerfile,app.js,package.json}
touch services/logistics-service/{Dockerfile,app.js,package.json}
touch services/order-service/{Dockerfile,app.js,package.json}
touch services/analytics-service/{Dockerfile,app.js,package.json}
touch services/api-gateway/{Dockerfile,nginx.conf,entrypoint.sh}

# Kubernetes manifests
mkdir -p kubernetes/{crm,supply-chain,ingress}
touch kubernetes/crm/{deployment.yaml,service.yaml}
touch kubernetes/supply-chain/{inventory-deployment.yaml,inventory-service.yaml,logistics-deployment.yaml,logistics-service.yaml,order-deployment.yaml,order-service.yaml,analytics-deployment.yaml,analytics-service.yaml}
touch kubernetes/ingress/ingress.yaml

# Pipeline (CI/CD)
mkdir -p pipeline/scripts
touch pipeline/Jenkinsfile
touch pipeline/scripts/{build.sh,deploy.sh,test.sh}

# Tests
mkdir -p tests/{integration,unit}
touch tests/integration/test-order-flow.sh
touch tests/unit/test-services.sh

# Root files
touch .gitignore
touch .dockerignore

echo "Project structure created successfully! Ready for implementation."
