#!/bin/bash

# Helm Chart Setup Script for Kubernetes Learning
# Run this script with sudo on the master node after helm_setup.sh

LOG_FILE="/var/log/helm_chart_setup.log"
echo "Starting Helm chart setup at $(date)" | tee -a $LOG_FILE

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to create and configure the Helm chart
setup_helm_chart() {
    # Check if Helm is installed
    if ! command_exists helm; then
        echo "Helm is not installed. Run helm_setup.sh first." | tee -a $LOG_FILE
        exit 1
    fi

    # Define chart directory
    CHART_DIR="../helm-charts/custom-nginx"
    echo "Creating custom Helm chart in $CHART_DIR..." | tee -a $LOG_FILE

    # Create the chart if it doesn’t exist
    if [ ! -d "$CHART_DIR" ]; then
        helm create "$CHART_DIR" || {
            echo "Failed to create Helm chart directory." | tee -a $LOG_FILE
            exit 1
        }
    else
        echo "Chart directory already exists, skipping creation." | tee -a $LOG_FILE
    fi

    # Customize Chart.yaml
    cat > "$CHART_DIR/Chart.yaml" <<EOF
apiVersion: v2
name: custom-nginx
description: A custom Nginx web application chart for learning Helm
version: 0.1.0
appVersion: "1.25"
maintainers:
  - name: ParthaSarathiKundu
    email: pxkundu2@shockers.wichita.edu
keywords:
  - nginx
  - webserver
EOF

    # Customize values.yaml
    cat > "$CHART_DIR/values.yaml" <<EOF
replicaCount: 2
image:
  repository: nginx
  tag: "1.25"
  pullPolicy: IfNotPresent
service:
  type: ClusterIP
  port: 80
ingress:
  enabled: true
  host: "nginx.example.com"
  path: "/"
  pathType: Prefix
resources:
  limits:
    cpu: "0.5"
    memory: "512Mi"
  requests:
    cpu: "0.2"
    memory: "256Mi"
EOF

    # Customize deployment.yaml
    cat > "$CHART_DIR/templates/deployment.yaml" <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .Release.Name }}-nginx
  labels:
    app: {{ .Release.Name }}-nginx
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      app: {{ .Release.Name }}-nginx
  template:
    metadata:
      labels:
        app: {{ .Release.Name }}-nginx
    spec:
      containers:
      - name: nginx
        image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
        imagePullPolicy: {{ .Values.image.pullPolicy }}
        ports:
        - containerPort: 80
        resources:
          {{- toYaml .Values.resources | nindent 12 }}
EOF

    # Customize service.yaml
    cat > "$CHART_DIR/templates/service.yaml" <<EOF
apiVersion: v1
kind: Service
metadata:
  name: {{ .Release.Name }}-nginx
  labels:
    app: {{ .Release.Name }}-nginx
spec:
  type: {{ .Values.service.type }}
  ports:
  - port: {{ .Values.service.port }}
    targetPort: 80
    protocol: TCP
  selector:
    app: {{ .Release.Name }}-nginx
EOF

    # Add ingress.yaml
    cat > "$CHART_DIR/templates/ingress.yaml" <<EOF
{{- if .Values.ingress.enabled }}
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: {{ .Release.Name }}-nginx
  labels:
    app: {{ .Release.Name }}-nginx
spec:
  rules:
  - host: {{ .Values.ingress.host }}
    http:
      paths:
      - path: {{ .Values.ingress.path }}
        pathType: {{ .Values.ingress.pathType }}
        backend:
          service:
            name: {{ .Release.Name }}-nginx
            port:
              number: {{ .Values.service.port }}
{{- end }}
EOF

    # Lint the chart to validate it
    echo "Linting the Helm chart..." | tee -a $LOG_FILE
    helm lint "$CHART_DIR" || {
        echo "Helm chart linting failed." | tee -a $LOG_FILE
        exit 1
    }

    # Install the chart
    echo "Installing custom Helm chart in 'my-app' namespace..." | tee -a $LOG_FILE
    helm upgrade --install custom-nginx "$CHART_DIR" \
        -n my-app \
        --timeout 10m \
        --debug \
        || {
            echo "Failed to install custom Helm chart." | tee -a $LOG_FILE
            exit 1
        }

    echo "Custom Nginx chart installed successfully. Check pods:" | tee -a $LOG_FILE
    kubectl get pods -n partha-app-ns
    echo "Access Nginx via ingress (configure DNS for nginx.example.com or use curl with --resolve)" | tee -a $LOG_FILE
}

# Main logic
if [ ! -f /root/.kube/config ]; then
    echo "Kubernetes cluster not set up. Run k8s_setup.sh first." | tee -a $LOG_FILE
    exit 1
fi

setup_helm_chart

echo "Helm chart setup completed successfully at $(date)" | tee -a $LOG_FILE
echo "Next steps to learn Helm with custom charts:"
echo "1. Upgrade: helm upgrade custom-nginx $CHART_DIR -n my-app --set replicaCount=3"
echo "2. Rollback: helm rollback custom-nginx 1 -n partha-app-ns"
echo "3. Uninstall: helm uninstall custom-nginx -n partha-app-ns"
echo "4. Modify $CHART_DIR/values.yaml or templates/ for custom changes"
