# ELK Stack - Log Management and Analytics

## 📊 Overview
The ELK Stack (Elasticsearch, Logstash, Kibana) provides comprehensive log management, search, and analytics capabilities for DevSecOps environments.

## 📁 Directory Structure

```
elk-stack/
├── README.md
├── elasticsearch/
│   ├── config/
│   ├── data/
│   └── scripts/
├── logstash/
│   ├── config/
│   ├── pipelines/
│   └── patterns/
├── kibana/
│   ├── dashboards/
│   ├── visualizations/
│   └── saved-objects/
└── kubernetes/
    ├── elasticsearch/
    ├── logstash/
    └── kibana/
```

## 🛠️ Elasticsearch Configuration

### 1. Elasticsearch Config
```yaml
# elasticsearch/config/elasticsearch.yml
cluster.name: devsecops-cluster
node.name: elasticsearch-node-1
network.host: 0.0.0.0
discovery.seed_hosts: ["elasticsearch-node-1", "elasticsearch-node-2", "elasticsearch-node-3"]
cluster.initial_master_nodes: ["elasticsearch-node-1", "elasticsearch-node-2", "elasticsearch-node-3"]

# Security settings
xpack.security.enabled: true
xpack.security.transport.ssl.enabled: true
xpack.security.transport.ssl.verification_mode: certificate
xpack.security.transport.ssl.key: certs/elasticsearch.key
xpack.security.transport.ssl.certificate: certs/elasticsearch.crt

# Index settings
action.auto_create_index: false
```

### 2. Index Templates
```json
{
  "index_patterns": ["logs-*"],
  "template": {
    "settings": {
      "number_of_shards": 1,
      "number_of_replicas": 1,
      "index.lifecycle.name": "logs-policy",
      "index.lifecycle.rollover_alias": "logs"
    },
    "mappings": {
      "properties": {
        "@timestamp": {
          "type": "date"
        },
        "level": {
          "type": "keyword"
        },
        "message": {
          "type": "text"
        },
        "service": {
          "type": "keyword"
        },
        "host": {
          "type": "keyword"
        }
      }
    }
  }
}
```

## 🔄 Logstash Configuration

### 1. Logstash Config
```ruby
# logstash/config/logstash.yml
http.host: "0.0.0.0"
xpack.monitoring.elasticsearch.hosts: [ "http://elasticsearch:9200" ]
```

### 2. Pipeline Configuration
```ruby
# logstash/pipelines/application-logs.conf
input {
  beats {
    port => 5044
  }
}

filter {
  if [fields][log_type] == "application" {
    grok {
      match => { "message" => "%{TIMESTAMP_ISO8601:timestamp} %{LOGLEVEL:level} %{GREEDYDATA:log_message}" }
    }
    
    date {
      match => [ "timestamp", "ISO8601" ]
    }
    
    mutate {
      remove_field => [ "timestamp" ]
    }
  }
  
  if [fields][log_type] == "nginx" {
    grok {
      match => { "message" => "%{NGINXACCESS}" }
    }
    
    date {
      match => [ "timestamp", "dd/MMM/yyyy:HH:mm:ss Z" ]
    }
  }
}

output {
  elasticsearch {
    hosts => ["elasticsearch:9200"]
    index => "logs-%{+YYYY.MM.dd}"
  }
}
```

### 3. Grok Patterns
```ruby
# logstash/patterns/custom-patterns
APPLICATION_LOG %{TIMESTAMP_ISO8601:timestamp} \[%{DATA:thread}\] %{LOGLEVEL:level} %{DATA:logger} - %{GREEDYDATA:message}
NGINXACCESS %{IPORHOST:clientip} %{USER:ident} %{USER:auth} \[%{HTTPDATE:timestamp}\] "(?:%{WORD:verb} %{NOTSPACE:request}(?: HTTP/%{NUMBER:httpversion})?|%{DATA:rawrequest})" %{NUMBER:response} (?:%{NUMBER:bytes}|-) "(?:%{DATA:referrer}|-)" "%{DATA:useragent}"
```

## 📈 Kibana Configuration

### 1. Index Patterns
```json
{
  "attributes": {
    "title": "logs-*",
    "timeFieldName": "@timestamp",
    "fields": "[]"
  }
}
```

### 2. Dashboard Configuration
```json
{
  "version": "8.0.0",
  "objects": [
    {
      "id": "dashboard-1",
      "type": "dashboard",
      "attributes": {
        "title": "DevSecOps Logs Dashboard",
        "panelsJSON": "[{\"version\":\"8.0.0\",\"gridData\":{\"x\":0,\"y\":0,\"w\":24,\"h\":15,\"i\":\"1\"},\"panelIndex\":\"1\",\"embeddableConfig\":{},\"panelType\":\"visualization\"}]"
      }
    }
  ]
}
```

## ☸️ Kubernetes Manifests

### 1. Elasticsearch Deployment
```yaml
# kubernetes/elasticsearch/elasticsearch.yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: elasticsearch
spec:
  serviceName: elasticsearch
  replicas: 3
  selector:
    matchLabels:
      app: elasticsearch
  template:
    metadata:
      labels:
        app: elasticsearch
    spec:
      containers:
      - name: elasticsearch
        image: docker.elastic.co/elasticsearch/elasticsearch:8.0.0
        ports:
        - containerPort: 9200
        - containerPort: 9300
        env:
        - name: cluster.name
          value: devsecops-cluster
        - name: node.name
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
        - name: discovery.seed_hosts
          value: "elasticsearch-0.elasticsearch,elasticsearch-1.elasticsearch,elasticsearch-2.elasticsearch"
        - name: cluster.initial_master_nodes
          value: "elasticsearch-0,elasticsearch-1,elasticsearch-2"
        - name: ES_JAVA_OPTS
          value: "-Xms1g -Xmx1g"
        volumeMounts:
        - name: data
          mountPath: /usr/share/elasticsearch/data
        - name: config
          mountPath: /usr/share/elasticsearch/config/elasticsearch.yml
          subPath: elasticsearch.yml
      volumes:
      - name: config
        configMap:
          name: elasticsearch-config
  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 10Gi
```

### 2. Logstash Deployment
```yaml
# kubernetes/logstash/logstash.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: logstash
spec:
  replicas: 2
  selector:
    matchLabels:
      app: logstash
  template:
    metadata:
      labels:
        app: logstash
    spec:
      containers:
      - name: logstash
        image: docker.elastic.co/logstash/logstash:8.0.0
        ports:
        - containerPort: 5044
        - containerPort: 9600
        env:
        - name: LS_JAVA_OPTS
          value: "-Xms512m -Xmx512m"
        volumeMounts:
        - name: config
          mountPath: /usr/share/logstash/config/logstash.yml
          subPath: logstash.yml
        - name: pipelines
          mountPath: /usr/share/logstash/pipeline
      volumes:
      - name: config
        configMap:
          name: logstash-config
      - name: pipelines
        configMap:
          name: logstash-pipelines
```

### 3. Kibana Deployment
```yaml
# kubernetes/kibana/kibana.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: kibana
spec:
  replicas: 1
  selector:
    matchLabels:
      app: kibana
  template:
    metadata:
      labels:
        app: kibana
    spec:
      containers:
      - name: kibana
        image: docker.elastic.co/kibana/kibana:8.0.0
        ports:
        - containerPort: 5601
        env:
        - name: ELASTICSEARCH_HOSTS
          value: "http://elasticsearch:9200"
        volumeMounts:
        - name: config
          mountPath: /usr/share/kibana/config/kibana.yml
          subPath: kibana.yml
      volumes:
      - name: config
        configMap:
          name: kibana-config
---
apiVersion: v1
kind: Service
metadata:
  name: kibana
spec:
  selector:
    app: kibana
  ports:
  - port: 5601
    targetPort: 5601
  type: LoadBalancer
```

## 🚀 Deployment Scripts

### 1. Install ELK Stack
```bash
#!/bin/bash
# scripts/install-elk.sh

echo "Installing ELK Stack..."

# Create namespace
kubectl create namespace logging

# Apply Elasticsearch
kubectl apply -f kubernetes/elasticsearch/

# Wait for Elasticsearch to be ready
kubectl wait --for=condition=ready pod -l app=elasticsearch -n logging --timeout=300s

# Apply Logstash
kubectl apply -f kubernetes/logstash/

# Wait for Logstash to be ready
kubectl wait --for=condition=ready pod -l app=logstash -n logging --timeout=300s

# Apply Kibana
kubectl apply -f kubernetes/kibana/

# Wait for Kibana to be ready
kubectl wait --for=condition=ready pod -l app=kibana -n logging --timeout=300s

echo "ELK Stack installation completed"
```

### 2. Configure Log Collection
```bash
#!/bin/bash
# scripts/configure-log-collection.sh

echo "Configuring log collection..."

# Install Filebeat
kubectl apply -f https://raw.githubusercontent.com/elastic/beats/8.0.0/deploy/kubernetes/filebeat-kubernetes.yaml

# Configure log forwarding
kubectl apply -f kubernetes/filebeat/

echo "Log collection configuration completed"
```

## 📋 Best Practices

### 1. Log Management
- Use structured logging
- Implement log rotation
- Set up proper indexing
- Monitor log volume

### 2. Performance
- Optimize Elasticsearch settings
- Use appropriate shard sizes
- Implement index lifecycle management
- Monitor cluster health

### 3. Security
- Enable authentication
- Use TLS encryption
- Implement access controls
- Regular security updates

---

**Ready to master ELK Stack?** Start with basic Elasticsearch setup and work your way up to comprehensive log analytics!
