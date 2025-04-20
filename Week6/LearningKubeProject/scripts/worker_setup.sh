#!/bin/bash
set -e
LOG_FILE="/var/log/k8s_worker_setup.log"
echo "Starting worker setup at $(date)" | tee -a $LOG_FILE

yum update -y && yum install -y curl wget containerd
systemctl enable containerd && systemctl start containerd
mkdir -p /etc/containerd
containerd config default > /etc/containerd/config.toml
sed -i 's/SystemdCgroup = false/SystemdCgroup = true/' /etc/containerd/config.toml
systemctl restart containerd

setenforce 0
sed -i 's/^SELINUX=enforcing/SELINUX=disabled/' /etc/selinux/config
swapoff -a
sed -i '/swap/d' /etc/fstab

modprobe br_netfilter
echo 'br_netfilter' > /etc/modules-load.d/br_netfilter.conf
sysctl -w net.ipv4.ip_forward=1
echo 'net.ipv4.ip_forward = 1' > /etc/sysctl.d/99-kubernetes.conf
sysctl --system

cat <<EOT > /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://pkgs.k8s.io/core:/stable:/v1.28/rpm/
enabled=1
gpgcheck=1
gpgkey=https://pkgs.k8s.io/core:/stable:/v1.28/rpm/repodata/repomd.xml.key
EOT

yum install -y kubelet kubeadm
systemctl enable kubelet && systemctl start kubelet

echo "Worker setup complete. Run the 'kubeadm join' command from the master." | tee -a $LOG_FILE
