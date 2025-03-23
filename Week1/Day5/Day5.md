**Week 1, Day 5: Mini-Project**, following the extensive, theory-rich, hands-on, and chaos-infused format we’ve established. 

This session is a culmination of Week 1, where participants deploy a static website on an EC2 instance within a custom VPC, automate the setup with a script, and handle a last-minute “CEO tweet” chaos twist. 

It’s packed with theoretical explanations, key concepts, keywords, and practical use cases to solidify AWS foundations while simulating real-world challenges.

---

### Week 1, Day 5: Mini-Project
- **Duration**: 5-6 hours
- **Objective**: Deploy a static website on EC2 in a custom VPC, automate with a script, and adapt to a simulated “CEO tweet” feature request.
- **Tools**: AWS Management Console, AWS CLI, Bash, SSH client (e.g., PuTTY, OpenSSH)
- **Focus Topics**: Infrastructure Automation, Web Hosting, Incident Response

---

### Detailed Breakdown

#### 1. Theory: Infrastructure Automation and Web Hosting (1 hour)
**Goal**: Understand the concepts behind automating AWS infrastructure and hosting a website.
- **Materials**: Slides/video (provided or self-paced), AWS docs (e.g., [EC2 User Guide](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/), [VPC User Guide](https://docs.aws.amazon.com/vpc/latest/userguide/)).
- **Key Concepts & Keywords**:
  - **Infrastructure Automation**: Managing resources programmatically for consistency and speed.
  - **Web Hosting**: Serving content (e.g., HTML) over HTTP/HTTPS.
  - **Elasticity**: Scaling resources based on demand (e.g., EC2 capacity).
  - **Resilience**: Ensuring systems recover from failures or changes.

- **Sub-Activities**:
  1. **Infrastructure Automation Overview (20 min)**:
     - **Concept**: **Infrastructure Automation** uses scripts or tools (e.g., AWS CLI, CloudFormation) to provision resources.
     - **Keywords**: Provisioning, Script, Idempotency, Repeatability.
     - **Details**:
       - **Provisioning**: Creating resources like VPCs, EC2s (e.g., `aws ec2 run-instances`).
       - **Script**: Code to automate tasks (e.g., Bash from Day 4).
       - **Idempotency**: Ensures re-running doesn’t duplicate (e.g., check if EC2 exists).
       - **Repeatability**: Same script, same outcome across environments.
     - **Use Case**: Deploy a dev environment in minutes instead of hours manually.
     - **Action**: Review Day 4’s `setup-ec2-website.sh` script structure.
     - **Why It Matters**: Automation reduces human error and speeds up deployments.

  2. **Web Hosting Basics (20 min)**:
     - **Concept**: **Web Hosting** delivers static or dynamic content via a server (e.g., Apache on EC2).
     - **Keywords**: HTTP, Static Content, Web Server, Port.
     - **Details**:
       - **HTTP**: Protocol for web access (port 80 default).
       - **Static Content**: Fixed files (e.g., HTML, CSS) vs. dynamic (e.g., PHP).
       - **Web Server**: Software like Apache (`httpd`) serving content.
       - **Port**: Network entry (e.g., 80 for HTTP, 443 for HTTPS).
     - **Use Case**: Host a company landing page on EC2 instead of S3 for custom server control.
     - **Action**: Run `curl http://example.com` locally to see HTTP in action.
     - **Why It Matters**: EC2 offers flexible hosting beyond S3’s static limits.

  3. **Tying It Together (15 min)**:
     - **Concept**: Combine VPC, EC2, and scripting for a resilient web setup.
     - **Keywords**: Networking, Security Group, Elastic IP, Failover.
     - **Details**:
       - **Networking**: VPC ensures isolation (Day 3).
       - **Security Group**: Controls access (e.g., HTTP open).
       - **Elastic IP**: Static address for consistency (Day 4).
       - **Failover**: Multi-AZ for **Resilience** (future scope).
     - **Use Case**: Automate a blog site deployment with a fixed IP.
     - **Action**: Skim [EC2 Web Server Guide](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/hosting-website.html).
     - **Why It Matters**: Integrates Week 1 skills into a production-like system.

  4. **Self-Check (5 min)**:
     - Question: “Why automate EC2 setup instead of using the Console?”
     - Answer (write or chat): “Automation ensures **Repeatability**, reduces errors, and scales with **Elasticity**.”

---

#### 2. Lab: Deploy a Static Website with Automation (2.5-3 hours)
**Goal**: Build a VPC, launch an EC2 instance, host a static website, and script the process.
- **Pre-Requisites**: AWS CLI configured, “bootcamp-key.pem”, Day 3’s VPC knowledge.
- **Key Concepts Reinforced**: Provisioning, Web Server, Security Group, Script.

- **Sub-Activities**:
1. **Set Up Environment (15 min)**:
   - **Step 1**: Verify AWS CLI: `aws sts get-caller-identity`.
   - **Step 2**: Ensure key file: `ls -l bootcamp-key.pem` (Windows: `dir`), `chmod 400 bootcamp-key.pem`.
   - **Step 3**: Create a working directory: `mkdir mini-project; cd mini-project`.
   - **Why**: Prepares for clean scripting and execution.

2. **Create Script: `deploy-website.sh` (1 hour)**:
   - **Step 1**: Write the script (adapt Day 4’s `setup-ec2-website.sh`):
     ```bash
     #!/bin/bash
     # Deploy a static website on EC2 in a custom VPC

     set -e  # Exit on error

     # Variables
     REGION="us-east-1"
     VPC_CIDR="10.0.0.0/16"
     SUBNET_CIDR="10.0.1.0/24"
     AMI_ID="ami-0c55b159cbfafe1f0"
     INSTANCE_TYPE="t2.micro"
     KEY_NAME="bootcamp-key"
     SG_NAME="MiniProjectSG"

     # Create VPC
     echo "Creating VPC..."
     VPC_ID=$(aws ec2 create-vpc --cidr-block "$VPC_CIDR" --query Vpc.VpcId --output text)
     aws ec2 modify-vpc-attribute --vpc-id "$VPC_ID" --enable-dns-hostnames
     aws ec2 create-tags --resources "$VPC_ID" --tags Key=Name,Value=MiniProjectVPC

     # Create Subnet
     echo "Creating Subnet..."
     SUBNET_ID=$(aws ec2 create-subnet --vpc-id "$VPC_ID" --cidr-block "$SUBNET_CIDR" --query Subnet.SubnetId --output text)
     aws ec2 create-tags --resources "$SUBNET_ID" --tags Key=Name,Value=PublicSubnet

     # Create Internet Gateway
     echo "Creating Internet Gateway..."
     IGW_ID=$(aws ec2 create-internet-gateway --query InternetGateway.InternetGatewayId --output text)
     aws ec2 attach-internet-gateway --vpc-id "$VPC_ID" --internet-gateway-id "$IGW_ID"

     # Configure Route Table
     echo "Configuring Route Table..."
     RT_ID=$(aws ec2 describe-route-tables --filters "Name=vpc-id,Values=$VPC_ID" --query "RouteTables[0].RouteTableId" --output text)
     aws ec2 create-route --route-table-id "$RT_ID" --destination-cidr-block 0.0.0.0/0 --gateway-id "$IGW_ID"
     aws ec2 associate-route-table --route-table-id "$RT_ID" --subnet-id "$SUBNET_ID"

     # Create Security Group
     echo "Creating Security Group..."
     SG_ID=$(aws ec2 create-security-group --group-name "$SG_NAME" --description "Web server SG" --vpc-id "$VPC_ID" --query GroupId --output text)
     aws ec2 authorize-security-group-ingress --group-id "$SG_ID" --protocol tcp --port 22 --cidr 0.0.0.0/0  # Replace with your IP
     aws ec2 authorize-security-group-ingress --group-id "$SG_ID" --protocol tcp --port 80 --cidr 0.0.0.0/0

     # Launch EC2
     echo "Launching EC2..."
     INSTANCE_ID=$(aws ec2 run-instances \
         --image-id "$AMI_ID" \
         --instance-type "$INSTANCE_TYPE" \
         --subnet-id "$SUBNET_ID" \
         --security-group-ids "$SG_ID" \
         --key-name "$KEY_NAME" \
         --query "Instances[0].InstanceId" --output text)
     aws ec2 wait instance-running --instance-ids "$INSTANCE_ID"
     PUBLIC_IP=$(aws ec2 describe-instances --instance-ids "$INSTANCE_ID" --query "Reservations[0].Instances[0].PublicIpAddress" --output text)

     # Configure Website
     echo "Configuring website on $PUBLIC_IP..."
     ssh -i "$KEY_NAME.pem" -o StrictHostKeyChecking=no ec2-user@"$PUBLIC_IP" << 'EOF'
         sudo yum update -y
         sudo yum install httpd -y
         echo "<h1>Mini-Project Website</h1><p>Built with AWS automation!</p>" | sudo tee /var/www/html/index.html
         sudo systemctl start httpd
         sudo systemctl enable httpd
         sudo chmod -R 755 /var/www/html
     EOF

     echo "Website live at http://$PUBLIC_IP"
     echo "Cleanup: aws ec2 terminate-instances --instance-ids $INSTANCE_ID; aws ec2 delete-vpc --vpc-id $VPC_ID"
     ```
   - **Step 2**: Make executable: `chmod +x deploy-website.sh`.
   - **Why**: Automates VPC, EC2, and web setup with **Provisioning**.

3. **Run and Verify (1-1.5 hours)**:
   - **Step 1**: Execute: `./deploy-website.sh`.
   - **Step 2**: Wait (~5 min) for output (e.g., “Website live at http://54.123.45.67”).
   - **Step 3**: Test in browser: `http://<PUBLIC_IP>` (shows “Mini-Project Website”).
   - **Step 4**: SSH for debug if needed: `ssh -i bootcamp-key.pem ec2-user@<PUBLIC_IP>`, check `systemctl status httpd`.
   - **Why**: Validates **Web Hosting** and **Elasticity** of the setup.

4. **Stretch Goal (Optional, 30 min)**:
   - Add an Elastic IP: Modify script with `aws ec2 allocate-address` and `associate-address`.
   - Tag resources: Add `aws ec2 create-tags` for all resources.
   - **Why**: Enhances **Resilience** and tracking.

---

#### 3. Chaos Twist: "CEO Tweet" (1-1.5 hours)
**Goal**: Adapt to a last-minute request to add a status page, simulating real-world pressure.
- **Trigger**: Instructor announces 30 min before demo: “CEO tweeted: ‘Add a status page now!’”
- **Key Concepts Reinforced**: Incident Response, Web Server, Automation.

- **Sub-Activities**:
1. **Identify the Request (15 min)**:
   - **Step 1**: Define need: A `/status.html` page (e.g., “System: Online”).
   - **Step 2**: Check current site: `curl http://<PUBLIC_IP>` (shows main page).
   - **Why**: Simulates **Incident Response** to stakeholder demands.

2. **Implement the Change (45 min)**:
   - **Step 1**: SSH to EC2: `ssh -i bootcamp-key.pem ec2-user@<PUBLIC_IP>`.
   - **Step 2**: Add status page:
     ```bash
     echo "<h1>Status</h1><p>System: Online</p>" | sudo tee /var/www/html/status.html
     sudo chmod 644 /var/www/html/status.html
     ```
   - **Step 3**: Update index:
     ```bash
     echo "<h1>Mini-Project Website</h1><p><a href='/status.html'>Check Status</a></p>" | sudo tee /var/www/html/index.html
     ```
   - **Step 4**: Test: `http://<PUBLIC_IP>/status.html` in browser.
   - **Why**: Adapts **Web Server** content under time pressure.

3. **Stretch Goal (Optional, 15 min)**:
   - Automate in script: Add status page to SSH heredoc.
   - Test rollback: `sudo mv /var/www/html/index.html.bak /var/www/html/index.html`.
   - **Why**: Builds **Repeatability** into chaos response.

---

#### 4. Wrap-Up: War Room Discussion (30-45 min)
**Goal**: Reflect, present, and reinforce learnings.
- **Key Concepts Reinforced**: Provisioning, Resilience, Incident Response.

- **Sub-Activities**:
  1. **Present Your Setup (15 min)**:
     - Show `http://<PUBLIC_IP>` and `/status.html` to peers.
     - Share a lesson: e.g., “**Security Group** must allow port 80 for HTTP.”
  2. **Chaos Debrief (15 min)**:
     - Discuss: “How did you handle the CEO tweet? What broke?”
     - Instructor explains: “Real-world demands test **Resilience** and adaptability.”
  3. **Q&A (10 min)**:
     - Ask: “Why did my site fail after the update?”
     - Answer: “Check Apache status or file permissions (e.g., `chmod 644`).”
     - Note a Week 2 tip: “Next, we’ll scale with CI/CD.”

---

### Theoretical Takeaways Packed In
- **Automation**: **Provisioning** with scripts, **Idempotency** checks, **Repeatability** across envs.
- **Web Hosting**: **HTTP** setup, **Static Content** deployment, **Web Server** management, **Port** config.
- **Resilience**: **Networking** isolation, **Elasticity** for growth, **Failover** readiness.
- **Incident Response**: Quick adaptation, stakeholder-driven changes.

---

### Practical Use Cases
1. **Company Website**: Automate a marketing site on EC2, update for campaigns (e.g., CEO tweet).
2. **Dev Environment**: Spin up isolated VPCs for testing, tear down post-use.
3. **Disaster Recovery**: Script EC2 relaunch with static backups for fast recovery.

---

### Tips for Participants
- **Prepare**: Bookmark [AWS CLI Reference](https://docs.aws.amazon.com/cli/latest/reference/) and Day 4’s script.
- **Track**: Save script outputs (`tee output.log`) and resource IDs.
- **Ask**: Use “mentor hotline” (e.g., “Why’s my subnet not public?”).

---

### Adjusted Timeline
- **Theory**: 1 hour
- **Lab**: 2.5-3 hours (with breaks)
- **Chaos Twist**: 1-1.5 hours
- **Wrap-Up**: 30-45 min
- **Total**: 5-6 hours (stretch goals optional)

---

This Day 5 ties together Week 1’s skills—VPC (Day 3), scripting (Day 4), and web hosting—into a practical mini-project with a chaotic twist.