## Updated Week 6: Capstone and Real-World Crunch - Kubernetes Focus
**Objective**: Design, build, secure, and deploy a Kubernetes-based e-commerce platform on AWS EKS, applying all Kubernetes best practices to ensure a scalable, secure, and resilient production system.

- **Duration**: 5 days, ~7-8 hours each (~35-40 hours total).
- **Structure**: Theoretical Deep Dive (~40%) + Practical Implementation (~60%).
- **Capstone Project**: **E-commerce Platform on EKS**
  - **Components**: Frontend (React), Backend (Node.js API), Database (RDS via EKS service), Storage (S3 via EKS pods).
  - **Scenario**: Retail app managing 10,000+ products, scaling for 100K+ transactions during peak season.

---

### Day 1: Capstone Kickoff - Plan Microservices, Swap a Tool Mid-Plan
- **Objective**: Design a Kubernetes-based microservices architecture and adapt to a tool swap, ensuring best practices from the start.
- **Theoretical Deep Dive**:
  - **Kubernetes Architecture**: Modular microservices, multi-AZ HA, Graviton2 nodes (AWS Well-Architected Reliability, Scalability).
  - **Tool Swapping**: Mid-plan pivot (e.g., Jenkins to GitHub Actions) for agility (DevSecOps adaptability).
  - **Best Practices**: Modular design, HA, IaC, resource optimization.
- **Practical Use Cases**:
  - **Amazon’s EKS Pivot**: Swapped ECS to EKS mid-2022, using 3 AZs for 1M+ customers (375M items, 2023).
  - **Netflix’s Tool Shift**: Moved from Travis CI to Spinnaker (2015), optimizing for 247M subscribers.
- **Tasks**:
  1. Define microservices: Frontend (React), Backend (Node.js API), RDS proxy.
  2. Design EKS: 2 `t4g.medium` nodes (Graviton2) across 3 AZs (`us-east-1a/b/c`), ALB Ingress, Karpenter, namespace (`prod`).
  3. Plan security: IAM roles, KMS, Secrets Manager.
  4. Start with Jenkins CI/CD plan, swap to GitHub Actions mid-day (document trade-offs).
  5. Document: `ecomm-architecture.md` with AZs, Graviton2, Karpenter, ALB.
- **Verification**: Diagram shows modular services, 3 AZs, Graviton2, updated CI/CD plan.

---

### Day 2: Build and Automate - CI/CD + EKS, Scale for a DDoS
- **Objective**: Develop and deploy microservices on EKS with CI/CD automation, scaling for a simulated DDoS attack.
- **Theoretical Deep Dive**:
  - **Microservices Development**: Containerized apps with requests/limits, probes (AWS Well-Architected Performance Efficiency).
  - **EKS + CI/CD**: Automated deployments with GitHub Actions, Helm (DevSecOps automation).
  - **Best Practices**: Scaling (HPA/Karpenter), networking (ALB), resource optimization, zero-downtime (probes).
- **Practical Use Cases**:
  - **Walmart’s EKS Scale**: Deploys Node.js on EKS, scaling 5x for 240M customers during Black Friday (2022).
  - **Amazon’s DDoS Resilience**: Uses ALB/EKS with Shield for 1M+ customers (2023).
- **Tasks**:
  1. Frontend (React):
     - Dockerize: `docker build -t <ecr-repo>/frontend:latest`.
     - Manifest: `frontend-deployment.yaml` (5 replicas, `requests: {cpu: "200m", memory: "256Mi"}, limits: {cpu: "500m", memory: "512Mi"}`, `livenessProbe: /health`, `podAntiAffinity`).
  2. Backend (Node.js API):
     - Dockerize, add `/inventory` endpoint, push to ECR.
     - Manifest: `backend-deployment.yaml` (same specs).
  3. Deploy: `kubectl apply -f .`, expose via ALB Ingress with TLS (`ingress.yaml`, `ssl-cert` ARN).
  4. Simulate DDoS: `ab -n 10000 -c 100 <alb-url>`, verify Karpenter scales pods/nodes.
- **Verification**: Pods running with limits/probes, ALB (HTTPS) accessible, scales to 10 pods under load.

---

### Day 3: Secure and Monitor - Add Encryption/Alarms, Pass a Pen Test
- **Objective**: Secure EKS with encryption and monitoring, passing a Kubernetes-specific pen test.
- **Theoretical Deep Dive**:
  - **Kubernetes Security**: RBAC, Network Policies, PSS, TLS, Secrets Manager (NIST 800-53 SC-13).
  - **Monitoring**: CloudWatch, X-Ray, dashboards for observability (AWS Well-Architected Reliability).
  - **Best Practices**: Security layers, monitoring, networking.
- **Practical Use Cases**:
  - **Amazon’s Security**: Encrypts EKS traffic, monitors with CloudWatch for 1M+ customers (2023).
  - **Airbnb’s Pen Test**: Passes `kube-hunter` for 100M+ bookings (2022).
- **Tasks**:
  1. Security:
     - RBAC: `role.yaml` limits namespace access.
     - Network Policy: `netpol.yaml` allows frontend-to-backend only.
     - OPA Gatekeeper: Denies privileged pods.
     - TLS on ALB, Secrets Manager for API keys (`kubectl create secret` from ARN).
     - Scan images: `aws ecr start-image-scan`.
  2. Monitoring:
     - Enable CloudWatch EKS metrics, set alarm (“CPU > 80%”).
     - Deploy X-Ray daemon, trace API calls.
     - Create Dashboard: `aws cloudwatch put-dashboard` (CPU, latency, “inventory updates/min”).
  3. Pen Test: Run `kube-hunter`, fix findings (e.g., open ports).
- **Verification**: HTTPS works, secrets secured, dashboard live, `kube-hunter` clean.

---

### Day 4: Chaos Crunch - Survive Outages/Spikes, Write a Runbook
- **Objective**: Test EKS resilience under chaos and document a runbook.
- **Theoretical Deep Dive**:
  - **Chaos Engineering**: Injecting failures (pod kills, spikes) to validate HA and scaling (AWS Well-Architected Reliability).
  - **Runbook**: Step-by-step incident response guide (DevSecOps operational readiness).
  - **Best Practices**: HA, scaling, resilience documentation.
- **Practical Use Cases**:
  - **Netflix’s Chaos**: Crashes 10% of EKS pods for 247M subscribers (2023), recovers with HPA.
  - **Amazon’s Runbook**: Documents RDS failover for 1M+ customers (2022).
- **Tasks**:
  1. Chaos:
     - Kill 50% pods: `kubectl delete pod -l app=backend --force`.
     - Spike traffic: `ab -n 10000 -c 100 <alb-url>`.
  2. Monitor: CloudWatch/X-Ray tracks recovery, Karpenter scales pods/nodes.
  3. Runbook: `runbook.md` → “Pod Crash → Check Logs → Scale Up”.
- **Verification**: Recovers in <5 min, runbook resolves outage.

---

### Day 5: Prod Push - Demo to “Execs,” Score on Resilience/Creativity
- **Objective**: Deploy to production, demo resilience and creativity, score the outcome.
- **Theoretical Deep Dive**:
  - **Production Deployment**: Rolling updates and blue-green for zero-downtime (AWS Well-Architected Operational Excellence).
  - **Resilience/Creativity**: Validating uptime and innovative metrics (DevSecOps maturity).
  - **Best Practices**: Zero-downtime, monitoring, resilience.
- **Practical Use Cases**:
  - **Walmart’s Prod Push**: Deploys EKS for 240M customers (2023), scoring 95% resilience.
  - **Netflix’s Creativity**: Demos “stream starts/sec” for 247M subscribers (2023).
- **Tasks**:
  1. Deploy:
     - Rolling update: `kubectl apply -f .` (probes ensure zero-downtime).
     - Blue-Green: Stage `v2` Deployment, switch ALB traffic.
  2. Chaos Test: Kill 50% pods, spike traffic.
  3. Demo: Show app, dashboard, recovery to “execs” (peers/instructors).
  4. Score: Resilience (uptime under 10K req/sec), Creativity (custom metric).
- **Verification**: App live, survives chaos, scores >90% (uptime, innovation).

---

## Learning Schedule (7-8 Hours/Day)
- **Day 1**:
  - **Theory (3h)**: Kubernetes architecture, tool swapping (CNCF, Gartner).
  - **Practice (4h)**: Design EKS with Graviton2/3 AZs, swap Jenkins → GitHub Actions.
- **Day 2**:
  - **Theory (3h)**: Microservices dev, EKS scaling (Docker, DORA).
  - **Practice (4h)**: Build/deploy frontend/backend with probes/limits.
- **Day 3**:
  - **Theory (3h)**: CI/CD, security (NIST, HashiCorp).
  - **Practice (4h)**: Automate with GitHub Actions/Helm, secure with RBAC/TLS.
- **Day 4**:
  - **Theory (3h)**: Chaos engineering, observability (Gartner, Chaos Monkey).
  - **Practice (4h)**: Test chaos, monitor with CloudWatch/X-Ray/dashboard.
- **Day 5**:
  - **Theory (3h)**: Prod deployment, resilience (DORA, IDC).
  - **Practice (4h)**: Push to prod, demo, score.

---

## Deliverables
- **Code**: `frontend/`, `backend/`, `terraform/eks.tf`, `.github/workflows/`, `helm/ecomm/`.
- **Docs**: `ecomm-architecture.md`, `runbook.md`.
- **Verification**: App at `<alb-url>` (HTTPS), survives chaos, monitored via dashboard.

---

## Why This Matters
- **Kubernetes Best Practices**: Fully integrates modularity, scaling, security, HA, observability, IaC, zero-downtime, and resilience.
- **DevSecOps Alignment**: Embeds automation, security, and monitoring (AWS Well-Architected, NIST 800-53).
- **Real-World Readiness**: Mirrors Amazon/Netflix standards, preparing learners for $1M+ impact roles.

