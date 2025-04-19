## Week 6: Capstone and Real-World Crunch
**Objective**: Synthesize Weeks 1-5 into a capstone project, tackling real-world DevSecOps challenges—planning, building, securing, surviving chaos, and delivering under pressure—to produce job-ready professionals.

- **Duration**: 5 days, ~7-8 hours each (~35-40 hours total).
- **Structure**: Theoretical Deep Dive (~40%) + Practical Use Cases/Implementation (~60%).

---

### Day 1: Capstone Kickoff - Plan Microservices, Swap a Tool Mid-Plan
- **Objective**: Plan a microservices architecture and adapt to mid-flight tool changes, mimicking real-world agility.
- **Theoretical Keyword Explanation**:
  - **Microservices Planning**: Designing loosely coupled, independently deployable services (e.g., inventory, payments) with scalability and security in mind.
    - **Context**: A DevSecOps shift from monoliths (2010s), aligning with AWS Well-Architected (Reliability, Scalability).
    - **Importance**: Enables 50% faster deployments (e.g., Gartner 2023), scales to millions of users, and supports resilience.
  - **Tool Swapping**: Replacing a planned tool (e.g., Jenkins → GitHub Actions) mid-process due to constraints or innovation.
    - **Context**: Reflects real-world pivots (e.g., Netflix’s Spinnaker adoption), testing adaptability.
    - **Importance**: Prepares pros for vendor shifts, saving 20-30% time/cost (e.g., IDC 2023).
- **Practical Use Cases**:
  - **Amazon’s Microservices Pivot**: Amazon planned ECS for retail but swapped to EKS mid-2022 for Kubernetes flexibility, supporting 1M+ customers’ 375M items sold (2023).
    - **Example**: Shifted CI tool from Bamboo to Jenkins → 30% faster builds.
  - **Netflix’s Tool Swap**: Netflix swapped Travis CI for Spinnaker mid-plan (2015), cutting deployment time by 40% for 247M subscribers.
- **Tasks**:
  - Plan microservices (inventory, payments, frontend) on EKS.
  - Start with Jenkins for CI/CD, swap to GitHub Actions mid-plan (e.g., after 2 hours).
  - Document trade-offs (e.g., Jenkins plugins vs. GitHub Actions simplicity).
- **Verification**: Architecture diagram, updated CI/CD plan with swap rationale.

---

### Day 2: Build and Automate - CI/CD + EKS, Scale for a DDoS
- **Objective**: Build the microservices platform with CI/CD automation and scale it to survive a simulated DDoS attack.
- **Theoretical Keyword Explanation**:
  - **CI/CD + EKS**: Continuous Integration/Deployment pipelines deploying to AWS Elastic Kubernetes Service (EKS) for containerized microservices.
    - **Context**: A DevSecOps cornerstone (EKS since 2018), aligning with AWS Well-Architected (Performance Efficiency).
    - **Importance**: Reduces deployment time by 70% (e.g., DORA 2023), scales to 1000s of pods, and ensures consistency.
  - **DDoS Scaling**: Dynamically scaling resources (e.g., pods, ALB) to mitigate Distributed Denial-of-Service attacks.
    - **Context**: Critical for DevSecOps resilience (e.g., 2021 AWS Shield growth), NIST 800-53 (SC-5: DoS Protection).
    - **Importance**: Handles 10x traffic spikes (e.g., Gartner 2023), saving $1M+ in downtime.
- **Practical Use Cases**:
  - **Walmart’s CI/CD Scale**: Walmart uses Jenkins + EKS to deploy 100+ microservices for 240M customers, scaling pods 5x during Black Friday (2022), surviving 20K+ req/sec.
    - **Example**: HPA (Horizontal Pod Autoscaler) → 50 pods → Stable.
  - **Amazon’s DDoS Defense**: Amazon scales ALB/EKS for 1M+ customers during a 2023 DDoS, saving $5M+ with Shield Advanced.
- **Tasks**:
  - Deploy EKS cluster (`eksctl create cluster --name ecomm`).
  - Set up GitHub Actions CI/CD for microservices (e.g., Node.js inventory app).
  - Configure HPA and AWS Shield, simulate DDoS with `stress` tool on EC2.
- **Verification**: App deploys in <5 min, scales to 10 pods under load, no downtime.

---

### Day 3: Secure and Monitor - Add Encryption/Alarms, Pass a Pen Test
- **Objective**: Secure the platform with encryption and monitoring, passing a penetration test to ensure DevSecOps readiness.
- **Theoretical Keyword Explanation**:
  - **Encryption/Alarms**: Implementing TLS, data-at-rest encryption (e.g., KMS), and CloudWatch alarms for security/performance monitoring.
    - **Context**: A DevSecOps must (KMS since 2014), AWS Well-Architected (Security Pillar), NIST 800-53 (SC-13: Cryptography).
    - **Importance**: Prevents 99% of data breaches (e.g., Verizon 2023), scales to petabytes, and ensures uptime (e.g., 99.9%).
  - **Penetration Testing**: Simulating attacks (e.g., SQL injection) to validate security controls.
    - **Context**: Industry standard (OWASP since 2001), critical for DevSecOps compliance.
    - **Importance**: Identifies 80% of vulns pre-prod (e.g., SANS 2023), saving $1M+ in breach costs.
- **Practical Use Cases**:
  - **Amazon’s TLS Rollout**: Amazon encrypts S3/ALB traffic for 1M+ customers (2023), adding CloudWatch alarms to catch 5% latency spikes, saving $2M+.
    - **Example**: Alarm: “Errors > 5” → Notify → Fixed.
  - **Airbnb’s Pen Test**: Airbnb passes OWASP ZAP tests for 100M+ bookings, fixing XSS in 2022, ensuring trust.
- **Tasks**:
  - Add TLS to ALB, encrypt RDS/S3 with KMS.
  - Set CloudWatch alarms (e.g., “CPU > 80%”).
  - Run OWASP ZAP pen test on frontend/API, fix findings (e.g., input sanitization).
- **Verification**: HTTPS works, data encrypted, alarms trigger, ZAP reports clean.

---

### Day 4: Chaos Crunch - Survive Outages/Spikes, Write a Runbook
- **Objective**: Test resilience under chaos (outages, spikes) and document a runbook for incident response.
- **Theoretical Keyword Explanation**:
  - **Chaos Engineering**: Intentionally injecting failures (e.g., pod crashes, traffic spikes) to test system resilience.
    - **Context**: Pioneered by Netflix (Chaos Monkey, 2011), a DevSecOps practice (AWS Well-Architected: Reliability).
    - **Importance**: Ensures 99.99% uptime (e.g., Netflix 2023), scales to millions of users, and reduces MTTR by 50%.
  - **Runbook**: A documented guide for diagnosing and resolving incidents (e.g., “DB down → Failover”).
    - **Context**: Standard in DevSecOps ops (ITIL since 1980s), critical for team handoff.
    - **Importance**: Cuts recovery time by 70% (e.g., PagerDuty 2023), ensures consistency.
- **Practical Use Cases**:
  - **Netflix’s Chaos Test**: Netflix crashes 10% of pods for 247M subscribers (2023), surviving with HPA, saving $5M+ in outages.
    - **Example**: Chaos: Kill pod → Auto-recover → Stable.
  - **Amazon’s Runbook**: Amazon’s 2022 RDS outage runbook (“Failover in 5 min”) ensures 1M+ customers’ uptime.
- **Tasks**:
  - Inject chaos: Kill 50% EKS pods, spike traffic with `ab -n 10000`.
  - Monitor with CloudWatch/X-Ray, adjust HPA/Karpenter.
  - Write runbook (`runbook.md`): “Pod Failure → Check Logs → Scale Up”.
- **Verification**: System recovers in <5 min, runbook resolves simulated DB crash.

---

### Day 5: Prod Push - Demo to “Execs,” Score on Resilience/Creativity
- **Objective**: Deploy to production, present to simulated executives, and evaluate resilience/creativity.
- **Theoretical Keyword Explanation**:
  - **Production Push**: Deploying a fully tested app to a live environment with zero-downtime strategies (e.g., blue-green).
    - **Context**: A DevSecOps culmination (e.g., AWS CodeDeploy since 2014), AWS Well-Architected (Operational Excellence).
    - **Importance**: Achieves 99.9% success rate (e.g., DORA 2023), scales to enterprise, and proves readiness.
  - **Resilience/Creativity Scoring**: Assessing system uptime under load and innovative solutions (e.g., custom metrics).
    - **Context**: Reflects real-world exec reviews (e.g., Amazon’s PRFAQ), testing DevSecOps maturity.
    - **Importance**: Prepares pros for scrutiny, driving $1M+ business value (e.g., IDC 2023).
- **Practical Use Cases**:
  - **Walmart’s Prod Demo**: Walmart deploys 100+ microservices for 240M customers (2023), scoring 95% resilience with auto-scaling, earning exec approval.
    - **Example**: Demo: 10K req/sec → No downtime → Funded.
  - **Netflix’s Creative Metrics**: Netflix pitches custom “stream starts/sec” dashboard (2023), securing $10M+ for 247M subscribers’ growth.
- **Tasks**:
  - Deploy to prod with blue-green via GitHub Actions/EKS.
  - Demo to “execs” (peers/instructors): Show app, metrics, chaos recovery.
  - Score: Resilience (uptime under 10K req/sec), Creativity (e.g., custom “inventory updates/min”).
- **Verification**: App live, demo runs 10 min, scores >90% on rubric (uptime, innovation).

---

## Learning Schedule (7-8 Hours/Day)
- **Day 1**:
  - **Theory (3h)**: Microservices planning, tool swapping (slides, AWS docs).
  - **Practice (4h)**: Diagram architecture, swap Jenkins → GitHub Actions.
- **Day 2**:
  - **Theory (3h)**: CI/CD + EKS, DDoS scaling (DORA 2023, NIST).
  - **Practice (4h)**: Build pipeline, deploy EKS, simulate DDoS.
- **Day 3**:
  - **Theory (3h)**: Encryption/alarms, pen testing (OWASP, Verizon).
  - **Practice (4h)**: Secure app, set alarms, run ZAP.
- **Day 4**:
  - **Theory (3h)**: Chaos engineering, runbooks (Netflix Chaos, ITIL).
  - **Practice (4h)**: Inject chaos, write runbook, test recovery.
- **Day 5**:
  - **Theory (3h)**: Prod push, resilience/creativity (DORA, IDC).
  - **Practice (4h)**: Deploy live, demo, score results.

---

## Why This Matters
- **Theoretical Value**: Covers end-to-end DevSecOps—planning, automation, security, resilience, delivery—preparing pros for real-world complexity.
- **Practical Impact**: Use cases from Amazon, Netflix, and Walmart show $1M+ savings and 99.9% uptime for millions, mirroring enterprise stakes.
- **DevSecOps Alignment**: Integrates AWS Well-Architected, NIST 800-53, and industry trends (e.g., chaos engineering, microservices), ensuring job-readiness.
- **Capstone Significance**: Tests all prior weeks (security, cost, monitoring) under pressure, producing portfolio-worthy skills.

