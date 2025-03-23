#!/bin/bash
APP_NAME=$1
MANIFEST_DIR=$2
for manifest in "$MANIFEST_DIR"/*.yaml; do
  IMAGE=$(yq e '.spec.image' "$manifest")
  TAG=$(yq e '.spec.instanceTag' "$manifest")
  PORT=$(yq e '.spec.port' "$manifest")
  NGINX_SECRET=$(yq e '.spec.nginxConfigSecret' "$manifest")
  ECR_TAG=$(yq e '.spec.postDeploy.ecrTag' "$manifest")
  INSTANCE_IP=$(aws ec2 describe-instances --filters "Name=tag:Name,Values=$TAG" "Name=instance-state-name,Values=running" --query 'Reservations[0].Instances[0].PublicIpAddress' --output text --region us-east-1)
  SSH_KEY=$(aws secretsmanager get-secret-value --secret-id jenkins-ssh-key --query SecretString --output text --region us-east-1)
  echo "$SSH_KEY" > ssh_key
  chmod 600 ssh_key
  ssh -i ssh_key -o StrictHostKeyChecking=no ec2-user@$INSTANCE_IP << 'INNEREOF'
    docker stop $(basename $IMAGE | cut -d: -f1) || true
    docker rm $(basename $IMAGE | cut -d: -f1) || true
    aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com
    docker pull $IMAGE
    docker run -d --name $(basename $IMAGE | cut -d: -f1) -p $PORT:$PORT $IMAGE
    if [ ! -z "$NGINX_SECRET" ]; then
      NGINX_CONFIG=$(aws secretsmanager get-secret-value --secret-id $NGINX_SECRET --query SecretString --output text --region us-east-1)
      echo "$NGINX_CONFIG" > /etc/nginx/conf.d/task-manager.conf
      systemctl restart nginx
    fi
    docker tag $IMAGE <account-id>.dkr.ecr.us-east-1.amazonaws.com/$(basename $IMAGE | cut -d: -f1):$ECR_TAG
    docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/$(basename $IMAGE | cut -d: -f1):$ECR_TAG
INNEREOF
  rm -f ssh_key
done
