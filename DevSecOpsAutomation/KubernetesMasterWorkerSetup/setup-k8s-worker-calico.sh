#!/bin/bash

# Kubernetes Worker Node Setup Script for Amazon Linux 2023
# Usage: sudo ./worker-setup.sh [--join "<kubeadm join command>"]

set -euo pipefail

LOG_FILE="/var/log/k8s_worker_setup.log"
echo "Starting Kubernetes worker setup at $(date)" | tee -a $LOG_FILE

# Optional: kubeadm join command as argument
JOIN_COMMAND=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --join)
            shift
            JOIN_COMMAND="$1"
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
    shift
done

echo "[INFO] Updating system..." | tee -a $LOG_FILE
yum update -y

echo "[INFO] Installing containerd..." | tee -a $LOG_FILE
yum install -y containerd
systemctl enable --now containerd

mkdir -p /etc/containerd
containerd config default > /etc/containerd/config.toml
sed -i 's/SystemdCgroup = false/SystemdCgroup = true/' /etc/containerd/config.toml
systemctl restart containerd

# Disable SELinux
setenforce 0 || true
sed -i 's/^SELINUX=enforcing/SELINUX=disabled/' /etc/selinux/config

# Disable swap
swapoff -a
sed -i '/swap/d' /etc/fstab

# Load kernel modules
modprobe br_netfilter
echo 'br_netfilter' > /etc/modules-load.d/br_netfilter.conf

# IP forwarding
cat <<EOF > /etc/sysctl.d/99-kubernetes.conf
net.ipv4.ip_forward = 1
net.bridge.bridge-nf-call-iptables = 1
net.bridge.bridge-nf-call-ip6tables = 1
EOF
sysctl --system

# Install Kubernetes components
cat <<EOF > /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://pkgs.k8s.io/core:/stable:/v1.28/rpm/
enabled=1
gpgcheck=1
gpgkey=https://pkgs.k8s.io/core:/stable:/v1.28/rpm/repodata/repomd.xml.key
EOF

yum install -y kubelet kubeadm kubectl
systemctl enable --now kubelet

echo "[INFO] Kubernetes worker node dependencies installed." | tee -a $LOG_FILE

# Join the cluster if join command is provided
if [[ -n "$JOIN_COMMAND" ]]; then
    echo "[INFO] Joining cluster..." | tee -a $LOG_FILE
    eval "$JOIN_COMMAND" | tee -a $LOG_FILE
    echo "[INFO] Successfully joined the cluster."
else
    echo "[WARNING] No kubeadm join command provided."
    echo "To join this node to the cluster, run the join command provided by the master node:"
    echo "Example: kubeadm join <master-ip>:6443 --token <token> --discovery-token-ca-cert-hash sha256:<hash>"
fi

echo "[INFO] Worker node setup complete at $(date)" | tee -a $LOG_FILE

