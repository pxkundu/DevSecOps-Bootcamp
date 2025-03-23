## Project Overview: Message Encoder/Decoder Application on Kubernetes

### Scenario
You’re a DevOps engineer at a startup building a tool for encoding English messages into binary and decoding them back, useful for secure communication or educational purposes. The app has two components:
- **Frontend**: A Node.js UI where users input messages and see encoded/decoded results.
- **Backend**: A Node.js API that handles encoding (English to binary) and decoding (binary to English).

### Objectives
- Deploy the encoder/decoder app on Minikube.
- Practice Kubernetes basics (Pods, Deployments, Services).
- Use `kubectl` to manage and verify the deployment.
- Simulate a real-world utility application.

### Technologies
- **Kubernetes**: Minikube for local orchestration.
- **Docker**: Containers for frontend and backend.
- **Node.js**: Application runtime for both components.

### Prerequisites
- Minikube, `kubectl`, Docker installed (per Day 3 instructions).
- Node.js (optional, for local testing).

---

## Updated Project Structure
```
MessageEncoderDecoderK8s/
├── frontend/
│   ├── Dockerfile          # Frontend container definition
│   ├── server.js          # Node.js web server with UI
│   └── package.json       # Dependencies
├── backend/
│   ├── Dockerfile         # Backend container definition
│   ├── server.js          # Node.js API for encoding/decoding
│   └── package.json       # Dependencies
├── k8s/
│   ├── frontend-deployment.yaml  # Frontend Deployment and Service
│   └── backend-deployment.yaml   # Backend Deployment and Service
├── .gitignore             # Ignore node_modules
└── README.md              # Instructions
```
---
# Message Encoder/Decoder Application on Kubernetes

A learning project to deploy an encoder/decoder app with Kubernetes on Minikube.

## Functionality
- **Frontend**: Input English text to encode into binary or binary to decode into English.
- **Backend**: API endpoints `/encode` and `/decode` for conversion.

## Setup Instructions
1. **Start Minikube**
   ```bash
   minikube start --driver=docker
   ```

2. **Build Docker Images**
   ```bash
   cd frontend
   docker build -t encoder-frontend:latest .
   cd ../backend
   docker build -t encoder-backend:latest .
   ```

3. **Deploy to Kubernetes**
   ```bash
   cd ../k8s
   kubectl apply -f backend-deployment.yaml
   kubectl apply -f frontend-deployment.yaml
   ```

4. **Access the App**
   ```bash
   minikube service encoder-frontend-service
   ```

5. **Verify**
   ```bash
   kubectl get pods
   kubectl get services
   ```

## Usage
- Enter an English message (e.g., "Hello") → Get binary (e.g., "01001000 01100101 01101100 01101100 01101111").
- Enter binary (e.g., "01001000 01100101 01101100 01101100 01101111") → Get "Hello".

## Cleanup
```bash
kubectl delete -f k8s/
minikube stop
```

## Learning Goals
- Deploy Pods via Deployments.
- Expose apps with Services.
- Use `kubectl` for management.

---

## Learning Outcomes
- **Pods**: Deployed frontend and backend containers.
- **Deployments**: Managed 2 replicas each, ensuring availability.
- **Services**: Exposed frontend externally (LoadBalancer), backend internally (ClusterIP).
- **kubectl**: Used for deployment, verification, and scaling.
- **Real-World Use**: Simulated a messaging tool with encoding/decoding, akin to secure chat apps.
