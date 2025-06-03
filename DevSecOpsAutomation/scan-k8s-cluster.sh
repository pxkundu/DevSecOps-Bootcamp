#!/bin/bash

# scan-k8s-cluster.sh
# Scans a Kubernetes cluster for resources and reports problems in a concise format
# Logs errors and debug info to scan-k8s-cluster.log

set -o pipefail
LOG_FILE="scan-k8s-cluster.log"
ERROR_LOG=""
PROBLEM_LOG=""
JQ_AVAILABLE=true

# Redirect debug logs to file
exec 3>&1
exec > >(tee -a "$LOG_FILE")
exec 2>&1

log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1" >&3
}

add_problem() {
    local severity="$1"
    local message="$2"
    PROBLEM_LOG+="$severity: $message\n"
}

log "Checking prerequisites..."
command -v kubectl >/dev/null 2>&1 || { log "ERROR: kubectl is required"; ERROR_LOG="kubectl not found"; exit 1; }
kubectl cluster-info >/dev/null 2>&1 || { log "ERROR: kubectl cannot connect to cluster"; ERROR_LOG="kubectl cluster access failed"; exit 1; }
command -v jq >/dev/null 2>&1 || { log "Warning: jq not found, some checks skipped"; JQ_AVAILABLE=false; }

log "=== Kubernetes Cluster Scan ==="

# Cluster Information
log "Cluster Information:"
if $JQ_AVAILABLE; then
    CLUSTER_INFO=$(timeout 60s kubectl version -o json 2>/dev/null || echo "{}")
    SERVER_VERSION=$(echo "$CLUSTER_INFO" | jq -r '.serverVersion.gitVersion' 2>/dev/null || echo "Unknown")
    CLUSTER_NAME=$(kubectl config view -o jsonpath='{.clusters[0].name}' 2>/dev/null || echo "Unknown")
else
    SERVER_VERSION=$(timeout 60s kubectl version --short 2>/dev/null | grep Server | awk '{print $3}' || echo "Unknown")
    CLUSTER_NAME="Unknown (install jq for cluster name)"
fi
printf "%-20s %-20s\n" "Cluster Name:" "$CLUSTER_NAME"
printf "%-20s %-20s\n" "Version:" "$SERVER_VERSION"
echo ""

# Nodes
log "Nodes:"
NODES=$(timeout 60s kubectl get nodes -o wide --no-headers 2>/dev/null || echo "")
if [ -z "$NODES" ]; then
    add_problem "Critical" "Failed to retrieve nodes. Check: kubectl get nodes"
    echo "No nodes retrieved."
else
    printf "%-30s %-10s %-20s %-10s %-15s\n" "Name" "Status" "Roles" "Age" "Version"
    echo "$NODES" | while read -r name status roles age version internal_ip external_ip; do
        printf "%-30s %-10s %-20s %-10s %-15s\n" "$name" "$status" "$roles" "$age" "$version"
    done
    NODE_COUNT=$(echo "$NODES" | wc -l)
    echo "Total Nodes: $NODE_COUNT"
    echo ""
    NOT_READY_NODES=$(echo "$NODES" | grep -v Ready || true)
    if [ -n "$NOT_READY_NODES" ]; then
        add_problem "Critical" "Nodes in NotReady state:\n$NOT_READY_NODES\nCheck: kubectl describe node <node-name>"
    fi
fi

# Namespaces
log "Namespaces:"
NAMESPACES=$(timeout 60s kubectl get namespaces -o name 2>/dev/null | sed 's/namespace\///' || echo "")
if [ -z "$NAMESPACES" ]; then
    add_problem "Critical" "Failed to retrieve namespaces. Check: kubectl get namespaces"
    echo "No namespaces retrieved."
else
    printf "%-30s\n" "Name"
    echo "$NAMESPACES" | while read -r ns; do
        printf "%-30s\n" "$ns"
    done
    NAMESPACE_COUNT=$(echo "$NAMESPACES" | wc -l)
    echo "Total Namespaces: $NAMESPACE_COUNT"
    echo ""
    if ! echo "$NAMESPACES" | grep -q "kube-system"; then
        add_problem "Critical" "kube-system namespace missing. Cluster may be misconfigured."
    fi
fi

# Pods
log "Pods:"
PODS=$(timeout 60s kubectl get pods -A -o wide --no-headers 2>/dev/null || echo "")
if [ -z "$PODS" ]; then
    add_problem "Critical" "Failed to retrieve pods. Check: kubectl get pods -A"
    echo "No pods retrieved."
else
    printf "%-20s %-40s %-10s %-15s %-10s\n" "Namespace" "Name" "Ready" "Status" "Restarts"
    echo "$PODS" | while read -r ns name ready status restarts age ip node; do
        printf "%-20s %-40s %-10s %-15s %-10s\n" "$ns" "$name" "$ready" "$status" "$restarts"
    done
    POD_COUNT=$(echo "$PODS" | wc -l)
    echo "Total Pods: $POD_COUNT"
    echo ""
    CRASHING_PODS=$(echo "$PODS" | grep -E "CrashLoopBackOff|Error|Pending" || true)
    if [ -n "$CRASHING_PODS" ]; then
        add_problem "Critical" "Pods in CrashLoopBackOff, Error, or Pending state:\n$CRASHING_PODS\nCheck: kubectl logs -n <namespace> <pod-name>"
    fi
    HIGH_RESTART_PODS=$(echo "$PODS" | awk '$5 ~ /[0-9]+/ && $5 > 10 {print}' || true)
    if [ -n "$HIGH_RESTART_PODS" ]; then
        add_problem "Warning" "Pods with high restarts (>10):\n$HIGH_RESTART_PODS\nCheck: kubectl logs -n <namespace> <pod-name>"
    fi
fi

# Services
log "Services:"
SERVICES=$(timeout 60s kubectl get services -A -o wide --no-headers 2>/dev/null || echo "")
if [ -z "$SERVICES" ]; then
    add_problem "Critical" "Failed to retrieve services. Check: kubectl get services -A"
    echo "No services retrieved."
else
    printf "%-20s %-30s %-15s %-20s\n" "Namespace" "Name" "Type" "External-IP"
    echo "$SERVICES" | while read -r ns name type cluster_ip external_ip ports age; do
        printf "%-20s %-30s %-15s %-20s\n" "$ns" "$name" "$type" "$external_ip"
    done
    SERVICE_COUNT=$(echo "$SERVICES" | wc -l)
    echo "Total Services: $SERVICE_COUNT"
    echo ""
    PENDING_SERVICES=$(echo "$SERVICES" | grep "<pending>" || true)
    if [ -n "$PENDING_SERVICES" ]; then
        add_problem "Critical" "Services with <pending> external IP (possible ALB issue):\n$PENDING_SERVICES\nCheck: kubectl logs -n kube-system -l app.kubernetes.io/name=aws-load-balancer-controller"
    fi
fi

# Deployments
log "Deployments:"
DEPLOYMENTS=$(timeout 60s kubectl get deployments -A -o wide --no-headers 2>/dev/null || echo "")
if [ -z "$DEPLOYMENTS" ]; then
    add_problem "Warning" "No deployments found or failed to retrieve. Check: kubectl get deployments -A"
    echo "No deployments retrieved."
else
    printf "%-20s %-30s %-10s\n" "Namespace" "Name" "Ready"
    echo "$DEPLOYMENTS" | while read -r ns name ready up_to_date available age; do
        printf "%-20s %-30s %-10s\n" "$ns" "$name" "$ready"
    done
    DEPLOYMENT_COUNT=$(echo "$DEPLOYMENTS" | wc -l)
    echo "Total Deployments: $DEPLOYMENT_COUNT"
    echo ""
    UNREADY_DEPLOYMENTS=$(echo "$DEPLOYMENTS" | awk '$3 !~ /^[0-9]+\/[0-9]+$/ || $3 ~ /0\/[0-9]+/ {print}' || true)
    if [ -n "$UNREADY_DEPLOYMENTS" ]; then
        add_problem "Warning" "Deployments with unready replicas:\n$UNREADY_DEPLOYMENTS\nCheck: kubectl describe deployment -n <namespace> <name>"
    fi
fi

# StatefulSets
log "StatefulSets:"
STATEFULSETS=$(timeout 60s kubectl get statefulsets -A -o wide --no-headers 2>/dev/null || echo "")
if [ -z "$STATEFULSETS" ]; then
    add_problem "Warning" "No statefulsets found or failed to retrieve. Check: kubectl get statefulsets -A"
    echo "No statefulsets retrieved."
else
    printf "%-20s %-30s %-10s\n" "Namespace" "Name" "Ready"
    echo "$STATEFULSETS" | while read -r ns name ready age; do
        printf "%-20s %-30s %-10s\n" "$ns" "$name" "$ready"
    done
    STATEFULSET_COUNT=$(echo "$STATEFULSETS" | wc -l)
    echo "Total StatefulSets: $STATEFULSET_COUNT"
    echo ""
    UNREADY_STATEFULSETS=$(echo "$STATEFULSETS" | awk '$3 !~ /^[0-9]+\/[0-9]+$/ || $3 ~ /0\/[0-9]+/ {print}' || true)
    if [ -n "$UNREADY_STATEFULSETS" ]; then
        add_problem "Warning" "StatefulSets with unready replicas:\n$UNREADY_STATEFULSETS\nCheck: kubectl describe statefulset -n <namespace> <name>"
    fi
fi

# DaemonSets
log "DaemonSets:"
DAEMONSETS=$(timeout 60s kubectl get daemonsets -A -o wide --no-headers 2>/dev/null || echo "")
if [ -z "$DAEMONSETS" ]; then
    add_problem "Warning" "No daemonsets found or failed to retrieve. Check: kubectl get daemonsets -A"
    echo "No daemonsets retrieved."
else
    printf "%-20s %-30s %-10s\n" "Namespace" "Name" "Ready"
    echo "$DAEMONSETS" | while read -r ns name desired current ready up_to_date available age; do
        printf "%-20s %-30s %-10s\n" "$ns" "$name" "$ready"
    done
    DAEMONSET_COUNT=$(echo "$DAEMONSETS" | wc -l)
    echo "Total DaemonSets: $DAEMONSET_COUNT"
    echo ""
    UNREADY_DAEMONSETS=$(echo "$DAEMONSETS" | awk '$5 < $3 || $5 == 0 {print}' || true)
    if [ -n "$UNREADY_DAEMONSETS" ]; then
        add_problem "Warning" "DaemonSets with unready pods:\n$UNREADY_DAEMONSETS\nCheck: kubectl describe daemonset -n <namespace> <name>"
    fi
fi

# Jobs
log "Jobs:"
JOBS=$(timeout 60s kubectl get jobs -A -o wide --no-headers 2>/dev/null || echo "")
if [ -z "$JOBS" ]; then
    add_problem "Warning" "No jobs found or failed to retrieve. Check: kubectl get jobs -A"
    echo "No jobs retrieved."
else
    printf "%-20s %-30s %-15s\n" "Namespace" "Name" "Completions"
    echo "$JOBS" | while read -r ns name completions duration age; do
        printf "%-20s %-30s %-15s\n" "$ns" "$name" "$completions"
    done
    JOB_COUNT=$(echo "$JOBS" | wc -l)
    echo "Total Jobs: $JOB_COUNT"
    echo ""
    FAILED_JOBS=$(echo "$JOBS" | awk '$3 !~ /[0-9]+\/[0-9]+/ || $3 ~ /0\/[0-9]+/ {print}' || true)
    if [ -n "$FAILED_JOBS" ]; then
        add_problem "Warning" "Jobs that failed or didn’t complete:\n$FAILED_JOBS\nCheck: kubectl describe job -n <namespace> <name>"
    fi
fi

# CronJobs
log "CronJobs:"
CRONJOBS=$(timeout 60s kubectl get cronjobs -A -o wide --no-headers 2>/dev/null || echo "")
if [ -z "$CRONJOBS" ]; then
    add_problem "Warning" "No cronjobs found or failed to retrieve. Check: kubectl get cronjobs -A"
    echo "No cronjobs retrieved."
else
    printf "%-20s %-30s %-20s\n" "Namespace" "Name" "Schedule"
    echo "$CRONJOBS" | while read -r ns name schedule suspend active last_schedule age; do
        printf "%-20s %-30s %-20s\n" "$ns" "$name" "$schedule"
    done
    CRONJOB_COUNT=$(echo "$CRONJOBS" | wc -l)
    echo "Total CronJobs: $CRONJOB_COUNT"
    echo ""
    SUSPENDED_CRONJOBS=$(echo "$CRONJOBS" | grep True || true)
    if [ -n "$SUSPENDED_CRONJOBS" ]; then
        add_problem "Warning" "Suspended CronJobs:\n$SUSPENDED_CRONJOBS\nCheck: kubectl describe cronjob -n <namespace> <name>"
    fi
fi

# Ingresses
log "Ingresses:"
INGRESSES=$(timeout 60s kubectl get ingresses -A -o wide --no-headers 2>/dev/null || echo "")
if [ -z "$INGRESSES" ]; then
    add_problem "Warning" "No ingresses found or failed to retrieve. Check: kubectl get ingresses -A"
    echo "No ingresses retrieved."
else
    printf "%-20s %-30s %-30s\n" "Namespace" "Name" "Hosts"
    echo "$INGRESSES" | while read -r ns name hosts address ports age; do
        printf "%-20s %-30s %-30s\n" "$ns" "$name" "$hosts"
    done
    INGRESS_COUNT=$(echo "$INGRESSES" | wc -l)
    echo "Total Ingresses: $INGRESS_COUNT"
    echo ""
    NO_ADDRESS_INGRESSES=$(echo "$INGRESSES" | grep "<none>" || true)
    if [ -n "$NO_ADDRESS_INGRESSES" ]; then
        add_problem "Warning" "Ingresses without an address:\n$NO_ADDRESS_INGRESSES\nCheck: kubectl describe ingress -n <namespace> <name>"
    fi
fi

# PersistentVolumeClaims
log "PersistentVolumeClaims:"
PVCS=$(timeout 60s kubectl get pvc -A -o wide --no-headers 2>/dev/null || echo "")
if [ -z "$PVCS" ]; then
    add_problem "Warning" "No PVCs found or failed to retrieve. Check: kubectl get pvc -A"
    echo "No PVCs retrieved."
else
    printf "%-20s %-30s %-10s\n" "Namespace" "Name" "Status"
    echo "$PVCS" | while read -r ns name status volume capacity storageclass age; do
        printf "%-20s %-30s %-10s\n" "$ns" "$name" "$status"
    done
    PVC_COUNT=$(echo "$PVCS" | wc -l)
    echo "Total PVCs: $PVC_COUNT"
    echo ""
    PENDING_PVCS=$(echo "$PVCS" | grep Pending || true)
    if [ -n "$PENDING_PVCS" ]; then
        add_problem "Warning" "Pending PVCs:\n$PENDING_PVCS\nCheck: kubectl describe pvc -n <namespace> <name>"
    fi
fi

# AWS Load Balancer Controller
log "AWS Load Balancer Controller:"
ALB_CONTROLLER=$(timeout 60s kubectl get pods -n kube-system -l app.kubernetes.io/name=aws-load-balancer-controller 2>/dev/null | grep Running || true)
if [ -z "$ALB_CONTROLLER" ]; then
    add_problem "Critical" "AWS Load Balancer Controller not running or not installed.\nInstall with: helm install aws-load-balancer-controller eks/aws-load-balancer-controller -n kube-system --set clusterName=<cluster-name>"
    echo "Status: Not running"
else
    echo "Status: Running"
fi

# Problem Summary
log "=== Problem Summary ==="
if [ -z "$PROBLEM_LOG" ]; then
    echo "No problems detected."
else
    echo -e "$PROBLEM_LOG"
    echo "Recommended Actions:"
    echo "- Critical issues require immediate attention (e.g., pending services, crashing pods)."
    echo "- Warnings indicate potential issues to monitor or resolve."
    echo "- Run suggested kubectl commands for detailed diagnostics."
fi

log "Scan complete!"
echo "For details, check logs in $LOG_FILE"
echo "To investigate issues:"
echo "  kubectl describe <resource> -n <namespace> <name>"
echo "  kubectl logs -n <namespace> <pod-name>"

exit 0
