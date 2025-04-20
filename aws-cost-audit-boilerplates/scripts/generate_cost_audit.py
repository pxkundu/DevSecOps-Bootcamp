import boto3
import os
import json
from datetime import datetime, timedelta
import re

def get_input(prompt):
    """Prompt for input or retrieve from environment variables."""
    try:
        return os.environ.get(prompt) or input(f"Enter {prompt}: ")
    except EOFError:
        raise ValueError(f"{prompt} not provided")

def get_cost_explorer_data(client, service):
    """Fetch monthly cost for a service using Cost Explorer."""
    end_date = datetime.utcnow().date()
    start_date = end_date - timedelta(days=30)
    response = client.get_cost_and_usage(
        TimePeriod={
            'Start': start_date.strftime('%Y-%m-%d'),
            'End': end_date.strftime('%Y-%m-%d')
        },
        Granularity='MONTHLY',
        Metrics=['UnblendedCost'],
        Filter={
            'Dimensions': {
                'Key': 'SERVICE',
                'Values': [service]
            }
        }
    )
    cost = response['ResultsByTime'][0]['Total']['UnblendedCost']['Amount']
    return float(cost)

def generate_markdown_report(data, output_file):
    """Generate Markdown report with cost audit data."""
    with open(output_file, 'w') as f:
        f.write("# AWS Cost Audit Report\n\n")
        f.write(f"**Generated on**: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}\n\n")
        f.write("| Service | Resource | Usage Metric | Estimated Monthly Cost | Optimization Recommendation |\n")
        f.write("|---------|----------|--------------|-----------------------|---------------------------|\n")
        for row in data:
            f.write(f"| {row['Service']} | {row['Resource']} | {row['Usage']} | ${row['Cost']:.2f} | {row['Recommendation']} |\n")

def main():
    # Get runtime inputs
    region = get_input('AWS_REGION')
    sns_topic_arn = get_input('SNS_TOPIC_ARN')
    
    # Initialize AWS clients
    ec2 = boto3.client('ec2', region_name=region)
    rds = boto3.client('rds', region_name=region)
    s3 = boto3.client('s3', region_name=region)
    lambda_client = boto3.client('lambda', region_name=region)
    dynamodb = boto3.client('dynamodb', region_name=region)
    ce = boto3.client('ce', region_name=region)
    sns = boto3.client('sns', region_name=region)
    
    # Collect cost audit data
    audit_data = []
    issues = []
    
    # EC2 Audit
    ec2_instances = ec2.describe_instances()['Reservations']
    ec2_count = sum(len(res['Instances']) for res in ec2_instances)
    ec2_types = {inst['InstanceType'] for res in ec2_instances for inst in res['Instances']}
    ec2_cost = get_cost_explorer_data(ce, 'Amazon Elastic Compute Cloud - Compute')
    if ec2_count > 0:
        audit_data.append({
            'Service': 'EC2',
            'Resource': f"{ec2_count} instances",
            'Usage': f"Types: {', '.join(ec2_types)}",
            'Cost': ec2_cost,
            'Recommendation': 'Use Reserved Instances for long-running instances; right-size instances based on utilization.'
        })
        if ec2_count > 10:
            issues.append(f"High EC2 instance count ({ec2_count}) detected. Consider auto-scaling or Reserved Instances.")
    
    # RDS Audit
    rds_instances = rds.describe_db_instances()['DBInstances']
    rds_count = len(rds_instances)
    rds_storage = sum(inst.get('AllocatedStorage', 0) for inst in rds_instances)
    rds_cost = get_cost_explorer_data(ce, 'Amazon RDS Service')
    if rds_count > 0:
        audit_data.append({
            'Service': 'RDS',
            'Resource': f"{rds_count} instances",
            'Usage': f"{rds_storage} GB storage",
            'Cost': rds_cost,
            'Recommendation': 'Use Reserved Instances; scale storage based on needs; enable Multi-AZ only for critical workloads.'
        })
        if rds_storage > 1000:
            issues.append(f"High RDS storage ({rds_storage} GB) detected. Review storage needs and consider Aurora Serverless.")
    
    # S3 Audit
    buckets = s3.list_buckets()['Buckets']
    s3_size = 0
    for bucket in buckets:
        try:
            # Note: S3 size requires CloudWatch metrics or analytics
            s3_size += 1  # Placeholder for bucket size (requires additional setup)
        except Exception:
            continue
    s3_cost = get_cost_explorer_data(ce, 'Amazon Simple Storage Service')
    if buckets:
        audit_data.append({
            'Service': 'S3',
            'Resource': f"{len(buckets)} buckets",
            'Usage': 'Size estimation requires S3 analytics',
            'Cost': s3_cost,
            'Recommendation': 'Enable lifecycle policies; use Intelligent-Tiering; reduce unnecessary GET requests.'
        })
        if len(buckets) > 50:
            issues.append(f"High S3 bucket count ({len(buckets)}) detected. Consolidate buckets and enable lifecycle policies.")
    
    # Lambda Audit
    functions = lambda_client.list_functions()['Functions']
    lambda_invocations = 0  # Requires CloudWatch metrics
    lambda_cost = get_cost_explorer_data(ce, 'AWS Lambda')
    if functions:
        audit_data.append({
            'Service': 'Lambda',
            'Resource': f"{len(functions)} functions",
            'Usage': 'Invocation count requires CloudWatch metrics',
            'Cost': lambda_cost,
            'Recommendation': 'Optimize memory allocation; reduce execution time; avoid Provisioned Concurrency unless necessary.'
        })
        if len(functions) > 100:
            issues.append(f"High Lambda function count ({len(functions)}) detected. Review for unused functions.")
    
    # DynamoDB Audit
    tables = dynamodb.list_tables()['TableNames']
    dynamodb_size = 0
    for table in tables:
        try:
            desc = dynamodb.describe_table(TableName=table)['Table']
            dynamodb_size += desc.get('TableSizeBytes', 0) / (1024 ** 3)  # Convert to GB
        except Exception:
            continue
    dynamodb_cost = get_cost_explorer_data(ce, 'Amazon DynamoDB')
    if tables:
        audit_data.append({
            'Service': 'DynamoDB',
            'Resource': f"{len(tables)} tables",
            'Usage': f"{dynamodb_size:.2f} GB storage",
            'Cost': dynamodb_cost,
            'Recommendation': 'Use On-Demand mode for unpredictable workloads; enable auto-scaling; optimize queries.'
        })
        if dynamodb_size > 100:
            issues.append(f"High DynamoDB storage ({dynamodb_size:.2f} GB) detected. Review table usage and enable TTL.")
    
    # Generate Markdown report
    report_file = os.path.join(os.path.dirname(__file__), '../reports/cost_audit_report.md')
    generate_markdown_report(audit_data, report_file)
    
    # Send SNS notification if issues found
    if issues:
        sns.publish(
            TopicArn=sns_topic_arn,
            Message='\n'.join(issues),
            Subject='AWS Cost Audit Issues Detected'
        )
    
    print(f"Cost audit report generated at {report_file}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error generating cost audit: {str(e)}")
        exit(1)
