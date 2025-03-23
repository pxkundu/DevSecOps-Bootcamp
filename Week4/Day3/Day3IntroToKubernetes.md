## Kubernetes Basics: Expanded Theoretical Grounding

### What is Kubernetes?
- **Definition**: An open-source platform for automating deployment, scaling, and management of containerized applications (e.g., Docker containers).
- **Origin**: Developed by Google, open-sourced in 2014, now maintained by the Cloud Native Computing Foundation (CNCF).
- **Core Idea**: Abstracts infrastructure, allowing you to declaratively define application states (e.g., “run 3 instances”) and let K8s handle the “how.”

### Why Kubernetes?
- **Container Orchestration**: Manages multiple containers across multiple hosts, unlike Docker’s single-host focus.
- **Key Features**:
  - **Self-Healing**: Restarts failed containers, replaces crashed Pods.
  - **Scaling**: Automatically adjusts replicas based on load.
  - **Service Discovery**: Provides stable networking via Services.
  - **Portability**: Runs on AWS, GCP, Azure, or on-prem.

### Core Components
1. **Cluster**: A master (control plane) and worker nodes.
   - **Control Plane**: Manages cluster state (API Server, Scheduler, etcd).
   - **Nodes**: Run workloads (kubelet, kube-proxy).
2. **Pod**: Smallest unit, hosts one or more containers.
3. **Deployment**: Manages Pod replicas and updates.
4. **Service**: Exposes Pods via a stable endpoint.
5. **Namespace**: Isolates resources (e.g., `dev`, `prod`).

---

## Installation Instructions

### On Windows WSL (Ubuntu)
Windows Subsystem for Linux (WSL) lets you run a Linux environment on Windows, ideal for Kubernetes tools like `kubectl`.

1. **Enable WSL and Install Ubuntu**:
   - Open PowerShell (Admin):
     ```powershell
     wsl --install
     ```
   - Install Ubuntu from Microsoft Store (e.g., Ubuntu 20.04).
   - Set WSL 2 as default:
     ```powershell
     wsl --set-default-version 2
     ```

2. **Update Ubuntu**:
   - Launch Ubuntu in WSL (`wsl -d Ubuntu-20.04`):
     ```bash
     sudo apt update && sudo apt upgrade -y
     ```

3. **Install `kubectl`**:
   - Add Kubernetes APT repository:
     ```bash
     curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.28/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
     echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.28/deb/ /' | sudo tee /etc/apt/sources.list.d/kubernetes.list
     ```
   - Install `kubectl`:
     ```bash
     sudo apt update
     sudo apt install -y kubectl
     ```
   - Verify:
     ```bash
     kubectl version --client
     ```

4. **Install Minikube (Optional Local Cluster)**:
   - Install dependencies:
     ```bash
     sudo apt install -y curl wget
     ```
   - Download Minikube:
     ```bash
     curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
     sudo install minikube-linux-amd64 /usr/local/bin/minikube
     ```
   - Install Docker (Minikube driver):
     ```bash
     sudo apt install -y docker.io
     sudo usermod -aG docker $USER && newgrp docker
     ```
   - Start Minikube:
     ```bash
     minikube start --driver=docker
     ```

### On macOS
macOS uses Homebrew for streamlined installation.

1. **Install Homebrew** (if not already installed):
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **Install `kubectl`**:
   ```bash
   brew install kubectl
   ```
   - Verify:
     ```bash
     kubectl version --client
     ```

3. **Install Minikube (Optional Local Cluster)**:
   ```bash
   brew install minikube
   ```
   - Install Docker (if not present):
     ```bash
     brew install docker
     ```
   - Start Minikube:
     ```bash
     minikube start --driver=docker
     ```

---

## Basic and Most Used Kubernetes Commands

### Setup Commands
1. **Check Cluster Info**:
   ```bash
   kubectl cluster-info
   ```
   - Shows cluster control plane and services.

2. **View Nodes**:
   ```bash
   kubectl get nodes
   ```
   - Lists all nodes in the cluster.

3. **Configure Context** (e.g., for EKS):
   ```bash
   aws eks update-kubeconfig --name dev-us-crm-us-east-1 --region us-east-1
   ```
   - Updates `~/.kube/config` to connect to an EKS cluster.

### Resource Management Commands
4. **Create Resources**:
   ```bash
   kubectl apply -f file.yaml
   ```
   - Deploys Pods, Deployments, Services from YAML.

5. **List Resources**:
   - Pods:
     ```bash
     kubectl get pods
     ```
   - Deployments:
     ```bash
     kubectl get deployments
     ```
   - Services:
     ```bash
     kubectl get services
     ```
   - Add `-n <namespace>` (e.g., `-n dev-us`) for specific namespaces.

6. **Describe Resources**:
   ```bash
   kubectl describe pod <pod-name>
   ```
   - Detailed info (e.g., events, status).

7. **Delete Resources**:
   ```bash
   kubectl delete -f file.yaml
   ```
   - Removes specified resources.

### Debugging Commands
8. **View Logs**:
   ```bash
   kubectl logs <pod-name>
   ```
   - Shows container output.

9. **Exec into Pod**:
   ```bash
   kubectl exec -it <pod-name> -- /bin/bash
   ```
   - Opens a shell inside the container.

10. **Port Forward**:
    ```bash
    kubectl port-forward <pod-name> 8080:80
    ```
    - Maps local port to Pod port for testing.

### Scaling Commands
11. **Scale Deployment**:
    ```bash
    kubectl scale deployment <deployment-name> --replicas=5
    ```
    - Adjusts number of Pod replicas.

12. **Check Namespace**:
    ```bash
    kubectl get namespaces
    ```
    - Lists all namespaces.

---

## Basic Use Cases with Practical Commands

### Use Case 1: Deploy a Simple Web App
- **Scenario**: Run an NGINX web server locally with Minikube.
- **Commands**:
  1. Start Minikube:
     ```bash
     minikube start
     ```
  2. Create Deployment:
     ```bash
     kubectl create deployment nginx-app --image=nginx --replicas=2
     ```
  3. Expose as Service:
     ```bash
     kubectl expose deployment nginx-app --type=LoadBalancer --port=80
     ```
  4. Access (Minikube):
     ```bash
     minikube service nginx-app
     ```
  5. Verify:
     ```bash
     kubectl get pods
     kubectl get svc
     ```
- **Outcome**: NGINX runs with 2 Pods, accessible via browser.

### Use Case 2: Manage a Microservice (CRM API)
- **Scenario**: Deploy `crm-api` from Day 2’s ECR to EKS.
- **Commands**:
  1. Connect to EKS:
     ```bash
     aws eks update-kubeconfig --name dev-us-crm-us-east-1 --region us-east-1
     ```
  2. Create Namespace:
     ```bash
     kubectl create namespace dev-us
     ```
  3. Apply YAML:
     ```bash
     cat << 'EOF' > crm-api.yaml
     apiVersion: apps/v1
     kind: Deployment
     metadata:
       name: crm-api
       namespace: dev-us
     spec:
       replicas: 3
       selector:
         matchLabels:
           app: crm-api
       template:
         metadata:
           labels:
             app: crm-api
         spec:
           containers:
           - name: crm-api
             image: 866934333672.dkr.ecr.us-east-1.amazonaws.com/dev-us-crm-api:latest
             ports:
             - containerPort: 3000
     ---
     apiVersion: v1
     kind: Service
     metadata:
       name: crm-api-service
       namespace: dev-us
     spec:
       selector:
         app: crm-api
       ports:
       - port: 80
         targetPort: 3000
       type: LoadBalancer
     EOF
     kubectl apply -f crm-api.yaml
     ```
  4. Verify:
     ```bash
     kubectl get pods -n dev-us
     kubectl get svc -n dev-us
     ```
  5. Access:
     - Copy LoadBalancer URL from `kubectl get svc`, test in browser (`http://<URL>`).
- **Outcome**: `crm-api` runs with 3 replicas on EKS.

### Use Case 3: Debug a Failing App
- **Scenario**: Troubleshoot a Pod not starting.
- **Commands**:
  1. List Pods:
     ```bash
     kubectl get pods -n dev-us
     ```
     - Note `<pod-name>` with `CrashLoopBackOff`.
  2. Check Details:
     ```bash
     kubectl describe pod <pod-name> -n dev-us
     ```
     - Look at `Events` for errors (e.g., image pull failure).
  3. View Logs:
     ```bash
     kubectl logs <pod-name> -n dev-us
     ```
  4. Fix (e.g., correct image tag), reapply:
     ```bash
     kubectl apply -f crm-api.yaml
     ```
- **Outcome**: Identify and resolve Pod issues.

---

## Practical Notes
- **Minikube**: Great for local testing; simulates a single-node cluster.
- **EKS**: Use Day 2’s cluster for real-world AWS practice.
- **kubectl Autocomplete**:
  - WSL: `source <(kubectl completion bash)`.
  - macOS: `brew install bash-completion; kubectl completion bash > ~/.kubectl-completion; source ~/.kubectl-completion`.

---

## Official Kubernetes Documentation Links
- **Kubernetes Overview**: [https://kubernetes.io/docs/concepts/overview/](https://kubernetes.io/docs/concepts/overview/)
- **Installation Guide**: [https://kubernetes.io/docs/setup/](https://kubernetes.io/docs/setup/)
- **kubectl Reference**: [https://kubernetes.io/docs/reference/kubectl/](https://kubernetes.io/docs/reference/kubectl/)
- **Tutorials (Deploying Apps)**: [https://kubernetes.io/docs/tutorials/](https://kubernetes.io/docs/tutorials/)
- **Minikube Docs**: [https://minikube.sigs.k8s.io/docs/](https://minikube.sigs.k8s.io/docs/)

---
