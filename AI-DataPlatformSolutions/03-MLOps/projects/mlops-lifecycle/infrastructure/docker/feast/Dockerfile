FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Feast and dependencies
RUN pip install --no-cache-dir \
    feast[aws,gcp,postgres,redis]==0.32.0 \
    psycopg2-binary \
    redis \
    boto3

# Create feast user
RUN groupadd -r feast && useradd -r -g feast feast

# Create directories
RUN mkdir -p /feast && chown -R feast:feast /feast
USER feast

WORKDIR /feast

# Expose Feast port
EXPOSE 6566

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:6566/health || exit 1

# Start Feast server
CMD ["feast", "serve", "--host", "0.0.0.0", "--port", "6566"]
