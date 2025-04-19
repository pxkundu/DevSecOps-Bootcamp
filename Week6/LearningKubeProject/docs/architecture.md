# Kubernetes Architecture Notes
- **Master Node**: Runs control plane (API server, scheduler, controller manager, etcd).
- **Worker Node**: Runs kubelet, kube-proxy, container runtime.
- **Networking**: Flannel in `kube-flannel` namespace.
- **Helm**: Package manager for Kubernetes:
  - Charts: Pre-packaged apps (e.g., Nginx).
  - Namespaces: Isolates apps (e.g., `my-app`).
  - Releases: Managed instances of charts.
