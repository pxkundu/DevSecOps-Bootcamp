#!/bin/bash
yum install -y docker
systemctl start docker
systemctl enable docker
usermod -aG docker ec2-user
