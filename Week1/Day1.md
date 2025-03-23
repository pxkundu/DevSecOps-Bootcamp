**Week 1, Day 1: AWS Basics Refresher** with all theoretical information fully integrated into the breakdown. 

I’ve added key concepts, keywords, and detailed explanations to ensure participants gain a deep understanding of AWS foundational services (EC2, S3, IAM, VPC) alongside the hands-on activities. This maximizes learning while keeping the chaotic, real-world twist engaging.

---

### Week 1, Day 1: AWS Basics Refresher
- **Duration**: 5-6 hours
- **Objective**: Master EC2, S3, IAM, and VPC basics, deploy a simple web server, and recover from a simulated "power outage."
- **Tools**: AWS Management Console, AWS CLI, SSH client (e.g., Terminal, PuTTY)
- **Focus Topics**: Compute (EC2), Storage (S3), Identity (IAM), Networking (VPC)

---

### Detailed Breakdown

#### 1. Theory: AWS Basics Overview (1 hour)
**Goal**: Build a comprehensive conceptual foundation for AWS services with key concepts and keywords.
- **Materials**: Slides/video (provided or self-paced), AWS documentation links (e.g., [AWS Glossary](https://docs.aws.amazon.com/general/latest/gr/glos-chap.html)).
- **Key Concepts & Keywords**:
  - **AWS (Amazon Web Services)**: A cloud computing platform offering scalable, on-demand services like compute, storage, and networking.
  - **Region**: A geographical area (e.g., us-east-1) hosting AWS data centers. Each region has multiple **Availability Zones (AZs)**—isolated locations for fault tolerance.
  - **Pay-as-You-Go**: Billing model where you pay only for resources used, no upfront costs.
  - **Free Tier**: Limited free usage for new users (e.g., 750 hours of t2.micro EC2/month).

- **Sub-Activities**:
  1. **Introduction to AWS (15 min)**:
     - **Concept**: AWS provides a global infrastructure for building applications.
     - **Keywords**: Cloud Computing, Scalability, Elasticity.
     - **Details**: Over 200 services, from compute (EC2) to AI (SageMaker). **Elasticity** means resources scale up/down automatically.
     - **Action**: Open AWS Console, select a region (e.g., us-east-1), note 2-3 services (e.g., EC2, S3).
     - **Why It Matters**: Understanding regions/AZs ensures high availability and low latency.

  2. **EC2 Deep Dive (15 min)**:
     - **Concept**: **Elastic Compute Cloud (EC2)** provides virtual servers in the cloud.
     - **Keywords**: Instance, AMI (Amazon Machine Image), Instance Type, Key Pair.
     - **Details**:
       - **Instance**: A virtual machine (e.g., t2.micro = 1 vCPU, 1 GiB RAM, Free Tier).
       - **AMI**: A pre-configured template (e.g., Amazon Linux 2) with OS and software.
       - **Instance Type**: Defines CPU/memory (e.g., t2 for general-purpose, m5 for compute-heavy).
       - **Key Pair**: Public/private keys for SSH access (e.g., `.pem` file).
     - **Action**: EC2 > Instance Types > Search “t2.micro”; note its specs.
     - **Why It Matters**: EC2 is the backbone of compute workloads; choosing the right type saves costs.

  3. **S3 Basics (10 min)**:
     - **Concept**: **Simple Storage Service (S3)** is object storage for files, not a traditional filesystem.
     - **Keywords**: Bucket, Object, Access Policy, Versioning.
     - **Details**:
       - **Bucket**: A container for data (globally unique name, e.g., “my-bucket-123”).
       - **Object**: A file + metadata (e.g., `photo.jpg`, size, type).
       - **Access Policy**: JSON rules for permissions (e.g., public read).
       - **Versioning**: Keeps multiple versions of an object.
     - **Action**: S3 Console > Note the “Create Bucket” button; read about versioning.
     - **Why It Matters**: S3 is durable (99.999999999% durability) and versatile (static sites, backups).

  4. **IAM Essentials (10 min)**:
     - **Concept**: **Identity and Access Management (IAM)** controls who/what accesses AWS resources.
     - **Keywords**: User, Role, Policy, Principle of Least Privilege.
     - **Details**:
       - **User**: An individual or app with credentials (access key, password).
       - **Role**: Temporary permissions for AWS services (e.g., EC2 accessing S3).
       - **Policy**: JSON defining actions (e.g., `s3:GetObject`) and resources.
       - **Principle of Least Privilege**: Grant only needed permissions.
     - **Action**: IAM > Policies > View `AmazonS3ReadOnlyAccess`:
       ```json
       {
         "Effect": "Allow",
         "Action": "s3:Get*",
         "Resource": "*"
       }
       ```
     - **Why It Matters**: IAM prevents unauthorized access, critical for security.

  5. **VPC Fundamentals (10 min)**:
     - **Concept**: **Virtual Private Cloud (VPC)** is a private network in AWS.
     - **Keywords**: Subnet, CIDR, Internet Gateway, Route Table, Security Group.
     - **Details**:
       - **Subnet**: A segment of VPC (e.g., public for web, private for DB).
       - **CIDR**: IP range (e.g., 10.0.0.0/16 = 65,536 IPs).
       - **Internet Gateway**: Connects VPC to the internet.
       - **Route Table**: Directs traffic (e.g., 0.0.0.0/0 → internet).
       - **Security Group**: Firewall for instances (e.g., allow port 22).
     - **Action**: VPC Console > View default VPC’s CIDR (e.g., 172.31.0.0/16).
     - **Why It Matters**: VPC isolates resources, enabling secure, scalable architectures.

- **Self-Check (5 min)**:
  - Question: “How does a VPC subnet differ from an S3 bucket?”
  - Answer (write or chat): “A subnet is a network segment in a VPC for instances; an S3 bucket stores objects.”

---

#### 2. Lab: Launch an EC2 Instance in a Custom VPC (2.5-3 hours)
**Goal**: Apply theory hands-on, deploying a web server with key concepts in action.
- **Pre-Requisites**: AWS account, AWS CLI installed (`aws --version`), SSH client.
- **Key Concepts Reinforced**: Instance, Subnet, Security Group, AMI, Key Pair.

- **Sub-Activities**:
1. **Set Up Your Environment (15 min)**:
   - **Step 1**: Log into AWS Console, select us-east-1 (a **Region** with multiple **AZs**).
   - **Step 2**: Create a **Key Pair**:
     - EC2 > Key Pairs > Create > Name: “bootcamp-key” > Download `bootcamp-key.pem`.
     - Secure it: `chmod 400 bootcamp-key.pem` (Linux/Mac) or restrict access (Windows).
   - **Step 3**: Verify AWS CLI:
     ```bash
     aws configure
     # Access Key, Secret Key, us-east-1, json
     ```
   - **Why**: **Key Pair** ensures secure SSH; CLI enables automation.

2. **Create a Custom VPC (30 min)**:
   - **Step 1**: VPC Dashboard > Create VPC.
     - Name: “BootcampVPC”, **CIDR**: 10.0.0.0/16 (65,536 IPs across **AZs**).
   - **Step 2**: Add a **Subnet**:
     - VPC > Subnets > Create > Name: “PublicSubnet”, **CIDR**: 10.0.1.0/24 (256 IPs).
     - Assign to “BootcampVPC”, pick an AZ (e.g., us-east-1a).
   - **Step 3**: Attach an **Internet Gateway**:
     - VPC > Internet Gateways > Create > Name: “BootcampIGW” > Attach to “BootcampVPC”.
   - **Step 4**: Configure **Route Table**:
     - VPC > Route Tables > Select “BootcampVPC” default > Edit Routes.
     - Add: Destination: 0.0.0.0/0 (all traffic), Target: “BootcampIGW”.
     - Associate with “PublicSubnet”.
   - **Why**: **VPC** isolates resources; **Subnet** hosts instances; **Internet Gateway** enables public access.

3. **Launch an EC2 Instance (45 min)**:
   - **Step 1**: EC2 > Launch Instance.
     - Select **AMI**: Amazon Linux 2 (Free Tier, pre-configured OS).
     - **Instance Type**: t2.micro (1 vCPU, 1 GiB RAM).
     - Network: “BootcampVPC”, Subnet: “PublicSubnet”.
     - **Key Pair**: “bootcamp-key”.
   - **Step 2**: Add **Security Group**:
     - Create new: Name “WebSG”.
     - Rules: SSH (port 22, your IP), HTTP (port 80, 0.0.0.0/0).
   - **Step 3**: Launch, note **Public IP** (e.g., 54.123.45.67).
   - **Why**: **Instance** runs your app; **Security Group** acts as a firewall.

4. **Set Up a Web Server (45 min)**:
   - **Step 1**: SSH into the instance:
     ```bash
     ssh -i bootcamp-key.pem ec2-user@<public-ip>
     ```
   - **Step 2**: Install Apache (HTTP server):
     ```bash
     sudo yum update -y
     sudo yum install httpd -y
     sudo systemctl start httpd
     sudo systemctl enable httpd
     ```
   - **Step 3**: Create a webpage:
     ```bash
     echo "<h1>Welcome to Bootcamp!</h1>" | sudo tee /var/www/html/index.html
     ```
   - **Step 4**: Test: `http://<public-ip>` in browser.
     - If it fails, check **Security Group** (port 80 open?) or instance status (running?).
   - **Why**: Demonstrates **Elasticity**—quickly spin up a server.

5. **Stretch Goal (Optional, 15 min)**:
   - **CLI Exploration**: Check instance details:
     ```bash
     aws ec2 describe-instances --filters "Name=tag:Name,Values=BootcampInstance"
     ```
   - **Tagging**: EC2 > Instances > Actions > Add/Edit Tags > Key: “Name”, Value: “BootcampInstance”.
   - **Why**: Tags organize resources; CLI builds automation skills.

---

#### 3. Chaos Twist: "Power Outage" (1.5-2 hours)
**Goal**: Simulate a failure (subnet or IGW loss) to teach recovery and resilience.
- **Trigger**: Instructor deletes “PublicSubnet” or detaches “BootcampIGW” mid-lab, announcing: “Power outage in us-east-1!”
- **Key Concepts Reinforced**: Route Table, Subnet, Internet Gateway, Troubleshooting.

- **Sub-Activities**:
1. **Identify the Failure (20 min)**:
   - **Step 1**: Test SSH: `ssh -i bootcamp-key.pem ec2-user@<public-ip>` → “Connection timed out.”
   - **Step 2**: Check browser: `http://<public-ip>` → Page unavailable.
   - **Step 3**: VPC Console > Subnets:
     - If “PublicSubnet” is gone, note the loss.
   - **Step 4**: VPC > Route Tables:
     - Check if 0.0.0.0/0 points to “BootcampIGW” or if IGW is detached.
   - **Why**: Simulates **Availability Zone** failure or network misconfiguration.

2. **Recover the Setup (1 hour)**:
   - **Step 1**: Recreate **Subnet** if deleted:
     - VPC > Subnets > Create > Name: “PublicSubnet”, **CIDR**: 10.0.1.0/24, VPC: “BootcampVPC”.
   - **Step 2**: Move EC2 to new **Subnet**:
     - EC2 > Instances > Actions > Networking > Change Subnet > “PublicSubnet”.
   - **Step 3**: Reattach **Internet Gateway** if detached:
     - VPC > Internet Gateways > Actions > Attach to “BootcampVPC”.
   - **Step 4**: Fix **Route Table**:
     - VPC > Route Tables > Edit Routes > 0.0.0.0/0 → “BootcampIGW”.
     - Associate with “PublicSubnet”.
   - **Step 5**: Test SSH and browser; confirm web server is back.
   - **Why**: Teaches **Fault Tolerance**—recovering from infra loss.

3. **Document the Fix (15 min)**:
   - Write an **Incident Report**:
     - What failed? (e.g., “Subnet deleted, no route to internet.”)
     - Steps taken? (e.g., “Recreated subnet, reassigned EC2.”)
     - Prevention? (e.g., “Use multiple AZs or IaC like CloudFormation.”)
   - **Why**: Post-mortems are a DevOps best practice.

4. **Stretch Goal (Optional, 15 min)**:
   - Simulate another outage: EC2 > Actions > Stop Instance.
   - Restart it (Actions > Start), verify recovery.
   - **Why**: Tests **Elasticity** and instance lifecycle.

---

#### 4. Wrap-Up: War Room Discussion (30-45 min)
**Goal**: Reflect and solidify learning with peers.
- **Key Concepts Reinforced**: Scalability, Fault Tolerance, Security Group.

- **Sub-Activities**:
  1. **Present Your Setup (15 min)**:
     - Show `http://<public-ip>` to peers/instructor.
     - Share a lesson: e.g., “**Security Groups** must allow HTTP for web access.”
  2. **Chaos Debrief (15 min)**:
     - Discuss: “What broke? How did you recover?”
     - Instructor explains: “Subnet loss mimics hardware failure; **Route Tables** are critical.”
  3. **Q&A (10 min)**:
     - Ask: “Why didn’t my SSH work after fixing the subnet?”
     - Answer: “Check **Security Group** rules or instance public IP change.”
     - Note a Day 2 tip: “Always tag resources for tracking.”

---

### Theoretical Takeaways Packed In
- **EC2**: **Instance** lifecycle (launch, stop, start), **AMI** selection, **Key Pair** security, **Instance Type** optimization.
- **S3**: **Bucket** as object storage, **Access Policy** basics, **Versioning** for durability.
- **IAM**: **Role** vs. **User**, **Policy** structure, **Principle of Least Privilege**.
- **VPC**: **Subnet** segmentation, **CIDR** notation, **Internet Gateway** for connectivity, **Route Table** routing, **Security Group** firewall.
- **General**: **Region/AZ** for HA, **Elasticity** for scaling, **Fault Tolerance** for resilience.

---

### Tips for Participants
- **Prepare**: Bookmark [AWS EC2 Docs](https://docs.aws.amazon.com/ec2/) and [VPC Docs](https://docs.aws.amazon.com/vpc/).
- **Track**: Save commands in `notes.txt` (e.g., `ssh`, `aws ec2 describe-instances`).
- **Ask**: Use the “mentor hotline” (e.g., “Why’s my **Route Table** not working?”).

---

### Adjusted Timeline
- **Theory**: 1 hour
- **Lab**: 2.5-3 hours (with breaks)
- **Chaos Twist**: 1.5-2 hours
- **Wrap-Up**: 30-45 min
- **Total**: 5-6 hours (stretch goals optional)

---

This version crams in all the theoretical meat—key concepts like **Elasticity**, **Fault Tolerance**, and **CIDR**—while tying them directly to hands-on steps. The chaos twist reinforces troubleshooting, making the learning stick. 