# 🏆 Dynatrace AWS Serverless Monitoring Best Practices

## 📋 Overview

This guide outlines best practices for implementing and maintaining Dynatrace monitoring for AWS serverless applications. Following these practices ensures optimal observability, cost efficiency, and operational excellence.

## 🎯 Instrumentation Best Practices

### 1. Lambda Extension Configuration

#### ✅ Do's

```yaml
# Recommended Lambda configuration
Environment:
  Variables:
    # Use Secrets Manager for tokens
    DT_CONNECTION_AUTH_TOKEN: "sm://dynatrace/config:auth_token"
    
    # Set appropriate log level for environment
    DT_LOGLEVELCON: "warning"  # Production
    
    # Enable OpenTelemetry integration
    DT_OPEN_TELEMETRY_ENABLE_INTEGRATION: "true"
    
    # Add meaningful custom properties
    DT_CUSTOM_PROP: "team=platform service=order-api version=v2.3.1"
```

#### ❌ Don'ts

```yaml
# Anti-patterns to avoid
Environment:
  Variables:
    # Don't hardcode tokens
    DT_CONNECTION_AUTH_TOKEN: "dt0c01.actual.token.value"  # ❌
    
    # Don't use debug in production
    DT_LOGLEVELCON: "debug"  # ❌ for production
```

### 2. Cold Start Optimization

Track and minimize cold starts for better performance:

```python
# Python Lambda with cold start awareness
import json
from datetime import datetime

# Module-level initialization (runs during cold start)
initialized_at = datetime.now()
is_cold_start = True

def handler(event, context):
    global is_cold_start
    
    # Add cold start attribute for Dynatrace
    if is_cold_start:
        # First invocation tracking
        is_cold_start = False
        
    # Your business logic
    return {"statusCode": 200}
```

### 3. Distributed Tracing

Ensure trace context propagation across services:

```python
# Python example with manual context propagation
import json
import requests

def handler(event, context):
    # Get incoming trace context from API Gateway
    headers = event.get('headers', {})
    trace_context = {
        'traceparent': headers.get('traceparent'),
        'tracestate': headers.get('tracestate')
    }
    
    # Propagate to downstream calls
    downstream_headers = {k: v for k, v in trace_context.items() if v}
    response = requests.post(
        'https://downstream-service.example.com/api',
        headers=downstream_headers,
        json={"data": "value"}
    )
    
    return {"statusCode": 200}
```

```javascript
// Node.js example
const axios = require('axios');

exports.handler = async (event) => {
    // Extract trace headers
    const traceHeaders = {
        'traceparent': event.headers?.traceparent,
        'tracestate': event.headers?.tracestate
    };
    
    // Forward to downstream service
    await axios.post('https://downstream-service.example.com/api', 
        { data: 'value' },
        { headers: traceHeaders }
    );
    
    return { statusCode: 200 };
};
```

## 📊 Metrics Best Practices

### 1. Golden Signals Focus

Prioritize the four golden signals for serverless:

| Signal | Lambda Metric | Target |
|--------|---------------|--------|
| **Latency** | Duration P95 | < 500ms |
| **Traffic** | Invocations | Monitor trends |
| **Errors** | Error rate | < 0.1% |
| **Saturation** | Concurrent executions | < 80% limit |

### 2. Custom Metrics Naming Convention

```
custom.<domain>.<entity>.<metric>
```

Examples:
- `custom.orders.checkout.duration`
- `custom.payments.processing.amount`
- `custom.users.authentication.failures`
- `custom.inventory.updates.count`

### 3. Dimension Guidelines

```python
# Good dimension choices
dimensions = {
    "environment": "production",        # Low cardinality
    "region": "us-east-1",              # Low cardinality
    "service_version": "v2.3.1",        # Low cardinality
    "http_method": "POST",              # Low cardinality
    "http_status_class": "2xx"          # Grouped status codes
}

# Avoid high-cardinality dimensions
avoid = {
    "user_id": "12345",                 # ❌ High cardinality
    "request_id": "abc-123-xyz",        # ❌ Unique per request
    "timestamp": "2024-01-15T10:30:00"  # ❌ Unique per second
}
```

## 🚨 Alerting Best Practices

### 1. Alert Hierarchy

Structure alerts by business impact:

```
Level 1: Business Critical (Page immediately)
├── Payment processing failures
├── User authentication unavailable
└── Critical data pipeline failures

Level 2: Service Degradation (Alert team, 5 min delay)
├── High error rates (> 5%)
├── Significant latency increase (> 3x baseline)
└── Resource exhaustion warnings

Level 3: Operational (Ticket/Email, 30 min delay)
├── Cold start increases
├── Minor performance degradation
└── Capacity planning warnings

Level 4: Informational (Dashboard only)
├── Deployment events
├── Scaling events
└── Configuration changes
```

### 2. Avoid Alert Fatigue

```json
{
  "name": "Smart Lambda Error Alert",
  "description": "Alert with proper baseline and dampening",
  "conditions": {
    "metric": "builtin:cloud.aws.lambda.errors",
    "threshold": {
      "type": "BASELINE",
      "sensitivity": "MEDIUM",
      "alertOnMissingData": false
    },
    "samples": 5,
    "violatingSamples": 3,
    "dealertingSamples": 5
  }
}
```

### 3. Actionable Alerts

Every alert should answer:
- **What** is broken?
- **Where** is it happening?
- **Why** might it be happening?
- **How** to investigate further?

```json
{
  "alertTitle": "Lambda High Error Rate - {FunctionName}",
  "message": "## Problem\nError rate for {FunctionName} exceeded {Threshold}%.\n\n## Current Status\n- Error Rate: {ErrorRate}%\n- Invocations: {InvocationCount}\n- Duration P95: {DurationP95}ms\n\n## Investigation Steps\n1. Check [CloudWatch Logs](link)\n2. Review [Dynatrace Traces](link)\n3. Check recent deployments\n\n## Runbook\n[Lambda Error Investigation](link)"
}
```

## 📈 Dashboard Best Practices

### 1. Dashboard Hierarchy

```
Executive Dashboard
├── Business KPIs and trends
├── SLO status
└── Cost overview

Team Dashboard (per service/team)
├── Service health overview
├── Error rates and latency
├── Key transactions
└── Infrastructure utilization

Deep Dive Dashboard
├── Function-level metrics
├── Trace analysis
├── Log patterns
└── Dependency mapping
```

### 2. Dashboard Design Principles

```
Layout Best Practices:
┌─────────────────────────────────────────────────────────────┐
│  Overall Health Score    │    SLO Status    │   Alerts     │
│  (Single Value)          │  (Status Light)  │   (Count)    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│           Invocations Over Time (Line Chart)                │
│                                                             │
├──────────────────────────────┬──────────────────────────────┤
│    Error Rate (Line Chart)   │   Latency P95 (Line Chart)  │
│                              │                              │
├──────────────────────────────┴──────────────────────────────┤
│                                                             │
│           Top Functions by Errors (Table)                   │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│           Resource Utilization (Heatmap)                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 3. Use Markdown Tiles for Context

```markdown
## 📊 Lambda Performance Dashboard

**Purpose**: Monitor Lambda function performance and identify issues

**Key Metrics**:
- 🟢 Healthy: Error rate < 0.1%, P95 < 500ms
- 🟡 Warning: Error rate 0.1-1%, P95 500-1000ms
- 🔴 Critical: Error rate > 1%, P95 > 1000ms

**Contact**: Platform Team (#platform-oncall)
**Runbook**: [Lambda Troubleshooting](link)
```

## 🔐 Security Best Practices

### 1. Token Management

```bash
# Store tokens in AWS Secrets Manager
aws secretsmanager create-secret \
  --name "dynatrace/production/api-token" \
  --secret-string '{"token":"dt0c01.XXX.YYY"}' \
  --kms-key-id alias/dynatrace-secrets

# Reference in Lambda (with proper IAM)
DT_CONNECTION_AUTH_TOKEN="sm://dynatrace/production/api-token:token"
```

### 2. IAM Least Privilege

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DynatraceMinimalAccess",
      "Effect": "Allow",
      "Action": [
        "cloudwatch:GetMetricStatistics",
        "cloudwatch:ListMetrics",
        "tag:GetResources",
        "lambda:ListFunctions",
        "lambda:ListTags"
      ],
      "Resource": "*",
      "Condition": {
        "StringEquals": {
          "aws:RequestedRegion": ["us-east-1", "us-west-2"]
        }
      }
    }
  ]
}
```

### 3. Data Classification

```yaml
# Tag sensitive functions for special handling
DT_CUSTOM_PROP: "data_classification=pii processing_type=payment"

# Configure data masking in Dynatrace
sensitive_data_masking:
  enabled: true
  patterns:
    - name: "Credit Card"
      pattern: '\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b'
      replacement: "****-****-****-****"
    - name: "SSN"
      pattern: '\b\d{3}-\d{2}-\d{4}\b'
      replacement: "***-**-****"
```

## 💰 Cost Optimization

### 1. Data Ingestion Optimization

```yaml
# Configure sampling for high-volume functions
high_volume_functions:
  - name: "health-check-function"
    sampling_rate: 0.01  # 1% of traces
    metrics_only: true   # Skip full traces

  - name: "webhook-receiver"
    sampling_rate: 0.1   # 10% of traces
    
  - name: "payment-processor"
    sampling_rate: 1.0   # 100% - critical function
```

### 2. Log Management

```python
# Structured logging with appropriate levels
import logging
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)  # Not DEBUG in production

def handler(event, context):
    # Log only necessary information
    logger.info(json.dumps({
        "action": "order_created",
        "order_id": event.get("order_id"),
        "customer_tier": event.get("tier")
        # Don't log full request/response bodies
    }))
```

### 3. Metric Cardinality Control

```yaml
# Avoid high-cardinality metric explosions
good_dimensions:
  - environment: ["dev", "staging", "prod"]  # 3 values
  - region: ["us-east-1", "us-west-2", "eu-west-1"]  # 3 values
  - service: ["orders", "payments", "users"]  # Limited values

bad_dimensions:
  - user_id: unlimited  # ❌ Creates millions of time series
  - request_id: unlimited  # ❌ Unique per request
  - timestamp: unlimited  # ❌ Already in time series
```

## 🔄 Operational Excellence

### 1. Configuration as Code

```yaml
# Monaco project structure
monaco/
├── environments/
│   ├── dev.yaml
│   ├── staging.yaml
│   └── production.yaml
├── projects/
│   └── aws-serverless/
│       ├── dashboard/
│       ├── alerting-profile/
│       ├── management-zone/
│       └── slo/
└── deploy.sh
```

### 2. Change Management

```bash
# Always preview changes before applying
monaco deploy --dry-run --project aws-serverless --environment production

# Version control all configurations
git commit -m "feat(monitoring): Add DynamoDB throttling alert"

# Implement PR reviews for monitoring changes
```

### 3. Documentation

Maintain documentation for:
- Alert runbooks with investigation steps
- Dashboard explanations and usage guides
- Custom metric definitions and business context
- Escalation procedures and contacts

## 📋 Checklist for New Services

When adding a new serverless service to monitoring:

```markdown
## Pre-Deployment
- [ ] Add Dynatrace Lambda layer to functions
- [ ] Configure environment variables
- [ ] Set up IAM permissions for monitoring
- [ ] Define custom metrics requirements

## Monitoring Setup
- [ ] Verify function appears in Dynatrace
- [ ] Create service-specific dashboard
- [ ] Configure alerting profile
- [ ] Set up notification channels
- [ ] Define SLOs/SLIs

## Documentation
- [ ] Document service architecture
- [ ] Create alert runbooks
- [ ] Update team dashboard
- [ ] Train team on monitoring

## Validation
- [ ] Trigger test alerts
- [ ] Verify trace correlation
- [ ] Check metric accuracy
- [ ] Review dashboard utility
```

## 🎓 Learning Resources

1. **Dynatrace University**: Free online courses
2. **Dynatrace Community**: Forums and knowledge base
3. **AWS Well-Architected Labs**: Observability pillar
4. **SRE Books**: Google SRE and SRE Workbook

---

Following these best practices will help you build a robust, maintainable, and cost-effective monitoring solution for your AWS serverless applications.

