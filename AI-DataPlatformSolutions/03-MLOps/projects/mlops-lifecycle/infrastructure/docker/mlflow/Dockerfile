FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install MLflow and dependencies
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir mlflow==2.7.1 psycopg2-binary boto3 pymysql

# Create mlflow user
RUN groupadd -r mlflow && useradd -r -g mlflow mlflow

# Create directories
RUN mkdir -p /mlflow/artifacts && chown -R mlflow:mlflow /mlflow
USER mlflow

# Expose MLflow port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Start MLflow server
CMD mlflow server \
    --backend-store-uri ${MLFLOW_BACKEND_STORE_URI} \
    --default-artifact-root ${MLFLOW_DEFAULT_ARTIFACT_ROOT} \
    --host 0.0.0.0 \
    --port 5000 \
    --serve-artifacts
