# AWS Cost Audit Report

**Generated on**: {{GENERATION_DATE}}

| Service | Resource | Usage Metric | Estimated Monthly Cost | Optimization Recommendation |
|---------|----------|--------------|-----------------------|---------------------------|
| EC2     | {{EC2_COUNT}} instances | {{EC2_TYPES}} | ${{EC2_COST}} | Use Reserved Instances for long-running instances; right-size instances based on utilization. |
| RDS     | {{RDS_COUNT}} instances | {{RDS_STORAGE}} GB storage | ${{RDS_COST}} | Use Reserved Instances; scale storage based on needs; enable Multi-AZ only for critical workloads. |
| S3      | {{S3_COUNT}} buckets | Size estimation requires S3 analytics | ${{S3_COST}} | Enable lifecycle policies; use Intelligent-Tiering; reduce unnecessary GET requests. |
| Lambda  | {{LAMBDA_COUNT}} functions | Invocation count requires CloudWatch metrics | ${{LAMBDA_COST}} | Optimize memory allocation; reduce execution time; avoid Provisioned Concurrency unless necessary. |
| DynamoDB | {{DYNAMODB_COUNT}} tables | {{DYNAMODB_SIZE}} GB storage | ${{DYNAMODB_COST}} | Use On-Demand mode for unpredictable workloads; enable auto-scaling; optimize queries. |

**Notes**:
- Costs are estimated using AWS Cost Explorer for the past 30 days.
- Enable CloudWatch metrics for precise Lambda invocation counts and S3 bucket sizes.
- Review recommendations to reduce costs and optimize resource usage.
