# E-Commerce Data Platform Setup Guide

This comprehensive guide will help you set up the complete e-commerce data platform on your local machine or cloud environment.

## 📋 Prerequisites

### System Requirements
- **OS**: Linux/macOS/Windows (with WSL2)
- **RAM**: Minimum 16GB (32GB recommended)
- **Storage**: 50GB free space
- **CPU**: 4+ cores

### Required Software
- [Docker](https://docs.docker.com/get-docker/) (v20.10+)
- [Docker Compose](https://docs.docker.com/compose/install/) (v2.0+)
- [Python](https://www.python.org/downloads/) (3.8+)
- [Git](https://git-scm.com/downloads)

### Optional (for cloud deployment)
- [Terraform](https://www.terraform.io/downloads) (v1.0+)
- [kubectl](https://kubernetes.io/docs/tasks/tools/) (v1.27+)
- [AWS CLI](https://aws.amazon.com/cli/) or [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/)

## 🚀 Quick Start (Local Development)

### Step 1: Clone and Setup

```bash
# Navigate to the project directory
cd e-commerce-data-platform

# Create environment file
cp .env.example .env

# Edit environment variables (optional for local setup)
nano .env
```

### Step 2: Start Infrastructure Services

```bash
# Start all services
docker-compose up -d

# Check if all services are running
docker-compose ps

# View logs (optional)
docker-compose logs -f
```

### Step 3: Initialize the Platform

```bash
# Install Python dependencies
pip install -r requirements.txt

# Initialize databases
python scripts/setup/init_databases.py

# Generate sample data
python data-sources/data-generators/generate_sample_data.py

# Wait for Airflow to be ready (may take 2-3 minutes)
echo "Waiting for Airflow to initialize..."
sleep 180
```

### Step 4: Verify Installation

Open your browser and check these services:

- **Airflow UI**: http://localhost:8080 (admin/admin)
- **Kafka UI**: http://localhost:8081
- **Grafana**: http://localhost:3000 (admin/admin)
- **MinIO**: http://localhost:9001 (minioadmin/minioadmin)
- **Jupyter**: http://localhost:8888 (token: data-engineering)
- **Prometheus**: http://localhost:9090

## 🔧 Detailed Setup Instructions

### Environment Configuration

Create a `.env` file with the following variables:

```bash
# Database Configuration
POSTGRES_USER=airflow
POSTGRES_PASSWORD=airflow
POSTGRES_DB=airflow
WAREHOUSE_DB=warehouse

# Kafka Configuration
KAFKA_BOOTSTRAP_SERVERS=kafka:29092

# MinIO Configuration
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin

# Airflow Configuration
AIRFLOW_UID=1000
AIRFLOW_GID=0
AIRFLOW__CORE__FERNET_KEY=81HqDtbqAywKSOumSHMpQfTOw4Aa5FlYX8xVDSGj8Cg=

# Monitoring
GRAFANA_ADMIN_PASSWORD=admin
PROMETHEUS_RETENTION=30d

# Environment
ENVIRONMENT=development
```

### Service-by-Service Setup

#### PostgreSQL Database
```bash
# Connect to PostgreSQL
docker exec -it ecommerce-data-platform-postgres-1 psql -U airflow

# Create additional databases
CREATE DATABASE warehouse;
CREATE DATABASE ecommerce;

# Create users and permissions
CREATE USER dataeng WITH PASSWORD 'dataeng123';
GRANT ALL PRIVILEGES ON DATABASE warehouse TO dataeng;
GRANT ALL PRIVILEGES ON DATABASE ecommerce TO dataeng;
```

#### Apache Airflow
```bash
# Create admin user (if not already created)
docker exec -it ecommerce-data-platform-airflow-webserver-1 \
  airflow users create \
  --username admin \
  --firstname Admin \
  --lastname User \
  --role Admin \
  --email admin@example.com \
  --password admin

# Enable DAGs
docker exec -it ecommerce-data-platform-airflow-webserver-1 \
  airflow dags unpause ecommerce_etl_pipeline
```

#### Apache Kafka
```bash
# Create topics manually (optional - auto-creation is enabled)
docker exec -it ecommerce-data-platform-kafka-1 \
  kafka-topics --create \
  --bootstrap-server localhost:9092 \
  --topic ecommerce.user.events \
  --partitions 3 \
  --replication-factor 1

# List topics
docker exec -it ecommerce-data-platform-kafka-1 \
  kafka-topics --list --bootstrap-server localhost:9092
```

#### MinIO Object Storage
```bash
# Create buckets
docker exec -it ecommerce-data-platform-minio-1 \
  mc alias set local http://localhost:9000 minioadmin minioadmin

docker exec -it ecommerce-data-platform-minio-1 \
  mc mb local/data-lake

docker exec -it ecommerce-data-platform-minio-1 \
  mc mb local/data-warehouse
```

### Data Generation and Loading

#### Generate Sample Data
```bash
# Generate sample e-commerce data
python data-sources/data-generators/generate_sample_data.py

# Verify data generation
ls -la data-sources/sample-data/
```

#### Start Data Pipelines
```bash
# Trigger the ETL pipeline
curl -X POST "http://localhost:8080/api/v1/dags/ecommerce_etl_pipeline/dagRuns" \
  -H "Content-Type: application/json" \
  -d '{"dag_run_id": "manual_trigger_' $(date +%s) '"}' \
  --user admin:admin

# Start real-time event streaming
python ingestion/stream-ingestion/kafka_producer.py &

# Start stream processing (in another terminal)
python processing/stream-processing/flink_consumer.py &
```

## 🌐 Cloud Deployment

### AWS Deployment

#### Prerequisites
```bash
# Install AWS CLI and configure
aws configure

# Install Terraform
wget https://releases.hashicorp.com/terraform/1.5.7/terraform_1.5.7_linux_amd64.zip
unzip terraform_1.5.7_linux_amd64.zip
sudo mv terraform /usr/local/bin/
```

#### Deploy Infrastructure
```bash
cd infrastructure/terraform

# Initialize Terraform
terraform init

# Create a terraform.tfvars file
cat > terraform.tfvars << EOF
aws_region = "us-west-2"
environment = "dev"
project_name = "ecommerce-data-platform"
owner = "your-name"

# Database configuration
database_password = "YourSecurePassword123!"

# Instance types (adjust for cost optimization)
rds_instance_type = "db.t3.medium"
eks_node_instance_type = "m5.large"
msk_instance_type = "kafka.m5.large"
redis_node_type = "cache.t3.micro"
EOF

# Plan and apply
terraform plan
terraform apply

# Get connection details
terraform output
```

#### Deploy Applications
```bash
# Update kubeconfig
aws eks update-kubeconfig --region us-west-2 --name ecommerce-data-platform-dev-eks

# Deploy applications using Helm or kubectl
kubectl apply -f infrastructure/kubernetes/
```

### Azure Deployment

#### Prerequisites
```bash
# Install Azure CLI
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Login to Azure
az login

# Install kubectl and Helm
az aks install-cli
```

#### Deploy Infrastructure
```bash
# Create resource group
az group create --name ecommerce-data-platform-rg --location westus2

# Deploy using ARM templates
az deployment group create \
  --resource-group ecommerce-data-platform-rg \
  --template-file infrastructure/azure/main.json \
  --parameters @infrastructure/azure/parameters.json
```

## 🔍 Verification and Testing

### Health Checks
```bash
# Check all services
./scripts/health-check.sh

# Test database connectivity
python scripts/test/test_database_connection.py

# Test Kafka connectivity
python scripts/test/test_kafka_connection.py

# Test MinIO connectivity
python scripts/test/test_minio_connection.py
```

### Data Quality Checks
```bash
# Run data quality validation
python processing/data-quality/great_expectations_suite.py

# View data quality reports
open data-sources/sample-data/great_expectations/uncommitted/data_docs/local_site/index.html
```

### Pipeline Testing
```bash
# Test batch processing
python processing/batch-processing/spark_etl.py

# Test stream processing
python ingestion/stream-ingestion/kafka_producer.py --duration 60

# Check processing results
python scripts/test/verify_pipeline_results.py
```

## 📊 Monitoring and Observability

### Access Monitoring Dashboards

1. **Grafana Dashboard**: http://localhost:3000
   - Username: admin
   - Password: admin
   - Import dashboard: monitoring/grafana/dashboards/

2. **Prometheus Metrics**: http://localhost:9090
   - Query examples in monitoring/prometheus/queries.md

3. **Airflow Monitoring**: http://localhost:8080
   - Check DAG runs and task status

### Custom Metrics
```bash
# Add custom metrics to your code
from prometheus_client import Counter, Histogram, Gauge

# Examples
RECORDS_PROCESSED = Counter('records_processed_total', 'Total processed records')
PROCESSING_TIME = Histogram('processing_time_seconds', 'Processing time')
QUEUE_SIZE = Gauge('queue_size', 'Current queue size')
```

## 🛠️ Troubleshooting

### Common Issues

#### Services Not Starting
```bash
# Check Docker resources
docker system df
docker system prune

# Check logs
docker-compose logs [service-name]

# Restart specific service
docker-compose restart [service-name]
```

#### Memory Issues
```bash
# Increase Docker memory limit to 8GB+
# Check Docker Desktop settings

# Reduce services for development
docker-compose -f docker-compose.dev.yml up -d
```

#### Port Conflicts
```bash
# Check port usage
lsof -i :8080
netstat -tulpn | grep :8080

# Kill processes using ports
sudo kill -9 $(lsof -t -i:8080)
```

#### Database Connection Issues
```bash
# Reset database
docker-compose down -v
docker-compose up -d postgres
sleep 30
python scripts/setup/init_databases.py
```

### Performance Optimization

#### For Development
```bash
# Use lightweight services
export AIRFLOW_EXECUTOR=LocalExecutor
export SPARK_MASTER_URL=local[2]

# Reduce resource allocation
docker-compose -f docker-compose.dev.yml up -d
```

#### For Production
```bash
# Use external managed services
export POSTGRES_HOST=your-rds-endpoint
export KAFKA_BOOTSTRAP_SERVERS=your-msk-endpoint
export REDIS_HOST=your-elasticache-endpoint
```

## 🧪 Development and Testing

### Running Tests
```bash
# Unit tests
pytest tests/unit/

# Integration tests
pytest tests/integration/

# Data quality tests
python processing/data-quality/great_expectations_suite.py

# End-to-end tests
pytest tests/e2e/
```

### Development Workflow
```bash
# Create feature branch
git checkout -b feature/new-pipeline

# Make changes and test locally
docker-compose up -d
python your_new_script.py

# Run quality checks
black . --check
flake8 .
mypy .

# Run tests
pytest

# Commit and push
git add .
git commit -m "Add new pipeline feature"
git push origin feature/new-pipeline
```

## 📚 Next Steps

1. **Explore the Platform**: Start with the [User Guide](user-guide.md)
2. **Customize Pipelines**: Modify existing DAGs and processors
3. **Add Data Sources**: Connect to your real data sources
4. **Scale the Platform**: Deploy to cloud for production use
5. **Monitor and Optimize**: Use the monitoring stack to optimize performance

## 🆘 Getting Help

- **Documentation**: Check the [docs/](../docs/) directory
- **Troubleshooting**: See [troubleshooting.md](troubleshooting.md)
- **Examples**: Explore [applications/](../applications/) for usage examples
- **Issues**: Create issues in the project repository

## 🔐 Security Considerations

### Local Development
- Change default passwords in `.env` file
- Use strong passwords for production
- Enable SSL/TLS for external access

### Production Deployment
- Use secrets management (AWS Secrets Manager, Azure Key Vault)
- Enable encryption at rest and in transit
- Configure proper network security groups
- Enable audit logging
- Implement backup and disaster recovery

---

**Success!** 🎉 You now have a fully functional e-commerce data platform running. Start exploring the various components and building your data engineering skills!
