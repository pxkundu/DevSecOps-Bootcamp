# Week 2, Day 5: Kubernetes on AWS EKS Capstone - "Production Siege"

## Overview
This README serves as a wrap-up index for **Week 2, Day 5** of our DevOps learning journey, focusing on deploying a **production-grade microservices application** on **Amazon EKS**. The capstone integrates CI/CD (Day 1), serverless (Day 2), containers (Day 3), and Kubernetes basics (Day 4) into a real-world scenario, simulating a "Production Siege" (e.g., traffic spikes, node failures). It’s tailored for DevOps engineers aiming to master Kubernetes orchestration on AWS, with practical use cases inspired by companies like Netflix, Spotify, and Airbnb.

- **Duration**: 6-7 hours
- **Objective**: Deploy a scalable, resilient app (React frontend, Node.js API, Redis cache) on EKS, automate with AWS CodePipeline, and survive production challenges.
- **Tools**: AWS CLI, `eksctl`, `kubectl`, Helm, Docker, Git, AWS CodePipeline.

---

## Content Index

### 1. Theory: EKS, Kubernetes in Production, and DevOps Best Practices (1.5 hours)
- **Focus**: Theoretical foundation for running Kubernetes on EKS in production.
- **Key Topics**:
  - **Amazon EKS**: Managed Kubernetes control plane for high availability (HA).
  - **Cluster Architecture**: Control plane + worker nodes (EC2/Fargate).
  - **Core Constructs**: Pods, Deployments, Services, Ingress, Horizontal Pod Autoscaler (HPA), PersistentVolumes (PV).
  - **AWS Integrations**: AWS Load Balancer Controller (ALB), Amazon EBS CSI Driver, Amazon CloudWatch Container Insights, AWS CodePipeline.
  - **DevOps Practices**: Automation, Collaboration, Continuous Deployment, Observability, Shift Left, Resilience, Cost Optimization, Security.
- **Keywords**: Amazon EKS, Kubernetes, Cluster, Pod, Deployment, Service, Ingress, HPA, PV, AWS Load Balancer Controller, EBS CSI Driver, CloudWatch Container Insights, CodePipeline, Automation, Resilience, Security, Shared Responsibility Model, Microservices, Production Readiness.
- **Real-World Relevance**: Netflix’s global streaming APIs, Spotify’s playlist scaling, Airbnb’s booking persistence.

### 2. Lab: Deploy a Production-Grade App on EKS with CI/CD (3-3.5 hours)
- **Goal**: Deploy a microservices app on EKS, automate with CI/CD, and prepare for production.
- **Components**:
  - **Frontend**: React app serving a streaming UI.
  - **API**: Node.js app with Redis caching for status checks.
  - **Redis**: Persistent cache for stateful data.
- **Steps**:
  1. **Setup**: Installed AWS CLI, `eksctl`, `kubectl`, Helm, Docker; initialized Git repo.
  2. **Containers**: Built and pushed React frontend and Node.js API to Amazon ECR.
  3. **EKS Cluster**: Created a production-ready cluster with `eksctl` (t3.large nodes, 3-6 scale).
  4. **Add-ons**: Installed AWS Load Balancer Controller (ALB), EBS CSI Driver, CloudWatch Container Insights.
  5. **Deployment**: Applied Kubernetes manifests (Deployments, Services, Ingress, PVC) for app components.
  6. **CI/CD**: Configured AWS CodePipeline to deploy from GitHub to EKS.
- **Structure**:
```
  eks-capstone/
  ├── frontend/                # React frontend
  ├── api/                    # Node.js API
  ├── k8s/                    # Kubernetes manifests
  ├── pipeline/               # CI/CD configs
  └── README.md              # This file
 ```
- **Commands**: See detailed steps in the [full Day 5 guide](#).

### 3. Chaos Twist: "Production Siege" (1-1.5 hours)
- **Goal**: Defend against simulated production challenges (e.g., traffic spikes, node failures).
- **Scenario**: High load (`ab -n 10000 -c 100`), node termination.
- **Tasks**:
  - Monitored with `kubectl get pods` and CloudWatch metrics.
  - Scaled pods (`kubectl scale`) and nodes (`eksctl scale nodegroup`).
  - Added HPA for dynamic scaling (`kubectl autoscale`).
- **Outcome**: App remained available, showcasing resilience.

### 4. Wrap-Up: War Room Debrief (45 min)
- **Goal**: Reflect on production readiness and DevOps lessons.
- **Activities**:
  - Demoed app at `http://<alb-dns>` and `/api/status`.
  - Reviewed siege fixes (scaling, recovery).
  - Analyzed CI/CD pipeline logs.
- **Takeaways**: Production-grade EKS deployment, real-world resilience strategies.

---

## Key Outcomes
- **Theoretical Mastery**:
  - Understood EKS architecture and Kubernetes production constructs.
  - Learned DevOps best practices for automation, resilience, and observability.
- **Practical Skills**:
  - Deployed a microservices app on EKS with ALB, EBS, and CloudWatch.
  - Automated deployments with CodePipeline.
  - Managed a production siege with scaling and recovery.

---

## Real-World DevOps Use Cases
1. **Netflix Streaming Platform**:
   - EKS cluster with frontend, API, and Redis.
   - Scales pods for millions of viewers (e.g., new season drop).
   - CI/CD deploys updates continuously.
2. **Spotify Playlist Service**:
   - API caches playlists in Redis, served via ALB.
   - HPA adjusts pod count during peak usage.
   - CloudWatch tracks latency and errors.
3. **Airbnb Booking System**:
   - Stateful Redis persists booking data with EBS.
   - EKS ensures HA across AZs.
   - Pipeline automates feature rollouts.

---

## Best Practices Applied
- **Automation**: CodePipeline for CI/CD.
- **Resilience**: Self-healing pods, HPA, multi-AZ nodes.
- **Observability**: CloudWatch Container Insights for metrics/logs.
- **Security**: IAM roles, RBAC (implicit via add-ons).
- **Cost Optimization**: Right-sized t3.large nodes, scalable design.

---

## Tips and Tricks
- **Quick Cluster Check**: `kubectl get nodes` and `eksctl get cluster`.
- **Debugging**: `kubectl describe pod <name>` for events, `kubectl logs` for issues.
- **Scaling**: Test HPA with `kubectl autoscale` before prod.
- **Pipeline**: Use `--dry-run` in `buildspec.yml` for testing.

---

## Resources
- **Docs**: [EKS User Guide](https://docs.aws.amazon.com/eks/latest/userguide/), [Kubernetes Concepts](https://kubernetes.io/docs/concepts/), [AWS Well-Architected](https://docs.aws.amazon.com/wellarchitected/latest/framework/).
- **Repo**: Clone this project for manifests and pipeline configs.
- **Next Steps**: Explore AWS X-Ray for tracing, Spot Instances for cost savings.

---

## Cleanup (Optional)
To avoid costs:
```bash
eksctl delete cluster --name StreamingCluster
aws cloudformation delete-stack --stack-name EKSPipeline
aws ecr delete-repository --repository-name streaming-frontend --force
aws ecr delete-repository --repository-name streaming-api --force
```

---

**Built by a DevOps Learner, for DevOps Learners**  
Happy clustering! 🚀


---

### Notes on the README
- **Structure**: Organized as a content index with clear sections for theory, lab, chaos twist, and wrap-up, mirroring the Day 5 structure.
- **Real-World Focus**: Ties content to Netflix, Spotify, and Airbnb use cases, emphasizing production relevance.
- **Practicality**: Includes commands, best practices, and tips for day-to-day DevOps work.
- **Extensibility**: Links to full docs and suggests next steps (e.g., X-Ray, Spot Instances).
- **Cleanup**: Provides cost-saving steps, a real-world DevOps consideration.
