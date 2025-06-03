# Deploying Bookinfo Application with Istio Service Mesh (1.22.3)

This repository documents the deployment of the Bookinfo application with Istio 1.22.3 on Kubernetes 1.28.15. The setup configures a service mesh with mutual TLS, traffic shifting, circuit breaking, fault injection, and observability tools, using NodePort for ingress to ensure fast and reliable access.

## Overview

### Istio Architecture
Istio is a service mesh that enhances microservice communication with traffic management, security, and observability. Its key components include:
- **Envoy Proxy**: Deployed as sidecars, Envoy proxies handle service-to-service traffic, enforcing policies and collecting telemetry.
- **Istiod**: The control plane, managing configuration, certificate issuance, and policy enforcement.
- **Gateway**: Manages external traffic, configured here as a NodePort service for ingress.
- **Telemetry**: Integrates with Prometheus, Grafana, and Kiali for monitoring and visualization of traffic, latency, and service health.

### Bookinfo Application
Bookinfo is a sample microservices application demonstrating Istio’s capabilities. It consists of:
- **productpage**: The main web interface, aggregating data from other services.
- **details**: Provides book details.
- **reviews**: Displays book reviews, available in multiple versions (v1, v2, v3).
- **ratings**: Supplies book ratings, used for fault injection and circuit breaking tests.

## Setup Instructions

The following steps detail the manual process to deploy Istio, Bookinfo, and required configurations. Each step includes the commands executed, their purpose, and their role in completing the task.

### Step 1: Install Prerequisites
**Purpose**: Ensure required tools are available for deployment.

**Commands**:
```bash
command -v kubectl >/dev/null 2>&1 || { echo "kubectl is required"; exit 1; }
command -v curl >/dev/null 2>&1 || { echo "curl is required"; exit 1; }
command -v jq >/dev/null 2>&1 || { echo "jq is required"; exit 1; }
kubectl cluster-info >/dev/null 2>&1 || { echo "kubectl cannot connect to cluster"; exit 1; }
```

**Explanation**:
- Verifies that `kubectl` (Kubernetes CLI), `curl` (for downloading Istio), and `jq` (for parsing JSON) are installed.
- Confirms `kubectl` can connect to the Kubernetes cluster.
- These checks ensure the environment is ready, preventing failures during deployment.

**Task Contribution**: Establishes a reliable foundation for subsequent steps.

### Step 2: Download and Prepare Istio
**Purpose**: Obtain Istio 1.22.3 and prepare its tools.

**Commands**:
```bash
ISTIO_VERSION="1.22.3"
ISTIO_DIR="$HOME/istio-$ISTIO_VERSION"
if [ ! -d "$ISTIO_DIR" ]; then
    curl -L "https://github.com/istio/istio/releases/download/$ISTIO_VERSION/istio-$ISTIO_VERSION-linux-amd64.tar.gz" | tar xz -C "$HOME"
fi
cd "$ISTIO_DIR"
export PATH="$PWD/bin:$PATH"
command -v istioctl >/dev/null 2>&1 || { echo "istioctl not found"; exit 1; }
```

**Explanation**:
- Downloads Istio 1.22.3 from its GitHub release if not already present.
- Extracts it to `$HOME/istio-1.22.3`.
- Adds the `istioctl` binary to the PATH, enabling Istio management commands.
- Verifies `istioctl` is available.

**Task Contribution**: Provides the Istio tools and configuration files (e.g., Bookinfo YAML) needed for deployment.

### Step 3: Install Istio
**Purpose**: Deploy Istio 1.22.3 with the demo profile.

**Command**:
```bash
istioctl install --set profile=demo -y
```

**Explanation**:
- Installs Istio using the `demo` profile, which includes core components (Istiod, ingress/egress gateways) and observability integrations.
- The `-y` flag auto-confirms the installation.
- Creates the `istio-system` namespace and deploys Istio pods (e.g., `istiod`, `istio-ingressgateway`).

**Task Contribution**: Sets up the service mesh infrastructure, enabling traffic management and security features for Bookinfo.

### Step 4: Enable Sidecar Injection
**Purpose**: Configure the default namespace for automatic Envoy sidecar injection.

**Command**:
```bash
kubectl label namespace default istio-injection=enabled --overwrite
```

**Explanation**:
- Adds the `istio-injection=enabled` label to the `default` namespace.
- Ensures that pods deployed in this namespace (e.g., Bookinfo services) automatically receive Envoy sidecar proxies.

**Task Contribution**: Prepares the namespace for Bookinfo deployment with Istio’s traffic management and security capabilities.

### Step 5: Configure Ingress as NodePort
**Purpose**: Set up `istio-ingressgateway` as a NodePort service for external access.

**Command**:
```bash
kubectl -n istio-system patch svc istio-ingressgateway -p '{"spec":{"type":"NodePort"}}'
```

**Explanation**:
- Patches the `istio-ingressgateway` service in the `istio-system` namespace to use NodePort instead of LoadBalancer.
- Exposes the gateway on a high port (30000–32767), accessible via a cluster node’s IP.
- Avoids delays associated with AWS LoadBalancer provisioning.

**Task Contribution**: Enables fast and reliable external access to the Bookinfo application, addressing the task’s performance concerns.

### Step 6: Deploy Bookinfo Application
**Purpose**: Deploy the Bookinfo microservices.

**Command**:
```bash
kubectl apply -f $HOME/istio-1.22.3/samples/bookinfo/platform/kube/bookinfo.yaml
```

**Explanation**:
- Applies the Bookinfo YAML from Istio’s samples, deploying services (`productpage`, `details`, `reviews`, `ratings`) and their pods.
- Due to sidecar injection (Step 4), each pod includes an Envoy proxy.

**Task Contribution**: Deploys the core application, enabling Istio’s features to be applied and tested.

### Step 7: Configure Istio Gateway
**Purpose**: Route external traffic to the Bookinfo `productpage`.

**Command**:
```bash
kubectl apply -f manifests/gateway.yaml
```

**File Content (`manifests/gateway.yaml`)**:
```yaml
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
```

**Explanation**:
- Applies `gateway.yaml`, which defines:
  - A `Gateway` resource to handle HTTP traffic on port 80 via `istio-ingressgateway`.
  - A `VirtualService` to route requests for `/productpage`, `/login`, `/logout`, and `/api/v1/products` to the `productpage` service on port 9080.
- Routes external traffic through the NodePort to the application.

**Task Contribution**: Enables users to access the Bookinfo product page externally, a key task requirement.

### Step 8: Enable Mutual TLS
**Purpose**: Secure service-to-service communication with strict mTLS.

**Command**:
```bash
kubectl apply -f manifests/mtls.yaml
```

**File Content (`manifests/mtls.yaml`)**:
```yaml
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: default
spec:
  mtls:
    mode: STRICT
```

**Explanation**:
- Applies `mtls.yaml`, enforcing strict mutual TLS in the `default` namespace.
- Ensures all service communication (e.g., `productpage` to `reviews`) uses encrypted TLS with mutual authentication.

**Task Contribution**: Implements a critical security feature, protecting microservice interactions.

### Step 9: Configure Traffic Shifting
**Purpose**: Implement a canary release with a 90/10 traffic split for `reviews` v1/v2.

**Command**:
```bash
kubectl apply -f manifests/traffic-shifting.yaml
```

**File Content (`manifests/traffic-shifting.yaml`)**:
```yaml
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
```

**Explanation**:
- Applies `traffic-shifting.yaml`, which:
  - Defines a `VirtualService` to route 90% of `reviews` traffic to v1 and 10% to v2.
  - Uses a `DestinationRule` to identify v1 and v2 based on pod labels (`version: v1`, `version: v2`).
- Implements a canary release, allowing testing of v2 with minimal impact.

**Task Contribution**: Demonstrates Istio’s traffic management for controlled rollouts.

### Step 10: Configure Circuit Breaking
**Purpose**: Protect the `ratings` service from failures.

**Command**:
```bash
kubectl apply -f manifests/circuit-breaker.yaml
```

**File Content (`manifests/circuit-breaker.yaml`)**:
```yaml
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
```

**Explanation**:
- Applies `circuit-breaker.yaml`, configuring outlier detection for the `ratings` service.
- Ejects instances after 5 consecutive 5xx errors, checked every 30 seconds, with a 30-second base ejection time.
- Prevents cascading failures by isolating unhealthy `ratings` pods.

**Task Contribution**: Enhances application resilience, a key service mesh feature.

### Step 11: Configure Fault Injection
**Purpose**: Simulate failures by injecting delays into `ratings` requests.

**Command**:
```bash
kubectl apply -f manifests/fault-injection.yaml
```

**File Content (`manifests/fault-injection.yaml`)**:
```yaml
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
```

**Explanation**:
- Applies `fault-injection.yaml`, which:
  - Injects a 7-second delay for 50% of requests to the `ratings` service (v1).
  - Defines a `DestinationRule` to identify the v1 subset.
- Simulates network issues to test application behavior under stress.

**Task Contribution**: Validates Istio’s fault tolerance capabilities.

### Step 12: Install Observability Tools
**Purpose**: Deploy Kiali, Grafana, and Prometheus for monitoring.

**Command**:
```bash
kubectl apply -f $HOME/istio-1.22.3/samples/addons
```

**Explanation**:
- Applies Istio’s addons (Prometheus, Grafana, Kiali) from the samples directory.
- Deploys these tools in the `istio-system` namespace, enabling visualization of traffic, latency, and service health.

**Task Contribution**: Provides observability, allowing analysis of traffic patterns and fault injection effects.

## Access

### Product Page
- **URL**: Access the product page at `http://<node-ip>:<nodeport>/productpage`.
- **Find `<node-ip>` and `<nodeport>`**:
  ```bash
  INGRESS_PORT=$(kubectl -n istio-system get svc istio-ingressgateway -o jsonpath='{.spec.ports[?(@.name=="http2")].nodePort}')
  INGRESS_HOST=$(kubectl get nodes -o jsonpath='{.items[0].status.addresses[?(@.type=="ExternalIP")].address}')
  if [ -z "$INGRESS_HOST" ]; then
      INGRESS_HOST=$(curl -s ifconfig.me || echo "localhost")
  fi
  echo "Product page: http://$INGRESS_HOST:$INGRESS_PORT/productpage"
  ```
- `<node-ip>` is the cluster node’s external IP (or EC2 public IP/localhost).
- `<nodeport>` is the NodePort assigned to `istio-ingressgateway` (e.g., 30000–32767).
- Ensure the EC2 security group allows inbound traffic on the NodePort range.

### Observability Dashboards
- **Setup Port Forwarding**:
  ```bash
  kubectl port-forward -n istio-system svc/kiali 20001:20001 &
  kubectl port-forward -n istio-system svc/grafana 3000:3000 &
  kubectl port-forward -n istio-system svc/prometheus 9090:9090 &
  ```
- **Access**:
  - Kiali: `http://localhost:20001/kiali` (visualizes service mesh topology).
  - Grafana: `http://localhost:3000` (displays latency and traffic metrics).
  - Prometheus: `http://localhost:9090` (queries raw metrics).

## Validation

### Retries
- **Description**: Istio’s default `VirtualService` configurations include retry policies for failed requests.
- **Verification**: Retries are automatically applied for transient failures (e.g., 5xx errors). Test by inducing failures:
  ```bash
  kubectl exec -it $(kubectl get pod -l app=productpage -o jsonpath='{.items[0].metadata.name}') -c productpage -- curl -s http://ratings:9080/ratings/1
  ```
- **Outcome**: Retries ensure robust communication, observable in Kiali or Prometheus.

### Circuit Breaking
- **Description**: The `ratings` service is protected by circuit breaking (Step 10).
- **Verification**:
  ```bash
  kubectl exec -it $(kubectl get pod -l app=productpage -o jsonpath='{.items[0].metadata.name}') -c productpage -- curl -s -o /dev/null -w "%{http_code}\n" http://ratings:9080/ratings/1 -H "Host: ratings" -X POST
  ```
- **Outcome**: After 5 consecutive 5xx errors, unhealthy `ratings` pods are ejected, visible in Kiali’s service graph.

### Canary Release
- **Description**: Traffic is split 90/10 between `reviews` v1 and v2 (Step 9).
- **Verification**:
  ```bash
  for i in {1..20}; do curl -s http://<node-ip>:<nodeport>/productpage | grep -q "color: black" && echo "v1" || echo "v2"; done
  ```
- **Outcome**: Expect ~2/20 requests to hit v2 (red stars in reviews), confirmed in Grafana’s traffic split chart.

### Fault Injection
- **Description**: 50% of `ratings` requests experience a 7-second delay (Step 11).
- **Verification**:
  ```bash
  for i in {1..10}; do START=$(date +%s); curl -s http://<node-ip>:<nodeport>/productpage > /dev/null; END=$(date +%s); [ $((END-START)) -ge 7 ] && echo "Delayed"; done
  ```
- **Outcome**: ~5/10 requests show delays, visible in Grafana’s latency chart and Kiali’s graph.

## Screenshots
Manually capture the following screenshots and save them in `manifests/docs/`:
- **`productpage.png`**: The Bookinfo product page at `http://<node-ip>:<nodeport>/productpage`.
- **`kiali-before-fault.png`**: Kiali graph (`http://localhost:20001/kiali`) before applying fault injection.
- **`kiali-after-fault.png`**: Kiali graph after fault injection, showing delays.
- **`grafana-latency.png`**: Grafana dashboard (`http://localhost:3000`) showing latency spikes from fault injection.
- **`grafana-traffic-split.png`**: Grafana dashboard showing the 90/10 traffic split for `reviews`.

**Steps**:
1. Deploy the application (follow the steps above).
2. Access the product page and dashboards as described in the Access section.
3. Take screenshots using a browser or tool.
4. Save to `manifests/docs/` in the repository.

## Repository Structure
```
├── README.md
├── deploy-istio-bookinfo.sh
├── manifests/
│   ├── docs/
│   │   ├── productpage.png
│   │   ├── kiali-before-fault.png
│   │   ├── kiali-after-fault.png
│   │   ├── grafana-latency.png
│   │   ├── grafana-traffic-split.png
│   ├── gateway.yaml
│   ├── mtls.yaml
│   ├── traffic-shifting.yaml
│   ├── circuit-breaker.yaml
│   ├── fault-injection.yaml
```

- **`README.md`**: This file, documenting the setup.
- **`deploy-istio-bookinfo.sh`**: A script automating the above steps (not used in this guide).
- **`manifests/docs/`**: Directory for storing screenshots.
- **`manifests/*.yaml`**: Istio configuration files for gateway, mTLS, traffic shifting, circuit breaking, and fault injection.

## Cleanup
To remove all deployed resources:
```bash
kubectl delete -f $HOME/istio-1.22.3/samples/bookinfo/platform/kube/bookinfo.yaml
kubectl delete -f $HOME/istio-1.22.3/samples/addons
kubectl delete -f manifests/gateway.yaml
kubectl delete -f manifests/mtls.yaml
kubectl delete -f manifests/traffic-shifting.yaml
kubectl delete -f manifests/circuit-breaker.yaml
kubectl delete -f manifests/fault-injection.yaml
istioctl uninstall --purge -y
kubectl delete namespace istio-system
kubectl label namespace default istio-injection-
```

**Explanation**:
- Deletes Bookinfo, observability addons, and custom Istio configurations.
- Uninstalls Istio and removes the `istio-system` namespace.
- Removes the sidecar injection label.
- Ensures a clean cluster state.