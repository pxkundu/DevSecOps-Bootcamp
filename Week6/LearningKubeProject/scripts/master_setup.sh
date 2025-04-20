#!/bin/bash
set -e
LOG_FILE="/var/log/k8s_setup.log"
echo "Starting master setup at $(date)" | tee -a $LOG_FILE

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

yum install -y kubelet kubeadm kubectl
systemctl enable kubelet && systemctl start kubelet

kubeadm init --pod-network-cidr=10.244.0.0/16 --ignore-preflight-errors=FileExisting-tc,Hostname
mkdir -p /root/.kube
cp -i /etc/kubernetes/admin.conf /root/.kube/config
chown root:root /root/.kube/config

kubectl apply -f https://github.com/flannel-io/flannel/releases/latest/download/kube-flannel.yml
kubeadm token create --print-join-command > /root/kubeadm_join_cmd.sh
chmod +x /root/kubeadm_join_cmd.sh

echo "Master setup complete. Use /root/kubeadm_join_cmd.sh to join workers." | tee -a $LOG_FILE
