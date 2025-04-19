# K8s Learning Project
A simple project to learn Kubernetes by setting up a cluster on AWS EC2 and deploying an Nginx web app.

## Prerequisites
- AWS account with EC2 access
- Two EC2 instances (t2.medium, Amazon Linux 2023)
- SSH access to instances

## Setup
1. Configure AWS resources (see `docs/setup-guide.md`).
2. Run `scripts/master_setup.sh` on the master node.
3. Run `scripts/worker_setup.sh` on the worker node and join the cluster.
4. Deploy the app using manifests in `manifests/`.

## Goals
- Learn Kubernetes architecture (master, worker, pods, services).
- Deploy and expose a simple web app.
