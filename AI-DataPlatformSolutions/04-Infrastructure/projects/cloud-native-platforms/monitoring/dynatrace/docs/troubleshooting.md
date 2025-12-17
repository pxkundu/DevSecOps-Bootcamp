# 🔧 Troubleshooting Guide

## 📋 Overview

This guide helps diagnose and resolve common issues with the Dynatrace AWS Serverless monitoring solution.

## 🔍 Diagnostic Flowchart

```
Problem Detected
       │
       ▼
┌─────────────────────┐
│ Is Dynatrace UI     │──No──▶ Check network/DNS
│ accessible?         │        Check Dynatrace status page
└─────────┬───────────┘
          │ Yes
          ▼
┌─────────────────────┐
│ Is AWS integration  │──No──▶ See "AWS Integration Issues"
│ connected?          │
└─────────┬───────────┘
          │ Yes
          ▼
┌─────────────────────┐
│ Are Lambda metrics  │──No──▶ See "CloudWatch Metrics Issues"
│ appearing?          │
└─────────┬───────────┘
          │ Yes
          ▼
┌─────────────────────┐
│ Are traces          │──No──▶ See "Lambda Extension Issues"
│ appearing?          │
└─────────┬───────────┘
          │ Yes
          ▼
┌─────────────────────┐
│ Are alerts          │──No──▶ See "Alerting Issues"
│ working?            │
└─────────────────────┘
```

## 🔌 AWS Integration Issues

### Problem: AWS integration shows "Disconnected"

**Symptoms:**
- AWS integration status shows disconnected in Dynatrace
- No AWS metrics appearing
- Error messages in integration settings

**Diagnosis:**
```bash
# Verify IAM role exists
aws iam get-role --role-name dynatrace-monitoring-role

# Verify trust policy
aws iam get-role --role-name dynatrace-monitoring-role \
  --query 'Role.AssumeRolePolicyDocument'

# Verify permissions
aws iam list-attached-role-policies \
  --role-name dynatrace-monitoring-role
```

**Solutions:**

1. **External ID mismatch:**
   ```bash
   # Get external ID from Dynatrace Settings > Cloud and virtualization > AWS
   # Update IAM role trust policy with correct external ID
   
   aws iam update-assume-role-policy \
     --role-name dynatrace-monitoring-role \
     --policy-document file://trust-policy.json
   ```

2. **Missing permissions:**
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Action": [
           "cloudwatch:GetMetricStatistics",
           "cloudwatch:ListMetrics",
           "tag:GetResources",
           "lambda:ListFunctions",
           "lambda:ListTags",
           "dynamodb:ListTables",
           "dynamodb:DescribeTable",
           "sqs:ListQueues",
           "sqs:GetQueueAttributes",
           "sns:ListTopics",
           "sns:GetTopicAttributes"
         ],
         "Resource": "*"
       }
     ]
   }
   ```

3. **Region not enabled:**
   - Check if all required regions are enabled in AWS integration settings
   - Verify services are deployed in monitored regions

### Problem: Partial metrics missing

**Symptoms:**
- Some AWS services show metrics, others don't
- Specific functions or tables not appearing

**Diagnosis:**
```bash
# Check if CloudWatch metrics exist for the resource
aws cloudwatch list-metrics \
  --namespace AWS/Lambda \
  --dimensions Name=FunctionName,Value=your-function-name

# Verify resource tags (if using tag filtering)
aws lambda list-tags --resource arn:aws:lambda:region:account:function:name
```

**Solutions:**

1. **Service not enabled in integration:**
   - Go to Settings > Cloud and virtualization > AWS
   - Edit your connection
   - Ensure required services are checked

2. **Tag filtering active:**
   - Check if "Monitor only tagged resources" is enabled
   - Verify resources have correct tags

3. **CloudWatch metrics delayed:**
   - AWS metrics can take 5-15 minutes to appear
   - Some metrics only appear after resource usage

## 🔧 Lambda Extension Issues

### Problem: Extension not loading

**Symptoms:**
- No Dynatrace logs in CloudWatch
- Function appears as unmonitored
- No traces or code-level metrics

**Diagnosis:**
```bash
# Check CloudWatch Logs for extension output
aws logs filter-log-events \
  --log-group-name "/aws/lambda/your-function" \
  --filter-pattern "dynatrace"

# Verify layer is attached
aws lambda get-function --function-name your-function \
  --query 'Configuration.Layers'

# Check environment variables
aws lambda get-function-configuration --function-name your-function \
  --query 'Environment.Variables'
```

**Solutions:**

1. **Layer not attached:**
   ```bash
   aws lambda update-function-configuration \
     --function-name your-function \
     --layers arn:aws:lambda:us-east-1:725887861453:layer:Dynatrace_OneAgent:1
   ```

2. **Missing environment variables:**
   ```bash
   aws lambda update-function-configuration \
     --function-name your-function \
     --environment "Variables={
       DT_TENANT=your-tenant-id,
       DT_CLUSTER_ID=-1,
       DT_CONNECTION_BASE_URL=https://your-tenant.live.dynatrace.com,
       DT_CONNECTION_AUTH_TOKEN=dt0c01.XXX.YYY,
       AWS_LAMBDA_EXEC_WRAPPER=/opt/dynatrace
     }"
   ```

3. **Invalid token:**
   ```bash
   # Test token validity
   curl -s -o /dev/null -w "%{http_code}" \
     "https://your-tenant.live.dynatrace.com/api/v1/deployment/installer/agent/connectioninfo" \
     -H "Authorization: Api-Token YOUR_PAAS_TOKEN"
   # Should return 200
   ```

### Problem: Extension timeout/slow startup

**Symptoms:**
- Lambda function timing out
- Very slow cold starts
- Extension initialization errors

**Diagnosis:**
```bash
# Check function timeout and memory
aws lambda get-function-configuration --function-name your-function \
  --query '{Timeout: Timeout, MemorySize: MemorySize}'

# Look for timeout errors in logs
aws logs filter-log-events \
  --log-group-name "/aws/lambda/your-function" \
  --filter-pattern "Task timed out"
```

**Solutions:**

1. **Increase function timeout:**
   ```bash
   # Extension needs ~500ms for cold start
   aws lambda update-function-configuration \
     --function-name your-function \
     --timeout 30
   ```

2. **Increase memory allocation:**
   ```bash
   # More memory = more CPU = faster extension load
   aws lambda update-function-configuration \
     --function-name your-function \
     --memory-size 512
   ```

3. **Check network connectivity:**
   - If Lambda is in VPC, ensure NAT gateway or VPC endpoints
   - Verify security groups allow outbound HTTPS

### Problem: Traces not correlated

**Symptoms:**
- Individual service traces visible
- No end-to-end transaction view
- Broken trace chains

**Diagnosis:**
- Check if trace headers are being propagated
- Verify all services in chain have extension enabled

**Solutions:**

1. **Enable OpenTelemetry integration:**
   ```bash
   DT_OPEN_TELEMETRY_ENABLE_INTEGRATION="true"
   ```

2. **Propagate trace context manually:**
   ```python
   import os
   
   def handler(event, context):
       # Get trace headers from incoming request
       headers = event.get('headers', {})
       
       # Forward to downstream calls
       downstream_headers = {
           'traceparent': headers.get('traceparent'),
           'tracestate': headers.get('tracestate'),
           'x-dynatrace': headers.get('x-dynatrace')
       }
   ```

## 📊 Metrics Issues

### Problem: Custom metrics not appearing

**Symptoms:**
- No custom metrics in Data Explorer
- Metric ingestion appears to work but no data visible

**Diagnosis:**
```bash
# Test metric ingestion
curl -X POST "${DT_TENANT_URL}/api/v2/metrics/ingest" \
  -H "Authorization: Api-Token ${DT_API_TOKEN}" \
  -H "Content-Type: text/plain" \
  -d "test.metric 42"

# Check API response - should be 202
```

**Solutions:**

1. **Wait for processing:**
   - Metrics can take 1-2 minutes to appear
   - Check Data Explorer with correct time range

2. **Check metric format:**
   ```
   # Correct format
   metric.name,dimension=value 42 1640000000000
   
   # Common errors:
   metric name     # No spaces in metric name
   metric,dim=     # Empty dimension value
   metric value    # Missing value
   ```

3. **Verify token permissions:**
   - Token needs `metrics.ingest` scope

### Problem: High cardinality warnings

**Symptoms:**
- Dynatrace showing cardinality warnings
- Metrics being dropped
- DDU consumption spikes

**Solutions:**

1. **Review dimensions:**
   ```python
   # Bad: High cardinality
   send_metric("api.requests", 1, dimensions={
       "user_id": user_id,  # Millions of users = millions of series
       "request_id": uuid  # Unique per request
   })
   
   # Good: Bounded cardinality
   send_metric("api.requests", 1, dimensions={
       "endpoint": "/api/orders",  # Limited endpoints
       "method": "POST",  # 4-5 HTTP methods
       "status_class": "2xx"  # 5 status classes
   })
   ```

2. **Use aggregation:**
   - Aggregate at source before sending
   - Use percentiles instead of individual values

## 🚨 Alerting Issues

### Problem: Alerts not firing

**Symptoms:**
- Conditions met but no alerts
- No notifications received

**Diagnosis:**
```bash
# Check alerting profile configuration
curl -s "${DT_TENANT_URL}/api/config/v1/alertingProfiles" \
  -H "Authorization: Api-Token ${DT_API_TOKEN}" | jq

# Check notification channels
curl -s "${DT_TENANT_URL}/api/config/v1/notifications" \
  -H "Authorization: Api-Token ${DT_API_TOKEN}" | jq
```

**Solutions:**

1. **Check alerting profile rules:**
   - Verify severity levels are enabled
   - Check delay settings
   - Verify management zone filter

2. **Test notification channel:**
   - Use test button in Dynatrace UI
   - Verify webhook URLs are accessible

3. **Check time filters:**
   - Alerts might be suppressed during maintenance windows

### Problem: Too many alerts (noise)

**Symptoms:**
- Alert fatigue
- Many false positives
- Repeated alerts for same issue

**Solutions:**

1. **Adjust thresholds:**
   ```json
   {
     "threshold": {
       "type": "BASELINE",
       "sensitivity": "MEDIUM"
     }
   }
   ```

2. **Add dampening:**
   ```json
   {
     "samples": 5,
     "violatingSamples": 3,
     "dealertingSamples": 5
   }
   ```

3. **Use alert grouping:**
   - Group related alerts
   - Configure proper inhibition rules

## 🔐 Authentication Issues

### Problem: API token errors

**Symptoms:**
- 401 Unauthorized errors
- "Invalid token" messages
- API calls failing

**Diagnosis:**
```bash
# Test token validity
curl -s -o /dev/null -w "%{http_code}" \
  "${DT_TENANT_URL}/api/v2/entities?pageSize=1" \
  -H "Authorization: Api-Token ${DT_API_TOKEN}"
# Should return 200
```

**Solutions:**

1. **Token expired:**
   - Create new token in Dynatrace UI
   - Update all configurations

2. **Missing permissions:**
   - Check token scopes match required operations
   - Add missing scopes to token

3. **Wrong token type:**
   - API Token for configuration/queries
   - PaaS Token for OneAgent/Extension

## 🌐 Network Issues

### Problem: Lambda in VPC can't reach Dynatrace

**Symptoms:**
- Extension timeout errors
- "Connection refused" in logs
- No data from VPC Lambda functions

**Diagnosis:**
```bash
# Check VPC configuration
aws lambda get-function-configuration --function-name your-function \
  --query 'VpcConfig'

# Check NAT Gateway
aws ec2 describe-nat-gateways \
  --filter Name=state,Values=available
```

**Solutions:**

1. **Add NAT Gateway:**
   - Lambda in private subnet needs NAT for internet access
   - Ensure route table points to NAT Gateway

2. **Use VPC Endpoints:**
   ```bash
   # Create VPC endpoint for Dynatrace (via PrivateLink)
   # Contact Dynatrace support for endpoint service name
   ```

3. **Check Security Groups:**
   ```bash
   # Allow outbound HTTPS
   aws ec2 authorize-security-group-egress \
     --group-id sg-xxx \
     --protocol tcp \
     --port 443 \
     --cidr 0.0.0.0/0
   ```

## 📝 Log Collection Issues

### Problem: Logs not appearing in Dynatrace

**Symptoms:**
- CloudWatch logs exist
- No logs visible in Dynatrace Log Viewer

**Solutions:**

1. **Enable log forwarding:**
   ```bash
   # Deploy log forwarder Lambda
   # See activegate/log-forwarding for templates
   ```

2. **Check log volume:**
   - Log ingestion has DDU costs
   - Verify log ingestion is enabled in license

3. **Configure log patterns:**
   - Set up log processing rules
   - Configure structured log parsing

## 🛠️ Useful Diagnostic Commands

### Quick Health Check Script

```bash
#!/bin/bash
# diagnostic.sh - Quick Dynatrace health check

echo "=== Dynatrace Diagnostic Script ==="
echo ""

# Check API connectivity
echo -n "API Connectivity: "
status=$(curl -s -o /dev/null -w "%{http_code}" \
  "${DT_TENANT_URL}/api/v2/entities?pageSize=1" \
  -H "Authorization: Api-Token ${DT_API_TOKEN}")
if [ "$status" = "200" ]; then
  echo "✓ OK"
else
  echo "✗ Failed (HTTP $status)"
fi

# Check AWS integration count
echo -n "AWS Integrations: "
count=$(curl -s "${DT_TENANT_URL}/api/config/v1/aws/credentials" \
  -H "Authorization: Api-Token ${DT_API_TOKEN}" | jq '.values | length')
echo "$count configured"

# Check Lambda functions discovered
echo -n "Lambda Functions: "
count=$(curl -s "${DT_TENANT_URL}/api/v2/entities?entitySelector=type(AWS_LAMBDA_FUNCTION)&pageSize=1" \
  -H "Authorization: Api-Token ${DT_API_TOKEN}" | jq '.totalCount')
echo "$count discovered"

# Check active problems
echo -n "Active Problems: "
count=$(curl -s "${DT_TENANT_URL}/api/v2/problems?problemSelector=status(\"open\")" \
  -H "Authorization: Api-Token ${DT_API_TOKEN}" | jq '.totalCount')
echo "$count open"

echo ""
echo "=== Diagnostic Complete ==="
```

## 📚 Additional Resources

- [Dynatrace Support Portal](https://support.dynatrace.com/)
- [Dynatrace Community](https://community.dynatrace.com/)
- [AWS Lambda Troubleshooting](https://docs.aws.amazon.com/lambda/latest/dg/troubleshooting.html)
- [CloudWatch Logs Insights Queries](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CWL_QuerySyntax.html)

---

Still stuck? Open a support ticket with Dynatrace including:
1. Tenant ID
2. Affected Lambda function ARNs
3. CloudWatch log excerpts
4. This diagnostic script output

