#!/bin/bash
aws cloudwatch put-metric-alarm \
  --alarm-name JenkinsQueueLength \
  --metric-name QueueLength \
  --namespace Jenkins \
  --threshold 5 \
  --comparison-operator GreaterThanThreshold \
  --period 300 \
  --evaluation-periods 2 \
  --alarm-actions <sns-topic-arn>
