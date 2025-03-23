
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

### Notes
- **Tools**: AWS CLI, Terraform, Docker, GitHub Actions, etc., installed locally or in a provided sandbox.
- **Chaos Triggers**: Instructors use scripts or manual interventions (e.g., terminate resources, change configs).
- **Support**: Daily war rooms + “mentor hotline” for stuck participants.

This breakdown ensures basics are covered with clear steps, while the chaos and gamification keep it engaging and real-world-focused. Let me know if you want a specific day expanded further!