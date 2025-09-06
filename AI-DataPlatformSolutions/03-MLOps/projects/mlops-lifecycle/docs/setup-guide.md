# 🚀 MLOps Platform Setup Guide

This comprehensive guide will help you set up the complete MLOps platform from scratch, whether for local development or cloud deployment.

## 📋 Prerequisites

### **System Requirements**
- **OS**: macOS, Linux, or Windows with WSL2
- **CPU**: 4+ cores recommended
- **RAM**: 16GB+ recommended (8GB minimum)
- **Storage**: 50GB+ free space
- **Network**: Reliable internet connection

### **Required Software**
```bash
# Core tools
✅ Docker Desktop (v4.0+)
✅ Docker Compose (v2.0+)
✅ kubectl (v1.27+)
✅ Helm (v3.12+)
✅ Python (3.8+)
✅ Git (v2.30+)

# Cloud tools (for cloud deployment)
✅ AWS CLI (v2.0+)
✅ Terraform (v1.5+)
✅ eksctl (v0.140+)
```

### **Cloud Accounts (Optional)**
- **AWS Account** with appropriate permissions
- **GitHub Account** for CI/CD integration
- **Docker Hub Account** for container registry

## 🏠 Local Development Setup

### **Step 1: Clone and Navigate**
```bash
# Clone the repository
git clone https://github.com/your-org/devsecops-bootcamp.git
cd devsecops-bootcamp/AI-DataPlatformSolutions/03-MLOps/projects/mlops-lifecycle

# Verify the structure
ls -la
```

### **Step 2: Environment Configuration**
```bash
# Create environment file
cp .env.example .env

# Edit the environment variables
nano .env
```

**Environment Variables:**
```bash
# MLOps Platform Configuration
PROJECT_NAME=mlops-platform
ENVIRONMENT=local
OWNER=your-name

# Database Configuration
POSTGRES_USER=mlops
POSTGRES_PASSWORD=mlops123
POSTGRES_DB=mlops

# MLflow Configuration
MLFLOW_TRACKING_URI=http://localhost:5000
MLFLOW_S3_ENDPOINT_URL=http://localhost:9000

# Feature Store Configuration
FEAST_REGISTRY_PATH=/feast/feature_store.yaml
REDIS_HOST=localhost
REDIS_PORT=6379

# Monitoring Configuration
PROMETHEUS_HOST=localhost
PROMETHEUS_PORT=9090
GRAFANA_HOST=localhost
GRAFANA_PORT=3000
```

### **Step 3: Install Python Dependencies**
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Verify installation
python -c "import mlflow; print(mlflow.__version__)"
```

### **Step 4: Start the Platform**
```bash
# Start all services
docker-compose up -d

# Check service status
docker-compose ps

# View logs (optional)
docker-compose logs -f mlflow-server
```

### **Step 5: Initialize the Platform**
```bash
# Wait for services to be ready (2-3 minutes)
sleep 180

# Initialize databases and services
python scripts/setup/init_mlops_platform.py

# Create sample data
python data/generators/generate_sample_data.py
```

### **Step 6: Verify Installation**
```bash
# Test MLflow
curl http://localhost:5000/health

# Test Model API
curl http://localhost:8000/health

# Test Grafana
curl http://localhost:3000/api/health

# Test Prometheus
curl http://localhost:9090/-/healthy
```

## 🌐 Service Access URLs

Once the platform is running, access these services:

| Service | URL | Credentials |
|---------|-----|-------------|
| 🧪 **MLflow UI** | http://localhost:5000 | No auth required |
| 📊 **Grafana** | http://localhost:3000 | admin / admin |
| 📈 **Prometheus** | http://localhost:9090 | No auth required |
| 🔗 **Model API** | http://localhost:8000 | No auth required |
| 📓 **Jupyter Lab** | http://localhost:8888 | Token: mlops-platform |
| 🗄️ **MinIO Console** | http://localhost:9001 | mlopsadmin / mlopsadmin123 |
| 📨 **Kafka UI** | http://localhost:8081 | No auth required |
| 🔍 **Kibana** | http://localhost:5601 | No auth required |

## ☁️ Cloud Deployment (AWS)

### **Step 1: AWS Setup**
```bash
# Configure AWS CLI
aws configure
# Enter your AWS Access Key ID, Secret, Region (us-west-2), and output format (json)

# Verify AWS access
aws sts get-caller-identity

# Create S3 bucket for Terraform state
aws s3 mb s3://mlops-platform-terraform-state-$(whoami)

# Create DynamoDB table for state locking
aws dynamodb create-table \
  --table-name mlops-platform-terraform-locks \
  --attribute-definitions AttributeName=LockID,AttributeType=S \
  --key-schema AttributeName=LockID,KeyType=HASH \
  --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5
```

### **Step 2: Terraform Configuration**
```bash
# Navigate to Terraform directory
cd infrastructure/terraform

# Initialize Terraform
terraform init

# Create terraform.tfvars
cat > terraform.tfvars << EOF
project_name = "mlops-platform"
environment = "dev"
owner = "$(whoami)"
aws_region = "us-west-2"
vpc_cidr = "10.0.0.0/16"

# EKS Configuration
kubernetes_version = "1.27"
eks_node_instance_types = ["t3.medium"]
eks_node_group_desired_size = 2

# RDS Configuration
rds_instance_class = "db.t3.micro"
rds_allocated_storage = 20

# Redis Configuration
redis_node_type = "cache.t3.micro"
redis_num_cache_nodes = 1
EOF
```

### **Step 3: Deploy Infrastructure**
```bash
# Plan the deployment
terraform plan

# Deploy the infrastructure
terraform apply

# Save outputs
terraform output > ../outputs.txt
```

### **Step 4: Configure kubectl**
```bash
# Update kubeconfig
aws eks update-kubeconfig --region us-west-2 --name mlops-platform-dev-eks

# Verify connection
kubectl get nodes
```

### **Step 5: Deploy Applications**
```bash
# Navigate back to project root
cd ../..

# Create namespace
kubectl create namespace mlops

# Deploy applications with Helm
helm install mlops-platform infrastructure/helm-charts/mlops-platform \
  --namespace mlops \
  --set image.tag=latest \
  --set postgresql.enabled=false \
  --set redis.enabled=false \
  --set externalPostgresql.host=$(terraform -chdir=infrastructure/terraform output -raw rds_endpoint) \
  --set externalRedis.host=$(terraform -chdir=infrastructure/terraform output -raw redis_endpoint)

# Wait for deployment
kubectl rollout status deployment/mlflow-server -n mlops
kubectl rollout status deployment/model-api -n mlops
```

### **Step 6: Configure Ingress**
```bash
# Install NGINX Ingress Controller
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update

helm install ingress-nginx ingress-nginx/ingress-nginx \
  --namespace ingress-nginx \
  --create-namespace \
  --set controller.service.type=LoadBalancer

# Get the load balancer URL
kubectl get service ingress-nginx-controller -n ingress-nginx
```

## 🧪 Testing Your Setup

### **Run the Test Suite**
```bash
# Unit tests
pytest tests/unit-tests/ -v

# Integration tests (requires running services)
pytest tests/integration-tests/ -v

# Model tests
pytest tests/model-tests/ -v

# End-to-end tests
pytest tests/e2e-tests/ -v
```

### **Manual Verification**
```bash
# Test model training
python ml-models/churn-prediction/train.py

# Test model serving
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "features": {
      "tenure_months": 24,
      "monthly_charges": 65.0,
      "total_charges": 1560.0,
      "contract_type": "One year",
      "payment_method": "Credit card",
      "internet_service": "Fiber optic"
    }
  }'

# Test batch predictions
curl -X POST http://localhost:8000/predict/batch \
  -H "Content-Type: application/json" \
  -d '{
    "features": [
      {"tenure_months": 12, "monthly_charges": 45.0},
      {"tenure_months": 36, "monthly_charges": 85.0}
    ]
  }'
```

### **Monitor System Health**
```bash
# Check Prometheus metrics
curl http://localhost:9090/api/v1/query?query=up

# Check model performance
curl http://localhost:8000/models

# View Grafana dashboards
open http://localhost:3000
```

## 🔧 Development Workflow

### **Model Development**
```bash
# Start Jupyter Lab
jupyter lab --ip=0.0.0.0 --port=8888 --no-browser

# Or use the containerized version
open http://localhost:8888?token=mlops-platform
```

### **Feature Development**
```bash
# Navigate to feature store
cd feature-engineering/feature-store

# Apply new features
feast apply

# Materialize features to online store
feast materialize-incremental $(date '+%Y-%m-%d')
```

### **Model Training**
```bash
# Train a new model
python ml-models/churn-prediction/train.py

# With custom parameters
python ml-models/churn-prediction/train.py \
  --experiment-name "churn-prediction-v2" \
  --optimize-hyperparams \
  --n-trials 100
```

### **Model Deployment**
```bash
# Deploy to staging
kubectl apply -f infrastructure/kubernetes/staging/

# Deploy to production
kubectl apply -f infrastructure/kubernetes/production/

# Monitor deployment
kubectl rollout status deployment/model-api -n mlops
```

## 🚨 Troubleshooting

### **Common Issues**

#### **Docker Issues**
```bash
# Problem: Services not starting
# Solution: Check Docker resources
docker system df
docker system prune

# Problem: Port conflicts
# Solution: Check what's using the ports
lsof -i :5000
lsof -i :8000
```

#### **Permission Issues**
```bash
# Problem: MLflow permissions
# Solution: Fix ownership
sudo chown -R $(whoami):$(whoami) ./mlruns
sudo chown -R $(whoami):$(whoami) ./artifacts
```

#### **Memory Issues**
```bash
# Problem: Out of memory errors
# Solution: Increase Docker memory limit or reduce services
docker-compose down
docker-compose up mlflow-server postgres redis  # Start essential services only
```

#### **Network Issues**
```bash
# Problem: Services can't connect
# Solution: Check network and restart
docker network ls
docker-compose down
docker-compose up -d
```

### **Performance Tuning**
```bash
# Monitor resource usage
docker stats

# Check service logs
docker-compose logs mlflow-server
docker-compose logs model-api

# Optimize database
docker-compose exec postgres psql -U mlops -d mlops -c "VACUUM ANALYZE;"
```

### **Data Issues**
```bash
# Problem: No training data
# Solution: Generate sample data
python data/generators/generate_sample_data.py

# Problem: Feature store empty
# Solution: Materialize features
cd feature-engineering/feature-store
feast materialize-incremental $(date -d "1 week ago" '+%Y-%m-%d') $(date '+%Y-%m-%d')
```

## 📈 Monitoring and Maintenance

### **Daily Operations**
```bash
# Check system health
docker-compose ps
curl http://localhost:8000/health

# Monitor disk usage
df -h
docker system df

# Check logs for errors
docker-compose logs --tail=100 | grep ERROR
```

### **Weekly Maintenance**
```bash
# Update dependencies
pip install --upgrade -r requirements.txt

# Clean up old Docker images
docker image prune -f

# Backup MLflow data
docker-compose exec postgres pg_dump -U mlops mlops > mlflow_backup_$(date +%Y%m%d).sql
```

### **Performance Monitoring**
```bash
# View Grafana dashboards
open http://localhost:3000/d/mlops-overview

# Check Prometheus metrics
curl http://localhost:9090/api/v1/query?query=model_prediction_requests_total

# Monitor model performance
python monitoring/model-monitoring/drift_detector.py
```

## 🎯 Next Steps

### **Learning Path**
1. 📚 **Explore Notebooks**: Start with `/notebooks/tutorials/`
2. 🧪 **Run Experiments**: Try different models and parameters
3. 📊 **Monitor Performance**: Set up alerts and dashboards
4. 🚀 **Deploy Models**: Practice CI/CD workflows
5. 🔍 **Optimize Performance**: Tune infrastructure and models

### **Advanced Features**
- Set up multi-environment deployments (dev/staging/prod)
- Implement custom monitoring and alerting
- Add new model types and use cases
- Integrate with external data sources
- Configure advanced security and compliance

### **Contributing**
- Follow the development workflow in `/docs/contributing.md`
- Submit issues and feature requests
- Create pull requests with improvements
- Share your success stories and learnings

---

## 🆘 Getting Help

### **Documentation**
- 📖 **Architecture**: `/docs/architecture.md`
- 🛠️ **Development**: `/docs/development-guide.md`
- 🐛 **Troubleshooting**: `/docs/troubleshooting.md`

### **Community**
- 💬 **Discussions**: GitHub Discussions
- 🐛 **Issues**: GitHub Issues
- 📧 **Email**: mlops-support@yourorg.com

### **Support Resources**
- 🎥 **Video Tutorials**: Available in `/docs/videos/`
- 📝 **Blog Posts**: Check the project wiki
- 🤝 **Office Hours**: Weekly community calls

---

**🎉 Congratulations! You now have a fully functional MLOps platform. Start building amazing ML applications!**
