**Week 1, Day 4: Intro to Scripting**, following the extensive, theory-rich, hands-on, and chaos-infused format we’ve established. 

We’ll dive into scripting with AWS CLI and Bash, automating EC2 provisioning, and handling a simulated script failure. 

This session is packed with theoretical explanations, key concepts, keywords, and practical use cases to ensure participants master automation fundamentals while applying them in real-world scenarios.

---

### Week 1, Day 4: Intro to Scripting
- **Duration**: 5-6 hours
- **Objective**: Master AWS CLI and Bash scripting, automate EC2 provisioning, and debug a simulated script failure.
- **Tools**: AWS Management Console, AWS CLI, Bash shell (e.g., Terminal, Git Bash), SSH client
- **Focus Topics**: Automation, Command-Line Interface, Scripting

---

### Detailed Breakdown

#### 1. Theory: Scripting Basics (1 hour)
**Goal**: Build a deep understanding of AWS CLI and Bash scripting with key concepts and keywords.
- **Materials**: Slides/video (provided or self-paced), AWS docs (e.g., [AWS CLI Reference](https://docs.aws.amazon.com/cli/latest/reference/)), [Bash Guide](https://www.gnu.org/software/bash/manual/).
- **Key Concepts & Keywords**:
  - **Automation**: Performing tasks programmatically to save time and reduce errors.
  - **Command-Line Interface (CLI)**: Text-based tool for interacting with systems (e.g., AWS CLI).
  - **Scripting**: Writing code to execute sequential commands (e.g., Bash scripts).
  - **Idempotency**: Ensuring a script can run multiple times with the same result.

- **Sub-Activities**:
  1. **AWS CLI Overview (20 min)**:
     - **Concept**: **AWS Command Line Interface (CLI)** is a tool to manage AWS services via commands.
     - **Keywords**: Profile, Command, Output Format, Region.
     - **Details**:
       - **Profile**: Configured credentials (e.g., access key, secret key) in `~/.aws/credentials`.
       - **Command**: Structured as `aws <service> <action> [options]` (e.g., `aws ec2 describe-instances`).
       - **Output Format**: JSON, text, or table (e.g., `--output table`).
       - **Region**: Specifies scope (e.g., `--region us-east-1`).
     - **Use Case**: List all S3 buckets across accounts with one command instead of Console clicks.
     - **Action**: Run `aws configure list` to see current setup.
     - **Why It Matters**: CLI enables **Automation** and scales beyond manual Console use.

  2. **Bash Scripting Basics (20 min)**:
     - **Concept**: **Bash** (Bourne Again Shell) is a Unix shell for writing scripts.
     - **Keywords**: Shebang, Variable, Conditional, Loop, Exit Code.
     - **Details**:
       - **Shebang**: `#!/bin/bash` declares the interpreter.
       - **Variable**: Stores data (e.g., `instance_id="i-123"`).
       - **Conditional**: Logic like `if [ "$status" == "running" ]; then ...`.
       - **Loop**: Repeats tasks (e.g., `for i in 1 2 3; do echo $i; done`).
       - **Exit Code**: 0 for success, non-zero for failure (e.g., `exit 1`).
     - **Use Case**: Automate EC2 launches across regions with a single script.
     - **Action**: Write a tiny script locally: `echo '#!/bin/bash' > test.sh; echo 'echo Hello' >> test.sh; chmod +x test.sh; ./test.sh`.
     - **Why It Matters**: Bash drives **Scripting** for repeatable, complex workflows.

  3. **Scripting AWS Resources (15 min)**:
     - **Concept**: Combine AWS CLI with Bash for dynamic automation.
     - **Keywords**: JSON Parsing, Error Handling, Dry Run.
     - **Details**:
       - **JSON Parsing**: Extract data with `jq` (e.g., `aws ec2 describe-instances | jq '.Reservations[0].Instances[0].InstanceId'`).
       - **Error Handling**: Check exit codes (e.g., `if [ $? -ne 0 ]; then echo "Failed"; fi`).
       - **Dry Run**: Test without changes (e.g., `--dry-run` in `aws ec2 run-instances`).
     - **Use Case**: Script a VPC setup, then deploy EC2s only if the VPC succeeds.
     - **Action**: Run `aws ec2 describe-regions --output table` to see CLI output.
     - **Why It Matters**: Combines CLI power with Bash logic for **Idempotency**.

  4. **Self-Check (5 min)**:
     - Question: “How does AWS CLI differ from a Bash script?”
     - Answer (write or chat): “CLI runs single commands interactively; a Bash script sequences them for **Automation**.”

---

#### 2. Lab: Automate EC2 Provisioning (2.5-3 hours)
**Goal**: Write and execute a Bash script to launch an EC2 instance with AWS CLI.
- **Pre-Requisites**: AWS CLI installed/configured, “bootcamp-key” from Day 1, VPC “MultiTierVPC” from Day 3.
- **Key Concepts Reinforced**: Command, Variable, Shebang, JSON Parsing, Automation.

- **Sub-Activities**:
1. **Set Up Your Environment (15 min)**:
   - **Step 1**: Verify AWS CLI: `aws sts get-caller-identity` (confirms identity).
   - **Step 2**: Check Bash: `bash --version` (ensure availability).
   - **Step 3**: Locate Day 3 resources: `aws vpc describe-vpcs --filters Name=tag:Name,Values=MultiTierVPC` (get VPC-ID).
     - Note Subnet-ID: `aws ec2 describe-subnets --filters Name=vpc-id,Values=<vpc-id>` (pick “PublicSubnet”).
   - **Why**: Ensures CLI and Bash are ready for **Scripting**.

2. **Write a Bash Script (1 hour)**:
   - **Step 1**: Create `launch-ec2.sh`:
     ```bash
     #!/bin/bash
     # Variables
     AMI_ID="ami-0c55b159cbfafe1f0"  # Amazon Linux 2 in us-east-1
     INSTANCE_TYPE="t2.micro"
     SUBNET_ID="<your-public-subnet-id>"  # From Day 3
     SG_ID="<your-public-sg-id>"          # From Day 3 (PublicSG)
     KEY_NAME="bootcamp-key"

     # Launch EC2
     echo "Launching EC2 instance..."
     INSTANCE_ID=$(aws ec2 run-instances \
       --image-id $AMI_ID \
       --instance-type $INSTANCE_TYPE \
       --subnet-id $SUBNET_ID \
       --security-group-ids $SG_ID \
       --key-name $KEY_NAME \
       --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=ScriptedEC2}]' \
       --query 'Instances[0].InstanceId' \
       --output text)

     if [ $? -eq 0 ]; then
       echo "Instance launched: $INSTANCE_ID"
     else
       echo "Launch failed!"
       exit 1
     fi
     ```
   - **Step 2**: Make executable: `chmod +x launch-ec2.sh`.
   - **Step 3**: Replace `<your-public-subnet-id>` and `<your-public-sg-id>` with Day 3 values (e.g., `subnet-123`, `sg-456`).
   - **Why**: Uses **Variables** and **Command** execution for **Automation**.


Connecting to an AWS Linux instance (e.g., Amazon Linux 2) from a Windows PC is a common task for managing EC2 instances, and there are several standard methods to achieve this securely via SSH (Secure Shell). This is the most widely used approaches, focusing on tools and steps tailored for Windows users, with practical details based on the context (e.g., using the “bootcamp-key.pem” from prior days). 

Each method assumes you have an EC2 instance running in a public subnet with a public IP, a Security Group allowing SSH (port 22), and a key pair downloaded.

---

### Standard Ways to Connect to AWS Linux Instances from a Windows PC

#### 1. Using PuTTY (Most Common GUI Method)
- **Overview**: PuTTY is a free, lightweight SSH client popular among Windows users for its simplicity and graphical interface.
- **Tools Needed**: PuTTY, PuTTYgen (for converting `.pem` to `.ppk`).
- **Steps**:
  1. **Download and Install PuTTY**:
     - Get PuTTY from [putty.org](https://www.putty.org/). Install both PuTTY and PuTTYgen.
  2. **Convert .pem to .ppk**:
     - AWS provides a `.pem` file (e.g., “bootcamp-key.pem”), but PuTTY requires a `.ppk` file.
     - Open PuTTYgen > Actions > Load > Select “bootcamp-key.pem” (change file type to “All Files” to see it).
     - Click “Save private key” > Name it “bootcamp-key.ppk” (no passphrase unless desired).
  3. **Configure PuTTY**:
     - Open PuTTY > Session:
       - Hostname: `ec2-user@<public-ip>` (e.g., `ec2-user@54.123.45.67`).
       - Port: 22 (default SSH).
     - Connection > SSH > Auth > Credentials:
       - Browse and select “bootcamp-key.ppk”.
     - Session: Save as “BootcampEC2” for reuse.
  4. **Connect**:
     - Click “Open” > Accept the security prompt (first-time connection).
     - You’re logged in as `ec2-user` if the Security Group and key match.
  5. **Verification**: Run `hostname` or `cat /etc/os-release` to confirm it’s your Linux instance.
- **Use Case**: Ideal for beginners or those preferring a GUI over command-line tools.
- **Troubleshooting**: If it fails, check the public IP, Security Group (port 22 open to your IP), and key file compatibility.

---

#### 2. Using Windows Command Prompt or PowerShell with OpenSSH
- **Overview**: Windows 10/11 includes a built-in OpenSSH client, allowing SSH connections without third-party tools.
- **Tools Needed**: OpenSSH (pre-installed in Windows 10/11), your `.pem` file.
- **Steps**:
  1. **Verify OpenSSH**:
     - Open Command Prompt (cmd) or PowerShell > Run `ssh -V`.
     - If not found, enable it: Settings > Apps > Optional Features > Add “OpenSSH Client”.
  2. **Prepare the .pem File**:
     - Place “bootcamp-key.pem” in a secure folder (e.g., `C:\Users\YourName\.ssh`).
     - Set permissions (optional but recommended):
       - Right-click file > Properties > Security > Edit > Disable inheritance, remove all but your user.
  3. **Connect via Command Prompt**:
     - Run: `ssh -i C:\Users\YourName\.ssh\bootcamp-key.pem ec2-user@<public-ip>`.
     - Example: `ssh -i C:\Users\YourName\.ssh\bootcamp-key.pem ec2-user@54.123.45.67`.
  4. **Connect via PowerShell**:
     - Same command: `ssh -i C:\Users\YourName\.ssh\bootcamp-key.pem ec2-user@<public-ip>`.
     - Accept host key prompt (first time).
  5. **Verification**: Run `whoami` (outputs `ec2-user`) or `uptime` to confirm connection.
- **Use Case**: Great for scripting or CLI enthusiasts integrating with automation (e.g., Day 4’s Bash script).
- **Troubleshooting**: Ensure the `.pem` path has no spaces (use quotes if it does), and check Security Group rules.

---

#### 3. Using Windows Subsystem for Linux (WSL)
- **Overview**: WSL provides a Linux environment (e.g., Ubuntu) on Windows, allowing native Linux SSH commands.
- **Tools Needed**: WSL (installed via Microsoft Store), `.pem` file.
- **Steps**:
  1. **Install WSL**:
     - Open PowerShell (Admin) > Run `wsl --install`.
     - Install a distro (e.g., Ubuntu) from Microsoft Store > Launch it.
  2. **Set Up WSL**:
     - Update: `sudo apt update && sudo apt upgrade -y`.
     - Copy “bootcamp-key.pem” to WSL (e.g., `/home/youruser/.ssh`):
       - From Windows: `cp /mnt/c/Users/YourName/bootcamp-key.pem ~/.ssh/`.
     - Set permissions: `chmod 400 ~/.ssh/bootcamp-key.pem`.
  3. **Connect**:
     - Run: `ssh -i ~/.ssh/bootcamp-key.pem ec2-user@<public-ip>`.
     - Example: `ssh -i ~/.ssh/bootcamp-key.pem ec2-user@54.123.45.67`.
  4. **Verification**: Run `uname -a` to see Linux details.
- **Use Case**: Perfect for devs familiar with Linux workflows or testing Bash scripts locally (e.g., Day 4’s `launch-ec2.sh`).
- **Troubleshooting**: Ensure WSL network aligns with Windows (e.g., same VPN), and verify file permissions.

---

#### 4. Using Git Bash
- **Overview**: Git Bash, bundled with Git for Windows, includes an SSH client for lightweight connections.
- **Tools Needed**: Git (download from [git-scm.com](https://git-scm.com/)), `.pem` file.
- **Steps**:
  1. **Install Git**:
     - Download and install Git, selecting “Use Git Bash” during setup.
  2. **Prepare the .pem File**:
     - Place “bootcamp-key.pem” in a folder (e.g., `C:\Users\YourName\.ssh`).
     - Open Git Bash > Set permissions: `chmod 400 /c/Users/YourName/.ssh/bootcamp-key.pem`.
  3. **Connect**:
     - Run: `ssh -i /c/Users/YourName/.ssh/bootcamp-key.pem ec2-user@<public-ip>`.
     - Example: `ssh -i /c/Users/YourName/.ssh/bootcamp-key.pem ec2-user@54.123.45.67`.
  4. **Verification**: Run `ls -l` (will fail, proving it’s Linux) or `cat /etc/os-release`.
- **Use Case**: Handy for Git users or lightweight scripting without WSL overhead.
- **Troubleshooting**: Check path syntax (`/c/` for Windows drives) and Security Group (port 22).

---

#### 5. Using AWS Systems Manager Session Manager (No SSH Key Needed)
- **Overview**: Session Manager provides browser- or CLI-based access to EC2 without SSH, using IAM roles.
- **Tools Needed**: AWS CLI, IAM permissions, SSM Agent on EC2 (pre-installed on Amazon Linux 2).
- **Steps**:
  1. **Configure IAM Role**:
     - Attach `AmazonSSMManagedInstanceCore` policy to your EC2 instance’s IAM role (via Console: EC2 > Modify IAM Role).
  2. **Verify SSM Agent**:
     - Ensure the instance is running Amazon Linux 2 (SSM Agent is default).
  3. **Connect via AWS Console**:
     - EC2 > Instances > Select instance > Actions > Connect > Session Manager > Connect.
     - Opens a browser terminal as `ssm-user`.
  4. **Connect via AWS CLI**:
     - Run: `aws ssm start-session --target <instance-id>` (e.g., `i-1234567890abcdef0`).
  5. **Verification**: Run `whoami` (outputs `ssm-user`) or `sudo su - ec2-user` to switch.
- **Use Case**: Ideal for secure access without key management or when SSH is blocked (e.g., private subnet with VPC endpoints).
- **Troubleshooting**: Check IAM role, instance reachability (must be “running”), and SSM Agent status.

---

### Key Considerations
- **Security**: Always restrict Security Group SSH (port 22) to your IP (e.g., 192.168.1.100/32) to prevent unauthorized access.
- **Public IP**: Ensure the EC2 instance has a public IP or Elastic IP (from a public subnet with IGW route, as in Day 3).
- **Key File**: Protect “bootcamp-key.pem” (e.g., chmod 400 or Windows permissions) and never share it.
- **Firewall**: Windows Defender or your network firewall must allow outbound port 22 traffic.

---

### Practical Context from Day 4
- In Day 4’s lab, you scripted an EC2 launch (`launch-ec2.sh`) and need to SSH to test the web server. Any of these methods work:
  - PuTTY for a quick GUI check.
  - OpenSSH/PowerShell to script further commands (e.g., `ssh -i ... "sudo systemctl start httpd"`).
  - WSL/Git Bash to align with Bash scripting workflows.
  - Session Manager if you skip SSH for security.

---

These methods cover the standard ways to connect from Windows, each with unique strengths. 

3. **Run and Verify (1 hour)**:
   - **Step 1**: Execute: `./launch-ec2.sh` (outputs “Instance launched: i-123…”).
   - **Step 2**: Check status: `aws ec2 describe-instances --instance-ids $INSTANCE_ID --query 'Reservations[0].Instances[0].State.Name'`.
     - Wait until “running” (takes ~1-2 min).
   - **Step 3**: SSH and setup web server:
     - `ssh -i bootcamp-key.pem ec2-user@<public-ip>` (get IP from Console or CLI).
     - `sudo yum install httpd -y; sudo systemctl start httpd; echo "<h1>Scripted Server</h1>" | sudo tee /var/www/html/index.html`.
   - **Step 4**: Test: `http://<public-ip>` in browser.
   - **Why**: Validates **Scripting** success and EC2 functionality.

4. **Stretch Goal (Optional, 30 min)**:
   - Add **JSON Parsing**: Modify script to wait for “running”:
     ```bash
     STATUS="pending"
     while [ "$STATUS" != "running" ]; do
       STATUS=$(aws ec2 describe-instances --instance-ids $INSTANCE_ID --query 'Reservations[0].Instances[0].State.Name' --output text)
       echo "Status: $STATUS"
       sleep 5
     done
     ```
   - Test **Dry Run**: `aws ec2 run-instances ... --dry-run` (no launch, just validation).
   - **Why**: Enhances **Error Handling** and **Idempotency**.

---

#### 3. Chaos Twist: "Script Fails" (1-1.5 hours)
**Goal**: Debug a script failure caused by an invalid AMI, simulating real-world errors.
- **Trigger**: Instructor swaps AMI_ID to an invalid value (e.g., “ami-999”) mid-lab: “Your script’s AMI is deprecated!”
- **Key Concepts Reinforced**: Error Handling, Exit Code, Troubleshooting, Automation.

- **Sub-Activities**:
1. **Identify the Failure (20 min)**:
   - **Step 1**: Run `./launch-ec2.sh` → Error: “InvalidAMIID.NotFound” or similar.
   - **Step 2**: Check exit code: `echo $?` (non-zero, e.g., 255).
   - **Step 3**: Read output: Note “The AMI ID 'ami-999' does not exist.”
   - **Why**: Mimics **Automation** failures like outdated configs.

2. **Debug and Fix (45 min)**:
   - **Step 1**: Find a valid AMI:
     - `aws ec2 describe-images --owners amazon --filters "Name=name,Values=amzn2-ami-hvm-*-x86_64-gp2" --query 'Images[-1].ImageId' --output text`.
     - Example output: `ami-0c55b159cbfafe1f0`.
   - **Step 2**: Update script:
     - Replace `AMI_ID="ami-999"` with `AMI_ID="ami-0c55b159cbfafe1f0"`.
   - **Step 3**: Rerun: `./launch-ec2.sh` → “Instance launched: i-456…”.
   - **Step 4**: Verify: SSH and test `http://<public-ip>` again.
   - **Why**: Teaches **Troubleshooting** and dynamic resource handling.

3. **Stretch Goal (Optional, 15 min)**:
   - Add **Error Handling**:
     ```bash
     if ! aws ec2 describe-images --image-ids $AMI_ID >/dev/null 2>&1; then
       echo "Invalid AMI! Fetching latest..."
       AMI_ID=$(aws ec2 describe-images --owners amazon --filters "Name=name,Values=amzn2-ami-hvm-*-x86_64-gp2" --query 'Images[-1].ImageId' --output text)
     fi
     ```
   - Test failure again with “ami-999”; script auto-corrects.
   - **Why**: Builds **Idempotency** into scripts.

---

#### 4. Wrap-Up: War Room Discussion (30-45 min)
**Goal**: Reflect, share, and reinforce scripting knowledge.
- **Key Concepts Reinforced**: Scripting, Automation, Error Handling.

- **Sub-Activities**:
  1. **Present Your Setup (15 min)**:
     - Show `http://<public-ip>` and share `launch-ec2.sh`.
     - Share a lesson: e.g., “**JSON Parsing** extracts INSTANCE_ID cleanly.”
  2. **Chaos Debrief (15 min)**:
     - Discuss: “What broke? How did you fix the AMI?”
     - Instructor explains: “Invalid AMIs mimic real-world drift; **Error Handling** is key.”
  3. **Q&A (10 min)**:
     - Ask: “Why did my script hang after launch?”
     - Answer: “Add a status check or timeout; EC2 takes time to start.”
     - Note a Day 5 tip: “Use scripts in mini-projects for consistency.”

---

### Theoretical Takeaways Packed In
- **AWS CLI**: **Profile** setup, **Command** syntax, **Output Format** options, **Region** scoping.
- **Bash**: **Shebang** declaration, **Variable** usage, **Conditional** logic, **Loop** iteration, **Exit Code** checks.
- **Scripting**: **JSON Parsing** with jq, **Error Handling** with conditionals, **Dry Run** for safety, **Idempotency** design.

---

### Practical Use Cases
1. **Infrastructure Provisioning**: Script EC2 and S3 setup for a dev environment, ensuring repeatability.
2. **Monitoring Automation**: Poll instance status every minute, alert if “stopped,” reducing manual checks.
3. **Disaster Recovery**: Automate snapshot creation and instance relaunch after failures, speeding recovery.

---

### Tips for Participants
- **Prepare**: Bookmark [AWS CLI EC2 Commands](https://docs.aws.amazon.com/cli/latest/reference/ec2/) and [Bash Scripting Guide](https://tldp.org/LDP/Bash-Beginners-Guide/html/).
- **Track**: Save scripts and CLI outputs in `notes.txt` (e.g., `aws ec2 run-instances` response).
- **Ask**: Use the “mentor hotline” (e.g., “Why’s my AMI invalid?”).

---

### Adjusted Timeline
- **Theory**: 1 hour
- **Lab**: 2.5-3 hours (with breaks)
- **Chaos Twist**: 1-1.5 hours
- **Wrap-Up**: 30-45 min
- **Total**: 5-6 hours (stretch goals optional)

---

This Day 4 delivers an extensive scripting foundation, blending theory (e.g., **Automation**, **Idempotency**) with practical automation and chaos-driven debugging.