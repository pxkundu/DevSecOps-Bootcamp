#!/bin/bash
aws ec2 run-instances \
  --image-id ami-0c55b159cbfafe1f0 \
  --instance-type t2.medium \
  --key-name <your-key> \
  --security-group-ids <sg-id> \
  --subnet-id <subnet-id-private-a> \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=JenkinsMasterActive}]' \
  --block-device-mappings '[{"DeviceName":"/dev/xvda","Ebs":{"Encrypted":true,"VolumeSize":20}}]' \
  --user-data '#!/bin/bash
    yum update -y
    yum install -y java-11-openjdk docker git awscli
    systemctl start docker
    usermod -aG docker ec2-user
    wget -O /etc/yum.repos.d/jenkins.repo https://pkg.jenkins.io/redhat-stable/jenkins.repo
    rpm --import https://pkg.jenkins.io/redhat-stable/jenkins.io.key
    yum install -y jenkins
    systemctl start jenkins
    systemctl enable jenkins
    echo "jenkins ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/jenkins
    echo "*/5 * * * * aws s3 sync /var/lib/jenkins s3://<your-bucket>/jenkins-backup --sse AES256" | crontab -'

aws ec2 run-instances \
  --image-id ami-0c55b159cbfafe1f0 \
  --instance-type t2.medium \
  --key-name <your-key> \
  --security-group-ids <sg-id> \
  --subnet-id <subnet-id-private-b> \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=JenkinsMasterPassive}]' \
  --block-device-mappings '[{"DeviceName":"/dev/xvda","Ebs":{"Encrypted":true,"VolumeSize":20}}]' \
  --user-data '#!/bin/bash
    yum update -y
    yum install -y java-11-openjdk docker git awscli
    systemctl start docker
    usermod -aG docker ec2-user
    wget -O /etc/yum.repos.d/jenkins.repo https://pkg.jenkins.io/redhat-stable/jenkins.repo
    rpm --import https://pkg.jenkins.io/redhat-stable/jenkins.io.key
    yum install -y jenkins
    systemctl stop jenkins
    aws s3 sync s3://<your-bucket>/jenkins-backup /var/lib/jenkins
    echo "*/5 * * * * aws s3 sync s3://<your-bucket>/jenkins-backup /var/lib/jenkins && systemctl restart jenkins" | crontab -'

aws elb create-load-balancer \
  --load-balancer-name JenkinsHA \
  --listeners "Protocol=HTTP,LoadBalancerPort=8080,InstanceProtocol=HTTP,InstancePort=8080" \
  --subnets <subnet-id-private-a> <subnet-id-private-b> \
  --security-groups <sg-id> \
  --region us-east-1
