FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir \
    fastapi==0.101.1 \
    uvicorn==0.23.2 \
    mlflow==2.7.1 \
    feast[aws,gcp,postgres,redis]==0.32.0 \
    scikit-learn==1.3.0 \
    pandas==2.0.3 \
    numpy==1.24.3 \
    pydantic==2.3.0 \
    psycopg2-binary \
    redis \
    prometheus-client

# Copy application code
COPY serving/ /app/serving/
COPY ml-models/ /app/ml-models/

# Create non-root user
RUN groupadd -r apiuser && useradd -r -g apiuser apiuser
RUN chown -R apiuser:apiuser /app
USER apiuser

# Expose API port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start FastAPI server
CMD ["uvicorn", "serving.api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
