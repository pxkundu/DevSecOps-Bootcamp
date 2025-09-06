FROM jupyter/all-spark-notebook:python-3.10

USER root

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    vim \
    git \
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
    jupyterlab_widgets

# Enable Jupyter extensions
RUN jupyter labextension install --no-build \
    @jupyterlab/git \
    && jupyter lab build --dev-build=False --minimize=False

# Copy custom Jupyter configuration
COPY infrastructure/docker/jupyter/jupyter_lab_config.py /home/jovyan/.jupyter/

# Create directories for notebooks and data
RUN mkdir -p /home/jovyan/work/notebooks \
    && mkdir -p /home/jovyan/work/data-sources \
    && mkdir -p /home/jovyan/work/processing \
    && mkdir -p /home/jovyan/work/storage

WORKDIR /home/jovyan/work
