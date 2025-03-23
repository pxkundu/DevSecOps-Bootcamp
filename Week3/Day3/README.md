# Week 3, Day 3: Advanced Jenkins - "Complex Architectures"

## Overview
This folder contains the implementation and documentation for **Week 3, Day 3** of our DevOps training, focusing on **Advanced Jenkins Master-Slave Architecture**. We’ve enhanced the SaaS Task Manager project with a secure, scalable, and reusable CI/CD pipeline adhering to Fortune 100 standards. Key topics include High Availability (HA) master setups, multi-region slaves, and specific optimizations, all built on AWS EC2 with Docker, leveraging services like ECR, S3, Secrets Manager, Auto Scaling, ELB, Route 53, and CloudWatch.

## Objectives
- Build a **High Availability (HA) Jenkins Master** setup with active-passive failover.
- Implement **Multi-Region Slaves** in us-east-1 and us-west-2 for resilience and performance.
- Optimize the pipeline with **Docker caching**, **parallel executors**, and **monitoring**.
- Deploy the Task Manager backend (task API) and frontend (task UI) on EC2 with Nginx.
- Ensure security, scalability, and team collaboration for 10+ DevOps members.

## Folder Structure
```
week3-day3/
├── README.md                # This index file
├── task-manager/            # Task Manager project source
│   ├── backend/            # Backend app (Node.js API)
│   │   ├── app.js
│   │   ├── package.json
│   │   ├── Dockerfile
│   │   └── .dockerignore
│   ├── frontend/           # Frontend app (Node.js UI)
│   │   ├── app.js
│   │   ├── package.json
│   │   ├── Dockerfile
│   │   └── .dockerignore
│   ├── scripts/            # Setup scripts for EC2 instances
│   │   ├── install_base.sh
│   │   ├── install_nginx.sh
│   │   ├── install_nodejs.sh
│   │   └── config_docker.sh
│   ├── Jenkinsfile         # Advanced pipeline definition
│   ├── README.md           # Project-specific README
│   └── .gitignore
├── pipeline-lib/           # Shared library for reusable pipeline code
│   ├── vars/
│   │   ├── buildDocker.groovy    # Docker build with caching
│   │   ├── deployEC2.groovy      # EC2 deployment with rollback
│   │   ├── scanImage.groovy      # Trivy security scan
│   │   └── logToCloudWatch.groovy # CloudWatch logging
│   ├── README.md           # Library documentation
│   └── .gitignore
├── docs/                   # Additional documentation
│   └── master-slave-deep-dive.md  # Theoretical notes on HA, multi-region, optimizations
└── setup-scripts/          # AWS setup commands
    ├── ha-master.sh        # HA master setup (active + passive)
    ├── multi-region-slaves.sh  # Slave setup for us-east-1 and us-west-2
    └── monitoring.sh       # CloudWatch monitoring setup
```

## Contents Covered

### 1. High Availability (HA) Master Setup
- **Purpose**: Ensure Jenkins uptime with active-passive masters in us-east-1.
- **Implementation**:
  - Two EC2 instances (t2.medium): `JenkinsMasterActive` and `JenkinsMasterPassive`.
  - S3 sync (`/var/lib/jenkins` to `s3://<your-bucket>/jenkins-backup`) every 5 minutes.
  - Elastic Load Balancer (ELB) with health checks (HTTP:8080/login, 10s interval).
  - Route 53 CNAME (`jenkins.taskmanager.com`) for seamless failover.
- **Outcome**: <30s failover, 99.99% uptime.

### 2. Multi-Region Slaves
- **Purpose**: Distribute builds across us-east-1 and us-west-2 for latency and resilience.
- **Implementation**:
  - Auto Scaling groups: `JenkinsSlavesEast` (us-east-1) and `JenkinsSlavesWest` (us-west-2).
  - Labels: `docker-slave-east` and `docker-slave-west`, 4 executors each.
  - Region-specific ECR repos for Docker images.
- **Outcome**: 20% faster builds, regional redundancy.

### 3. Specific Optimizations
- **Docker Caching**: Use `--cache-from` with ECR to reduce build time (e.g., 10m to 2m).
- **Parallel Executors**: 4 executors per t2.medium slave for concurrency.
- **Monitoring**: CloudWatch alarms on queue length, logs for debugging.
- **Outcome**: 50% faster pipeline execution, proactive scaling.

### 4. Task Manager Pipeline
- **Jenkinsfile**: Defines a multi-stage pipeline with setup, build/scan, approval, and deploy stages.
- **Shared Library**: Reusable Groovy scripts (`buildDocker`, `deployEC2`, etc.) in `pipeline-lib`.
- **Deployment**: Backend (port 3000) and frontend (port 8080) on EC2 with Nginx reverse proxy.
- **Security**: Secrets Manager for GitHub token, Trivy scans, encrypted EBS/S3.

### 5. Team Collaboration
- **Features**: Multi-branch support, RBAC (`dev` vs. `ops`), Slack notifications.
- **Outcome**: Supports 10+ team members with isolated workflows.

## Prerequisites
- AWS Account with IAM roles (`JenkinsSlaveRole`, `JenkinsMasterRole`).
- GitHub repo for `task-manager` and `pipeline-lib`.
- EC2 key pair (`<your-key>.pem`).
- S3 bucket (`<your-bucket>`), ECR repos, Secrets Manager secret (`github-token`).

## Setup Instructions
1. **Master Setup**: Run `setup-scripts/ha-master.sh`.
2. **Slaves Setup**: Run `setup-scripts/multi-region-slaves.sh`.
3. **Monitoring**: Run `setup-scripts/monitoring.sh`.
4. **Pipeline**: Configure Jenkins with `TaskManagerMultiBranch` job, point to `task-manager` repo.
5. **Test**: Build `main` branch, verify at `http://<frontend-ip>/tasks`.

## Key Learnings
- **HA**: Master redundancy eliminates downtime.
- **Multi-Region**: Slaves enhance global performance.
- **Optimizations**: Caching and executors boost efficiency.
- **Real-World**: Applies to SaaS, finance, retail CI/CD.

## Next Steps
- Simulate HA failover by stopping active master.
- Explore active-active HA with CloudBees Jenkins Enterprise.
- Add multi-region deployment targets for Task Manager.

---
