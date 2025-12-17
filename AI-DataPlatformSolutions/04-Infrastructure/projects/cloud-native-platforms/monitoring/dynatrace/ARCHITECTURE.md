# 🏗️ Dynatrace AWS Serverless Monitoring Architecture

## 📋 Executive Summary

This document describes the architecture of a comprehensive monitoring solution for AWS serverless applications using Dynatrace. The solution provides full-stack observability including distributed tracing, metrics collection, log aggregation, and AI-powered problem detection.

## 🎯 Design Principles

1. **Zero-Code Instrumentation**: Leverage Dynatrace OneAgent and AWS integrations for automatic instrumentation
2. **Infrastructure as Code**: All monitoring configurations are version-controlled and deployable via CI/CD
3. **Least Privilege Access**: Minimal IAM permissions required for monitoring
4. **Cost Optimization**: Efficient data collection without impacting application performance
5. **Multi-Environment Support**: Consistent monitoring across dev, staging, and production

## 🏛️ High-Level Architecture

```mermaid
graph TB
    subgraph "End Users"
        CLIENT[Client Applications]
    end
    
    subgraph "AWS Cloud Region"
        subgraph "Edge Layer"
            CF[CloudFront]
            WAF[WAF]
            R53[Route 53]
            SHIELD[Shield]
        end
        
        subgraph "API Layer"
            APIGW[API Gateway<br/>REST/HTTP/WebSocket]
        end
        
        subgraph "Compute Layer"
            subgraph "Lambda Functions"
                LAMBDA[Lambda with<br/>Dynatrace Extension]
            end
            STEP[Step Functions]
        end
        
        subgraph "Data Layer"
            DDB[(DynamoDB)]
            S3[(S3)]
            CACHE[(ElastiCache)]
        end
        
        subgraph "Messaging Layer"
            SQS[SQS]
            SNS[SNS]
            EB[EventBridge]
        end
    end
    
    subgraph "Dynatrace Platform"
        subgraph "Data Collection"
            EXT[Lambda Extension]
            AG[ActiveGate]
            AWSINT[AWS Integration]
        end
        
        subgraph "Grail Data Platform"
            METRICS[(Metrics)]
            TRACES[(Traces)]
            LOGS[(Logs)]
            EVENTS[(Events)]
        end
        
        DAVIS[Davis AI Engine]
        
        subgraph "Visualization"
            DASH[Dashboards]
            FLOW[Service Flow]
            PROBLEMS[Problems Console]
            NOTIFY[Notifications]
        end
    end
    
    CLIENT --> CF
    CF --> WAF
    WAF --> R53
    R53 --> APIGW
    APIGW --> LAMBDA
    LAMBDA --> DDB
    LAMBDA --> S3
    LAMBDA --> CACHE
    LAMBDA --> SQS
    SQS --> LAMBDA
    SNS --> LAMBDA
    EB --> LAMBDA
    LAMBDA --> STEP
    STEP --> LAMBDA
    
    LAMBDA -.-> EXT
    EXT --> AG
    AWSINT --> METRICS
    AG --> METRICS
    AG --> TRACES
    AG --> LOGS
    
    METRICS --> DAVIS
    TRACES --> DAVIS
    LOGS --> DAVIS
    EVENTS --> DAVIS
    
    DAVIS --> DASH
    DAVIS --> FLOW
    DAVIS --> PROBLEMS
    DAVIS --> NOTIFY
```

## 🔌 Data Collection Components

### 1. Dynatrace Lambda Extension

The Lambda Extension is deployed as a Lambda Layer that provides automatic instrumentation:

```mermaid
graph TB
    subgraph "Lambda Execution Environment"
        subgraph "Extension Layer"
            EXT[Dynatrace Extension]
            OA[OneAgent Code Modules]
            TC[Trace Context Manager]
            MC[Metrics Collector]
            LF[Log Forwarder]
        end
        
        subgraph "Function Layer"
            HANDLER[Lambda Handler]
            CODE[Business Logic]
        end
        
        RUNTIME[Lambda Runtime]
    end
    
    subgraph "External"
        DT[Dynatrace Platform]
    end
    
    RUNTIME --> HANDLER
    HANDLER --> CODE
    EXT --> OA
    OA --> TC
    OA --> MC
    OA --> LF
    TC -.-> HANDLER
    MC -.-> HANDLER
    EXT -->|HTTPS 443| DT
```

**Data Flow:**
1. Function receives invocation event
2. Extension captures trace context from headers
3. Function code executes with automatic instrumentation
4. Extension collects metrics (duration, memory, cold start)
5. Extension forwards data to Dynatrace (buffered, async)
6. Function returns response

**Supported Runtimes:**
- Node.js 14.x, 16.x, 18.x, 20.x
- Python 3.8, 3.9, 3.10, 3.11, 3.12
- Java 8, 11, 17, 21
- .NET Core 3.1, .NET 6, .NET 8
- Go 1.x (via manual instrumentation)

### 2. AWS Integration (CloudWatch Metrics)

```mermaid
flowchart TB
    subgraph "AWS CloudWatch"
        CW[CloudWatch Metrics]
    end
    
    subgraph "AWS Services"
        DDB[DynamoDB Metrics]
        APIGW[API Gateway Metrics]
        LAMBDA[Lambda Metrics]
        SQS[SQS Metrics]
        SNS[SNS Metrics]
    end
    
    subgraph "Dynatrace"
        AWSMON[AWS Monitor]
        CLUSTER[Dynatrace Cluster]
    end
    
    DDB --> CW
    APIGW --> CW
    LAMBDA --> CW
    SQS --> CW
    SNS --> CW
    CW --> AWSMON
    AWSMON --> CLUSTER
```

**Collected Metrics:**
- **Lambda**: Invocations, Duration, Errors, Throttles, ConcurrentExecutions
- **API Gateway**: Count, Latency, 4XXError, 5XXError, IntegrationLatency
- **DynamoDB**: ConsumedRCU, ConsumedWCU, ThrottledRequests, LatencyGetItem
- **SQS**: NumberOfMessagesSent, ApproximateAgeOfOldestMessage, ApproximateNumberOfMessagesVisible
- **SNS**: NumberOfMessagesPublished, PublishSize, NumberOfNotificationsDelivered

### 3. ActiveGate Architecture

ActiveGate serves as a secure proxy and processing node:

```mermaid
graph TB
    subgraph "ActiveGate"
        subgraph "Modules"
            AWS[AWS Monitor]
            METRICS[Metrics Ingestion]
            LOG[Log Analytics]
            SYNTH[Synthetic Execution]
            PROBLEM[Problem Correlation]
            API[API Gateway]
        end
    end
    
    subgraph "Data Sources"
        LAMBDA[Lambda Functions]
        CW[CloudWatch]
        LOGS[Log Streams]
    end
    
    subgraph "Destination"
        DT[Dynatrace SaaS]
    end
    
    LAMBDA --> AWS
    CW --> AWS
    LOGS --> LOG
    AWS --> DT
    METRICS --> DT
    LOG --> DT
    SYNTH --> DT
```

## 🔄 Data Flow Patterns

### Pattern 1: Synchronous API Request

```mermaid
sequenceDiagram
    participant Client
    participant APIGW as API Gateway
    participant Lambda
    participant DDB as DynamoDB
    participant DT as Dynatrace
    
    Client->>APIGW: HTTP Request
    APIGW->>Lambda: Invoke (with trace context)
    Note over Lambda: Dynatrace Extension<br/>captures trace
    Lambda->>DDB: Query/Put Item
    DDB-->>Lambda: Response
    Lambda-->>APIGW: Response
    APIGW-->>Client: HTTP Response
    
    Lambda--)DT: Spans, Metrics, Logs
    APIGW--)DT: CloudWatch Metrics
    DDB--)DT: CloudWatch Metrics
```

### Pattern 2: Asynchronous Event Processing

```mermaid
sequenceDiagram
    participant EB as EventBridge
    participant Lambda1 as Lambda Handler
    participant SQS
    participant Lambda2 as Lambda Worker
    participant DDB as DynamoDB
    participant DT as Dynatrace
    
    EB->>Lambda1: Trigger Event
    Lambda1->>SQS: Send Message
    Lambda1--)DT: Trace & Metrics
    
    SQS->>Lambda2: Poll Messages
    Lambda2->>DDB: Process & Store
    Lambda2--)DT: Correlated Trace
    
    Note over DT: Davis AI correlates<br/>async traces
```

### Pattern 3: Step Functions Orchestration

```mermaid
graph LR
    subgraph "Step Functions State Machine"
        S1[State 1<br/>Lambda A]
        S2[State 2<br/>Lambda B]
        S3[State 3<br/>Lambda C]
        S4{Choice}
        S5[State 4<br/>Lambda D]
        S6[End]
    end
    
    subgraph "Dynatrace"
        TRACE[Correlated Trace]
    end
    
    S1 --> S2
    S2 --> S3
    S3 --> S4
    S4 -->|condition A| S5
    S4 -->|condition B| S6
    S5 --> S6
    
    S1 -.-> TRACE
    S2 -.-> TRACE
    S3 -.-> TRACE
    S5 -.-> TRACE
```

## 🔐 Security Architecture

### IAM Roles and Permissions

```mermaid
graph TB
    subgraph "IAM Architecture"
        subgraph "Dynatrace AWS Role"
            DT_ROLE[Dynatrace Monitoring Role]
            CW_PERM[cloudwatch:GetMetricStatistics<br/>cloudwatch:ListMetrics]
            TAG_PERM[tag:GetResources]
            LAMBDA_PERM[lambda:ListFunctions<br/>lambda:ListTags]
            DDB_PERM[dynamodb:DescribeTable<br/>dynamodb:ListTables]
            SQS_PERM[sqs:ListQueues]
        end
        
        subgraph "ActiveGate Role"
            AG_ROLE[ActiveGate Instance Role]
            EC2_PERM[ec2:DescribeInstances]
            LOGS_PERM[logs:DescribeLogGroups<br/>logs:FilterLogEvents]
            SSM_PERM[ssm:GetParameter]
        end
        
        subgraph "Lambda Extension"
            LAMBDA_ROLE[Lambda Execution Role]
            SM_PERM[secretsmanager:GetSecretValue]
            HTTPS[Outbound HTTPS to Dynatrace]
        end
    end
    
    DT_ROLE --> CW_PERM
    DT_ROLE --> TAG_PERM
    DT_ROLE --> LAMBDA_PERM
    DT_ROLE --> DDB_PERM
    DT_ROLE --> SQS_PERM
    
    AG_ROLE --> EC2_PERM
    AG_ROLE --> LOGS_PERM
    AG_ROLE --> SSM_PERM
    
    LAMBDA_ROLE --> SM_PERM
    LAMBDA_ROLE --> HTTPS
```

### Network Security

```mermaid
graph TB
    subgraph "Internet"
        DT[Dynatrace SaaS]
    end
    
    subgraph "AWS VPC"
        subgraph "Public Subnet"
            IGW[Internet Gateway]
            NAT[NAT Gateway]
        end
        
        subgraph "Private Subnet A"
            LAMBDA1[Lambda VPC Functions]
            AG[ActiveGate]
        end
        
        subgraph "Private Subnet B"
            LAMBDA2[Lambda VPC Functions]
        end
    end
    
    DT <-->|HTTPS 443| IGW
    IGW --> NAT
    NAT --> LAMBDA1
    NAT --> LAMBDA2
    LAMBDA1 --> AG
    LAMBDA2 --> AG
    AG --> NAT
```

## 📊 Metrics Architecture

### Custom Metrics Pipeline

```mermaid
flowchart LR
    subgraph "Lambda Function"
        CODE[Business Code]
        METRIC[Record Custom Metric]
    end
    
    subgraph "Extension"
        BUFFER[Metric Buffer]
        BATCH[Batch Processor<br/>every 60s]
    end
    
    subgraph "Dynatrace"
        OTLP[OTLP/Metrics API]
        ENGINE[Metrics Engine]
        AGG[Aggregation]
        BASE[Baselining]
        ALERT[Alerting]
    end
    
    CODE --> METRIC
    METRIC --> BUFFER
    BUFFER --> BATCH
    BATCH --> OTLP
    OTLP --> ENGINE
    ENGINE --> AGG
    ENGINE --> BASE
    ENGINE --> ALERT
```

### Metric Dimensions

```yaml
# Standard dimensions applied to all serverless metrics
dimensions:
  # AWS Infrastructure
  - aws.account.id
  - aws.region
  - aws.availability_zone
  
  # Lambda Specific
  - aws.lambda.function_name
  - aws.lambda.function_version
  - aws.lambda.memory_size
  - aws.lambda.runtime
  
  # Custom Business Dimensions
  - environment           # dev, staging, production
  - service.name          # order-service, payment-service
  - service.version       # v1.2.3
  - team                  # platform, payments, orders
  
  # Request Context
  - http.method
  - http.status_code
  - http.route
```

## 🚨 Alerting Architecture

### Problem Detection Pipeline

```mermaid
flowchart TB
    subgraph "Data Sources"
        METRICS[Metrics]
        TRACES[Traces]
        LOGS[Logs]
    end
    
    subgraph "Detection"
        AD[Anomaly Detection]
        STAT[Statistical Analysis]
        ML[ML-based Detection]
        THRESH[Threshold Checks]
    end
    
    subgraph "Correlation"
        EC[Event Correlation]
        TIME[Time-based]
        TOPO[Topology-based]
        CAUSAL[Causal Analysis]
    end
    
    subgraph "Davis AI"
        ROOT[Root Cause Analysis]
        IMPACT[Impact Score]
        REMED[Remediation Suggestions]
    end
    
    subgraph "Notifications"
        SLACK[Slack]
        PD[PagerDuty]
        SNS[AWS SNS]
        EMAIL[Email]
    end
    
    METRICS --> AD
    TRACES --> AD
    LOGS --> AD
    
    AD --> STAT
    AD --> ML
    AD --> THRESH
    
    STAT --> EC
    ML --> EC
    THRESH --> EC
    
    EC --> TIME
    EC --> TOPO
    EC --> CAUSAL
    
    TIME --> ROOT
    TOPO --> ROOT
    CAUSAL --> ROOT
    
    ROOT --> IMPACT
    IMPACT --> REMED
    
    REMED --> SLACK
    REMED --> PD
    REMED --> SNS
    REMED --> EMAIL
```

### Alert Severity Matrix

| Condition | Severity | Response Time | Notification |
|-----------|----------|---------------|--------------|
| Lambda Error Rate > 10% | Critical | Immediate | PagerDuty |
| Lambda P95 Latency > 5s | High | 5 min | Slack + Email |
| DynamoDB Throttling | High | 5 min | Slack |
| SQS DLQ Messages > 0 | Warning | 15 min | Email |
| Cold Start Rate > 50% | Info | 1 hour | Dashboard |

## 📈 Capacity Planning

### Resource Sizing

```mermaid
graph TB
    subgraph "ActiveGate Sizing"
        SMALL[t3.medium<br/>< 50 Lambda functions]
        MEDIUM[t3.large<br/>50-200 functions]
        LARGE[t3.xlarge<br/>200+ functions]
        AUTO[ECS Auto-scaling<br/>Variable load]
    end
    
    subgraph "Lambda Extension Impact"
        COLD[Cold Start: +35ms]
        WARM[Warm Invocation: +5ms]
        MEM[Memory: +25MB baseline]
    end
    
    subgraph "Data Retention"
        METRICS_RET[Metrics: 3 years]
        TRACES_RET[Traces: 35 days]
        LOGS_RET[Logs: 35 days]
    end
```

### DDU Estimation

| Component | DDU Usage |
|-----------|-----------|
| Lambda invocation | ~0.001 DDU |
| Trace | ~0.01 DDU |
| Log line | ~0.0001 DDU |

## 🔄 Deployment Architecture

### GitOps Workflow

```mermaid
sequenceDiagram
    participant Dev as Developer
    participant Git as Git Repository
    participant CI as CI/CD Pipeline
    participant TF as Terraform
    participant AWS
    participant DT as Dynatrace API
    
    Dev->>Git: Push Monitoring Config
    Git->>CI: Webhook Trigger
    CI->>TF: Terraform Plan
    TF->>AWS: Apply Infrastructure
    AWS-->>TF: Resources Created
    CI->>DT: Configure Dynatrace
    DT-->>CI: Configuration Applied
    CI->>AWS: Validate Setup
    AWS-->>CI: Validation Results
    CI-->>Dev: Deployment Status
```

## 📝 Configuration as Code

### Monaco Project Structure

```mermaid
graph TB
    subgraph "Monaco Project"
        ROOT[monaco/]
        
        subgraph "Projects"
            PROJ[projects/aws-serverless/]
            MZ[management-zone/]
            AP[alerting-profile/]
            DASH[dashboard/]
            SLO[slo/]
            SYNTH[synthetic-monitor/]
        end
        
        subgraph "Environments"
            DEV[dev.yaml]
            STAGING[staging.yaml]
            PROD[production.yaml]
        end
    end
    
    ROOT --> PROJ
    PROJ --> MZ
    PROJ --> AP
    PROJ --> DASH
    PROJ --> SLO
    PROJ --> SYNTH
    
    ROOT --> DEV
    ROOT --> STAGING
    ROOT --> PROD
```

## 🎯 Success Criteria

| Metric | Target | Measurement |
|--------|--------|-------------|
| Mean Time to Detection | < 2 min | Dynatrace problem timeline |
| Mean Time to Resolution | < 30 min | Problem close time |
| False Positive Rate | < 5% | Alert accuracy review |
| Dashboard Load Time | < 3s | User experience |
| Data Completeness | > 99% | Missing data alerts |
| Extension Availability | > 99.9% | Layer deployment health |

## 🔗 Integration Points

```mermaid
graph LR
    subgraph "CI/CD"
        GHA[GitHub Actions]
        GITLAB[GitLab CI]
        JENKINS[Jenkins]
        CODEPIPE[AWS CodePipeline]
    end
    
    subgraph "Dynatrace"
        API[Dynatrace API]
        MONACO[Monaco CLI]
    end
    
    subgraph "Notifications"
        SLACK[Slack]
        PD[PagerDuty]
        TEAMS[MS Teams]
        SNS[AWS SNS]
    end
    
    GHA --> MONACO
    GITLAB --> MONACO
    JENKINS --> API
    CODEPIPE --> API
    
    MONACO --> API
    
    API --> SLACK
    API --> PD
    API --> TEAMS
    API --> SNS
```

---

**Next Steps**: See the [Getting Started Guide](docs/getting-started.md) for implementation instructions.
