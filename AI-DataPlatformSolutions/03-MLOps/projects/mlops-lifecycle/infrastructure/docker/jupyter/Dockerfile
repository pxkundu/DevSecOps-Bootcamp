FROM jupyter/all-spark-notebook:python-3.10

USER root

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    vim \
    git \
    graphviz \
    && rm -rf /var/lib/apt/lists/*

USER jovyan

# Copy requirements and install Python packages
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Install additional Jupyter extensions
RUN pip install --no-cache-dir \
    jupyter-bokeh \
    jupyterlab-git \
    jupyterlab-drawio \
    jupyterlab_widgets \
    ipywidgets \
    plotly \
    kaleido

# Enable Jupyter extensions
RUN jupyter labextension install --no-build \
    @jupyterlab/git \
    && jupyter lab build --dev-build=False --minimize=False

# Install MLflow, Feast, and other MLOps tools
RUN pip install --no-cache-dir \
    mlflow==2.7.1 \
    feast[aws,gcp,postgres,redis]==0.32.0 \
    evidently==0.4.2 \
    shap==0.42.1 \
    optuna==3.3.0

# Create directories for notebooks and data
RUN mkdir -p /home/jovyan/work/notebooks \
    && mkdir -p /home/jovyan/work/ml-models \
    && mkdir -p /home/jovyan/work/data \
    && mkdir -p /home/jovyan/work/feature-engineering \
    && mkdir -p /home/jovyan/work/training

# Copy custom Jupyter configuration if it exists
COPY --chown=jovyan:users infrastructure/docker/jupyter/jupyter_lab_config.p* /home/jovyan/.jupyter/

WORKDIR /home/jovyan/work

# Set environment variables
ENV MLFLOW_TRACKING_URI="http://mlflow-server:5000"
ENV FEAST_REGISTRY_PATH="/feast/feature_store.yaml"
