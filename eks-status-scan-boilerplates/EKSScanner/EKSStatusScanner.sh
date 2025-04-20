#!/bin/bash

# EKS Cluster Status and DevSecOps Scan Script
# This script gathers information about an EKS cluster's status, health, and
# provides some DevSecOps relevant insights by running various kubectl and aws commands.
# It generates a report file in the same directory.

# --- Configuration ---
REPORT_FILE="eks_cluster_report_$(date +%Y%m%d_%H%M%S).txt"

# --- Functions ---

# Function to check if a command exists
command_exists() {
  command -v "$1" >/dev/null 2>&1
}

# Function to prompt for input
get_user_input() {
  local prompt_text="$1"
  local var_name="$2"
  read -r -p "$prompt_text" "$var_name"
}

# Function to check for essential tools
check_dependencies() {
  echo "--- Checking Dependencies ---" | tee -a "$REPORT_FILE"
  local missing_tools=()
  if ! command_exists kubectl; then
    missing_tools+=("kubectl")
  fi
  if ! command_exists aws; then
    missing_tools+=("aws")
  fi

  if [ ${#missing_tools[@]} -gt 0 ]; then
    echo "Error: The following required tools are not installed: ${missing_tools[*]}" | tee -a "$REPORT_FILE"
    echo "Please install them and run the script again." | tee -a "$REPORT_FILE"
    exit 1
  fi
  echo "All required dependencies (kubectl, aws) are installed." | tee -a "$REPORT_FILE"
  echo "" | tee -a "$REPORT_FILE"
}

# Function to configure kubectl
configure_kubectl() {
  echo "--- Configuring kubectl ---" | tee -a "$REPORT_FILE"
  aws eks update-kubeconfig --region "$AWS_REGION" --name "$EKS_CLUSTER_NAME"
  if [ $? -ne 0 ]; then
    echo "Error: Could not configure kubectl for cluster $EKS_CLUSTER_NAME in region $AWS_REGION." | tee -a "$REPORT_FILE"
    echo "Please ensure your AWS credentials are configured correctly and you have access to the cluster." | tee -a "$REPORT_FILE"
    exit 1
  fi
  echo "kubectl configured for $EKS_CLUSTER_NAME." | tee -a "$REPORT_FILE"
  echo "" | tee -a "$REPORT_FILE"
}

# Function to get cluster general information
get_cluster_info() {
  echo "--- EKS Cluster General Information ---" | tee -a "$REPORT_FILE"
  aws eks describe-cluster --name "$EKS_CLUSTER_NAME" --region "$AWS_REGION" --query "cluster.{Name:name, Version:version, Status:status, Arn:arn, Endpoint:resourcesVpcConfig.endpointPublicAccess, PrivateEndpoint:resourcesVpcConfig.endpointPrivateAccess, PublicAccessCIDRs:resourcesVpcConfig.publicAccessCidrs}" --output text | tee -a "$REPORT_FILE"
  echo "" | tee -a "$REPORT_FILE"
  echo "Interpretation:" | tee -a "$REPORT_FILE"
  echo "- Name, Version, Status, Arn: Basic identification and current state of the cluster." | tee -a "$REPORT_FILE"
  echo "- Endpoint, PrivateEndpoint, PublicAccessCIDRs: Crucial for understanding network access to the Kubernetes API server. Public access should be restricted to known CIDRs or disabled if not needed for security." | tee -a "$REPORT_FILE"
  echo "" | tee -a "$REPORT_FILE"
}

# Function to get node information
get_node_info() {
  echo "--- Node Status ---" | tee -a "$REPORT_FILE"
  kubectl get nodes -o wide | tee -a "$REPORT_FILE"
  echo "" | tee -a "$REPORT_FILE"
  echo "Interpretation:" | tee -a "$REPORT_FILE"
  echo "- NAME: The name of the node." | tee -a "$REPORT_FILE"
  echo "- STATUS: Should be 'Ready'. Any other status (e.g., 'NotReady', 'MemoryPressure', 'DiskPressure') indicates potential issues." | tee -a "$REPORT_FILE"
  echo "- ROLES: Indicates the role of the node (e.g., control-plane)." | tee -a "$REPORT_FILE"
  echo "- AGE: How long the node has been in its current state." | tee -a "$REPORT_FILE"
  echo "- VERSION: The Kubernetes version running on the node." | tee -a "$REPORT_FILE"
  echo "- INTERNAL-IP, EXTERNAL-IP: IP addresses of the node." | tee -a "$REPORT_FILE"
  echo "- OS-IMAGE, KERNEL-VERSION, CONTAINER-RUNTIME: Details about the node's environment." | tee -a "$REPORT_FILE"
  echo "" | tee -a "$REPORT_FILE"

  echo "--- Node Resource Utilization (kubectl top nodes) ---" | tee -a "$REPORT_FILE"
  if command_exists kubectl-top; then
    kubectl top nodes | tee -a "$REPORT_FILE"
  else
    echo "kubectl top plugin not found. Skipping node resource utilization." | tee -a "$REPORT_FILE"
    echo "Install kubectl-top for resource usage information." | tee -a "$REPORT_FILE"
  fi
  echo "" | tee -a "$REPORT_FILE"
  echo "Interpretation (if available):" | tee -a "$REPORT_FILE"
  echo "- CPU(cores), CPU(%), MEMORY(bytes), MEMORY(%): Shows current resource usage on each node. High utilization might indicate resource bottlenecks." | tee -a "$REPORT_FILE"
  echo "" | tee -a "$REPORT_FILE"
}

# Function to get pod information, focusing on problematic states
get_pod_info() {
  echo "--- Pod Status (Non-Running or with Restarts) ---" | tee -a "$REPORT_FILE"
  kubectl get pods --all-namespaces -o wide | awk '$4 != "Running" || $3 != "0"' | tee -a "$REPORT_FILE"
  echo "" | tee -a "$REPORT_FILE"
  echo "Interpretation:" | tee -a "$REPORT_FILE"
  echo "- This section shows pods that are not in a 'Running' state or have a non-zero restart count. These indicate potential application or configuration issues." | tee -a "$REPORT_FILE"
  echo "- STATUS: Look for 'Pending', 'Init:Error', 'CrashLoopBackOff', 'Error', 'ImagePullBackOff', etc." | tee -a "$REPORT_FILE"
  echo "- RESTARTS: A high restart count suggests the pod is repeatedly crashing." | tee -a "$REPORT_FILE"
  echo "" | tee -a "$REPORT_FILE"

  echo "--- Pods in kube-system namespace ---" | tee -a "$REPORT_FILE"
  kubectl get pods -n kube-system -o wide | tee -a "$REPORT_FILE"
  echo "" | tee -a "$REPORT_FILE"
  echo "Interpretation:" | tee -a "$REPORT_FILE"
  echo "- This shows the status of core Kubernetes system components. Issues here can indicate fundamental cluster problems." | tee -a "$REPORT_FILE"
  echo "" | tee -a "$REPORT_FILE"
}

# Function to get recent events
get_recent_events() {
  echo "--- Recent Cluster Events (Warnings and Errors) ---" | tee -a "$REPORT_FILE"
  kubectl get events --all-namespaces --field-selector type!=Normal --sort-by='.lastTimestamp' | tail -n 50 | tee -a "$REPORT_FILE"
  echo "" | tee -a "$REPORT_FILE"
  echo "Interpretation:" | tee -a "$REPORT_FILE"
  echo "- This shows recent events that are not of type 'Normal'. Warnings and Errors can highlight issues like failed scheduling, failed volume mounts, or crashing containers." | tee -a "$REPORT_FILE"
  echo "- Look for events related to 'Failed', 'Error', 'Warning'." | tee -a "$REPORT_FILE"
  echo "" | tee -a "$REPORT_FILE"
}

# Function to check for default service account usage (basic security check)
check_default_service_accounts() {
  echo "--- Default Service Account Usage Check (Basic Security) ---" | tee -a "$REPORT_FILE"
  echo "Listing pods running with the 'default' service account where automountServiceAccountToken is not explicitly set to false." | tee -a "$REPORT_FILE"
  kubectl get pods --all-namespaces -o json | jq -c '.items[] | select((.spec.serviceAccountName=="default" or .spec.serviceAccountName==null) and (.spec.automountServiceAccountToken==null or .spec.automountServiceAccountToken==true))' | tee -a "$REPORT_FILE"
  echo "" | tee -a "$REPORT_FILE"
  echo "Interpretation:" | tee -a "$REPORT_FILE"
  echo "- Pods running with the default service account have broader permissions by default than a dedicated service account with least privileges." | tee -a "$REPORT_FILE"
  echo "- It's a security best practice to use dedicated service accounts with minimal required permissions for your applications." | tee -a "$REPORT_FILE"
  echo "- The output lists pods that might be using the default service account without explicitly disabling token automount, which could potentially expose the service account token to the pod." | tee -a "$REPORT_FILE"
  echo "" | tee -a "$REPORT_FILE"
}

# Function to check for privileged containers (basic security check)
check_privileged_containers() {
  echo "--- Privileged Container Check (Basic Security) ---" | tee -a "$REPORT_FILE"
  echo "Listing containers running with privileged mode enabled." | tee -a "$REPORT_FILE"
  kubectl get pods --all-namespaces -o json | jq -c '.items[] | .metadata.namespace as $ns | .metadata.name as $pod | .spec.containers[] | select(.securityContext.privileged==true) | "Namespace: \($ns), Pod: \($pod), Container: \(.name)"' | tee -a "$REPORT_FILE"
  echo "" | tee -a "$REPORT_FILE"
  echo "Interpretation:" | tee -a "$REPORT_FILE"
  echo "- Privileged containers have full root capabilities on the host node and are a significant security risk." | tee -a "$REPORT_FILE"
  echo "- Avoid running containers in privileged mode unless absolutely necessary and with careful consideration." | tee -a "$REPORT_FILE"
  echo "" | tee -a "$REPORT_FILE"
}

# Function to check for pods with hostPath volumes (basic security check)
check_hostpath_volumes() {
  echo "--- hostPath Volume Check (Basic Security) ---" | tee -a "$REPORT_FILE"
  echo "Listing pods using hostPath volumes." | tee -a "$REPORT_FILE"
  kubectl get pods --all-namespaces -o json | jq -c '.items[] | .metadata.namespace as $ns | .metadata.name as $pod | select(.spec.volumes[]?.hostPath != null) | "Namespace: \($ns), Pod: \($pod)"' | tee -a "$REPORT_FILE"
  echo "" | tee -a "$REPORT_FILE"
  echo "Interpretation:" | tee -a "$REPORT_FILE"
  echo "- hostPath volumes mount a file or directory from the host node into a pod." | tee -a "$REPORT_FILE"
  echo "- Misconfiguring hostPath volumes can allow containers to access sensitive files or directories on the host, leading to potential security breaches." | tee -a "$REPORT_FILE"
  echo "- Use more secure alternatives like Persistent Volumes with appropriate storage classes when possible." | tee -a "$REPORT_FILE"
  echo "" | tee -a "$REPORT_FILE"
}

# Function to check for ImagePullPolicy: Always (DevOps/Security consideration)
check_image_pull_policy() {
    echo "--- ImagePullPolicy: Always Check (DevOps/Security Consideration) ---" | tee -a "$REPORT_FILE"
    echo "Listing containers without ImagePullPolicy: Always explicitly set (default is IfNotPresent or Always depending on tag)." | tee -a "$REPORT_FILE"
    echo "It's generally recommended to explicitly set the pull policy." | tee -a "$REPORT_FILE"
    kubectl get pods --all-namespaces -o json | jq -c '.items[] | .metadata.namespace as $ns | .metadata.name as $pod | .spec.containers[] | select(.imagePullPolicy == null) | "Namespace: \($ns), Pod: \($pod), Container: \(.name), Image: \(.image)"' | tee -a "$REPORT_FILE"
    echo "" | tee -a "$REPORT_FILE"
    echo "Interpretation:" | tee -a "$REPORT_FILE"
    echo "- Containers without an explicit ImagePullPolicy might behave differently based on the image tag (e.g., 'latest' often defaults to Always, specific versions to IfNotPresent)." | tee -a "$REPORT_FILE"
    echo "- Explicitly setting ImagePullPolicy to 'Always' ensures that the image is always pulled, which is important for getting the latest version during rolling updates or to prevent using a potentially compromised cached image." | tee -a "$REPORT_FILE"
    echo "- For production, using specific image tags instead of 'latest' is recommended for better control and reproducibility." | tee -a "$REPORT_FILE"
    echo "" | tee -a "$REPORT_FILE"
}


# --- Main Script ---

echo "EKS Cluster Status and DevSecOps Scan Script"
echo "This script will gather information about your EKS cluster and generate a report."
echo ""

# Get user input
get_user_input "Enter EKS Cluster Name: " EKS_CLUSTER_NAME
get_user_input "Enter AWS Region: " AWS_REGION

echo ""
echo "Generating report: $REPORT_FILE"
echo "" > "$REPORT_FILE" # Clear or create the report file

# Run checks
check_dependencies
configure_kubectl
get_cluster_info
get_node_info
get_pod_info
get_recent_events
check_default_service_accounts
check_privileged_containers
check_hostpath_volumes
check_image_pull_policy

echo "--- Scan Complete ---" | tee -a "$REPORT_FILE"
echo "Report saved to $REPORT_FILE"
echo "Please review the report for cluster status and potential DevSecOps related issues."
