## Phase 4: Chaos Crunch - Survive Outages/Spikes, Write a Runbook

### Plan
1. **Objective**: Test the EKS cluster’s resilience against chaos scenarios (pod failures, traffic spikes) and document recovery procedures in a runbook.
2. **Duration**: Approximately 7-8 hours.
3. **Focus Areas**:
   - Simulate chaos: Kill 50% of pods and spike traffic to 10,000 requests.
   - Validate recovery: Ensure Horizontal Pod Autoscaler (HPA), Karpenter, and high availability (HA) mechanisms respond effectively.
   - Document a runbook: Create a step-by-step guide for diagnosing and resolving incidents.
4. **Approach**:
   - Build on Phases 1-3 (architecture, infrastructure, security/observability).
   - Use chaos engineering principles to stress-test the system.
   - Leverage industry-standard tools and practices (e.g., Chaos Monkey, AWS Well-Architected Reliability).
5. **Outcome**: A resilient EKS deployment that survives chaos with minimal downtime, supported by a comprehensive runbook.

---

### Learning Points
1. **Chaos Engineering Fundamentals**:
   - Understanding how to intentionally introduce failures (e.g., pod kills, traffic spikes) to test system resilience.
   - Learning the importance of HA and auto-scaling in Kubernetes (e.g., multi-AZ, HPA, Karpenter).
2. **DevSecOps Resilience**:
   - Grasping how observability (CloudWatch, X-Ray) aids in diagnosing chaos-induced issues.
   - Recognizing the value of documentation (runbook) for operational readiness and team handoff.
3. **Real-World Application**:
   - Applying chaos testing techniques used by Netflix (e.g., Chaos Monkey for 247M subscribers) and Amazon (e.g., 1M+ customers during Black Friday).
   - Learning to design systems that recover automatically, reducing manual intervention.
4. **Incident Management**:
   - Developing skills to analyze logs, metrics, and traces during outages.
   - Creating actionable recovery steps aligned with industry incident response practices (e.g., SRE runbooks).
5. **Industry Standards**:
   - Aligning with AWS Well-Architected Reliability Pillar (e.g., fault tolerance, recovery).
   - Meeting DORA metrics (e.g., mean-time-to-recover <5 min).

---

### Implemented Functionalities
1. **Chaos Simulation**:
   - **Pod Failure**: Killed 50% of frontend and backend pods to simulate outages.
   - **Traffic Spike**: Generated 10,000 requests using `ab` (Apache Benchmark) to mimic a DDoS-like scenario.
2. **Resilience Validation**:
   - **HPA**: Scaled pods from 5 to 10+ based on CPU > 80%.
   - **Karpenter**: Added nodes dynamically (e.g., from 2 to 4) under load.
   - **HA**: Ensured multi-AZ deployment and anti-affinity maintained availability.
3. **Observability Utilization**:
   - Monitored pod recovery and scaling via CloudWatch metrics (CPU, memory).
   - Tracked latency and errors during traffic spike with X-Ray traces.
4. **Runbook Creation**:
   - Documented chaos scenarios, symptoms (e.g., pod crashes, latency spikes), and recovery steps (e.g., check logs, scale manually if needed).
   - Included verification commands (e.g., `kubectl get pods`, CloudWatch dashboards).

---

### Detailed Design of Each Solution Component

#### 1. Chaos Simulation: Pod Failure
- **How We Think About It**: Simulate a realistic outage (e.g., hardware failure, human error) to test Kubernetes’ self-healing capabilities.
- **Design**:
  - Kill 50% of frontend and backend pods (e.g., 5 → 2 per service).
  - Use `kubectl delete pod -l app=frontend --force` and similar for backend.
- **Why**:
  - Validates Deployment controllers’ ability to reschedule pods (e.g., Netflix’s 10% pod kill tests, 2023).
  - Ensures HA across AZs prevents single-point failures (e.g., Amazon’s 99.99% uptime).
- **Industry Standard**: Chaos Monkey-style testing ensures resilience (Netflix’s 247M subscribers).

#### 2. Chaos Simulation: Traffic Spike
- **How We Think About It**: Mimic a DDoS or Black Friday surge to stress-test scaling mechanisms.
- **Design**:
  - Use `ab -n 10000 -c 100 <alb-url>` to generate 10,000 requests with 100 concurrent users.
  - Target frontend ALB endpoint to trigger backend load.
- **Why**:
  - Tests HPA and Karpenter under realistic load (e.g., Walmart’s 46M items, 2022).
  - Ensures system scales without downtime (e.g., Amazon’s 375M items sold, 2023).
- **Industry Standard**: Load testing aligns with AWS Well-Architected Performance Efficiency (e.g., 10K+ req/sec).

#### 3. Resilience Validation: HPA
- **How We Think About It**: Ensure pods scale automatically to handle increased demand or recover from failures.
- **Design**:
  - HPA configured (from Phase 2) to scale on CPU > 80%, min 2, max 10 pods.
  - Validate: Pods increase from 5 to 10+ during traffic spike.
- **Why**:
  - Maintains performance under load (e.g., Walmart’s 5x scaling).
  - Reduces manual intervention (e.g., DORA’s elite performers, 2023).
- **Industry Standard**: HPA is a Kubernetes staple (e.g., Google’s GKE for 1B+ users).

#### 4. Resilience Validation: Karpenter
- **How We Think About It**: Dynamically scale nodes to support pod growth during chaos.
- **Design**:
  - Karpenter (from Phase 2) adds nodes when pod scheduling fails (e.g., 2 → 4 nodes).
  - Validate: `kubectl get nodes` shows new nodes during spike.
- **Why**:
  - Ensures resource availability (e.g., Netflix’s elastic scaling).
  - Saves costs by scaling down post-chaos (e.g., 30% savings, Flexera 2023).
- **Industry Standard**: Cluster autoscaling mirrors AWS best practices (e.g., Amazon’s EKS).

#### 5. Resilience Validation: High Availability (HA)
- **How We Think About It**: Confirm multi-AZ and anti-affinity prevent downtime during outages.
- **Design**:
  - Pods spread across 3 AZs (from Phase 2) with anti-affinity rules.
  - Validate: Remaining pods (after 50% kill) stay online in different AZs.
- **Why**:
  - Guarantees 99.9% uptime (e.g., Amazon’s 1M+ customers).
  - Mitigates regional failures (e.g., AWS outage resilience).
- **Industry Standard**: Multi-AZ HA is a reliability cornerstone (AWS Well-Architected).

#### 6. Observability Utilization
- **How We Think About It**: Leverage Phase 3’s CloudWatch and X-Ray to monitor and diagnose chaos effects.
- **Design**:
  - CloudWatch tracks CPU/memory during pod kills and scaling.
  - X-Ray traces latency/errors during traffic spike.
  - Validate: Dashboards show recovery, traces pinpoint bottlenecks.
- **Why**:
  - Reduces MTTR by 50% (Gartner 2023).
  - Enables data-driven recovery (e.g., Netflix’s 17B+ hours).
- **Industry Standard**: Observability is critical for SRE (e.g., Google’s 1B+ user monitoring).

#### 7. Runbook Creation
- **How We Think About It**: Document chaos scenarios and recovery to ensure operational readiness and knowledge transfer.
- **Design**:
  - Sections: Scenario (e.g., pod crash), Symptoms (e.g., 503 errors), Steps (e.g., check logs, scale).
  - Include commands: `kubectl logs`, `kubectl get hpa`, CloudWatch dashboard URLs.
- **Why**:
  - Cuts recovery time by 70% with clear steps (e.g., Amazon’s SRE runbooks).
  - Prepares teams for incidents (e.g., Walmart’s 240M customer ops).
- **Industry Standard**: Runbooks are a DevSecOps/SRE staple (e.g., Google’s SRE handbook).

---

### Why This Phase is Industry-Standard and DevSecOps-Compliant
- **Kubernetes Best Practices**:
  - **Resilience**: HPA, Karpenter, HA (e.g., Netflix’s Chaos Monkey).
  - **Observability**: CloudWatch, X-Ray (e.g., Amazon’s 1M+ customer monitoring).
- **DevSecOps Principles**:
  - **Automation**: Self-healing via Kubernetes controllers (e.g., 90% less manual effort, DORA 2023).
  - **Reliability**: Chaos testing ensures uptime (e.g., AWS Well-Architected Reliability).
  - **Documentation**: Runbook aligns with operational excellence (e.g., Google SRE).
- **Model Project**: 
  - Teaches chaos engineering, a sought-after skill (e.g., $1M+ savings from downtime prevention).
  - Provides a practical, documented resilience strategy for learners.

---
