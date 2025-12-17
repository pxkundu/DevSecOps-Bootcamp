# ⚙️ Dynatrace Configuration Guide

## 📋 Overview

This guide provides detailed configuration options for the Dynatrace AWS Serverless monitoring solution. It covers all configurable components and their options.

## 🔧 Lambda Extension Configuration

### Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DT_TENANT` | Yes | - | Dynatrace tenant ID (e.g., `abc12345`) |
| `DT_CLUSTER_ID` | Yes | `-1` | Cluster ID (`-1` for SaaS) |
| `DT_CONNECTION_BASE_URL` | Yes | - | Full Dynatrace URL |
| `DT_CONNECTION_AUTH_TOKEN` | Yes | - | PaaS token for authentication |
| `AWS_LAMBDA_EXEC_WRAPPER` | Yes | - | Must be `/opt/dynatrace` |
| `DT_OPEN_TELEMETRY_ENABLE_INTEGRATION` | No | `false` | Enable OTLP integration |
| `DT_LOGLEVELCON` | No | `warning` | Log level: `debug`, `info`, `warning`, `error` |
| `DT_CUSTOM_PROP` | No | - | Custom properties (key=value pairs) |
| `DT_TAGS` | No | - | Custom tags for the service |
| `DT_INJECTION_RULES` | No | - | Custom injection rules |

### Log Level Configuration

```bash
# Development: Verbose logging
DT_LOGLEVELCON="debug"

# Staging: Moderate logging
DT_LOGLEVELCON="info"

# Production: Minimal logging (recommended)
DT_LOGLEVELCON="warning"
```

### Custom Properties

Add custom metadata to your Lambda functions:

```bash
# Format: key1=value1 key2=value2
DT_CUSTOM_PROP="team=platform cost_center=CC-1234 criticality=high"
```

These properties appear in Dynatrace service properties and can be used for filtering.

### Custom Tags

```bash
# Format: tag1 tag2=value
DT_TAGS="production payment-service tier=1"
```

### Trace Sampling Configuration

For high-volume functions, configure sampling:

```python
# In your Lambda code
import os
from opentelemetry import trace

# Set sampling rate (0.0 to 1.0)
# 0.1 = 10% of traces
os.environ["DT_SAMPLE_RATIO"] = "0.1"
```

## 📊 AWS Integration Configuration

### Monitored Services Configuration

Configure which AWS services to monitor and their polling intervals:

```json
{
  "name": "production-serverless",
  "label": "Production Serverless",
  "partitionType": "AWS_DEFAULT",
  "taggedOnly": false,
  "authenticationData": {
    "roleBasedAuthentication": {
      "iamRole": "arn:aws:iam::123456789012:role/dynatrace-monitoring-role",
      "accountId": "123456789012",
      "externalId": "your-external-id"
    }
  },
  "servicesMonitoringEnabled": true,
  "services": [
    {
      "name": "lambda",
      "monitoringEnabled": true,
      "metrics": {
        "resolution": "PT1M"
      }
    },
    {
      "name": "apigateway",
      "monitoringEnabled": true,
      "metrics": {
        "resolution": "PT1M"
      }
    },
    {
      "name": "dynamodb",
      "monitoringEnabled": true,
      "metrics": {
        "resolution": "PT5M"
      }
    },
    {
      "name": "sqs",
      "monitoringEnabled": true,
      "metrics": {
        "resolution": "PT1M"
      }
    },
    {
      "name": "sns",
      "monitoringEnabled": true,
      "metrics": {
        "resolution": "PT5M"
      }
    }
  ]
}
```

### Tag-Based Filtering

Monitor only resources with specific tags:

```json
{
  "taggedOnly": true,
  "tagsToMonitor": [
    {
      "name": "Environment",
      "value": "production"
    },
    {
      "name": "Team",
      "value": "platform"
    }
  ]
}
```

## 🎯 Management Zones

### Creating Management Zones

Management zones help organize and filter data by team, environment, or application:

```json
{
  "name": "Serverless Production",
  "description": "All production serverless resources",
  "rules": [
    {
      "type": "SERVICE",
      "enabled": true,
      "propagationTypes": [],
      "conditions": [
        {
          "key": {
            "attribute": "AWS_LAMBDA_FUNCTION_NAME"
          },
          "comparisonInfo": {
            "type": "STRING",
            "operator": "CONTAINS",
            "value": "prod",
            "negate": false,
            "caseSensitive": false
          }
        }
      ]
    },
    {
      "type": "AWS_LAMBDA_FUNCTION",
      "enabled": true,
      "propagationTypes": [],
      "conditions": [
        {
          "key": {
            "attribute": "AWS_ACCOUNT_ID"
          },
          "comparisonInfo": {
            "type": "STRING",
            "operator": "EQUALS",
            "value": "123456789012",
            "negate": false,
            "caseSensitive": true
          }
        }
      ]
    }
  ]
}
```

### Environment-Based Zones

```json
{
  "name": "Development Environment",
  "rules": [
    {
      "type": "SERVICE",
      "enabled": true,
      "conditions": [
        {
          "key": {
            "attribute": "CUSTOM_DIMENSION",
            "dynamicKey": "environment"
          },
          "comparisonInfo": {
            "type": "STRING",
            "operator": "EQUALS",
            "value": "dev"
          }
        }
      ]
    }
  ]
}
```

## 🚨 Alerting Profiles

### Profile Structure

```json
{
  "displayName": "Serverless Critical",
  "rules": [
    {
      "severityLevel": "AVAILABILITY",
      "tagFilter": {
        "includeMode": "INCLUDE_ANY",
        "tagFilters": [
          {
            "context": "CONTEXTLESS",
            "key": "criticality",
            "value": "high"
          }
        ]
      },
      "delayInMinutes": 0
    },
    {
      "severityLevel": "ERROR",
      "tagFilter": {
        "includeMode": "NONE"
      },
      "delayInMinutes": 5
    },
    {
      "severityLevel": "PERFORMANCE",
      "tagFilter": {
        "includeMode": "NONE"
      },
      "delayInMinutes": 15
    },
    {
      "severityLevel": "RESOURCE_CONTENTION",
      "tagFilter": {
        "includeMode": "NONE"
      },
      "delayInMinutes": 30
    },
    {
      "severityLevel": "CUSTOM_ALERT",
      "tagFilter": {
        "includeMode": "NONE"
      },
      "delayInMinutes": 0
    }
  ],
  "managementZoneId": null,
  "eventTypeFilters": [
    {
      "predefinedEventFilter": {
        "eventType": "CUSTOM_DEPLOYMENT",
        "negate": false
      }
    }
  ]
}
```

### Alert Conditions

#### Lambda Error Rate Alert

```json
{
  "name": "Lambda High Error Rate",
  "description": "Alert when Lambda error rate exceeds threshold",
  "type": "METRIC_ALERT",
  "severity": "ERROR",
  "metricId": "builtin:cloud.aws.lambda.errors",
  "threshold": 10,
  "aggregationType": "PERCENTILE",
  "alertCondition": "ABOVE",
  "samples": 5,
  "violatingSamples": 3,
  "dealertingSamples": 5,
  "entityFilter": {
    "dimensionKey": "dt.entity.aws_lambda_function",
    "conditions": []
  },
  "alertingScope": [
    {
      "filterType": "MANAGEMENT_ZONE",
      "managementZone": {
        "id": "1234567890"
      }
    }
  ]
}
```

#### Lambda Cold Start Alert

```json
{
  "name": "Lambda High Cold Start Rate",
  "type": "CUSTOM_CHART",
  "metricSelector": "builtin:cloud.aws.lambda.coldStarts:splitBy(\"dt.entity.aws_lambda_function\"):avg:auto:sort(value(avg,descending)):limit(20)",
  "threshold": 50,
  "aggregationType": "PERCENTILE",
  "alertCondition": "ABOVE"
}
```

#### DynamoDB Throttling Alert

```json
{
  "name": "DynamoDB Throttling Detected",
  "description": "Alert when DynamoDB tables are being throttled",
  "type": "METRIC_ALERT",
  "severity": "PERFORMANCE",
  "metricId": "builtin:cloud.aws.dynamodb.throttledRequests",
  "threshold": 1,
  "aggregationType": "SUM",
  "alertCondition": "ABOVE",
  "samples": 3,
  "violatingSamples": 2
}
```

## 📈 Custom Metrics Configuration

### Metric Ingestion via API

```python
# Python example for custom metric ingestion
import requests
import time

def send_custom_metric(tenant_url, api_token, metric_name, value, dimensions=None):
    """Send a custom metric to Dynatrace."""
    endpoint = f"{tenant_url}/api/v2/metrics/ingest"
    
    # Build metric line
    dimension_str = ""
    if dimensions:
        dimension_str = "," + ",".join([f'{k}="{v}"' for k, v in dimensions.items()])
    
    metric_line = f"{metric_name}{dimension_str} {value} {int(time.time() * 1000)}"
    
    headers = {
        "Authorization": f"Api-Token {api_token}",
        "Content-Type": "text/plain"
    }
    
    response = requests.post(endpoint, headers=headers, data=metric_line)
    return response.status_code == 202

# Usage
send_custom_metric(
    tenant_url="https://abc12345.live.dynatrace.com",
    api_token="dt0c01.XXX",
    metric_name="custom.payment.amount",
    value=123.45,
    dimensions={
        "currency": "USD",
        "payment_method": "credit_card",
        "region": "us-east-1"
    }
)
```

### Metric Metadata Definition

```json
{
  "displayName": "Payment Amount",
  "description": "Total payment amount processed",
  "unit": "Count",
  "dimensions": [
    "currency",
    "payment_method",
    "region"
  ],
  "metricId": "custom.payment.amount"
}
```

### Lambda Custom Metrics Integration

```python
# In your Lambda function
from dynatrace import OneAgentSDK

sdk = OneAgentSDK()

def handler(event, context):
    # Record custom metric
    sdk.add_custom_request_attribute("order_id", event.get("order_id"))
    sdk.add_custom_request_attribute("customer_tier", event.get("tier"))
    
    # Business metric
    metric_value = process_order(event)
    
    # Report metric
    sdk.report_custom_metric(
        "custom.orders.value",
        metric_value,
        dimensions={"tier": event.get("tier")}
    )
    
    return {"statusCode": 200}
```

## 🔍 Service Level Objectives (SLOs)

### SLO Definition

```json
{
  "name": "Lambda Function Availability",
  "description": "Availability SLO for critical Lambda functions",
  "metricExpression": "(100)*(builtin:service.availability:filter(in(\"dt.entity.service\",entitySelector(\"type(SERVICE),tag(critical)\"))))",
  "evaluationType": "AGGREGATE",
  "filter": "type(SERVICE),tag(critical)",
  "target": 99.9,
  "warning": 99.95,
  "timeframe": "-1M",
  "errorBudgetBurnRate": {
    "fastBurnMinutes": 60,
    "burnRateVisualizationEnabled": true
  }
}
```

### API Latency SLO

```json
{
  "name": "API Gateway P95 Latency",
  "description": "95th percentile latency should be under 500ms",
  "metricExpression": "(100)*((builtin:cloud.aws.apigateway.latency:filter(and(eq(\"dt.entity.custom_device\",ENTITY_SELECTOR))):splitBy():percentile(95))<(500))",
  "evaluationType": "AGGREGATE",
  "target": 95.0,
  "warning": 97.0,
  "timeframe": "-7d"
}
```

## 🎨 Dashboard Configuration

### Dashboard JSON Structure

```json
{
  "metadata": {
    "configurationVersions": [7],
    "clusterVersion": "1.285.0"
  },
  "dashboardMetadata": {
    "name": "AWS Serverless Overview",
    "shared": true,
    "owner": "admin@example.com",
    "dashboardFilter": {
      "timeframe": "-2h",
      "managementZone": null
    },
    "tags": ["aws", "serverless", "monitoring"]
  },
  "tiles": [
    {
      "name": "Lambda Invocations",
      "tileType": "DATA_EXPLORER",
      "configured": true,
      "bounds": {
        "top": 0,
        "left": 0,
        "width": 456,
        "height": 304
      },
      "customName": "Lambda Invocations",
      "queries": [
        {
          "id": "A",
          "spaceAggregation": "AUTO",
          "timeAggregation": "DEFAULT",
          "splitBy": ["dt.entity.aws_lambda_function"],
          "metricSelector": "builtin:cloud.aws.lambda.invocations:splitBy(\"dt.entity.aws_lambda_function\"):sum:auto:sort(value(sum,descending)):limit(20)",
          "enabled": true
        }
      ],
      "visualConfig": {
        "type": "GRAPH_CHART",
        "global": {
          "hideLegend": false
        },
        "rules": [],
        "axes": {
          "xAxis": {
            "visible": true
          },
          "yAxes": []
        }
      }
    }
  ]
}
```

### Dashboard Variables

```json
{
  "variables": [
    {
      "name": "function",
      "type": "ENTITY_SELECTOR",
      "entityType": "AWS_LAMBDA_FUNCTION",
      "defaultValue": "*",
      "allowMultiple": true,
      "displayName": "Lambda Function"
    },
    {
      "name": "environment",
      "type": "TAG",
      "tagFilter": {
        "key": "environment"
      },
      "defaultValue": "production",
      "displayName": "Environment"
    }
  ]
}
```

## 🔔 Notification Configuration

### Slack Webhook

```json
{
  "type": "SLACK",
  "name": "Serverless Alerts - Slack",
  "active": true,
  "alertingProfile": "alerting-profile-id",
  "channel": "#serverless-alerts",
  "title": "{ProblemTitle}",
  "message": "**Problem Details:**\n- Impact: {ProblemImpact}\n- Severity: {ProblemSeverity}\n- Status: {State}\n\n[View in Dynatrace]({ProblemURL})"
}
```

### PagerDuty Integration

```json
{
  "type": "PAGER_DUTY",
  "name": "Serverless Critical - PagerDuty",
  "active": true,
  "alertingProfile": "critical-alerting-profile-id",
  "account": "your-account",
  "serviceApiKey": "your-service-api-key",
  "serviceName": "AWS Serverless"
}
```

### AWS SNS Integration

```json
{
  "type": "AWS_SNS",
  "name": "Serverless Alerts - SNS",
  "active": true,
  "alertingProfile": "alerting-profile-id",
  "topicArn": "arn:aws:sns:us-east-1:123456789012:dynatrace-alerts",
  "subject": "[{Severity}] {ProblemTitle}"
}
```

## 🔐 Security Configuration

### API Token Permissions Matrix

| Operation | Required Scope |
|-----------|----------------|
| Read metrics | `metrics.read` |
| Write metrics | `metrics.ingest` |
| Read config | `ReadConfig` |
| Write config | `WriteConfig` |
| Read problems | `problems.read` |
| Write SLOs | `slo.write` |
| Synthetic monitors | `syntheticExecutions.write` |
| Access logs | `logs.read` |

### Token Creation Script

```bash
#!/bin/bash
# Create API token with required permissions

curl -X POST "${DT_TENANT_URL}/api/v2/apiTokens" \
  -H "Authorization: Api-Token ${DT_ADMIN_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "serverless-monitoring-token",
    "scopes": [
      "metrics.read",
      "metrics.ingest",
      "ReadConfig",
      "WriteConfig",
      "problems.read",
      "slo.read",
      "slo.write",
      "DataExport",
      "entities.read"
    ],
    "expirationDate": "2025-12-31T23:59:59Z"
  }'
```

## 📝 Configuration Validation

### Validation Script

```bash
#!/bin/bash
# validate-config.sh

echo "Validating Dynatrace configuration..."

# Check API connectivity
echo -n "API connectivity: "
if curl -s -o /dev/null -w "%{http_code}" \
    "${DT_TENANT_URL}/api/v2/entities?pageSize=1" \
    -H "Authorization: Api-Token ${DT_API_TOKEN}" | grep -q "200"; then
    echo "✓"
else
    echo "✗ Failed"
    exit 1
fi

# Check AWS integration
echo -n "AWS integration: "
AWS_CREDS=$(curl -s "${DT_TENANT_URL}/api/config/v1/aws/credentials" \
    -H "Authorization: Api-Token ${DT_API_TOKEN}")
if echo "$AWS_CREDS" | jq -e '.values | length > 0' > /dev/null; then
    echo "✓"
else
    echo "✗ No AWS integrations found"
fi

# Check Lambda functions discovered
echo -n "Lambda functions: "
LAMBDA_COUNT=$(curl -s "${DT_TENANT_URL}/api/v2/entities?entitySelector=type(AWS_LAMBDA_FUNCTION)" \
    -H "Authorization: Api-Token ${DT_API_TOKEN}" | jq '.totalCount')
echo "${LAMBDA_COUNT} discovered"

echo "Configuration validation complete."
```

---

For troubleshooting configuration issues, see [Troubleshooting Guide](troubleshooting.md).

