#!/bin/bash

# Helm Setup Script for Kubernetes Learning
# Run this script with sudo on the master node after k8s_setup.sh

LOG_FILE="/var/log/helm_setup.log"
echo "Starting Helm setup at $(date)" | tee -a $LOG_FILE

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to install Helm
install_helm() {
    if command_exists helm; then
        echo "Helm is already installed." | tee -a $LOG_FILE
    else
        echo "Installing Helm..." | tee -a $LOG_FILE
        curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3
        chmod +x get_helm.sh
        ./get_helm.sh
        rm get_helm.sh
        if command_exists helm; then
            echo "Helm installed successfully." | tee -a $LOG_FILE
        else
            echo "Failed to install Helm." | tee -a $LOG_FILE
            exit 1
        fi
    fi
}

# Function to set up Helm and deploy an app
setup_helm() {
    # Add Helm stable repository
    echo "Adding Helm stable repository..." | tee -a $LOG_FILE
    helm repo add bitnami https://charts.bitnami.com/bitnami
    helm repo update

    # Create a new namespace for the app
    echo "Creating namespace 'my-app'..." | tee -a $LOG_FILE
    kubectl create namespace my-app --dry-run=client -o yaml | kubectl apply -f -

    # Install Nginx using Helm
    echo "Installing Nginx with Helm in 'my-app' namespace..." | tee -a $LOG_FILE
    helm upgrade --install my-nginx bitnami/nginx \
        -n my-app \
        --set replicaCount=2 \
        --set service.type=NodePort \
        --wait \
        || {
            echo "Failed to install Nginx with Helm." | tee -a $LOG_FILE
            exit 1
        }

    echo "Nginx installed successfully. Check pods:" | tee -a $LOG_FILE
    kubectl get pods -n my-app
    echo "Access Nginx at <worker-ip>:<node-port> (use 'kubectl get svc -n my-app' to find the port)" | tee -a $LOG_FILE

    # Demonstrate Helm list and status
    echo "Listing Helm releases:" | tee -a $LOG_FILE
    helm list -n my-app
    echo "Showing Helm release status:" | tee -a $LOG_FILE
    helm status my-nginx -n my-app
}

# Main logic
if [ ! -f /root/.kube/config ]; then
    echo "Kubernetes cluster not set up. Run k8s_setup.sh first." | tee -a $LOG_FILE
    exit 1
fi

install_helm
setup_helm

echo "Helm setup completed successfully at $(date)" | tee -a $LOG_FILE
echo "Next steps to learn Helm:"
echo "1. Upgrade Nginx: helm upgrade my-nginx bitnami/nginx -n my-app --set replicaCount=3"
echo "2. Rollback: helm rollback my-nginx 1 -n my-app"
echo "3. Uninstall: helm uninstall my-nginx -n my-app"
echo "4. Explore custom charts in helm-charts/"
