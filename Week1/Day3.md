**Week 1, Day 3: Networking Deep Dive**, crafted in the same extensive, theory-rich, hands-on, and chaos-infused format as Days 1 and 2. 

We’ll explore AWS VPC networking in depth, covering subnets, route tables, NAT Gateways, and Security Groups, with a focus on building a multi-tier architecture and handling a simulated DDoS attack. 

This session is packed with theoretical explanations, key concepts, keywords, and practical use cases to ensure participants master AWS networking fundamentals while applying them in real-world scenarios.

---

### Week 1, Day 3: Networking Deep Dive
- **Duration**: 5-6 hours
- **Objective**: Master VPC networking, deploy a multi-tier architecture, and mitigate a simulated DDoS attack.
- **Tools**: AWS Management Console, AWS CLI, SSH client (e.g., Terminal, PuTTY)
- **Focus Topics**: Virtual Networking (VPC), Traffic Routing, Security

---

### Detailed Breakdown

#### 1. Theory: Networking Essentials (1 hour)
**Goal**: Build a comprehensive understanding of AWS VPC and networking components with key concepts and keywords.
- **Materials**: Slides/video (provided or self-paced), AWS docs (e.g., [VPC User Guide](https://docs.aws.amazon.com/vpc/latest/userguide/)).
- **Key Concepts & Keywords**:
  - **Virtual Private Cloud (VPC)**: A logically isolated network in AWS for your resources.
  - **High Availability (HA)**: Ensuring resources remain accessible despite failures (e.g., across AZs).
  - **Security**: Protecting resources from unauthorized access or attacks.
  - **Routing**: Directing network traffic between resources and the internet.

- **Sub-Activities**:
  1. **VPC Overview (15 min)**:
     - **Concept**: **VPC** provides a private, customizable network in the cloud.
     - **Keywords**: CIDR Block, Subnet, Internet Gateway, Route Table.
     - **Details**:
       - **CIDR Block**: IP address range (e.g., 10.0.0.0/16 = 65,536 IPs).
       - **Subnet**: A subdivision of VPC (e.g., 10.0.1.0/24 = 256 IPs), tied to an AZ.
       - **Internet Gateway (IGW)**: Connects VPC to the internet for public access.
       - **Route Table**: Rules for traffic (e.g., 0.0.0.0/0 → IGW for all destinations).
     - **Use Case**: Host a web app in a public subnet, a database in a private subnet.
     - **Action**: VPC Console > View default VPC’s **CIDR** and subnets.
     - **Why It Matters**: VPC enables **Isolation** and **Scalability** for multi-tier apps.

  2. **Subnets and Availability (15 min)**:
     - **Concept**: **Subnets** segment a VPC into public (internet-facing) or private (internal) zones.
     - **Keywords**: Public Subnet, Private Subnet, Availability Zone (AZ), NAT Gateway.
     - **Details**:
       - **Public Subnet**: Has a route to IGW (e.g., for web servers).
       - **Private Subnet**: No direct internet access (e.g., for databases).
       - **Availability Zone**: Isolated data center in a region (e.g., us-east-1a).
       - **NAT Gateway**: Allows private subnets outbound internet access (e.g., for updates).
     - **Use Case**: Public subnet hosts an EC2 web server; private subnet secures an RDS instance.
     - **Action**: VPC > Subnets > Note public vs. private by route table association.
     - **Why It Matters**: Subnets support **High Availability** and **Security** by design.

  3. **Security Groups and Routing (15 min)**:
     - **Concept**: **Security Groups** and **Route Tables** control traffic flow and access.
     - **Keywords**: Security Group, Inbound Rule, Outbound Rule, Default Route.
     - **Details**:
       - **Security Group**: Virtual firewall for instances (e.g., allow SSH on port 22).
       - **Inbound Rule**: Permits incoming traffic (e.g., HTTP from 0.0.0.0/0).
       - **Outbound Rule**: Permits outgoing traffic (default: all allowed).
       - **Default Route**: 0.0.0.0/0 sends unmatched traffic to a target (e.g., IGW).
     - **Use Case**: Allow HTTP to a web server, block all to a private DB.
     - **Action**: EC2 > Security Groups > View default rules (e.g., all outbound).
     - **Why It Matters**: Fine-tuned **Security** prevents attacks like DDoS.

  4. **Real-World Context (10 min)**:
     - **Concept**: Networking ensures **Performance**, **Security**, and **Resilience**.
     - **Keywords**: Latency, Bandwidth, DDoS Mitigation.
     - **Details**:
       - **Latency**: Delay in traffic (minimized by AZ proximity).
       - **Bandwidth**: Data throughput (e.g., NAT Gateway limits).
       - **DDoS Mitigation**: Block malicious traffic (e.g., via Security Groups).
     - **Use Case**: Multi-AZ VPC survives an AZ outage; Security Groups stop brute-force SSH attempts.
     - **Action**: Skim [VPC Best Practices](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-security-best-practices.html).
     - **Why It Matters**: Robust networking is the backbone of production systems.

  5. **Self-Check (5 min)**:
     - Question: “How does a private subnet differ from a public subnet?”
     - Answer (write or chat): “Public has an **Internet Gateway** route; private uses a **NAT Gateway** for outbound only.”

---

#### 2. Lab: Build a Multi-Tier VPC (2.5-3 hours)
**Goal**: Deploy a VPC with public and private subnets, an EC2 instance, and validate connectivity.
- **Pre-Requisites**: AWS account, AWS CLI configured, SSH key (“bootcamp-key” from Day 1).
- **Key Concepts Reinforced**: Subnet, Route Table, NAT Gateway, Security Group, High Availability.

- **Sub-Activities**:
1. **Set Up Your Environment (15 min)**:
   - **Step 1**: Log into AWS Console, use us-east-1.
   - **Step 2**: Verify SSH key: Ensure “bootcamp-key.pem” is accessible.
   - **Step 3**: Check AWS CLI: `aws vpc describe-vpcs` (lists VPCs).
   - **Why**: Prepares for multi-tier networking.

2. **Create a Multi-Tier VPC (1 hour)**:
   - **Step 1**: Create a **VPC**:
     - VPC > Create VPC > Name: “MultiTierVPC”, **CIDR Block**: 10.0.0.0/16.
   - **Step 2**: Add **Subnets**:
     - Public: VPC > Subnets > Create > Name: “PublicSubnet”, **CIDR**: 10.0.1.0/24, AZ: us-east-1a.
     - Private: VPC > Subnets > Create > Name: “PrivateSubnet”, **CIDR**: 10.0.2.0/24, AZ: us-east-1a.
   - **Step 3**: Attach an **Internet Gateway**:
     - VPC > Internet Gateways > Create > Name: “MultiTierIGW” > Attach to “MultiTierVPC”.
   - **Step 4**: Create a **NAT Gateway**:
     - VPC > NAT Gateways > Create > PublicSubnet > Allocate Elastic IP > Name: “MultiTierNAT”.
   - **Step 5**: Configure **Route Tables**:
     - Public Route Table:
       - VPC > Route Tables > Create > Name: “PublicRT” > Associate with “PublicSubnet”.
       - Edit Routes > Add: 0.0.0.0/0 → “MultiTierIGW”.
     - Private Route Table:
       - VPC > Route Tables > Create > Name: “PrivateRT” > Associate with “PrivateSubnet”.
       - Edit Routes > Add: 0.0.0.0/0 → “MultiTierNAT”.
   - **Why**: Public subnet hosts accessible resources; private subnet secures internal ones.

3. **Deploy an EC2 Instance in Private Subnet (1 hour)**:
   - **Step 1**: Launch EC2:
     - EC2 > Launch Instance > Amazon Linux 2 AMI, t2.micro.
     - Network: “MultiTierVPC”, Subnet: “PrivateSubnet”, Key Pair: “bootcamp-key”.
   - **Step 2**: Configure **Security Group**:
     - Create new: Name “PrivateSG”, Rule: SSH (port 22, your IP).
   - **Step 3**: Install a web server:
     - No direct SSH (private subnet); use a bastion host or skip for now (test later).
     - For simplicity, launch a second EC2 in “PublicSubnet”:
       - Security Group “PublicSG”: SSH (port 22, your IP), HTTP (port 80, 0.0.0.0/0).
       - SSH: `ssh -i bootcamp-key.pem ec2-user@<public-ip>`.
       - `sudo yum install httpd -y; sudo systemctl start httpd; echo "<h1>Public Tier</h1>" | sudo tee /var/www/html/index.html`.
   - **Step 4**: Test: `http://<public-ip>` (works); private EC2 unreachable directly.
   - **Why**: Demonstrates **Public Subnet** vs. **Private Subnet** access.

4. **Stretch Goal (Optional, 30 min)**:
   - Add a secondAZ subnet: “PublicSubnet2” (10.0.3.0/24, us-east-1b), associate with “PublicRT”.
   - Test **High Availability**: Launch another EC2 in “PublicSubnet2”, verify access.
   - Use CLI: `aws ec2 describe-subnets --filters "Name=vpc-id,Values=<vpc-id>"`.
   - **Why**: Prepares for **HA** across **AZs**.

---

#### 3. Chaos Twist: "DDoS" Blocks Subnet (1-1.5 hours)
**Goal**: Simulate a DDoS attack by blocking traffic, forcing mitigation with Security Groups.
- **Trigger**: Instructor modifies “PublicSG” to block SSH/HTTP: “DDoS hitting your public subnet!”
- **Key Concepts Reinforced**: Security Group, Inbound Rule, DDoS Mitigation, Troubleshooting.

- **Sub-Activities**:
1. **Identify the Attack (20 min)**:
   - **Step 1**: Test SSH: `ssh -i bootcamp-key.pem ec2-user@<public-ip>` → “Connection refused.”
   - **Step 2**: Check browser: `http://<public-ip>` → Page timeout.
   - **Step 3**: EC2 > Security Groups > “PublicSG” > Note missing rules (instructor removed).
   - **Why**: Mimics a **DDoS** overwhelming or misconfiguring access.

2. **Mitigate the Attack (45 min)**:
   - **Step 1**: Update **Security Group**:
     - EC2 > Security Groups > “PublicSG” > Edit Inbound Rules.
     - Add: SSH (port 22, your IP), HTTP (port 80, 0.0.0.0/0).
   - **Step 2**: Test recovery:
     - SSH again; browser `http://<public-ip>` should show “Public Tier.”
   - **Step 3**: Harden against DDoS:
     - Limit HTTP to a specific IP range (e.g., your network) instead of 0.0.0.0/0.
     - Document: “Restricted HTTP to 192.168.1.0/24 for safety.”
   - **Why**: **Security Groups** are first-line **DDoS Mitigation**.

3. **Stretch Goal (Optional, 15 min)**:
   - Simulate overload: Launch 2 more EC2s in “PublicSubnet”, observe behavior.
   - Add a deny rule: “PublicSG” > Inbound > Deny all from a fake attacker IP (e.g., 1.2.3.4).
   - **Why**: Tests **Scalability** and proactive defense.

---

#### 4. Wrap-Up: War Room Discussion (30-45 min)
**Goal**: Reflect, share, and reinforce networking knowledge.
- **Key Concepts Reinforced**: Route Table, NAT Gateway, Security, High Availability.

- **Sub-Activities**:
  1. **Present Your Setup (15 min)**:
     - Show `http://<public-ip>` and describe your VPC (public vs. private).
     - Share a lesson: e.g., “**NAT Gateway** enables private subnet updates.”
  2. **Chaos Debrief (15 min)**:
     - Discuss: “How did the DDoS hit? What fixed it?”
     - Instructor explains: “**Security Group** misconfigs mimic attack fallout.”
  3. **Q&A (10 min)**:
     - Ask: “Why can’t I SSH to my private EC2?”
     - Answer: “No public IP or route; use a bastion host.”
     - Note a Day 4 tip: “Script VPC setup to avoid manual errors.”

---

### Theoretical Takeaways Packed In
- **VPC**: **CIDR Block** sizing, **Subnet** roles, **Internet Gateway** for connectivity, **Route Table** logic.
- **Subnets**: **Public Subnet** vs. **Private Subnet**, **AZ** for **High Availability**, **NAT Gateway** for outbound.
- **Security**: **Security Group** as a firewall, **Inbound/Outbound Rules**, **DDoS Mitigation** basics.
- **General**: **Latency** in routing, **Bandwidth** limits, **Resilience** via multi-tier design.

---

### Practical Use Cases
1. **E-commerce Platform**: Public subnet for web servers, private for payment DB, NAT for updates.
2. **Content Delivery**: Public subnet hosts an app, private subnet runs analytics, IGW serves users.
3. **Secure API**: Private subnet for backend, Security Groups limit access, NAT for external APIs.

---

### Tips for Participants
- **Prepare**: Bookmark [VPC Networking](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Networking.html).
- **Track**: Save configs (e.g., **Route Table** routes, Security Group rules) in `notes.txt`.
- **Ask**: Use the “mentor hotline” (e.g., “Why’s my private EC2 inaccessible?”).

---

### Adjusted Timeline
- **Theory**: 1 hour
- **Lab**: 2.5-3 hours (with breaks)
- **Chaos Twist**: 1-1.5 hours
- **Wrap-Up**: 30-45 min
- **Total**: 5-6 hours (stretch goals optional)

---

This Day 3 delivers an extensive networking deep dive, blending theory (e.g., **High Availability**, **DDoS Mitigation**) with practical steps and a chaotic twist. 

Tomorrow, we’ll tackle **Week 1, Day 4: Intro to Scripting**—see you then! 