#!/bin/bash

# There is a simple BUG is the code!!
# IF YOU WANT TO USE IT, FIX IT AND USE IT!!!

# Dynamic Kubernetes Setup Script for Amazon Linux 2023 with Master Setup Check and Reset Option
# Run this script with sudo privileges on both master and worker nodes

# Log file for debugging
LOG_FILE="/var/log/k8s_setup.log"
echo "Starting Kubernetes setup at $(date)" | tee -a $LOG_FILE

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check if master control plane is already set up
check_master_setup() {
    echo "Checking if master control plane is already set up..." | tee -a $LOG_FILE
    
    # Check if kubelet is running
    if ! systemctl is-active kubelet >/dev/null 2>&1; then
        echo "Kubelet is not running." | tee -a $LOG_FILE
        return 1
    fi
    
    # Check for static pod manifests
    if [ ! -f /etc/kubernetes/manifests/kube-apiserver.yaml ] || \
       [ ! -f /etc/kubernetes/manifests/kube-controller-manager.yaml ] || \
       [ ! -f /etc/kubernetes/manifests/kube-scheduler.yaml ] || \
       [ ! -f /etc/kubernetes/manifests/etcd.yaml ]; then
        echo "One or more static pod manifests are missing." | tee -a $LOG_FILE
        return 1
    fi
    
    # Check if control plane pods are running (skip if kubectl not installed yet)
    if command_exists kubectl; then
        if ! kubectl get pods -n kube-system --request-timeout=10s >/dev/null 2>&1; then
            echo "Cannot connect to the cluster with kubectl." | tee -a $LOG_FILE
            return 1
        fi
        if ! kubectl get pods -n kube-system | grep -q "kube-apiserver" || \
           ! kubectl get pods -n kube-system | grep -q "kube-controller-manager" || \
           ! kubectl get pods -n kube-system | grep -q "kube-scheduler" || \
           ! kubectl get pods -n kube-system | grep -q "etcd"; then
            echo "One or more control plane pods are not running." | tee -a $LOG_FILE
            return 1
        fi
    else
        echo "kubectl not found, cannot verify pod status." | tee -a $LOG_FILE
        return 1
    fi
    
    # Check if kubeconfig exists
    if [ ! -f /root/.kube/config ]; then
        echo "Kubeconfig file not found." | tee -a $LOG_FILE
        return 1
    fi
    
    # Check if Flannel namespace exists and pods are running
    if ! kubectl get ns kube-flannel >/dev/null 2>&1 || \
       ! kubectl get pods -n kube-flannel | grep -q "kube-flannel"; then
        echo "Flannel CNI is not installed or namespace kube-flannel is missing." | tee -a $LOG_FILE
        return 1
    fi
    
    echo "Master control plane is fully set up." | tee -a $LOG_FILE
    return 0
}

# Function to reset the cluster
reset_cluster() {
    echo "Resetting Kubernetes cluster..." | tee -a $LOG_FILE
    kubeadm reset -f | tee -a $LOG_FILE
    rm -rf /etc/kubernetes /root/.kube /root/kubeadm_join_cmd.sh /var/lib/etcd
    systemctl stop kubelet
    systemctl stop containerd
    ip link delete cni0 2>/dev/null || true
    ip link delete flannel.1 2>/dev/null || true
    echo "Cluster reset complete. Proceeding with setup..." | tee -a $LOG_FILE
}

# Function to prompt user for reset
prompt_reset() {
    echo "The master control plane is already fully configured." | tee -a $LOG_FILE
    echo "Would you like to reset the cluster and set it up again? (y/N)"
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        reset_cluster
        return 0  # Indicate setup should proceed
    else
        echo "Exiting without changes." | tee -a $LOG_FILE
        exit 0
    fi
}

# Function to identify if this is master or worker node
NODE_TYPE=${1:-"master"}  # Default to master if no argument provided

# Main setup logic
setup_kubernetes() {
    set -e  # Enable error checking within setup
    # Update system and install basic utilities
    echo "Updating system..." | tee -a $LOG_FILE
    yum update -y
    yum install -y curl wget vim git

    # Install containerd as container runtime
    echo "Installing containerd..." | tee -a $LOG_FILE
    if ! rpm -q containerd >/dev/null 2>&1; then
        yum install -y containerd
    fi
    systemctl enable containerd
    systemctl start containerd

    # Configure containerd
    mkdir -p /etc/containerd
    if [ ! -f /etc/containerd/config.toml ] || ! grep -q "SystemdCgroup = true" /etc/containerd/config.toml; then
        containerd config default > /etc/containerd/config.toml
        sed -i 's/SystemdCgroup = false/SystemdCgroup = true/' /etc/containerd/config.toml
        systemctl restart containerd
    fi

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

    if ! rpm -q kubelet kubeadm kubectl >/dev/null 2>&1; then
        yum install -y kubelet kubeadm kubectl
    fi
    systemctl enable kubelet

    # Master node specific configuration
    if [ "$NODE_TYPE" = "master" ]; then
        echo "Configuring master node..." | tee -a $LOG_FILE
        
        # Initialize the Kubernetes cluster with ignore flags for warnings
        kubeadm init --pod-network-cidr=10.244.0.0/16 --ignore-preflight-errors=FileExisting-tc,Hostname | tee -a $LOG_FILE
        
        # Set up kubeconfig for root user
        mkdir -p /root/.kube
        cp -f /etc/kubernetes/admin.conf /root/.kube/config
        chown root:root /root/.kube/config
        
        # Create kube-flannel namespace and install Flannel
        echo "Creating kube-flannel namespace and installing Flannel CNI..." | tee -a $LOG_FILE
        kubectl create namespace kube-flannel --dry-run=client -o yaml | kubectl apply -f -
        curl -sSL https://github.com/flannel-io/flannel/releases/latest/download/kube-flannel.yml | \
            sed 's/kube-system/kube-flannel/g' | kubectl apply -f -
        
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

    # Start kubelet if not already running
    if ! systemctl is-active kubelet >/dev/null 2>&1; then
        systemctl start kubelet
    fi
}

# Main logic
if [ "$NODE_TYPE" = "master" ]; then
    if check_master_setup; then
        prompt_reset
        # If user chooses reset, prompt_reset returns 0 and we proceed
        setup_kubernetes
    else
        # If not fully configured, proceed with setup
        setup_kubernetes
    fi
else
    # For worker nodes, always proceed with setup
    setup_kubernetes
fi

echo "Kubernetes setup completed successfully at $(date)" | tee -a $LOG_FILE
echo "Node type: $NODE_TYPE"
echo "Next steps:"
if [ "$NODE_TYPE" = "master" ]; then
    echo "1. Verify cluster: kubectl get nodes"
    echo "2. Share the join command with worker nodes"
else
    echo "1. Obtain and run the join command from master node"
fi
