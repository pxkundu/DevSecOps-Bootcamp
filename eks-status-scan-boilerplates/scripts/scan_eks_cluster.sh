#!/bin/bash

# Script to scan an EKS cluster and generate a status report for DevSecOps

# Function to check prerequisites
check_prerequisites() {
  echo "Checking prerequisites..."
  command -v aws >/dev/null 2>&1 || { echo "Error: AWS CLI not installed."; exit 1; }
  command -v kubectl >/dev/null 2>&1 || { echo "Error: kubectl not installed."; exit 1; }
  command -v jq >/dev/null 2>&1 || { echo "Error: jq not installed."; exit 1; }
  aws sts get-caller-identity >/dev/null 2>&1 || { echo "Error: AWS credentials not configured."; exit 1; }
}

# Function to get input or environment variable
get_input() {
  local prompt=$1
  if [ -n "${!prompt}" ]; then
    echo "${!prompt}"
  else
    read -p "Enter $prompt: " value
    echo "$value"
  fi
}

# Function to write Markdown report
write_report() {
  local section=$1
  local content=$2
  echo "$content" >> "$REPORT_FILE"
}

# Initialize variables
ROOT_DIR="eks-status-scan-boilerplates"
REPORT_FILE="$ROOT_DIR/reports/eks_cluster_status_report.md"
ISSUES=()
RECOMMENDATIONS=()

# Check prerequisites
check_prerequisites

# Get runtime inputs
EKS_CLUSTER_NAME=$(get_input EKS_CLUSTER_NAME)
AWS_REGION=$(get_input AWS_REGION)
SNS_TOPIC_ARN=$(get_input SNS_TOPIC_ARN)

# Configure kubectl
echo "Configuring kubectl..."
aws eks update-kubeconfig --region "$AWS_REGION" --name "$EKS_CLUSTER_NAME" >/dev/null 2>&1 || {
  echo "Error: Failed to configure kubectl for cluster $EKS_CLUSTER_NAME."
  exit 1
}

# Create report directory
mkdir -p "$ROOT_DIR/reports" || { echo "Error: Failed to create reports directory."; exit 1; }

# Initialize report
echo "Generating report at $REPORT_FILE..."
cat << 'REPORT' > "$REPORT_FILE"
# EKS Cluster Status Report

**Generated on**: $(date -u '+%Y-%m-%d %H:%M:%S UTC')

**Cluster Name**: $EKS_CLUSTER_NAME

**Region**: $AWS_REGION

## Cluster Overview
| Attribute | Value | Status | Notes |
|-----------|-------|--------|-------|
REPORT

# Cluster Overview
echo "Scanning cluster overview..."
CLUSTER_INFO=$(aws eks describe-cluster --region "$AWS_REGION" --name "$EKS_CLUSTER_NAME" --query 'cluster' 2>/dev/null)
if [ -z "$CLUSTER_INFO" ]; then
  echo "Error: Failed to retrieve cluster info for $EKS_CLUSTER_NAME."
  exit 1
fi

VERSION=$(echo "$CLUSTER_INFO" | jq -r '.version')
ENDPOINT_PUBLIC=$(echo "$CLUSTER_INFO" | jq -r '.resourcesVpcConfig.endpointPublicAccess')
AUTH_MODE=$(echo "$CLUSTER_INFO" | jq -r '.accessConfig.authenticationMode')
STATUS=$(echo "$CLUSTER_INFO" | jq -r '.status')

# Check for issues
if [ "$ENDPOINT_PUBLIC" = "true" ]; then
  ISSUES+=("Public endpoint enabled for cluster $EKS_CLUSTER_NAME.")
  RECOMMENDATIONS+=("Disable public endpoint or restrict access using security groups.")
fi
if [ "$AUTH_MODE" != "API_AND_CONFIG_MAP" ]; then
  ISSUES+=("Insecure authentication mode ($AUTH_MODE) for cluster $EKS_CLUSTER_NAME.")
  RECOMMENDATIONS+=("Use API_AND_CONFIG_MAP for secure authentication.")
fi
if [ "$STATUS" != "ACTIVE" ]; then
  ISSUES+=("Cluster status is $STATUS.")
  RECOMMENDATIONS+=("Investigate and resolve cluster status issues.")
fi

write_report "Cluster Overview" "| Version | $VERSION | $([ "$VERSION" \< "1.24" ] && echo "Outdated" || echo "OK") | Upgrade if outdated |\n| Endpoint Public Access | $ENDPOINT_PUBLIC | $([ "$ENDPOINT_PUBLIC" = "true" ] && echo "Warning" || echo "OK") | Disable if not needed |\n| Authentication Mode | $AUTH_MODE | $([ "$AUTH_MODE" = "API_AND_CONFIG_MAP" ] && echo "OK" || echo "Warning") | Use API_AND_CONFIG_MAP |\n| Status | $STATUS | $([ "$STATUS" = "ACTIVE" ] && echo "OK" || echo "Critical") | Ensure cluster is ACTIVE |"

# Node Status
echo "Scanning nodes..."
NODES=$(kubectl get nodes -o json)
NODE_COUNT=$(echo "$NODES" | jq '.items | length')
NODE_TYPES=$(echo "$NODES" | jq -r '.items[].metadata.labels."beta.kubernetes.io/instance-type" | select(.!=null)' | sort | uniq | paste -sd "," -)
NODE_ISSUES=$(echo "$NODES" | jq -r '.items[] | select(.status.conditions[] | select(.type=="Ready" and .status!="True")) | .metadata.name')

write_report "Node Status" "## Node Status\n| Metric | Value | Status | Notes |\n|--------|-------|--------|-------|\n| Node Count | $NODE_COUNT | $([ "$NODE_COUNT" -gt 0 ] && echo "OK" || echo "Critical") | Ensure sufficient nodes |\n| Instance Types | $NODE_TYPES | OK | Verify sizing |\n| Unhealthy Nodes | $([ -n "$NODE_ISSUES" ] && echo "$NODE_ISSUES" || echo "None") | $([ -n "$NODE_ISSUES" ] && echo "Warning" || echo "OK") | Investigate unhealthy nodes |"

if [ -n "$NODE_ISSUES" ]; then
  ISSUES+=("Unhealthy nodes detected: $NODE_ISSUES.")
  RECOMMENDATIONS+=("Check node conditions and logs for issues.")
fi

# Pod Status
echo "Scanning pods..."
PODS=$(kubectl get pods --all-namespaces -o json)
POD_COUNT=$(echo "$PODS" | jq '.items | length')
NAMESPACES=$(echo "$PODS" | jq -r '.items[].metadata.namespace' | sort | uniq | paste -sd "," -)
FAILED_PODS=$(echo "$PODS" | jq -r '.items[] | select(.status.phase=="Failed" or .status.phase=="CrashLoopBackOff") | .metadata.namespace + "/" + .metadata.name')

write_report "Pod Status" "## Pod Status\n| Metric | Value | Status | Notes |\n|--------|-------|--------|-------|\n| Pod Count | $POD_COUNT | $([ "$POD_COUNT" -gt 0 ] && echo "OK" || echo "Critical") | Ensure pods are running |\n| Namespaces | $NAMESPACES | OK | Verify namespace usage |\n| Failed Pods | $([ -n "$FAILED_PODS" ] && echo "$FAILED_PODS" || echo "None") | $([ -n "$FAILED_PODS" ] && echo "Critical" || echo "OK") | Investigate failed pods |"

if [ -n "$FAILED_PODS" ]; then
  ISSUES+=("Failed pods detected: $FAILED_PODS.")
  RECOMMENDATIONS+=("Check pod logs and events for errors.")
fi

# Networking
echo "Scanning networking..."
VPC_ID=$(echo "$CLUSTER_INFO" | jq -r '.resourcesVpcConfig.vpcId')
SUBNETS=$(echo "$CLUSTER_INFO" | jq -r '.resourcesVpcConfig.subnetIds[]' | paste -sd "," -)
SECURITY_GROUPS=$(echo "$CLUSTER_INFO" | jq -r '.resourcesVpcConfig.securityGroupIds[]' | paste -sd "," -)

write_report "Networking" "## Networking\n| Metric | Value | Status | Notes |\n|--------|-------|--------|-------|\n| VPC ID | $VPC_ID | OK | Verify VPC configuration |\n| Subnets | $SUBNETS | OK | Ensure sufficient IPs |\n| Security Groups | $SECURITY_GROUPS | OK | Restrict inbound rules |"

# Security
echo "Scanning security..."
IAM_ROLE=$(echo "$CLUSTER_INFO" | jq -r '.identity.oidc.issuer' | grep -o 'oidc-provider/.*' || echo "Unknown")
RBAC_ROLES=$(kubectl get clusterroles -o json | jq '.items | length')
NETWORK_POLICIES=$(kubectl get networkpolicies --all-namespaces -o json | jq '.items | length')

write_report "Security" "## Security\n| Metric | Value | Status | Notes |\n|--------|-------|--------|-------|\n| OIDC Provider | $IAM_ROLE | OK | Ensure secure IAM roles |\n| RBAC Roles | $RBAC_ROLES | $([ "$RBAC_ROLES" -gt 50 ] && echo "Warning" || echo "OK") | Limit overly permissive roles |\n| Network Policies | $NETWORK_POLICIES | $([ "$NETWORK_POLICIES" -eq 0 ] && echo "Critical" || echo "OK") | Implement network policies |"

if [ "$NETWORK_POLICIES" -eq 0 ]; then
  ISSUES+=("No network policies detected.")
  RECOMMENDATIONS+=("Implement network policies to restrict pod communication.")
fi
if [ "$RBAC_ROLES" -gt 50 ]; then
  ISSUES+=("High number of RBAC roles ($RBAC_ROLES).")
  RECOMMENDATIONS+=("Audit RBAC roles for least privilege.")
fi

# Logging and Monitoring
echo "Scanning logging and monitoring..."
LOGGING=$(echo "$CLUSTER_INFO" | jq -r '.logging.clusterLogging[].types[]' | paste -sd "," - || echo "Disabled")
CLOUDWATCH=$(aws cloudwatch describe-alarms --region "$AWS_REGION" --query 'MetricAlarms[?Namespace=="AWS/EKS"].AlarmName' --output text 2>/dev/null || echo "None")

write_report "Logging and Monitoring" "## Logging and Monitoring\n| Metric | Value | Status | Notes |\n|--------|-------|--------|-------|\n| Cluster Logging | ${LOGGING:-Disabled} | $([ -n "$LOGGING" ] && echo "OK" || echo "Warning") | Enable control plane logging |\n| CloudWatch Alarms | ${CLOUDWATCH:-None} | $([ -n "$CLOUDWATCH" ] && echo "OK" || echo "Warning") | Set up alarms for metrics |"

if [ -z "$LOGGING" ]; then
  ISSUES+=("Cluster logging is disabled.")
  RECOMMENDATIONS+=("Enable control plane logging to CloudWatch.")
fi

# Critical Issues and Recommendations
write_report "Critical Issues" "## Critical Issues\n$(for issue in "${ISSUES[@]}"; do echo "- $issue"; done)"
write_report "Recommendations" "## Recommendations\n$(for rec in "${RECOMMENDATIONS[@]}"; do echo "- $rec"; done)"

# Send SNS notification if issues found
if [ ${#ISSUES[@]} -gt 0 ]; then
  echo "Sending SNS notification..."
  aws sns publish --topic-arn "$SNS_TOPIC_ARN" --message "$(printf '%s\n' "${ISSUES[@]}")" --subject "EKS Cluster Issues: $EKS_CLUSTER_NAME" --region "$AWS_REGION" >/dev/null 2>&1 || {
    echo "Warning: Failed to send SNS notification."
  }
fi

echo "EKS cluster status scan complete. Report generated at $REPORT_FILE."
exit 0
