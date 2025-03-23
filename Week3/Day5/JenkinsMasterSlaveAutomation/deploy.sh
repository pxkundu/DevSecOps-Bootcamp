#!/bin/bash
aws cloudformation validate-template --template-body file://templates/jenkins-master-slave.yaml
aws cloudformation create-stack \
  --stack-name JenkinsMasterSlave \
  --template-body file://templates/jenkins-master-slave.yaml \
  --parameters ParameterKey=KeyName,ParameterValue=TrainingSetup \
  --region us-east-1
