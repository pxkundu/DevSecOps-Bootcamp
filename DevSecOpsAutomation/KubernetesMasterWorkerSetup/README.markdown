# Kubernetes Cluster Setup Automation Scripts with Calico CNI

This document explains the purpose, implementation, and usage of two automation scripts designed to set up a Kubernetes v1.29.7 cluster on Amazon Linux 2023, using Calico as the Container Network Interface (CNI). The scripts are tailored for AWS EC2 `t3.medium` instances but are flexible for various environments and use cases.

## Why These Scripts?

### Purpose
The scripts automate the setup of a Kubernetes cluster (master and worker nodes) to:
- **Reduce Manual Effort**: Eliminate repetitive, error-prone manual configuration steps.
- **Ensure Consistency**: Provide a standardized, repeatable process for cluster deployment.
- **Support Learning and Production**: Facilitate rapid prototyping for development, testing, or production environments, such as deploying Istio service mesh and sample applications like Bookinfo.
- **Enable Flexibility**: Allow easy adaptation for different CNIs (e.g., Calico, Cilium, Flannel) and use cases (e.g., service mesh, CI/CD, observability).

### Use Cases
- **Development and Testing**: Quickly spin up clusters for learning Kubernetes, testing workloads, or experimenting with service meshes like Istio.
- **Service Mesh Deployment**: Prepare a cluster for Istio, enabling features like mutual TLS, traffic shaping, and observability (e.g., Bookinfo application).
- **Production Clusters**: Serve as a foundation for production-grade clusters by integrating with additional tools (e.g., monitoring, logging, autoscaling).
- **CNI Experimentation**: Test different CNIs to evaluate performance, security, or compatibility with specific workloads.

## What Do the Scripts Do?

### Overview
The scripts configure a Kubernetes v1.29.7 cluster on Amazon Linux 2023 with Calico v3.28.2 as the CNI:
- **Master Script (`setup-k8s-master-calico.sh`)**:
  - Installs dependencies (`containerd`, `kubeadm`, `kubelet`, `kubectl`).
  - Configures system settings (e.g., disables swap, enables kernel modules).
  - Initializes the control plane with `kubeadm init`.
  - Deploys Calico CNI.
  - Sets up `kubeconfig` for `ec2-user` and `root`.
  - Saves the `kubeadm join` command for workers.
- **Worker Script (`setup-k8s-worker-calico.sh`)**:
  - Installs dependencies and configures system settings.
  - Prepares the node for joining the cluster but defers the `kubeadm join` command for manual execution.
  - Validates connectivity to the master node.

### Key Features
- **Dynamic Configuration**: Fetches the master’s private IP via AWS IMDSv2 and prompts for the master IP (worker script) and optional SSH key.
- **Error Handling**: Uses `set -e` for critical failures, logs all steps to `/var/log/k8s-*.log`, and includes status checks.
- **Modularity**: Structured as functions (e.g., `install_deps`, `configure_system`) for easy modification.
- **CNI Flexibility**: Currently uses Calico but can be adapted for other CNIs (see Customization section).
- **Minimal Resource Usage**: Optimized for `t3.medium` instances (2 vCPUs, 4 GiB RAM).

## How Are the Scripts Implemented?

### Master Script: `setup-k8s-master-calico.sh`
- **Prerequisites Validation**:
  - Checks for `ec2-user`, internet connectivity, instance type (`t3.medium` recommended), and optional SSH key.
  - Fetches the private IP via IMDSv2 (`http://169.254.169.254/latest/meta-data/local-ipv4`).
- **Dependency Installation**:
  - Installs `containerd`, `conntrack-tools`, `socat`, and Kubernetes components (`kubeadm`, `kubelet`, `kubectl` v1.29.7).
  - Configures `containerd` with `SystemdCgroup = true`.
- **System Configuration**:
  - Disables swap, enables `overlay` and `br_netfilter` kernel modules, and sets sysctl parameters for networking.
- **Control Plane Initialization**:
  - Runs `kubeadm init` with `--pod-network-cidr=192.168.0.0/16` and `--apiserver-advertise-address=<master-ip>`.
  - Sets up `kubeconfig` for `ec2-user` and `root`.
  - Saves the `kubeadm join` command to `/home/ec2-user/kubeadm-join.sh`.
- **Calico Installation**:
  - Applies Calico v3.28.2 manifest (`calico.yaml`).
  - Waits for Calico pods to be `Running` (timeout 300s).
- **Validation**:
  - Verifies node readiness and Calico pod status.

### Worker Script: `setup-k8s-worker-calico.sh`
- **Prerequisites Validation**:
  - Checks for `ec2-user`, internet connectivity, instance type, and optional SSH key.
  - Prompts for the master’s IP and validates connectivity to port 6443 (API server).
- **Dependency Installation and System Configuration**:
  - Same as the master script, ensuring consistency.
- **Kubernetes Installation**:
  - Installs `kubeadm`, `kubelet`, `kubectl` v1.29.7.
  - Enables `kubelet` service.
- **Validation**:
  - Confirms `containerd` and `kubelet` services are active.
  - Re-validates master connectivity.
- **Deferred Join**:
  - Instructs the user to manually run the `kubeadm join` command from `/home/ec2-user/kubeadm-join.sh`.

### Logging
- Logs are saved to:
  - Master: `/var/log/k8s-master-setup.log`
  - Worker: `/var/log/k8s-worker-setup.log`
- Each step is timestamped and color-coded (green for success, red for errors).

## How to Use the Scripts

### Prerequisites
- **Instances**: AWS EC2 `t3.medium` running Amazon Linux 2023.
- **Security Group**: Allow:
  - TCP 6443 (API server) from VPC subnet (e.g., `10.0.5.0/24`).
  - TCP 10250 (kubelet) from VPC subnet.
  - TCP 30000–32767 (NodePort) for external access (e.g., Istio).
  - TCP 179 (BGP, for Calico) between nodes.
  - SSH (22) between nodes and from your IP.
  Example AWS CLI commands:
  ```bash
  aws ec2 authorize-security-group-ingress --group-id <sg-id> --protocol tcp --port 6443 --cidr 10.0.5.0/24
  aws ec2 authorize-security-group-ingress --group-id <sg-id> --protocol tcp --port 10250 --cidr 10.0.5.0/24
  aws ec2 authorize-security-group-ingress --group-id <sg-id> --protocol tcp --port 30000-32767 --cidr 0.0.0.0/0
  aws ec2 authorize-security-group-ingress --group-id <sg-id> --protocol tcp --port 179 --cidr 10.0.5.0/24
  aws ec2 authorize-security-group-ingress --group-id <sg-id> --protocol tcp --port 22 --cidr 10.0.5.0/24
  ```
- **SSH Key**: Optional, ensure `chmod 400` if used.
- **Internet Access**: Required for downloading packages and Calico manifests.

### Master Node Setup
1. **Save Script**:
   ```bash
   vi setup-k8s-master-calico.sh
   ```
   Paste the master script content, save, and exit.

2. **Set Permissions**:
   ```bash
   chmod +x setup-k8s-master-calico.sh
   ```

3. **Run Script**:
   ```bash
   ./setup-k8s-master-calico.sh | tee setup.log
   ```
   - Enter SSH key path (e.g., `/home/ec2-user/.ssh/my-key.pem`) or press Enter to skip.
   - The script fetches the private IP automatically.

4. **Verify**:
   ```bash
   kubectl get nodes -o wide
   kubectl get pods -n kube-system -l k8s-app=calico-node
   cat /var/log/k8s-master-setup.log
   cat /home/ec2-user/kubeadm-join.sh
   ```

### Worker Node Setup
1. **Copy Join Command**:
   On the master:
   ```bash
   cat /home/ec2-user/kubeadm-join.sh
   ```
   On the worker:
   ```bash
   vi /home/ec2-user/kubeadm-join.sh
   ```
   Paste the command, save, and exit. Set permissions:
   ```bash
   chmod +x /home/ec2-user/kubeadm-join.sh
   ```

2. **Save Script**:
   ```bash
   vi setup-k8s-worker-calico.sh
   ```
   Paste the worker script content, save, and exit.

3. **Set Permissions**:
   ```bash
   chmod +x setup-k8s-worker-calico.sh
   ```

4. **Run Script**:
   ```bash
   ./setup-k8s-worker-calico.sh | tee setup.log
   ```
   - Enter the master’s IP (e.g., `10.0.5.182`) and SSH key path (or skip).

5. **Join Cluster (When Ready)**:
   ```bash
   sudo bash /home/ec2-user/kubeadm-join.sh
   ```

6. **Verify**:
   On the master (after joining):
   ```bash
   kubectl get nodes -o wide
   ```
   On the worker:
   ```bash
   cat /var/log/k8s-worker-setup.log
   sudo systemctl status containerd kubelet
   kubectl version --client
   ```

## Adapting for Different CNI Configurations

The scripts are designed with modularity, allowing easy swapping of the CNI. Below are instructions to adapt the master script for other CNIs (the worker script remains unchanged, as it doesn’t install the CNI).

### Using Cilium CNI
1. **Modify Master Script**:
   - Replace the `install_calico` function with:
     ```bash
     install_cilium() {
         log "Installing Cilium 1.16.2..."
         curl -L --remote-name-all https://github.com/cilium/cilium-cli/releases/latest/download/cilium-linux-amd64.tar.gz
         sudo tar xzvf cilium-linux-amd64.tar.gz -C /usr/local/bin
         rm cilium-linux-amd64.tar.gz
         cilium version >/dev/null 2>&1
         check_status "Cilium CLI installation"

         cilium install \
             --version 1.16.2 \
             --set ipam.mode=cluster-pool \
             --set ipam.clusterPool.podCIDR="$POD_CIDR" \
             --set kubeProxyReplacement=false \
             --set aws.enabled=true \
             --set ingressController.enabled=false \
             --set istio.enabled=true
         check_status "Cilium installation"

         log "Waiting for Cilium pods to be ready..."
         timeout 300 bash -c "until kubectl get pods -n kube-system -l k8s-app=cilium | grep -q 'Running'; do sleep 5; done"
         check_status "Cilium pods ready"

         cilium status >/dev/null 2>&1
         check_status "Cilium status check"
     }
     ```
   - Update variables:
     ```bash
     CILIUM_VERSION="1.16.2"
     POD_CIDR="10.244.0.0/16"
     ```
   - Replace `install_calico` with `install_cilium` in the main execution block.

2. **Save and Rename**:
   Save as `setup-k8s-master-cilium.sh`.

3. **Run**:
   Follow the same steps as for Calico, ensuring security groups allow Cilium’s ports (e.g., TCP 8472 for VXLAN).

### Using Flannel CNI
1. **Modify Master Script**:
   - Replace the `install_calico` function with:
     ```bash
     install_flannel() {
         log "Installing Flannel v0.25.6..."
         kubectl apply -f https://raw.githubusercontent.com/flannel-io/flannel/v0.25.6/Documentation/kube-flannel.yml
         check_status "Flannel installation"

         log "Waiting for Flannel pods to be ready..."
         timeout 300 bash -c "until kubectl get pods -n kube-system -l app=flannel | grep -q 'Running'; do sleep 5; done"
         check_status "Flannel pods ready"

         kubectl get pods -n kube-system -l app=flannel
         check_status "Flannel status check"
     }
     ```
   - Update variables:
     ```bash
     FLANNEL_VERSION="v0.25.6"
     POD_CIDR="10.244.0.0/16"
     ```
   - Replace `install_calico` with `install_flannel` in the main execution block.

2. **Save and Rename**:
   Save as `setup-k8s-master-flannel.sh`.

3. **Run**:
   Follow the same steps, ensuring the `POD_CIDR` matches Flannel’s default.

### General CNI Customization
- **POD_CIDR**: Adjust the `POD_CIDR` variable to match the CNI’s requirements (e.g., `192.168.0.0/16` for Calico, `10.244.0.0/16` for Cilium/Flannel).
- **Manifests or CLI**: Replace the CNI installation function with the appropriate manifest URL or CLI commands.
- **Security Groups**: Update ports based on the CNI (e.g., Calico uses TCP 179 for BGP, Cilium uses TCP 8472 for VXLAN).
- **Validation**: Update the `validate_setup` function to check for CNI-specific pods (e.g., `calico-node`, `cilium`, `flannel`).

## Use Cases and Customization

### 1. Istio Service Mesh
- **Purpose**: Deploy Istio for traffic management, observability, and security (e.g., Bookinfo application).
- **Customization**:
  - Ensure `POD_CIDR` is compatible with Istio (Calico’s `192.168.0.0/16` works well).
  - Add Istio installation post-setup:
    ```bash
    curl -L https://istio.io/downloadIstio | ISTIO_VERSION=1.25.2 sh -
    cd istio-1.25.2
    export PATH=$PWD/bin:$PATH
    istioctl install --set profile=minimal --set components.egressGateways[0].enabled=false -y
    kubectl edit svc istio-ingressgateway -n istio-system  # Set type: NodePort
    kubectl label namespace default istio-injection=enabled --overwrite
    ```
  - Deploy Bookinfo and configure VirtualServices/DestinationRules (see previous responses).
- **CNI Choice**: Calico is suitable due to its simplicity and compatibility with Istio. Cilium is preferred for advanced observability (e.g., Hubble).

### 2. Production Clusters
- **Purpose**: Build a scalable, secure cluster for production workloads.
- **Customization**:
  - Increase instance size (e.g., `t3.large` or `m5.large`) for higher resource demands.
  - Enable Calico network policies for security:
    ```bash
    kubectl apply -f https://raw.githubusercontent.com/projectcalico/calico/v3.28.2/manifests/calico-policy-only.yaml
    ```
  - Add monitoring tools (e.g., Prometheus, Grafana) post-setup.
  - Configure high availability (HA) by running multiple control-plane nodes (modify `kubeadm init` for HA).
- **CNI Choice**: Calico for policy enforcement, Cilium for performance-critical workloads.

### 3. Development and Testing
- **Purpose**: Create lightweight clusters for learning or CI/CD pipelines.
- **Customization**:
  - Use smaller instances (e.g., `t3.micro`) with reduced resource settings in `kubeadm init`.
  - Skip SSH key validation if not needed.
  - Use Flannel for simplicity and low overhead.
- **CNI Choice**: Flannel for minimal resource usage, Calico for learning network policies.

### 4. Multi-Cloud or Hybrid Clusters
- **Purpose**: Deploy clusters across AWS, GCP, or on-premises.
- **Customization**:
  - Replace IMDSv2 IP fetching with cloud-specific metadata endpoints (e.g., GCP’s `metadata.google.internal`).
  - Use a portable CNI like Calico with BGP for multi-cloud compatibility.
  - Adjust security group rules for non-AWS environments (e.g., firewall rules for on-premises).
- **CNI Choice**: Calico for cross-cloud compatibility, Cilium for advanced networking features.

## Troubleshooting

- **IMDSv2 Issues**:
  - Test:
    ```bash
    TOKEN=$(curl -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600" -s)
    curl -s -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/local-ipv4
    ```
  - Check security groups or VPC settings if it fails.
- **Calico Pods Not Running**:
  - Check logs:
    ```bash
    kubectl logs -n kube-system -l k8s-app=calico-node
    ```
  - Reapply Calico:
    ```bash
    kubectl delete -f https://raw.githubusercontent.com/projectcalico/calico/v3.28.2/manifests/calico.yaml
    kubectl apply -f https://raw.githubusercontent.com/projectcalico/calico/v3.28.2/manifests/calico.yaml
    ```
- **Join Command Failure**:
  - Verify token:
    ```bash
    kubeadm token list
    ```
  - Regenerate:
    ```bash
    kubeadm token create --print-join-command > /home/ec2-user/kubeadm-join.sh
    ```
  - Test connectivity:
    ```bash
    nc -v -z <master-ip> 6443
    ```
- **Dependency Issues**:
  - Check yum logs:
    ```bash
    cat /var/log/yum.log
    ```
  - Verify packages:
    ```bash
    rpm -q containerd kubelet kubeadm kubectl
    ```

## Next Steps
After setting up the cluster:
1. **Verify Cluster**:
   ```bash
   kubectl get nodes -o wide
   kubectl get pods -n kube-system -l k8s-app=calico-node
   ```
2. **Deploy Workloads**:
   - For Istio, follow the installation steps above.
   - For other workloads, apply manifests or use Helm charts.
3. **Monitor and Scale**:
   - Add observability tools (e.g., Prometheus, Grafana).
   - Scale the cluster by adding more worker nodes using the worker script.

These scripts provide a solid foundation for Kubernetes cluster automation, adaptable to various CNIs and use cases, ensuring flexibility and reliability for your projects.