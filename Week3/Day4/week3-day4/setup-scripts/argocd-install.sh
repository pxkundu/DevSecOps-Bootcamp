#!/bin/bash
aws ec2 run-instances \
  --image-id ami-0c55b159cbfafe1f0 \
  --instance-type t2.medium \
  --key-name <your-key> \
  --security-group-ids <sg-id> \
  --subnet-id <subnet-id> \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=ArgoCD}]' \
  --user-data '#!/bin/bash
    yum update -y
    yum install -y docker git awscli
    systemctl start docker
    usermod -aG docker ec2-user
    docker run -d --name argocd -p 8080:8080 -p 8443:8443 argoproj/argocd:latest'
