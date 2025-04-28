#!/bin/bash

# deploy-istio-bookinfo.sh
# Deploys Bookinfo with Istio 1.22.3 on Kubernetes 1.28.15
# Uses NodePort for istio-ingressgateway, skips screenshot generation, and cleans up on error/warning

set -e
set -o pipefail

ERROR_LOG=""
WARNING_LOG=""
cleanup_triggered=false

cleanup() {
    if [ "$cleanup_triggered" = true ]; then
        return
    fi
    cleanup_triggered=true
    echo "ERROR or WARNING detected. Cleaning up resources..."
    echo "Removing Bookinfo application..."
    kubectl delete -f "$ISTIO_DIR/samples/bookinfo/platform/kube/bookinfo.yaml" --ignore-not-found=true 2>/dev/null || true
    echo "Removing observability addons..."
    kubectl delete -f "$ISTIO_DIR/samples/addons" --ignore-not-found=true 2>/dev/null || true
    echo "Removing custom Istio configurations..."
    kubectl delete -f manifests/gateway.yaml --ignore-not-found=true 2>/dev/null || true
    kubectl delete -f manifests/mtls.yaml --ignore-not-found=true 2>/dev/null || true
    kubectl delete -f manifests/traffic-shifting.yaml --ignore-not-found=true 2>/dev/null || true
    kubectl delete -f manifests/circuit-breaker.yaml --ignore-not-found=true 2>/dev/null || true
    kubectl delete -f manifests/fault-injection.yaml --ignore-not-found=true 2>/dev/null || true
    echo "Uninstalling Istio..."
    istioctl uninstall --purge -y 2>/dev/null || true
    kubectl delete namespace istio-system --ignore-not-found=true 2>/dev/null || true
    echo "Removing sidecar injection label..."
    kubectl label namespace default istio-injection- --ignore-not-found=true 2>/dev/null || true
    echo "Cleanup complete."
    echo "Summary:"
    echo "Errors: $ERROR_LOG"
    echo "Warnings: $WARNING_LOG"
    exit 1
}

exec 3>&1
exec 2> >(while read -r line; do
    if [[ "$line" =~ "error" || "$line" =~ "Error" ]]; then
        ERROR_LOG+="$line\n"
        cleanup
    elif [[ "$line" =~ "warning" || "$line" =~ "Warning" ]]; then
        WARNING_LOG+="$line\n"
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
command -v curl >/dev/null 2>&1 || { log "curl is required"; ERROR_LOG="curl not found"; cleanup; }
command -v jq >/dev/null 2>&1 || { log "jq is required"; ERROR_LOG="jq not found"; cleanup; }
kubectl cluster-info >/dev/null 2>&1 || { log "kubectl cannot connect to cluster"; ERROR_LOG="kubectl cluster access failed"; cleanup; }

log "Checking Kubernetes version..."
K8S_VERSION=$(kubectl version -o json | jq -r '.serverVersion.gitVersion' | cut -d'+' -f1)
if [ -z "$K8S_VERSION" ]; then
    log "Failed to retrieve Kubernetes version"
    ERROR_LOG="kubectl version retrieval failed"
    cleanup
fi
log "Kubernetes version: $K8S_VERSION"
K8S_MAJOR=$(echo "$K8S_VERSION" | cut -d'.' -f1 | tr -d 'v')
K8S_MINOR=$(echo "$K8S_VERSION" | cut -d'.' -f2)

case "$K8S_MAJOR.$K8S_MINOR" in
    "1.28")
        ISTIO_VERSION="1.22.3"
        ;;
    "1.27")
        ISTIO_VERSION="1.21.3"
        ;;
    "1.29" | "1.30" | "1.31")
        ISTIO_VERSION="1.25.2"
        ;;
    *)
        log "Unsupported Kubernetes version: $K8S_VERSION"
        ERROR_LOG="Unsupported Kubernetes version: $K8S_VERSION"
        cleanup
        ;;
esac
log "Selected Istio version: $ISTIO_VERSION"

ISTIO_DIR="$HOME/istio-$ISTIO_VERSION"
log "Downloading Istio $ISTIO_VERSION..."
if [ ! -d "$ISTIO_DIR" ]; then
    curl -L "https://github.com/istio/istio/releases/download/$ISTIO_VERSION/istio-$ISTIO_VERSION-linux-amd64.tar.gz" | tar xz -C "$HOME" || { log "Failed to download Istio"; ERROR_LOG="Istio download failed"; cleanup; }
fi
cd "$ISTIO_DIR" || { log "Failed to cd to $ISTIO_DIR"; ERROR_LOG="cd $ISTIO_DIR failed"; cleanup; }
export PATH="$PWD/bin:$PATH"
command -v istioctl >/dev/null 2>&1 || { log "istioctl not found"; ERROR_LOG="istioctl not found"; cleanup; }

log "Installing Istio..."
istioctl install --set profile=demo -y || { log "Istio installation failed"; ERROR_LOG="Istio install failed"; cleanup; }

log "Verifying Istio pods..."
sleep 10
if ! kubectl get pods -n istio-system | grep -E "istiod|istio-ingressgateway|istio-egressgateway" | grep -q Running; then
    log "Istio pods not running"
    ERROR_LOG="Istio pods not running"
    cleanup
fi

log "Enabling sidecar injection..."
kubectl label namespace default istio-injection=enabled --overwrite || { log "Failed to label namespace"; ERROR_LOG="Namespace labeling failed"; cleanup; }

log "Configuring istio-ingressgateway as NodePort..."
kubectl -n istio-system patch svc istio-ingressgateway -p '{"spec":{"type":"NodePort"}}' || { log "Failed to patch istio-ingressgateway to NodePort"; ERROR_LOG="NodePort patch failed"; cleanup; }
INGRESS_PORT=$(kubectl -n istio-system get svc istio-ingressgateway -o jsonpath='{.spec.ports[?(@.name=="http2")].nodePort}')
INGRESS_HOST=$(kubectl get nodes -o jsonpath='{.items[0].status.addresses[?(@.type=="ExternalIP")].address}')
if [ -z "$INGRESS_HOST" ]; then
    INGRESS_HOST=$(curl -s ifconfig.me 2>/dev/null || echo "localhost")
fi
GATEWAY_URL="http://$INGRESS_HOST:$INGRESS_PORT/productpage"
log "NodePort assigned: $GATEWAY_URL"

log "Deploying Bookinfo application..."
kubectl apply -f samples/bookinfo/platform/kube/bookinfo.yaml || { log "Bookinfo deployment failed"; ERROR_LOG="Bookinfo apply failed"; cleanup; }

log "Waiting for Bookinfo pods to be ready..."
timeout 300 bash -c 'while ! kubectl get pods -n default | grep -E "details|productpage|ratings|reviews" | grep -v grep | grep -q "2/2.*Running"; do sleep 5; done' || { log "Bookinfo pods not ready"; ERROR_LOG="Bookinfo pods not ready"; cleanup; }

log "Verifying Bookinfo service..."
if ! kubectl exec -it $(kubectl get pod -l app=ratings -o jsonpath='{.items[0].metadata.name}') -c ratings -- curl -s productpage:9080/productpage | grep -q "<title>Simple Bookstore App</title>"; then
    log "Bookinfo service verification failed"
    ERROR_LOG="Bookinfo service check failed"
    cleanup
fi

log "Configuring Istio Gateway..."
kubectl apply -f manifests/gateway.yaml || { log "Gateway configuration failed"; ERROR_LOG="Gateway apply failed"; cleanup; }

log "Testing product page..."
if ! curl -s "$GATEWAY_URL" | grep -q "<title>Simple Bookstore App</title>"; then
    log "Product page not accessible"
    ERROR_LOG="Product page curl failed"
    cleanup
fi

log "Enabling mutual TLS..."
kubectl apply -f manifests/mtls.yaml || { log "mTLS configuration failed"; ERROR_LOG="mTLS apply failed"; cleanup; }

log "Verifying mTLS..."
if ! kubectl exec -it $(kubectl get pod -l app=productpage -o jsonpath='{.items[0].metadata.name}') -c istio-proxy -- curl -s localhost:15000/stats | grep -q ssl; then
    log "mTLS verification failed"
    ERROR_LOG="mTLS check failed"
    cleanup
fi

log "Configuring traffic shifting..."
kubectl apply -f manifests/traffic-shifting.yaml || { log "Traffic shifting failed"; ERROR_LOG="Traffic shifting apply failed"; cleanup; }

log "Testing traffic shifting..."
V1_COUNT=0
for i in {1..20}; do
    if curl -s "$GATEWAY_URL" | grep -q "color: black"; then
        V1_COUNT=$((V1_COUNT+1))
    fi
done
if [ "$V1_COUNT" -lt 1 ] || [ "$V1_COUNT" -gt 5 ]; then
    log "Traffic shifting verification failed (expected ~2/20 for v2, got $V1_COUNT)"
    ERROR_LOG="Traffic shifting test failed"
    cleanup
fi

log "Configuring circuit breaking..."
kubectl apply -f manifests/circuit-breaker.yaml || { log "Circuit breaking failed"; ERROR_LOG="Circuit breaking apply failed"; cleanup; }

log "Configuring fault injection..."
kubectl apply -f manifests/fault-injection.yaml || { log "Fault injection failed"; ERROR_LOG="Fault injection apply failed"; cleanup; }

log "Testing fault injection..."
DELAY_COUNT=0
for i in {1..10}; do
    START_TIME=$(date +%s)
    curl -s "$GATEWAY_URL" > /dev/null
    END_TIME=$(date +%s)
    if [ $((END_TIME - START_TIME)) -ge 7 ]; then
        DELAY_COUNT=$((DELAY_COUNT+1))
    fi
done
if [ "$DELAY_COUNT" -lt 3 ] || [ "$DELAY_COUNT" -gt 7 ]; then
    log "Fault injection verification failed (expected ~5/10 delays, got $DELAY_COUNT)"
    ERROR_LOG="Fault injection test failed"
    cleanup
fi

log "Installing observability tools..."
kubectl apply -f samples/addons || { log "Observability tools installation failed"; ERROR_LOG="Addons apply failed"; cleanup; }

log "Waiting for observability pods..."
timeout 300 bash -c 'while ! kubectl get pods -n istio-system | grep -E "kiali|grafana|prometheus" | grep -v grep | grep -q "1/1.*Running"; do sleep 5; done' || { log "Observability pods not ready"; ERROR_LOG="Observability pods not ready"; cleanup; }

log "Setup complete!"
echo "Access method: NodePort"
echo "Product page accessible at: $GATEWAY_URL"
echo "To capture screenshots, open the following in your browser:"
echo "  - Product page: $GATEWAY_URL"
echo "For dashboards, use port forwarding:"
echo "  kubectl port-forward -n istio-system svc/kiali 20001:20001 &"
echo "  kubectl port-forward -n istio-system svc/grafana 3000:3000 &"
echo "  kubectl port-forward -n istio-system svc/prometheus 9090:9090 &"
echo "Then access:"
echo "  - Kiali: http://localhost:20001/kiali"
echo "  - Grafana: http://localhost:3000"
echo "  - Prometheus: http://localhost:9090"
echo "Save screenshots in manifests/docs/"

exit 0
