#!/bin/bash

# cleanup-unwanted-pods.sh
# Deletes unwanted pods in CrashLoopBackOff or Error state from specified namespaces
# Handles kube-system crashing pods and my-app Deployment to prevent recreation

set -e
set -o pipefail

ERROR_LOG=""
cleanup_triggered=false

cleanup() {
    if [ "$cleanup_triggered" = true ]; then
        return
    fi
    cleanup_triggered=true
    echo "ERROR detected. Exiting..."
    echo "Summary:"
    echo "Errors: $ERROR_LOG"
    exit 1
}

exec 3>&1
exec 2> >(while read -r line; do
    if [[ "$line" =~ "error" || "$line" =~ "Error" ]]; then
        ERROR_LOG+="$line\n"
        cleanup
    else
        echo "$line" >&3
    fi
done)

log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1"
}

log "Checking prerequisites..."
command -v kubectl >/dev/null 2>&1 || { log "kubectl is required"; ERROR_LOG="kubectl not found"; cleanup; }
kubectl cluster-info >/dev/null 2>&1 || { log "kubectl cannot connect to cluster"; ERROR_LOG="kubectl cluster access failed"; cleanup; }

log "Deleting unwanted pods in argocd namespace..."
kubectl delete pod -n argocd argocd-applicationset-controller-555cf564b4-jxxrx --force --ignore-not-found=true 2>/dev/null || true
kubectl delete pod -n argocd argocd-notifications-controller-8f5c7f7ff-bpvhp --force --ignore-not-found=true 2>/dev/null || true
kubectl delete pod -n argocd argocd-redis-85888cc66-2tmjz --force --ignore-not-found=true 2>/dev/null || true
kubectl delete pod -n argocd argocd-server-746f4c996d-f2cmw --force --ignore-not-found=true 2>/dev/null || true
kubectl delete pod -n argocd argocd-dex-server-55874cb5fd-7sc2k --force --ignore-not-found=true 2>/dev/null || true
kubectl delete pod -n argocd argocd-repo-server-6c4b9ffbf7-ntk6j --force --ignore-not-found=true 2>/dev/null || true

log "Deleting unwanted pod in default namespace..."
kubectl delete pod -n default curl-test --force --ignore-not-found=true 2>/dev/null || true

log "Deleting unwanted resources in my-app namespace..."
# Delete nginx pod and its Deployment to prevent recreation
kubectl delete pod -n my-app nginx-68768cbb9d-bsmrr --force --ignore-not-found=true 2>/dev/null || true
kubectl delete deployment -n my-app nginx --ignore-not-found=true 2>/dev/null || true

log "Handling crashing pods in kube-system namespace..."
if kubectl get pod -n kube-system calico-node-cssxz --ignore-not-found=true | grep -q "Running\|CrashLoopBackOff"; then
    log "Deleting calico-node-cssxz to trigger recreation..."
    kubectl delete pod -n kube-system calico-node-cssxz --force --ignore-not-found=true 2>/dev/null || true
fi
if kubectl get pod -n kube-system kube-proxy-4mdm7 --ignore-not-found=true | grep -q CrashLoopBackOff; then
    log "Deleting crashing kube-proxy-4mdm7 to trigger recreation..."
    kubectl delete pod -n kube-system kube-proxy-4mdm7 --force --ignore-not-found=true 2>/dev/null || true
fi

log "Checking Calico stability..."
CALICO_ISSUE=false
if ! kubectl get pods -n kube-system -l k8s-app=calico-node | grep -v NAME | grep -q "1/1.*Running"; then
    log "Calico pods are not stable. Reinstalling Calico CNI..."
    kubectl delete -f https://docs.projectcalico.org/manifests/calico.yaml --ignore-not-found=true 2>/dev/null || true
    kubectl apply -f https://docs.projectcalico.org/manifests/calico.yaml || { log "Calico reinstall failed"; ERROR_LOG="Calico reinstall failed"; cleanup; }
    timeout 300 bash -c 'while ! kubectl get pods -n kube-system -l k8s-app=calico-node | grep -v NAME | grep -q "1/1.*Running"; do sleep 5; done' || {
        log "Calico pods not ready after reinstall"
        CALICO_ISSUE=true
    }
fi

log "Verifying cleanup..."
sleep 5
CRASHING_PODS=$(kubectl get pods -A | grep -E "CrashLoopBackOff|Error" || true)
if [ -n "$CRASHING_PODS" ]; then
    log "Some pods are still in CrashLoopBackOff or Error state:"
    echo "$CRASHING_PODS"
    echo "Inspect logs for persistent issues:"
    echo "  kubectl logs -n argocd argocd-dex-server-55874cb5fd-7sc2k"
    echo "  kubectl logs -n argocd argocd-repo-server-6c4b9ffbf7-ntk6j"
    echo "  kubectl logs -n kube-system kube-proxy-4mdm7"
    if [ "$CALICO_ISSUE" = true ]; then
        echo "  kubectl logs -n kube-system -l k8s-app=calico-node"
    fi
    echo "Check pod status with:"
    echo "  kubectl get pods -A"
    echo "Manually delete ArgoCD deployments if no longer needed:"
    echo "  kubectl delete deployment -n argocd argocd-dex-server argocd-repo-server"
else
    log "Cleanup successful. No CrashLoopBackOff or Error pods detected."
fi

log "Cleanup complete!"
echo "Verify pod status with:"
echo "  kubectl get pods -A"
echo "If issues persist, check node status:"
echo "  kubectl describe node"
echo "To continue with Istio deployment, run deploy-istio-bookinfo-part1.sh."

exit 0
