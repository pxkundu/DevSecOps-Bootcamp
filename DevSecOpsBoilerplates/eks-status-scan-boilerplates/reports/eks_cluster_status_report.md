# EKS Cluster Status Report

**Generated on**: {{GENERATION_DATE}}

**Cluster Name**: {{EKS_CLUSTER_NAME}}

**Region**: {{AWS_REGION}}

## Cluster Overview
| Attribute | Value | Status | Notes |
|-----------|-------|--------|-------|
| Version | {{VERSION}} | {{VERSION_STATUS}} | Upgrade if outdated |
| Endpoint Public Access | {{ENDPOINT_PUBLIC}} | {{ENDPOINT_STATUS}} | Disable if not needed |
| Authentication Mode | {{AUTH_MODE}} | {{AUTH_STATUS}} | Use API_AND_CONFIG_MAP |
| Status | {{STATUS}} | {{STATUS_STATUS}} | Ensure cluster is ACTIVE |

## Node Status
| Metric | Value | Status | Notes |
|--------|-------|--------|-------|
| Node Count | {{NODE_COUNT}} | {{NODE_COUNT_STATUS}} | Ensure sufficient nodes |
| Instance Types | {{NODE_TYPES}} | OK | Verify sizing |
| Unhealthy Nodes | {{UNHEALTHY_NODES}} | {{UNHEALTHY_STATUS}} | Investigate unhealthy nodes |

## Pod Status
| Metric | Value | Status | Notes |
|--------|-------|--------|-------|
| Pod Count | {{POD_COUNT}} | {{POD_COUNT_STATUS}} | Ensure pods are running |
| Namespaces | {{NAMESPACES}} | OK | Verify namespace usage |
| Failed Pods | {{FAILED_PODS}} | {{FAILED_STATUS}} | Investigate failed pods |

## Networking
| Metric | Value | Status | Notes |
|--------|-------|--------|-------|
| VPC ID | {{VPC_ID}} | OK | Verify VPC configuration |
| Subnets | {{SUBNETS}} | OK | Ensure sufficient IPs |
| Security Groups | {{SECURITY_GROUPS}} | OK | Restrict inbound rules |

## Security
| Metric | Value | Status | Notes |
|--------|-------|--------|-------|
| OIDC Provider | {{IAM_ROLE}} | OK | Ensure secure IAM roles |
| RBAC Roles | {{RBAC_ROLES}} | {{RBAC_STATUS}} | Limit overly permissive roles |
| Network Policies | {{NETWORK_POLICIES}} | {{NETWORK_POLICY_STATUS}} | Implement network policies |

## Logging and Monitoring
| Metric | Value | Status | Notes |
|--------|-------|--------|-------|
| Cluster Logging | {{LOGGING}} | {{LOGGING_STATUS}} | Enable control plane logging |
| CloudWatch Alarms | {{CLOUDWATCH}} | {{CLOUDWATCH_STATUS}} | Set up alarms for metrics |

## Critical Issues
- {{ISSUE_1}}
- {{ISSUE_2}}

## Recommendations
- {{RECOMMENDATION_1}}
- {{RECOMMENDATION_2}}

**Notes**:
- Review critical issues and apply recommendations to improve cluster health.
- Enable additional tools like kubescape for pod security scanning.
- Schedule this script to run periodically for ongoing monitoring.
