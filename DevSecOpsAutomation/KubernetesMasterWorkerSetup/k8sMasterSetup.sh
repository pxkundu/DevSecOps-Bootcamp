#!/bin/bash

# Fail-proof script to set up Kubernetes master node on Amazon Linux 2023
# Run as ec2-user with sudo privileges
# Logs to /var/log/k8s-master-setup.log

# Exit on any error
set -e

# Variables
LOG_FILE="/var/log/k8s-master-setup.log"
K8S_VERSION="1.29.7"
CILIUM_VERSION="1.16.2"
POD_CIDR="10.244.0.0/16"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# Function to log messages
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Function to check command success
check_status() {
    if [ $? -eq 0 ]; then
        log "${GREEN}SUCCESS: $1${NC}"
    else
        log "${RED}ERROR: $1 failed${NC}"
        exit 1
    fi
}

# Function to get private IP using IMDSv2
get_private_ip() {
    log "Fetching private IP from EC2 metadata..."
    TOKEN=$(curl -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600" -s)
    if [ -n "$TOKEN" ]; then
        MASTER_IP=$(curl -s -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/local-ipv4 || echo "")
        if [ -z "$MASTER_IP" ]; then
            log "${RED}ERROR: Failed to fetch private IP${NC}"
            exit 1
        fi
        log "Private IP: $MASTER_IP"
    else
        log "${RED}ERROR: Failed to obtain IMDSv2 token${NC}"
        exit 1
    fi
}

# Function to validate prerequisites
validate_prereqs() {
    log "Validating prerequisites..."
    # Check if running as ec2-user
    if [ "$(whoami)" != "ec2-user" ]; then
        log "${RED}ERROR: Must run as ec2-user${NC}"
        exit 1
    fi
    # Check internet connectivity
    ping -c 1 google.com >/dev/null 2>&1
    check_status "Internet connectivity check"
    # Prompt for SSH key
    read -p "Enter path to SSH key (or press Enter to skip): " SSH_KEY
    if [ -n "$SSH_KEY" ] && [ ! -f "$SSH_KEY" ]; then
        log "${RED}ERROR: SSH key $SSH_KEY not found${NC}"
        exit 1
    fi
    # Check instance type (t3.medium recommended)
    TOKEN=$(curl -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600" -s)
    if [ -n "$TOKEN" ]; then
        instance_type=$(curl -s -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/instance-type || echo "unknown")
    else
        instance_type="unknown"
    fi
    if [[ "$instance_type" != "t3.medium" ]]; then
        log "WARNING: Instance type is $instance_type, t3.medium recommended"
    else
        log "Instance type is $instance_type"
    fi
}

# Function to install dependencies
install_deps() {
    log "Installing dependencies..."
    sudo yum update -y
    sudo yum install -y containerd conntrack-tools socat
    check_status "Dependency installation"

    # Configure containerd
    sudo mkdir -p /etc/containerd
    containerd config default | sudo tee /etc/containerd/config.toml
    sudo sed -i 's/SystemdCgroup = false/SystemdCgroup = true/' /etc/containerd/config.toml
    sudo systemctl enable --now containerd
    check_status "containerd configuration"
}

# Function to install Kubernetes components
install_k8s() {
    log "Installing Kubernetes $K8S_VERSION..."
    cat <<EOF | sudo tee /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://pkgs.k8s.io/core:/stable:/v1.29/rpm/
enabled=1
gpgcheck=1
gpgkey=https://pkgs.k8s.io/core:/stable:/v1.29/rpm/repodata/repomd.xml.key
EOF
    sudo yum install -y kubelet-$K8S_VERSION kubeadm-$K8S_VERSION kubectl-$K8S_VERSION --disableexcludes=kubernetes
    check_status "Kubernetes installation"
    sudo systemctl enable --now kubelet
    check_status "kubelet enable"
}

# Function to configure system settings
configure_system() {
    log "Configuring system settings..."
    # Disable swap
    sudo swapoff -a
    sudo sed -i '/ swap / s/^/#/' /etc/fstab
    check_status "Swap disabled"

    # Enable kernel modules
    cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
overlay
br_netfilter
EOF
    sudo modprobe overlay
    sudo modprobe br_netfilter
    check_status "Kernel modules enabled"

    # Set sysctl params
    cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-iptables  = 1
net.bridge.bridge-nf-call-ip6tables = 1
net.ipv4.ip_forward                 = 1
EOF
    sudo sysctl --system
    check_status "Sysctl configuration"
}

# Function to initialize Kubernetes control plane
init_k8s() {
    log "Initializing Kubernetes control plane..."
    sudo kubeadm init \
        --pod-network-cidr="$POD_CIDR" \
        --apiserver-advertise-address="$MASTER_IP" \
        --kubernetes-version="$K8S_VERSION" \
        --ignore-preflight-errors=NumCPU \
        | tee /tmp/kubeadm-init.log
    check_status "Kubernetes initialization"

    # Set up kubeconfig for ec2-user
    mkdir -p "$HOME/.kube"
    sudo cp -f /etc/kubernetes/admin.conf "$HOME/.kube/config"
    sudo chown $(id -u):$(id -g) "$HOME/.kube/config"
    check_status "ec2-user kubeconfig setup"

    # Set up kubeconfig for root
    sudo mkdir -p /root/.kube
    sudo cp -f /etc/kubernetes/admin.conf /root/.kube/config
    sudo chown root:root /root/.kube/config
    check_status "root kubeconfig setup"

    # Save join command
    grep 'kubeadm join' /tmp/kubeadm-init.log > /home/ec2-user/kubeadm-join.sh
    chmod +x /home/ec2-user/kubeadm-join.sh
    check_status "Join command saved"
}

# Function to install Cilium
install_cilium() {
    log "Installing Cilium $CILIUM_VERSION..."
    curl -L --remote-name-all https://github.com/cilium/cilium-cli/releases/latest/download/cilium-linux-amd64.tar.gz
    sudo tar xzvf cilium-linux-amd64.tar.gz -C /usr/local/bin
    rm cilium-linux-amd64.tar.gz
    cilium version >/dev/null 2>&1
    check_status "Cilium CLI installation"

    cilium install \
        --version "$CILIUM_VERSION" \
        --set ipam.mode=cluster-pool \
        --set ipam.clusterPool.podCIDR="$POD_CIDR" \
        --set kubeProxyReplacement=false \
        --set aws.enabled=true \
        --set ingressController.enabled=false \
        --set istio.enabled=true
    check_status "Cilium installation"

    # Wait for Cilium pods
    log "Waiting for Cilium pods to be ready..."
    timeout 300 bash -c "until kubectl get pods -n kube-system -l k8s-app=cilium | grep -q 'Running'; do sleep 5; done"
    check_status "Cilium pods ready"

    cilium status >/dev/null 2>&1
    check_status "Cilium status check"
}

# Function to validate setup
validate_setup() {
    log "Validating Kubernetes setup..."
    kubectl get nodes | grep -q Ready
    check_status "Node readiness check"
    kubectl get pods -n kube-system -l k8s-app=cilium | grep -q Running
    check_status "Cilium pod check"
    cilium connectivity test >/dev/null 2>&1
    check_status "Cilium connectivity test"
}

# Main execution
log "Starting Kubernetes master node setup..."

get_private_ip
validate_prereqs
install_deps
install_k8s
configure_system
init_k8s
install_cilium
validate_setup

log "${GREEN}Kubernetes master node setup completed successfully!${NC}"
log "Join worker nodes using: /home/ec2-user/kubeadm-join.sh"
log "Logs saved to: $LOG_FILE"
