#!/bin/bash
aws ec2 create-launch-template \
  --launch-template-name JenkinsSlaveEastTemplate \
  --version-description "v1" \
  --launch-template-data '{
    "ImageId": "ami-0c55b159cbfafe1f0",
    "InstanceType": "t2.medium",
    "KeyName": "<your-key>",
    "SecurityGroupIds": ["<sg-id-east>"],
    "IamInstanceProfile": {"Name": "JenkinsSlaveRole"},
    "BlockDeviceMappings": [{"DeviceName": "/dev/xvda", "Ebs": {"Encrypted": true, "VolumeSize": 10}}],
    "UserData": "IyEvYmluL2Jhc2gKeXVtIHVwZGF0ZSAteQp5dW0gaW5zdGFsbCAteSBqYXZhLTExLW9wZW5qZGsgZG9ja2VyIGdpdCBub2RlanMgYXdzY2xpCnN5c3RlbWN0bCBzdGFydCBkb2NrZXIKdXNlcm1vZCAtYUcgZG9ja2VyIGVjMi11c2VyCmVjaG8gPG1hc3Rlci1wdWJsaWMta2V5PiA+IC9ob21lL2VjMi11c2VyLy5zc2gvYXV0aG9yaXplZF9rZXlzCmNobW9kIDYwMCAvaG9tZS9lYzItdXNlci8uc3NoL2F1dGhvcml6ZWRfa2V5cwpjaG1vZCA3MDAgL2hvbWUvZWMyLXVzZXIvLnNzaA=="
  }'

aws autoscaling create-auto-scaling-group \
  --auto-scaling-group-name JenkinsSlavesEast \
  --launch-template LaunchTemplateName=JenkinsSlaveEastTemplate \
  --min-size 0 \
  --max-size 10 \
  --desired-capacity 2 \
  --vpc-zone-identifier "<subnet-id-east>" \
  --region us-east-1

aws ec2 create-launch-template \
  --launch-template-name JenkinsSlaveWestTemplate \
  --version-description "v1" \
  --launch-template-data '{
    "ImageId": "ami-0c55b159cbfafe1f0",
    "InstanceType": "t2.medium",
    "KeyName": "<your-key>",
    "SecurityGroupIds": ["<sg-id-west>"],
    "IamInstanceProfile": {"Name": "JenkinsSlaveRole"},
    "BlockDeviceMappings": [{"DeviceName": "/dev/xvda", "Ebs": {"Encrypted": true, "VolumeSize": 10}}],
    "UserData": "IyEvYmluL2Jhc2gKeXVtIHVwZGF0ZSAteQp5dW0gaW5zdGFsbCAteSBqYXZhLTExLW9wZW5qZGsgZG9ja2VyIGdpdCBub2RlanMgYXdzY2xpCnN5c3RlbWN0bCBzdGFydCBkb2NrZXIKdXNlcm1vZCAtYUcgZG9ja2VyIGVjMi11c2VyCmVjaG8gPG1hc3Rlci1wdWJsaWMta2V5PiA+IC9ob21lL2VjMi11c2VyLy5zc2gvYXV0aG9yaXplZF9rZXlzCmNobW9kIDYwMCAvaG9tZS9lYzItdXNlci8uc3NoL2F1dGhvcml6ZWRfa2V5cwpjaG1vZCA3MDAgL2hvbWUvZWMyLXVzZXIvLnNzaA=="
  }' \
  --region us-west-2

aws autoscaling create-auto-scaling-group \
  --auto-scaling-group-name JenkinsSlavesWest \
  --launch-template LaunchTemplateName=JenkinsSlaveWestTemplate \
  --min-size 0 \
  --max-size 10 \
  --desired-capacity 2 \
  --vpc-zone-identifier "<subnet-id-west>" \
  --region us-west-2
