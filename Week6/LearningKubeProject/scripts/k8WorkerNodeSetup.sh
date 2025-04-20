#!/bin/bash

# Kubernetes Worker Node Setup Script for Amazon Linux 2023
# Run this script with sudo privileges on the worker node

# Exit on any error
set -e

# Log file for debugging
LOG_FILE="/var/log/k8s_worker_setup.log"
echo "Starting Kubernetes worker node setup at $(date)" | tee -a $LOG_FILE

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

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

yum install -y kubelet kubeadm
systemctl enable kubelet
systemctl start kubelet

echo "Worker node setup completed successfully at $(date)" | tee -a $LOG_FILE
echo "Next steps:"
echo "1. Obtain the 'kubeadm join' command from the master node's /root/kubeadm_join_cmd.sh"
echo "2. Run the 'kubeadm join' command on this worker node with sudo"
echo "3. Verify on the master node with: kubectl get nodes"

