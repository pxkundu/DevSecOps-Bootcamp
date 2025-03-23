# Master-Slave Deep Dive

Notes on HA master setups, multi-region slaves, and optimizations for Jenkins.

## HA Master
- Active-passive setup with ELB and S3 sync.
- Failover in <30s.

## Multi-Region Slaves
- us-east-1 and us-west-2 with region-specific labels.
- Reduces latency by 20%.

## Optimizations
- Docker caching cuts build time by 50%.
- 4 executors per slave for concurrency.
