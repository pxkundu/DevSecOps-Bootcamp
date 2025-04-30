#!/bin/bash

# Fail-proof script to set up Kubernetes worker node environment on Amazon Linux 2023 with Calico CNI
# Run as ec2-user with sudo privileges
# Prepares environment but does not run kubeadm join (to be executed manually)
# Logs to /var/log/k8s-worker-setup.log

# Exit on critical errors
set -e

# Variables
LOG_FILE="/var/log/k8s-worker-setup.log"
K8S_VERSION="1.29.7"

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
    # Prompt for master IP
    read -p "Enter the master node IP address: " MASTER_IP
    if [ -z "$MASTER_IP" ]; then
        log "${RED}ERROR: Master IP address is required${NC}"
        exit 1
    fi
    # Validate IP format (basic check)
    if ! [[ "$MASTER_IP" =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
        log "${RED}ERROR: Invalid IP address format${NC}"
        exit 1
    fi
    # Prompt for SSH key
    read -p "Enter path to SSH key (or press Enter to skip): " SSH_KEY
    if [ -n "$SSH_KEY" ] && [ ! -f "$SSH_KEY" ]; then
        log "${RED}ERROR: SSH key $SSH_KEY not found${NC}"
        exit 1
    fi
    # Check instance type (t3.medium recommended)
    log "Checking instance type..."
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
    # Test connectivity to master
    log "Testing connectivity to master API server ($MASTER_IP:6443)..."
    nc -z -v -w 5 "$MASTER_IP" 6443 2>&1 | tee -a "$LOG_FILE"
    check_status "Connectivity to master API server ($MASTER_IP:6443)"
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

# Function to validate setup
validate_setup() {
    log "Validating worker node environment..."
    # Check services
    sudo systemctl is-active --quiet containerd
    check_status "containerd service check"
    sudo systemctl is-active --quiet kubelet
    check_status "kubelet service check"
    # Verify connectivity to master
    nc -z -v -w 5 "$MASTER_IP" 6443 2>&1 | tee -a "$LOG_FILE"
    check_status "Master API server connectivity post-setup"
}

# Main execution
log "Starting Kubernetes worker node environment setup with Calico CNI..."

validate_prereqs
install_deps
install_k8s
configure_system
validate_setup

log "${GREEN}Kubernetes worker node environment setup completed successfully!${NC}"
log "To join the cluster, run the kubeadm join command manually from /home/ec2-user/kubeadm-join.sh"
log "Example: sudo bash /home/ec2-user/kubeadm-join.sh"
log "Logs saved to: $LOG_FILE"
