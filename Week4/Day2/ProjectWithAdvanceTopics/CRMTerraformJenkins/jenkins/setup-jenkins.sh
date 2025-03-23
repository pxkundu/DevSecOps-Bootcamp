#!/bin/bash
yum update -y
amazon-linux-extras install java-openjdk11 docker -y
systemctl start docker
systemctl enable docker
usermod -aG docker ec2-user
wget -O /etc/yum.repos.d/jenkins.repo https://pkg.jenkins.io/redhat-stable/jenkins.repo
rpm --import https://pkg.jenkins.io/redhat-stable/jenkins.io.key
yum install -y jenkins awscli git
systemctl start jenkins
systemctl enable jenkins
