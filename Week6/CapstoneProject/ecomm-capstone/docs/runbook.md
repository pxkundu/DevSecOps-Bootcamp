# E-commerce Platform Runbook

## Overview
This runbook documents recovery procedures for the Secure, Scalable Microservices-Based E-commerce Platform on AWS EKS, including RCA and postmortem processes.

## Chaos Scenarios

### 1. Pod Failure (50% Outage)
- **Description**: 50% of frontend or backend pods are terminated.
- **Symptoms**:
  - 503 Service Unavailable errors on ALB URL.
  - CloudWatch shows reduced pod count and CPU spikes.
  - X-Ray traces indicate increased latency.
- **Recovery Steps**:
  1. Check pod status: `kubectl get pods -n prod`
  2. View logs: `kubectl logs -l app=frontend -n prod` (or backend)
  3. Verify HPA scaling: `kubectl get hpa -n prod`
  4. Confirm Karpenter nodes: `kubectl get nodes`
  5. Monitor CloudWatch dashboard for recovery (<5 min).
- **Root Cause Analysis (RCA)**:
  1. Check logs for crash reasons: `kubectl logs <pod-name> -n prod`
  2. Analyze X-Ray traces for upstream failures.
  3. Review CloudWatch CPU/memory to identify resource exhaustion.
- **Expected Outcome**: Pods reschedule, service restores in <5 min.

### 2. Traffic Spike (DDoS-like Load)
- **Description**: 10,000 requests with 100 concurrent users hit the ALB.
- **Symptoms**:
  - Increased latency on ALB URL.
  - CloudWatch CPU > 80%, pod count rises.
  - X-Ray shows backend bottlenecks.
- **Recovery Steps**:
  1. Simulate spike: `ab -n 10000 -c 100 <alb-url>`
  2. Monitor scaling: `kubectl get hpa -n prod`
  3. Check nodes: `kubectl get nodes`
  4. Review CloudWatch metrics and X-Ray traces.
  5. Verify stability post-spike (latency <1s).
- **Root Cause Analysis (RCA)**:
  1. Check X-Ray for latency bottlenecks (e.g., /orders).
  2. Analyze CloudWatch 'OrderLatency' metric for spikes.
  3. Review pod logs for throttling or errors.
- **Expected Outcome**: System scales up, stabilizes, then scales down.

## General Troubleshooting
- **Logs**: `kubectl logs <pod-name> -n prod`
- **Events**: `kubectl get events -n prod`
- **Dashboard**: Check CloudWatch for CPU, memory, orders/min, latency, errors.

## Postmortem Template
- **Incident Summary**: [Brief description]
- **Timeline**: [Start time, detection, resolution]
- **Root Cause**: [e.g., Backend overload from traffic spike]
- **Impact**: [e.g., 5 min downtime, 10% error rate]
- **Resolution**: [e.g., HPA scaled pods to 10]
- **Lessons Learned**: [e.g., Adjust HPA threshold]
- **Action Items**: [e.g., Add latency alarm]
