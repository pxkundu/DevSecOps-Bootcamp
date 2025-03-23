#!/bin/bash
yum install -y nginx
systemctl enable nginx
systemctl start nginx
