# Kubernetes Cluster Setup on AWS EC2

This project sets up a simple Kubernetes cluster with a master node (central control plane) and a worker node on AWS EC2 instances running Amazon Linux 2023. The provided script automates the installation and configuration process.

## Prerequisites
- **AWS Account**: Access to create EC2 instances.
- **SSH Key Pair**: Generate a `.pem` key in AWS for SSH access.
- **Two EC2 Instances**:
  - AMI: Amazon Linux 2023
  - Instance Type: t2.medium (2 vCPUs, 4 GiB RAM) or larger
  - One for the master node, one for the worker node
- **Security Group Rules**:
  - **Master Inbound**:
    - TCP 6443 (API server) from anywhere or worker subnet
    - TCP 2379-2380 (etcd) from master subnet
    - TCP 10250-10252 (kubelet, scheduler, controller) from all nodes
  - **Worker Inbound**:
    - TCP 10250 (kubelet) from all nodes
    - TCP 30000-32767 (NodePort) from anywhere
  - **All**:
    - TCP 22 (SSH) from your IP
    - ICMP (ping) from anywhere

## Setup Instructions

### 1. Launch EC2 Instances
1. Log in to the AWS Management Console.
2. Navigate to **EC2 > Instances > Launch Instances**.
3. Configure:
   - **Name**: `k8s-master` for the master, `k8s-worker` for the worker.
   - **AMI**: Search for "Amazon Linux 2023" and select it.
   - **Instance Type**: Choose `t2.medium`.
   - **Key Pair**: Select or create a `.pem` key (e.g., `my-key.pem`).
   - **Security Group**: Create one with the rules above.
   - Launch one instance for the master and one for the worker.
4. Note the public/private IPs of both instances.

### 2. Prepare the Script
1. Save the script as `k8-setup-dynamic.sh` on your nodes with sudo and execute it (see script details below).
2. Make it executable:
   ```bash
   chmod +x k8-setup-dynamic.sh
