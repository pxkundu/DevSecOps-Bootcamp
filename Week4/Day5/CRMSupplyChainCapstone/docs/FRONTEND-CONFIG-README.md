Below is a detailed documentation as tailored for setting up the **Phase 3: Frontend - User Interfaces** components (`crm-ui` and `tracking-ui`) of the **CRM-Integrated Global Supply Chain System** capstone project. 

This README provides step-by-step instructions for both **local setup** (using Docker on a developer’s machine) and **AWS cloud setup** (using Amazon ECR and ECS/EKS), ensuring the frontend services are functional in both environments. 

It aligns with industry standards, incorporates DevSecOps best practices, and ensures a professional setup process for the project’s face—the user interfaces.

---

# FRONTEND-CONFIG-README: Frontend Setup for Phase 3 (crm-ui and tracking-ui)

This guide details how to set up and run the **Phase 3: Frontend - User Interfaces** components (`crm-ui` and `tracking-ui`) of the CRM-Integrated Global Supply Chain System. It covers two environments:
- **Local Setup**: Running Dockerized services on your machine for development and testing.
- **AWS Cloud Setup**: Deploying to AWS using ECR (Elastic Container Registry) and ECS/EKS (Elastic Container Service or Kubernetes Service) for production-like scenarios.

These frontends rely on the Phase 2 backend services (`crm-api`, `order-service`, `logistics-service`) being operational, either locally or in AWS.

---

## Prerequisites

### Local Setup
- **Docker**: Latest stable version for building/running containers.
  - Install: `sudo apt-get install docker.io` (Linux) or [Docker Desktop](https://www.docker.com/products/docker-desktop) (Windows/Mac).
- **Node.js**: Version 18.x (optional, for manual inspection).
  - Install: `curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash - && sudo apt-get install -y nodejs` (Linux).
- **Git**: For cloning/managing the repo.
  - Install: `sudo apt-get install git`.
- **Backend Services**: Phase 2 services running locally (see `docs/CONFIG-README.md` for backend setup).

### AWS Cloud Setup
- **AWS CLI**: Version 2.x for interacting with AWS services.
  - Install: `curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && unzip awscliv2.zip && sudo ./aws/install`.
- **AWS Account**: Configured with IAM user/role having ECR/ECS/EKS permissions.
  - Configure: `aws configure` (set access key, secret key, region, e.g., `us-east-1`).
- **Docker**: As above, for building/pushing images.
- **ECR Repositories**: Created for `crm-ui` and `tracking-ui`.
- **ECS/EKS Cluster**: Pre-provisioned (via Terraform in `infrastructure/` or manually).
- **Backend Services**: Deployed to AWS (e.g., ECS/EKS) with accessible endpoints.

---

## Project Structure (Relevant Files)
```
CRMSupplyChainCapstone/
├── services/
│   ├── crm-ui/                # CRM UI service
│   │   ├── Dockerfile
│   │   ├── app.js
│   │   ├── package.json
│   │   ├── views/
│   │   │   ├── index.ejs
│   │   │   ├── order-details.ejs
│   │   │   └── partials/
│   │   │       └── order-table.ejs
│   │   └── public/
│   │       ├── styles.css
│   │       └── script.js
│   ├── tracking-ui/           # Tracking UI service
│   │   ├── Dockerfile
│   │   ├── app.js
│   │   ├── package.json
│   │   ├── views/
│   │   │   ├── index.ejs
│   │   │   └── partials/
│   │   │       └── shipment-card.ejs
│   │   └── public/
│   │       └── styles.css
```

---

## Local Setup

### 1. Generate Deliverables
- Ensure Phase 3 deliverables are generated:
  ```bash
  chmod +x generate-phase3-deliverables.sh
  ./generate-phase3-deliverables.sh
  ```
- Navigate to project root:
  ```bash
  cd CRMSupplyChainCapstone
  ```

### 2. Verify Backend Services
- Ensure Phase 2 backend services are running locally (ports 3000, 6000, 5000):
  ```bash
  docker ps
  ```
- If not running, follow `docs/CONFIG-README.md` for backend setup.

### 3. Build and Run Frontend Containers

#### a. `crm-ui`
- Build:
  ```bash
  cd services/crm-ui
  docker build -t crm-ui:latest .
  ```
- Run:
  ```bash
  docker run -d -p 7000:7000 --name crm-ui \
    -e CRM_API_URL=http://host.docker.internal:3000 \
    -e ORDER_SERVICE_URL=http://host.docker.internal:6000 \
    -e API_KEY=default-key \
    crm-ui:latest
  ```
  - Note: `host.docker.internal` links to your local machine; use `--network host` on Linux if needed.

#### b. `tracking-ui`
- Build:
  ```bash
  cd ../tracking-ui
  docker build -t tracking-ui:latest .
  ```
- Run:
  ```bash
  docker run -d -p 8000:8000 --name tracking-ui \
    -e LOGISTICS_SERVICE_URL=http://host.docker.internal:5000 \
    -e API_KEY=default-key \
    tracking-ui:latest
  ```

### 4. Verify Services
- Check logs:
  ```bash
  docker logs crm-ui
  docker logs tracking-ui
  ```
- Expected output: “running on port 7000” and “running on port 8000”.

### 5. Test Endpoints
- **crm-ui**: Open `http://localhost:7000` in a browser.
  - View orders, submit a new order (e.g., Product ID: `prod-001`, Quantity: `5`).
- **tracking-ui**: Open `http://localhost:8000`.
  - Enter a shipment ID (e.g., `ship-123`) from a prior order to track.

---

## AWS Cloud Setup

### 1. Prepare ECR Repositories
- Create repositories:
  ```bash
  aws ecr create-repository --repository-name crm-ui --region us-east-1
  aws ecr create-repository --repository-name tracking-ui --region us-east-1
  ```
- Authenticate Docker to ECR:
  ```bash
  aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <aws_account_id>.dkr.ecr.us-east-1.amazonaws.com
  ```
  - Replace `<aws_account_id>` with your AWS account ID.

### 2. Build and Push Docker Images

#### a. `crm-ui`
- Build and tag:
  ```bash
  cd services/crm-ui
  docker build -t crm-ui:latest .
  docker tag crm-ui:latest <aws_account_id>.dkr.ecr.us-east-1.amazonaws.com/crm-ui:latest
  ```
- Push:
  ```bash
  docker push <aws_account_id>.dkr.ecr.us-east-1.amazonaws.com/crm-ui:latest
  ```

#### b. `tracking-ui`
- Build and tag:
  ```bash
  cd ../tracking-ui
  docker build -t tracking-ui:latest .
  docker tag tracking-ui:latest <aws_account_id>.dkr.ecr.us-east-1.amazonaws.com/tracking-ui:latest
  ```
- Push:
  ```bash
  docker push <aws_account_id>.dkr.ecr.us-east-1.amazonaws.com/tracking-ui:latest
  ```

### 3. Deploy to AWS (ECS or EKS)

#### Option 1: ECS (Simpler)
- **Task Definitions**:
  - Create `crm-ui-task.json`:
    ```json
    {
      "family": "crm-ui",
      "containerDefinitions": [
        {
          "name": "crm-ui",
          "image": "<aws_account_id>.dkr.ecr.us-east-1.amazonaws.com/crm-ui:latest",
          "portMappings": [{ "containerPort": 7000, "hostPort": 7000 }],
          "environment": [
            { "name": "CRM_API_URL", "value": "<crm-api-endpoint>" },
            { "name": "ORDER_SERVICE_URL", "value": "<order-service-endpoint>" },
            { "name": "API_KEY", "value": "<secure-api-key>" }
          ]
        }
      ]
    }
    ```
  - Create `tracking-ui-task.json`:
    ```json
    {
      "family": "tracking-ui",
      "containerDefinitions": [
        {
          "name": "tracking-ui",
          "image": "<aws_account_id>.dkr.ecr.us-east-1.amazonaws.com/tracking-ui:latest",
          "portMappings": [{ "containerPort": 8000, "hostPort": 8000 }],
          "environment": [
            { "name": "LOGISTICS_SERVICE_URL", "value": "<logistics-service-endpoint>" },
            { "name": "API_KEY", "value": "<secure-api-key>" }
          ]
        }
      ]
    }
    ```
- Register tasks:
  ```bash
  aws ecs register-task-definition --cli-input-json file://crm-ui-task.json
  aws ecs register-task-definition --cli-input-json file://tracking-ui-task.json
  ```
- **Service**: Deploy to an ECS cluster with an Application Load Balancer (ALB) targeting ports 7000 and 8000.

#### Option 2: EKS (Kubernetes, Phase 4 Preview)
- Use `kubernetes/crm/deployment.yaml` and `kubernetes/supply-chain/tracking-deployment.yaml` (to be populated in Phase 4):
  ```yaml
  apiVersion: apps/v1
  kind: Deployment
  metadata:
    name: crm-ui
  spec:
    replicas: 2
    selector:
      matchLabels:
        app: crm-ui
    template:
      metadata:
        labels:
          app: crm-ui
      spec:
        containers:
        - name: crm-ui
          image: <aws_account_id>.dkr.ecr.us-east-1.amazonaws.com/crm-ui:latest
          ports:
          - containerPort: 7000
          env:
          - name: CRM_API_URL
            value: "<crm-api-endpoint>"
          - name: ORDER_SERVICE_URL
            value: "<order-service-endpoint>"
          - name: API_KEY
            valueFrom:
              secretKeyRef:
                name: api-key-secret
                key: api-key
  ```
- Apply with `kubectl apply -f`.

### 4. Configure Backend Endpoints
- Replace `<crm-api-endpoint>`, `<order-service-endpoint>`, `<logistics-service-endpoint>` with actual URLs (e.g., ALB DNS from backend ECS/EKS setup).
- Store `API_KEY` in AWS Secrets Manager and reference it in ECS/EKS.

### 5. Access the UIs
- Use the ALB DNS (e.g., `http://<alb-dns>:7000` for `crm-ui`, `http://<alb-dns>:8000` for `tracking-ui`).

---

## DevSecOps Best Practices
- **Security**:
  - Local: Hardcoded `API_KEY` for simplicity; replace with `.env` or secrets in production.
  - AWS: Use Secrets Manager for `API_KEY`, enforce HTTPS via ALB.
- **Resilience**:
  - Error handling in UI (`error` variable in EJS) ensures graceful failure if backend is down.
- **Observability**:
  - Local: Check Docker logs.
  - AWS: Integrate with CloudWatch Logs (auto-enabled in ECS/EKS).
- **Automation**:
  - Docker builds enable CI/CD (Phase 5 Jenkins pipeline).
  - ECR/ECS/EKS setup supports Infrastructure as Code (IaC) via Terraform.

---

## Troubleshooting
- **Local**:
  - **Port Conflict**: Stop other services on 7000/8000 (`sudo lsof -i :7000`).
  - **Backend Unreachable**: Verify backend URLs and API key match Phase 2 setup.
- **AWS**:
  - **Image Pull Fails**: Check ECR permissions and AWS CLI login.
  - **UI Not Loading**: Ensure ALB targets are healthy; verify backend endpoints.

---

## Notes
- **Local**: Ideal for development; assumes backend runs locally or is network-accessible.
- **AWS**: Previews Phase 4/5 deployment; requires backend services in ECS/EKS and network config (e.g., VPC).
- **Next Steps**: Phase 4 will formalize Kubernetes manifests, Phase 5 will add CI/CD.

This setup ensures `crm-ui` and `tracking-ui` are professional, functional, and ready for both local testing and cloud deployment!


---

### Explanation
- **Local Setup**: Guides developers to build/run Docker containers with env vars linking to local backend services, mirroring Phase 2’s setup process.
- **AWS Setup**: Covers ECR for image storage, ECS for a simpler deployment, and EKS as a Kubernetes preview, with secure API key handling via Secrets Manager.
- **Structure**: Focuses on `crm-ui` and `tracking-ui` files, ensuring all dependencies (e.g., backend URLs) are clear.
- **DevSecOps**: Embeds security (secrets), resilience (error handling), observability (logs), and automation (Docker/ECR), aligning with industry standards (e.g., Amazon’s cloud practices).
- **Professionalism**: Clear, concise steps with troubleshooting ensure a polished frontend deployment, critical as the project’s user-facing layer.

