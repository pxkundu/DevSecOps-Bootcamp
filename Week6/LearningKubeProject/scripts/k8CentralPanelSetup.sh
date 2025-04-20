#!/bin/bash

# Kubernetes Setup Script for Amazon Linux 2023
# Run this script with sudo privileges on both master and worker nodes

# Exit on any error
set -e

# Log file for debugging
LOG_FILE="/var/log/k8s_setup.log"
echo "Starting Kubernetes setup at $(date)" | tee -a $LOG_FILE

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to identify if this is master or worker node
NODE_TYPE=${1:-"master"}  # Default to master if no argument provided

# Update system and install basic utilities
echo "Updating system..." | tee -a $LOG_FILE
yum update -y

# Install containerd as container runtime
echo "Installing containerd..." | tee -a $LOG_FILE
yum install -y containerd
systemctl enable containerd
systemctl start containerd

# Configure containerd
mkdir -p /etc/containerd
containerd config default > /etc/containerd/config.toml
sed -i 's/SystemdCgroup = false/SystemdCgroup = true/' /etc/containerd/config.toml
systemctl restart containerd

# Disable SELinux (simplified for learning)
setenforce 0
sed -i 's/^SELINUX=enforcing/SELINUX=disabled/' /etc/selinux/config

# Disable swap (Kubernetes requirement)
swapoff -a
sed -i '/swap/d' /etc/fstab

# Load required kernel modules
echo "Loading kernel modules..." | tee -a $LOG_FILE
modprobe br_netfilter
echo 'br_netfilter' > /etc/modules-load.d/br_netfilter.conf

# Enable IP forwarding
echo "Enabling IP forwarding..." | tee -a $LOG_FILE
sysctl -w net.ipv4.ip_forward=1
echo 'net.ipv4.ip_forward = 1' > /etc/sysctl.d/99-kubernetes.conf
sysctl --system

# Install Kubernetes components
echo "Installing Kubernetes components..." | tee -a $LOG_FILE
cat <<EOF > /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://pkgs.k8s.io/core:/stable:/v1.28/rpm/
enabled=1
gpgcheck=1
gpgkey=https://pkgs.k8s.io/core:/stable:/v1.28/rpm/repodata/repomd.xml.key
EOF

yum install -y kubelet kubeadm kubectl
systemctl enable kubelet

# Master node specific configuration
if [ "$NODE_TYPE" = "master" ]; then
    echo "Configuring master node..." | tee -a $LOG_FILE
    
    # Initialize the Kubernetes cluster with ignore flags for warnings
    kubeadm init --pod-network-cidr=10.244.0.0/16 --ignore-preflight-errors=FileExisting-tc,Hostname | tee -a $LOG_FILE
    
    # Set up kubeconfig for root user
    mkdir -p /root/.kube
    cp -i /etc/kubernetes/admin.conf /root/.kube/config
    chown root:root /root/.kube/config
    
    # Install Flannel network plugin
    echo "Installing Flannel CNI..." | tee -a $LOG_FILE
    kubectl apply -f https://github.com/flannel-io/flannel/releases/latest/download/kube-flannel.yml
    
    # Save join command for workers
    kubeadm token create --print-join-command > /root/kubeadm_join_cmd.sh
    chmod +x /root/kubeadm_join_cmd.sh
    
    echo "Master node setup complete. Save the join command from /root/kubeadm_join_cmd.sh" | tee -a $LOG_FILE
fi

# Worker node specific configuration
if [ "$NODE_TYPE" = "worker" ]; then
    echo "Configuring worker node..." | tee -a $LOG_FILE
    echo "Please run the join command from the master node's /root/kubeadm_join_cmd.sh" | tee -a $LOG_FILE
fi

# Start kubelet
systemctl start kubelet

echo "Kubernetes setup completed successfully at $(date)" | tee -a $LOG_FILE
echo "Node type: $NODE_TYPE"
echo "Next steps:"
if [ "$NODE_TYPE" = "master" ]; then
    echo "1. Verify cluster: kubectl get nodes"
    echo "2. Share the join command with worker nodes"
else
    echo "1. Obtain and run the join command from master node"
fi

