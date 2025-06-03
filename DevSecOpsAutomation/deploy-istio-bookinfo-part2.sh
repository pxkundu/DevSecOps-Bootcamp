#!/bin/bash

# deploy-istio-bookinfo-part2.sh
# Part 2: Checks LoadBalancer DNS and completes Bookinfo deployment, Istio configs, and observability

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
    kubectl delete -f "$WORK_DIR/manifests/gateway.yaml" --ignore-not-found=true 2>/dev/null || true
    kubectl delete -f "$WORK_DIR/manifests/mtls.yaml" --ignore-not-found=true 2>/dev/null || true
    kubectl delete -f "$WORK_DIR/manifests/traffic-shifting.yaml" --ignore-not-found=true 2>/dev/null || true
    kubectl delete -f "$WORK_DIR/manifests/circuit-breaker.yaml" --ignore-not-found=true 2>/dev/null || true
    kubectl delete -f "$WORK_DIR/manifests/fault-injection.yaml" --ignore-not-found=true 2>/dev/null || true
    echo "Uninstalling Istio..."
    istioctl uninstall --purge -y 2>/dev/null || true
    kubectl delete namespace istio-system --ignore-not-found=true 2>/dev/null || true
    echo "Removing sidecar injection label..."
    kubectl label namespace default istio-injection- --ignore-not-found=true 2>/dev/null || true
    rm -rf "$WORK_DIR" 2>/dev/null || true
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

log "Loading state from Part 1..."
STATE_FILE="$HOME/istio-bookinfo/state.conf"
if [ ! -f "$STATE_FILE" ]; then
    log "State file $STATE_FILE not found. Run deploy-istio-bookinfo-part1.sh first."
    ERROR_LOG="State file missing"
    exit 1
fi
source "$STATE_FILE"
if [ -z "$ISTIO_VERSION" ] || [ -z "$WORK_DIR" ] || [ -z "$ISTIO_DIR" ] || [ -z "$CLUSTER_NAME" ]; then
    log "Invalid state file. Ensure deploy-istio-bookinfo-part1.sh completed successfully."
    ERROR_LOG="Invalid state file"
    cleanup
fi
if [ ! -d "$ISTIO_DIR" ]; then
    log "Istio directory $ISTIO_DIR not found."
    ERROR_LOG="Istio directory missing"
    cleanup
fi
export PATH="$ISTIO_DIR/bin:$PATH"

log "Checking LoadBalancer DNS..."
timeout 60 bash -c 'while ! kubectl -n istio-system get svc istio-ingressgateway -o jsonpath="{.status.loadBalancer.ingress[0].hostname}" | grep -q "."; do sleep 5; done' || {
    log "LoadBalancer DNS not assigned yet."
    echo "Check status with:"
    echo "  kubectl -n istio-system get svc istio-ingressgateway -o jsonpath='{.status.loadBalancer.ingress[0].hostname}'"
    echo "Inspect controller logs:"
    echo "  kubectl logs -n kube-system -l app.kubernetes.io/name=aws-load-balancer-controller"
    echo "Verify subnet tags (kubernetes.io/cluster/$CLUSTER_NAME=shared) and IAM permissions."
    echo "Run this script again when DNS is available."
    exit 1
}
INGRESS_DNS=$(kubectl -n istio-system get svc istio-ingressgateway -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')
GATEWAY_URL="http://$INGRESS_DNS/productpage"
log "Gateway URL: $GATEWAY_URL"

mkdir -p "$WORK_DIR/manifests/docs" || { log "Failed to create manifests/docs"; ERROR_LOG="mkdir manifests/docs failed"; cleanup; }
cd "$WORK_DIR" || { log "Failed to cd to $WORK_DIR"; ERROR_LOG="cd $WORK_DIR failed"; cleanup; }

log "Deploying Bookinfo application..."
kubectl apply -f "$ISTIO_DIR/samples/bookinfo/platform/kube/bookinfo.yaml" || { log "Bookinfo deployment failed"; ERROR_LOG="Bookinfo apply failed"; cleanup; }

log "Waiting for Bookinfo pods to be ready..."
timeout 300 bash -c 'while ! kubectl get pods -n default | grep -E "details|productpage|ratings|reviews" | grep -v grep | grep -q "2/2.*Running"; do sleep 5; done' || { log "Bookinfo pods not ready"; ERROR_LOG="Bookinfo pods not ready"; cleanup; }

log "Verifying Bookinfo service..."
if ! kubectl exec -it $(kubectl get pod -l app=ratings -o jsonpath='{.items[0].metadata.name}') -c ratings -- curl -s productpage:9080/productpage | grep -q "<title>Simple Bookstore App</title>"; then
    log "Bookinfo service verification failed"
    ERROR_LOG="Bookinfo service check failed"
    cleanup
fi

log "Configuring Istio Gateway..."
cat > "$WORK_DIR/manifests/gateway.yaml" << 'EOF'
apiVersion: networking.istio.io/v1alpha3
kind: Gateway
metadata:
  name: bookinfo-gateway
spec:
  selector:
    istio: ingressgateway
  servers:
  - port:
      number: 80
      name: http
      protocol: HTTP
    hosts:
    - "*"
---
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: bookinfo
spec:
  hosts:
  - "*"
  gateways:
  - bookinfo-gateway
  http:
  - match:
    - uri:
        prefix: /productpage
    - uri:
        prefix: /login
    - uri:
        prefix: /logout
    - uri:
        prefix: /api/v1/products
    route:
    - destination:
        host: productpage
        port:
          number: 9080
EOF
kubectl apply -f "$WORK_DIR/manifests/gateway.yaml" || { log "Gateway configuration failed"; ERROR_LOG="Gateway apply failed"; cleanup; }

log "Testing product page..."
if ! curl -s "$GATEWAY_URL" | grep -q "<title>Simple Bookstore App</title>"; then
    log "Product page not accessible"
    ERROR_LOG="Product page curl failed"
    cleanup
fi

log "Enabling mutual TLS..."
cat > "$WORK_DIR/manifests/mtls.yaml" << 'EOF'
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: default
spec:
  mtls:
    mode: STRICT
EOF
kubectl apply -f "$WORK_DIR/manifests/mtls.yaml" || { log "mTLS configuration failed"; ERROR_LOG="mTLS apply failed"; cleanup; }

log "Verifying mTLS..."
if ! kubectl exec -it $(kubectl get pod -l app=productpage -o jsonpath='{.items[0].metadata.name}') -c istio-proxy -- curl -s localhost:15000/stats | grep -q ssl; then
    log "mTLS verification failed"
    ERROR_LOG="mTLS check failed"
    cleanup
fi

log "Configuring traffic shifting..."
cat > "$WORK_DIR/manifests/traffic-shifting.yaml" << 'EOF'
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: reviews
spec:
  hosts:
  - reviews
  http:
  - route:
    - destination:
        host: reviews
        subset: v1
      weight: 90
    - destination:
        host: reviews
        subset: v2
      weight: 10
---
apiVersion: networking.istio.io/v1alpha3
kind: DestinationRule
metadata:
  name: reviews
spec:
  host: reviews
  subsets:
  - name: v1
    labels:
      version: v1
  - name: v2
    labels:
      version: v2
EOF
kubectl apply -f "$WORK_DIR/manifests/traffic-shifting.yaml" || { log "Traffic shifting failed"; ERROR_LOG="Traffic shifting apply failed"; cleanup; }

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
cat > "$WORK_DIR/manifests/circuit-breaker.yaml" << 'EOF'
apiVersion: networking.istio.io/v1alpha3
kind: DestinationRule
metadata:
  name: ratings-circuit-breaker
spec:
  host: ratings
  trafficPolicy:
    outlierDetection:
      consecutive5xxErrors: 5
      interval: 30s
      baseEjectionTime: 30s
EOF
kubectl apply -f "$WORK_DIR/manifests/circuit-breaker.yaml" || { log "Circuit breaking failed"; ERROR_LOG="Circuit breaking apply failed"; cleanup; }

log "Configuring fault injection..."
cat > "$WORK_DIR/manifests/fault-injection.yaml" << 'EOF'
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: ratings
spec:
  hosts:
  - ratings
  http:
  - fault:
      delay:
        percentage:
          value: 50.0
        fixedDelay: 7s
    route:
    - destination:
        host: ratings
        subset: v1
---
apiVersion: networking.istio.io/v1alpha3
kind: DestinationRule
metadata:
  name: ratings
spec:
  host: ratings
  subsets:
  - name: v1
    labels:
      version: v1
EOF
kubectl apply -f "$WORK_DIR/manifests/fault-injection.yaml" || { log "Fault injection failed"; ERROR_LOG="Fault injection apply failed"; cleanup; }

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
kubectl apply -f "$ISTIO_DIR/samples/addons" || { log "Observability tools installation failed"; ERROR_LOG="Addons apply failed"; cleanup; }

log "Waiting for observability pods..."
timeout 300 bash -c 'while ! kubectl get pods -n istio-system | grep -E "kiali|grafana|prometheus" | grep -v grep | grep -q "1/1.*Running"; do sleep 5; done' || { log "Observability pods not ready"; ERROR_LOG="Observability pods not ready"; cleanup; }

log "Part 2 complete!"
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
echo "Save screenshots in $WORK_DIR/manifests/docs/"

exit 0
