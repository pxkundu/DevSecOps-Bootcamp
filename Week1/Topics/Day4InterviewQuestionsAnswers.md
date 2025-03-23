10 interview questions tailored to **Week 1, Day 4: Intro to Scripting** topics, designed to reflect the depth and practical focus of Fortune 100 companies (e.g., Amazon, Microsoft, Google) for AWS DevOps and Cloud Engineer roles. 

These questions test theoretical knowledge, hands-on scripting skills, and troubleshooting abilities related to AWS CLI, Bash scripting, automation, and error handling—core concepts from Day 4. 

Each question is paired with a brief intent to show what it evaluates.

---

### Interview Questions for Day 4 Topics

1. **What is the AWS CLI, and how does it differ from the AWS Management Console?**
   - **Intent**: Tests understanding of **Command-Line Interface (CLI)** vs. GUI and its role in **Automation**.

2. **How would you configure the AWS CLI to manage multiple AWS accounts on a single machine?**
   - **Intent**: Assesses knowledge of **Profile** management and practical CLI setup.

3. **Explain the structure of an AWS CLI command with an example for launching an EC2 instance.**
   - **Intent**: Evaluates grasp of **Command** syntax and ability to apply it to a Day 4 use case (e.g., `aws ec2 run-instances`).

4. **You need to script the creation of an S3 bucket using Bash and AWS CLI. Write a sample script and explain it.**
   - **Intent**: Probes **Bash** scripting skills (**Shebang**, **Variable**) and CLI integration for **Automation**.

5. **What does idempotency mean in the context of scripting, and how would you ensure it when launching EC2 instances?**
   - **Intent**: Tests theoretical understanding of **Idempotency** and practical application in scripts.

6. **Your Bash script to launch an EC2 instance fails with an “InvalidAMIID” error. How do you debug and fix it?**
   - **Intent**: Mirrors Day 4’s chaos twist, assessing **Error Handling** and **Troubleshooting** skills.

7. **How can you use AWS CLI with JSON parsing in a Bash script to extract an instance’s public IP after launch?**
   - **Intent**: Focuses on **JSON Parsing** (e.g., with `jq`) and scripting efficiency.

8. **What’s the purpose of exit codes in Bash, and how would you use them to handle AWS CLI command failures?**
   - **Intent**: Evaluates understanding of **Exit Code** and **Error Handling** in automation workflows.

9. **A team member’s script runs fine once but fails on the second run due to duplicate resources. How would you fix it?**
   - **Intent**: Tests problem-solving for **Idempotency** and resource management (e.g., checking existing instances).

10. **Describe a real-world scenario where you’d automate an AWS task with a Bash script. How would you approach it?**
    - **Intent**: Assesses ability to connect **Automation** theory to practical use cases (e.g., provisioning, monitoring).

---

### Sample Answers (Brief for Reference)

1. **What is the AWS CLI, and how does it differ from the AWS Management Console?**
   - The AWS CLI is a command-line tool to manage AWS services programmatically, unlike the Console’s GUI. For example, `aws ec2 describe-instances` lists instances instantly, while the Console requires navigation. CLI excels in automation and scripting; Console is better for manual exploration.

2. **How would you configure the AWS CLI to manage multiple AWS accounts on a single machine?**
   - I’d use profiles: `aws configure --profile dev` for one account, then `aws configure --profile prod` for another, setting access keys and regions per profile. Commands use `--profile` (e.g., `aws s3 ls --profile dev`), and `~/.aws/credentials` stores them securely.

3. **Explain the structure of an AWS CLI command with an example for launching an EC2 instance.**
   - Structure: `aws <service> <action> [options]`. Example: `aws ec2 run-instances --image-id ami-0c55b159cbfafe1f0 --instance-type t2.micro --subnet-id subnet-123 --key-name bootcamp-key` launches an EC2 with an AMI, instance type, subnet, and key pair specified.

4. **You need to script the creation of an S3 bucket using Bash and AWS CLI. Write a sample script and explain it.**
   - Script:
     ```bash
     #!/bin/bash
     BUCKET="my-bucket-$(date +%s)"
     aws s3 mb s3://$BUCKET --region us-east-1
     if [ $? -eq 0 ]; then
       echo "Bucket $BUCKET created!"
     else
       echo "Failed!"
       exit 1
     fi
     ```
   - Explanation: **Shebang** sets Bash, **Variable** ensures a unique bucket name, `aws s3 mb` makes it, and **Exit Code** (`$?`) checks success.

5. **What does idempotency mean in the context of scripting, and how would you ensure it when launching EC2 instances?**
   - Idempotency means a script produces the same result regardless of how many times it runs. For EC2, I’d check if an instance with a specific tag (e.g., “Name=ScriptedEC2”) exists using `aws ec2 describe-instances` before launching, skipping if it’s already there.

6. **Your Bash script to launch an EC2 instance fails with an “InvalidAMIID” error. How do you debug and fix it?**
   - I’d check the AMI ID in the script—likely outdated. Run `aws ec2 describe-images --owners amazon --filters "Name=name,Values=amzn2-ami-hvm-*" --region us-east-1` to find a valid AMI, update the script (e.g., `AMI_ID="ami-0c55b159cbfafe1f0"`), and rerun it.

7. **How can you use AWS CLI with JSON parsing in a Bash script to extract an instance’s public IP after launch?**
   - I’d use `aws ec2 describe-instances --instance-ids $INSTANCE_ID --query 'Reservations[0].Instances[0].PublicIpAddress' --output text` to get the IP, piped through `jq` if needed (`| jq -r '.Reservations[0].Instances[0].PublicIpAddress'`). In Bash: `IP=$(aws ...)` stores it.

8. **What’s the purpose of exit codes in Bash, and how would you use them to handle AWS CLI command failures?**
   - Exit codes indicate success (0) or failure (non-zero). After `aws ec2 run-instances`, I’d check `if [ $? -ne 0 ]; then echo "Launch failed"; exit 1; fi` to halt the script and alert on failure, ensuring robust error handling.

9. **A team member’s script runs fine once but fails on the second run due to duplicate resources. How would you fix it?**
   - It’s not idempotent. I’d add a check: `aws ec2 describe-instances --filters "Name=tag:Name,Values=ScriptedEC2" --query 'Reservations[].Instances[].InstanceId'` to see if it exists. If so, skip or terminate it before relaunching, avoiding duplicates.

10. **Describe a real-world scenario where you’d automate an AWS task with a Bash script. How would you approach it?**
    - Scenario: Daily backup of EC2 instances. I’d script `aws ec2 create-snapshot` for tagged instances, using a loop to iterate over `aws ec2 describe-instances`, add error handling for failed snapshots, and email results with `mail`. It’d run via cron for automation.

---

These questions align with Day 4’s focus on **Automation**, **AWS CLI**, and **Bash**, testing both theory and practical skills.