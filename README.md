# DevSecOps-Bootcamp
6-week DevSecOps bootcamp with step-by-step instructions for participants to follow. Used out-of-the-box approach intact, blending foundational learning with chaos, gamification, and real-world simulation.

Below is a detailed breakdown of each day’s activities for the 6-week bootcamp, with step-by-step instructions for participants to follow. 

I’ve kept the out-of-the-box approach intact, blending foundational learning with chaos, gamification, and real-world simulation. Each day is structured for 4-6 hours, with clear tasks, tools, and processes to guide intermediate AWS DevOps and Cloud Engineers.

---
### Content Index

## Table of Contents

### Week1

- [Week1 Overview](Week1/README.md) - General introduction to Week 1
- [Week1 Day1 Overview](Week1/Day1.md) - Day 1 activities and notes
- [Week1 Day2 Overview](Week1/Day2.md) - Day 2 activities and notes
- [Week1 Day3 Overview](Week1/Day3.md) - Day 3 activities and notes
- [Week1 Day4 Overview](Week1/Day4.md) - Day 4 activities and notes
- [Week1 Day5 Overview](Week1/Day5/README.md) - Day 5 summary and project overview
  - [Day5 Project Details](Week1/Day5/Day5.md) - Detailed Day 5 project documentation

### Week2

- [Week2 Overview](Week2/README.md) - General introduction to Week 2
- [Week2 Day1 Overview](Week2/Day1.md) - Day 1 activities and notes
- [Week2 Day2 Overview](Week2/Day2.md) - Day 2 activities and notes
- [Week2 Day3 Overview](Week2/Day3.md) - Day 3 activities and notes
- [Week2 Day4 Overview](Week2/Day4/Day4.md) - Day 4 summary and project overview
- [Week2 Day5 Overview](Week2/Day5/README.md) - Day 5 summary and project overview
  - [Day5 Project Details](Week2/Day5/Day5.md) - Detailed Day 5 project documentation

### Week3

- [Week3 Overview](Week3/README.md) - General introduction to Week 3
- [Week3 Day1 Overview](Week3/Day1.md) - Day 1 activities and notes
- [Week3 Day2 Overview](Week3/Day2.md) - Day 2 activities and notes
- [Week3 Day3 Overview](Week3/Day3/README.md) - Day 3 summary and project overview
  - [Pipeline Library Documentation](Week3/Day3/week3-day3/pipeline-lib/README.md) - Pipeline library details
  - [Task Manager Documentation](Week3/Day3/week3-day3/task-manager/README.md) - Task manager project details
- [Week3 Day4 Overview](Week3/Day4/README.md) - Day 4 summary and project overview
  - [Pipeline Library Documentation](Week3/Day4/week3-day4/pipeline-lib/README.md) - Pipeline library details
  - [Task Manager GitOps Documentation](Week3/Day4/week3-day4/task-manager-gitops/README.md) - GitOps implementation details
- [Week3 Day5 Overview](Week3/Day5/Day5.md) - Day 5 summary and project overview
  - [Jenkins Master-Slave Automation Documentation](Week3/Day5/JenkinsMasterSlaveAutomation/README.md) - Jenkins automation project details

### Week4

- [Week4 Overview](Week4/README.md) - General introduction to Week 4
- [Week4 Day1 Overview](Week4/Day1/README.md) - Day 1 summary and project overview
  - [Static Website Terraform Jenkins Documentation](Week4/Day1/StaticWebsiteTerraformJenkins/README.md) - Static website project with Terraform and Jenkins
- [Week4 Day2 Overview](Week4/Day2/README.md) - Day 2 summary and project overview
  - [Advance Topics Project Overview](Week4/Day2/ProjectWithAdvanceTopics/README.md) - Overview of advanced topics project
  - [CRM Terraform Jenkins Documentation](Week4/Day2/ProjectWithAdvanceTopics/CRMTerraformJenkins/README.md) - CRM project with Terraform and Jenkins
- [Week4 Day3 Overview](Week4/Day3/README.md) - Day 3 summary and project overview
  - [Message Encoder Decoder K8s Documentation](Week4/Day3/MessageEncoderDecoderK8s/README.md) - Kubernetes-based message encoder/decoder project
- [Week4 Day4 Overview](Week4/Day4/README.md) - Day 4 activities and notes
- [Week4 Day5 Overview](Week4/Day5/README.md) - Day 5 summary and capstone project overview
  - [CRM Supply Chain Capstone Documentation](Week4/Day5/CRMSupplyChainCapstone/README.md) - Main capstone project documentation
  - [Capstone Docs Overview](Week4/Day5/CRMSupplyChainCapstone/docs/README.md) - Additional documentation for capstone
  - [Project Implementation Plan Overview](Week4/Day5/ProjectImplementationPlan/README.md) - Implementation plan overview
  - [Phase1 Documentation](Week4/Day5/ProjectImplementationPlan/Phase1/README.md) - Phase 1 details
  - [Phase2 Documentation](Week4/Day5/ProjectImplementationPlan/Phase2/README.md) - Phase 2 details
  - [Phase3 Documentation](Week4/Day5/ProjectImplementationPlan/Phase3/README.md) - Phase 3 details
  - [Phase4 Documentation](Week4/Day5/ProjectImplementationPlan/Phase4/README.md) - Phase 4 details
  - [Phase5 Documentation](Week4/Day5/ProjectImplementationPlan/Phase5/README.md) - Phase 5 details

### Week5

- [Week5 Overview](Week5/README.md) - General introduction to Week 5
- [Week5 Day1 Overview](Week5/Day1/README.md) - Day 1 activities and security focus
--- 

### Week 1: Core AWS Foundations with a Twist
**Goal**: Build AWS basics with light chaos to spark engagement.

#### Day 1: AWS Basics Refresher
- **Duration**: 4-5 hours
- **Objective**: Set up foundational AWS resources and recover from a simulated failure.
- **Tools**: AWS Console, AWS CLI

**Activities**:
1. **Theory (1 hour)** - AWS Basics Overview
   - Watch a 30-minute video or live session on EC2, S3, IAM, and VPC basics.
   - Review key concepts: instance types, bucket policies, roles, subnets.
   - Take a 5-question quiz (e.g., “What’s an IAM role?”) to self-assess.

2. **Lab: Launch an EC2 Instance in a Custom VPC (2 hours)**
   - **Step 1**: Log into AWS Console and select a region (e.g., us-east-1).
   - **Step 2**: Create a VPC (CIDR: 10.0.0.0/16), add one public subnet (10.0.1.0/24).
     - Go to VPC Dashboard > Create VPC > Name it “BootcampVPC”.
     - Add subnet under Subnets > Associate with default route table.
   - **Step 3**: Set up an Internet Gateway and attach it to the VPC.
     - VPC > Internet Gateways > Create > Attach to “BootcampVPC”.
   - **Step 4**: Launch an EC2 instance (t2.micro, Amazon Linux 2).
     - EC2 Dashboard > Launch Instance > Assign to “BootcampVPC” subnet.
     - Create a Security Group allowing SSH (port 22) from your IP.
   - **Step 5**: SSH into the instance (`ssh -i <key.pem> ec2-user@<public-ip>`).
     - Install a simple web server: `sudo yum install httpd -y; sudo systemctl start httpd`.
   - **Step 6**: Verify the web server works via browser (`http://<public-ip>`).

3. **Chaos Twist: "Power Outage" (1 hour)**
   - **Trigger**: Instructor terminates the subnet mid-lab (simulated via deletion or route table change).
   - **Step 1**: Notice the instance is unreachable (SSH fails, web server down).
   - **Step 2**: Check VPC resources in AWS Console; identify missing subnet.
   - **Step 3**: Recreate the subnet (10.0.1.0/24) and reassign the instance.
     - VPC > Subnets > Create > Assign to “BootcampVPC”.
     - EC2 > Actions > Networking > Change Subnet.
   - **Step 4**: Update route table to point to Internet Gateway.
   - **Step 5**: Test SSH and web server again; document what broke and how you fixed it.

4. **Wrap-Up (30 min)**: Share recovery steps in a quick “war room” discussion.

---

#### Day 2: Storage and Databases
- **Duration**: 4-5 hours
- **Objective**: Deploy S3 and RDS with a competitive twist.
- **Tools**: AWS Console, MySQL Workbench

**Activities**:
1. **Theory (1 hour)** - Storage and DB Basics
   - Learn S3 (buckets, policies, versioning) and RDS (instances, endpoints) via slides/video.
   - Key takeaway: Public vs. private access, DB connectivity.

2. **Lab: Deploy a Static Site + RDS (2.5 hours)**
   - **Step 1**: Create an S3 bucket (`bootcamp-<yourname>-site`).
     - S3 > Create Bucket > Enable static website hosting.
     - Upload a simple `index.html` (e.g., “Hello, Bootcamp!”).
     - Set bucket policy for public read:
       ```json
       {
         "Statement": [
           {
             "Effect": "Allow",
             "Principal": "*",
             "Action": "s3:GetObject",
             "Resource": "arn:aws:s3:::bootcamp-<yourname>-site/*"
           }
         ]
       }
       ```
   - **Step 2**: Launch an RDS instance (MySQL, db.t2.micro).
     - RDS > Create Database > Free Tier > Set password, assign to “BootcampVPC”.
     - Security Group: Allow MySQL (port 3306) from your IP.
   - **Step 3**: Connect via MySQL Workbench (`<endpoint>:3306`, username: admin).
     - Create a table: `CREATE TABLE users (id INT, name VARCHAR(50));`.
     - Insert data: `INSERT INTO users VALUES (1, 'Alice');`.
   - **Step 4**: Test S3 site in browser (`http://<bucket-url>`).

3. **Gamified Twist: Speed Race (1 hour)**
   - Instructor starts a timer; fastest team to deploy site + DB wins “Storage Master” title.
   - Bonus: Add a second HTML file to S3 and query RDS (`SELECT * FROM users;`).

4. **Wrap-Up (30 min)**: Share URLs and DB outputs with peers.

---

#### Day 3: Networking Deep Dive
- **Duration**: 4-5 hours
- **Objective**: Build a multi-tier VPC and handle a simulated attack.
- **Tools**: AWS Console

**Activities**:
1. **Theory (1 hour)** - Networking Essentials
   - Study VPC subnets, NAT Gateways, and Security Groups (video or live).
   - Focus: Public vs. private subnets, routing.

2. **Lab: Build a Multi-Tier VPC (2 hours)**
   - **Step 1**: Create a VPC (10.0.0.0/16).
   - **Step 2**: Add subnets:
     - Public (10.0.1.0/24) + Private (10.0.2.0/24).
   - **Step 3**: Attach an Internet Gateway to the VPC.
   - **Step 4**: Create a NAT Gateway in the public subnet.
     - Allocate an Elastic IP > NAT Gateway > Assign to public subnet.
   - **Step 5**: Update route tables:
     - Public: 0.0.0.0/0 → Internet Gateway.
     - Private: 0.0.0.0/0 → NAT Gateway.
   - **Step 6**: Launch an EC2 in the private subnet; verify no public access.

3. **Chaos Twist: "DDoS" Blocks Subnet (1.5 hours)**
   - **Trigger**: Instructor modifies Security Group to block SSH (port 22).
   - **Step 1**: Notice SSH failure to private EC2.
   - **Step 2**: Check Security Groups and route tables in AWS Console.
   - **Step 3**: Add a new rule to allow SSH from your IP.
   - **Step 4**: Test connectivity and secure the setup (e.g., limit IP range).

4. **Wrap-Up (30 min)**: Discuss attack mitigation strategies.

---

#### Day 4: Intro to Scripting
- **Duration**: 4-5 hours
- **Objective**: Automate EC2 setup with a scripted failure.
- **Tools**: AWS CLI, Bash

**Activities**:
1. **Theory (1 hour)** - Scripting Basics
   - Learn AWS CLI commands and Bash essentials (video or live).
   - Example: `aws ec2 describe-instances`.

2. **Lab: Automate EC2 Provisioning (2 hours)**
   - **Step 1**: Install AWS CLI locally (`aws configure` with access keys).
   - **Step 2**: Write a Bash script (`launch-ec2.sh`):
     ```bash
     #!/bin/bash
     aws ec2 run-instances --image-id ami-0c55b159cbfafe1f0 --instance-type t2.micro --subnet-id <subnet-id> --security-group-ids <sg-id> --key-name <keypair>
     ```
   - **Step 3**: Make it executable (`chmod +x launch-ec2.sh`) and run it.
   - **Step 4**: SSH into the instance and install httpd as on Day 1.

3. **Chaos Twist: Script Fails (1.5 hours)**
   - **Trigger**: Instructor swaps AMI ID to an invalid one mid-lab.
   - **Step 1**: Run script; note the error (`InvalidAMIID`).
   - **Step 2**: Debug: Check AMI availability (`aws ec2 describe-images --filters "Name=name,Values=amzn2*"`).
   - **Step 3**: Update script with a valid AMI (e.g., `ami-0c55b159cbfafe1f0`).
   - **Step 4**: Rerun and verify the web server works.

4. **Wrap-Up (30 min)**: Share scripts and fixes.

---

#### Day 5: Mini-Project
- **Duration**: 5-6 hours
- **Objective**: Deploy a web app with a last-minute twist.
- **Tools**: AWS Console, AWS CLI

**Activities**:
1. **Project Setup (2 hours)**:
   - **Step 1**: Reuse “BootcampVPC” with public subnet.
   - **Step 2**: Launch an EC2 with httpd installed (manual or scripted).
   - **Step 3**: Create an S3 bucket for static assets (e.g., CSS file).
   - **Step 4**: Link S3 asset in EC2’s `index.html` (e.g., `<link href="http://<bucket-url>/style.css">`).

2. **Chaos Twist: "CEO Tweet" (2 hours)**:
   - **Trigger**: Instructor demands a status page 30 minutes before demo.
   - **Step 1**: Create `status.html` (“System: Online”) and upload to S3.
   - **Step 2**: Update EC2’s `index.html` with a link to the status page.
   - **Step 3**: Test both pages in browser.

3. **Demo and Wrap-Up (1-2 hours)**:
   - Present app to peers (URL + architecture sketch).
   - Discuss chaos response in a war room session.

---

### Weeks 2-6: Summary with Similar Detail Available
To avoid overwhelming this response, here’s a high-level breakdown for the remaining weeks. I can expand any day with step-by-step instructions if you’d like!

#### Week 2: Infrastructure as Code and Containers
- **Day 1**: CloudFormation Basics - Write a template, deploy EC2 + RDS, fix a random error.
- **Day 2**: Terraform Intro - Rebuild Day 1 stack, race against peers.
- **Day 3**: Docker Fundamentals - Build/run a container, solve an escape room challenge.
- **Day 4**: Containers on ECS - Deploy to Fargate, scale after a traffic spike.
- **Day 5**: Mini-Hackathon - IaC + ECS app, recover from Chaos Monkey.

#### Week 3: CI/CD and Serverless with Incident Drills
- **Day 1**: CI/CD Basics - GitHub Actions pipeline, rollback a bad commit.
- **Day 2**: AWS CodeSuite - CodePipeline for ECS, fix a prod outage.
- **Day 3**: Serverless Foundations - Lambda API, secure from a rival “hack.”
- **Day 4**: Pipeline Under Pressure - Multi-stage deploy, add a feature mid-build.
- **Day 5**: Incident Showdown - Fix a cascading failure, write a post-mortem.

#### Week 4: Scalability and Monitoring with Chaos
- **Day 1**: Load Balancing - ALB setup, tune for a surge.
- **Day 2**: Autoscaling - Add autoscaling, recover a terminated instance.
- **Day 3**: CloudWatch - Monitor ECS, solve a performance mystery.
- **Day 4**: EKS Intro - Deploy to EKS, heal a crashed pod.
- **Day 5**: Resilience Rally - Scalable app, survive a chaos test.

#### Week 5: Security, Cost, and Troubleshooting
- **Day 1**: Security Basics - Encrypt S3/RDS, fix an exposed bucket.
- **Day 2**: Disaster Recovery - Multi-AZ RDS, failover after outage.
- **Day 3**: Cost Optimization - Cut costs, avoid “firing” for overspending.
- **Day 4**: Troubleshooting - Debug with X-Ray, solve a gauntlet.
- **Day 5**: Mini-Project - Secure app with DR, pass a peer audit.

#### Week 6: Capstone and Real-World Crunch
- **Day 1**: Capstone Kickoff - Plan microservices, swap a tool mid-plan.
- **Day 2**: Build and Automate - CI/CD + EKS, scale for a DDoS.
- **Day 3**: Secure and Monitor - Add encryption/alarms, pass a pen test.
- **Day 4**: Chaos Crunch - Survive outages/spikes, write a runbook.
- **Day 5**: Prod Push - Demo to “execs,” score on resilience/creativity.

---

### Notes
- **Tools**: AWS CLI, Terraform, Docker, GitHub Actions, etc., installed locally or in a provided sandbox.
- **Chaos Triggers**: Instructors use scripts or manual interventions (e.g., terminate resources, change configs).
- **Support**: Daily war rooms + “mentor hotline” for stuck participants.

This breakdown ensures basics are covered with clear steps, while the chaos and gamification keep it engaging and real-world-focused.
