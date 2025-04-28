# Deploying Bookinfo Application with Istio Service Mesh (1.22.3)

This repository contains the setup for deploying the Bookinfo application with Istio 1.22.3 on Kubernetes 1.28.15, configured via the `deploy-istio-bookinfo.sh` script.

## Overview
### Istio Architecture
- **Envoy Proxy**: Sidecar proxies manage traffic, security, and observability.
- **Istiod**: Control plane for configuration, certificate management, and policy enforcement.
- **Gateway**: Manages ingress traffic via NodePort on the Kubernetes cluster.
- **Telemetry**: Integrates with Prometheus, Grafana, and Kiali for monitoring and visualization.

### Bookinfo Application
- **productpage**: Main web interface, aggregating data from other services.
- **details**: Provides book details.
- **reviews**: Displays book reviews (versions v1, v2, v3).
- **ratings**: Supplies book ratings.

## Setup Instructions
Run the deployment script to set up Istio and Bookinfo:
```bash
chmod +x deploy-istio-bookinfo.sh
./deploy-istio-bookinfo.sh
```
Key steps performed by the script:
1. **Istio Installation**: Installs Istio 1.22.3 with demo profile.
2. **Bookinfo Deployment**: Deploys Bookinfo with sidecar injection in the default namespace.
3. **Gateway**: Configures `bookinfo-gateway` using NodePort.
4. **mTLS**: Enables strict mutual TLS for secure service communication.
5. **Traffic Management**: Configures traffic shifting (90/10 split for reviews:v1/v2), circuit breaking for ratings, and fault injection (7s delay for 50% of ratings requests).
6. **Observability**: Installs Kiali, Grafana, and Prometheus for monitoring.

## Commands Executed
The deployment script executes:
```bash
cd ~/istio-1.22.3
export PATH=$PWD/bin:$PATH
istioctl install --set profile=demo -y
kubectl label namespace default istio-injection=enabled
kubectl -n istio-system patch svc istio-ingressgateway -p '{"spec":{"type":"NodePort"}}'
kubectl apply -f samples/bookinfo/platform/kube/bookinfo.yaml
kubectl apply -f manifests/gateway.yaml
kubectl apply -f manifests/mtls.yaml
kubectl apply -f manifests/traffic-shifting.yaml
kubectl apply -f manifests/circuit-breaker.yaml
kubectl apply -f manifests/fault-injection.yaml
kubectl apply -f samples/addons
```

## Access
- **Product Page**: Access at the URL printed by the script (e.g., `http://<node-ip>:<nodeport>/productpage`).
- **Dashboards**: Use port forwarding to access observability tools:
  ```bash
  kubectl port-forward -n istio-system svc/kiali 20001:20001 &
  kubectl port-forward -n istio-system svc/grafana 3000:3000 &
  kubectl port-forward -n istio-system svc/prometheus 9090:9090 &
  ```
  - Kiali: `http://localhost:20001/kiali`
  - Grafana: `http://localhost:3000`
  - Prometheus: `http://localhost:9090`

## Validation
- **Retries**: Included in default VirtualServices for automatic retries on failures.
- **Circuit Breaking**: Configured for ratings service to eject unhealthy instances after 5 consecutive 5xx errors. Test with:
  ```bash
  kubectl exec -it $(kubectl get pod -l app=productpage -o jsonpath='{.items[0].metadata.name}') -c productpage -- curl -s -o /dev/null -w "%{http_code}\n" http://ratings:9080/ratings/1 -H "Host: ratings" -X POST
  ```
- **Canary Release**: Verified 90/10 traffic split for reviews:v1/v2.
- **Fault Injection**: Verified 7s delay for 50% of ratings requests.

## Screenshots
Manually capture and save in `manifests/docs/`:
- `productpage.png`: Product page at the NodePort URL.
- `kiali-before-fault.png`: Kiali graph before fault injection.
- `kiali-after-fault.png`: Kiali graph after fault injection.
- `grafana-latency.png`: Grafana latency chart showing fault injection delays.
- `grafana-traffic-split.png`: Grafana chart showing 90/10 traffic split.

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

## Cleanup
To remove all resources created by the deployment script:
```bash
kubectl delete -f samples/bookinfo/platform/kube/bookinfo.yaml
kubectl delete -f samples/addons
kubectl delete -f manifests/gateway.yaml
kubectl delete -f manifests/mtls.yaml
kubectl delete -f manifests/traffic-shifting.yaml
kubectl delete -f manifests/circuit-breaker.yaml
kubectl delete -f manifests/fault-injection.yaml
istioctl uninstall --purge -y
kubectl delete namespace istio-system
kubectl label namespace default istio-injection-
```
