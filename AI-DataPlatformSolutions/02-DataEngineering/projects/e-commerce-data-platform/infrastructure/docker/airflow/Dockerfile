FROM apache/airflow:2.7.0-python3.10

USER root

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        default-jdk \
        git \
        curl \
        wget \
    && apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set JAVA_HOME
ENV JAVA_HOME=/usr/lib/jvm/default-java

USER airflow

# Copy requirements and install Python packages
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

# Install additional Airflow providers
RUN pip install --no-cache-dir \
    apache-airflow-providers-apache-spark==4.1.3 \
    apache-airflow-providers-apache-kafka==1.1.0 \
    apache-airflow-providers-great-expectations==0.2.2

# Copy custom plugins and configurations
COPY infrastructure/docker/airflow/airflow.cfg /opt/airflow/airflow.cfg

# Initialize Airflow database
RUN airflow db init

# Create default admin user
RUN airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com \
    --password admin
