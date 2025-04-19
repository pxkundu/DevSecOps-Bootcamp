# Setup Guide
1. **Launch EC2 Instances**:
   - AMI: Amazon Linux 2023
   - Instance type: t2.medium (2 vCPU, 4 GiB RAM)
   - 1 master, 1 worker
   - Attach IAM role with EC2 permissions

2. **Configure Security Groups** (see `config/aws-security-group.txt`):
   - Master: 6443, 2379-2380, 10250-10252
   - Worker: 10250, 30000-32767
   - All: SSH (22), ICMP

3. **SSH into Instances**:
   - `ssh -i <key.pem> ec2-user@<instance-ip>`

4. **Run Scripts**:
   - Master: `sudo ./master_setup.sh`
   - Worker: `sudo ./worker_setup.sh`, then run the `kubeadm join` command from master.

5. **Deploy Application**:
   - On master: `kubectl apply -f manifests/nginx-deployment.yaml`
   - Expose: `kubectl apply -f manifests/nginx-service.yaml`

# Helm Setup Guide
1. **Launch EC2 Instances**:
   - AMI: Amazon Linux 2023
   - Type: t2.medium
2. **Configure Security Groups**: See `config/aws-security-group.txt`.
3. **Run Kubernetes Setup**:
   - Master: `sudo scripts/k8s_setup.sh master`
   - Worker: `sudo scripts/k8s_setup.sh worker` + join command
4. **Run Helm Setup**:
   - Master: `sudo scripts/helm_setup.sh`
   - Deploys Nginx in `my-app` namespace
5. **Explore Helm**:
   - Upgrade: `helm upgrade my-nginx bitnami/nginx -n my-app --set replicaCount=3`
   - Rollback: `helm rollback my-nginx 1 -n my-app`
   - Uninstall: `helm uninstall my-nginx -n my-app`
