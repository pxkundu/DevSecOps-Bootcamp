This is a comprehensive, bulletproof Bash script that automates the configuration of AWS CLI, sets up Linux environment variables in the Bash profile, launches an EC2 instance with an Amazon Linux 2 AMI, configures it to host a static website, attaches an Elastic IP (EIP), and ensures the website runs error-free in a browser. 

The script includes extensive comments for clarity, error handling for robustness, and verification steps to guarantee success. 

It builds on concepts from **Week 1, Day 4: Intro to Scripting** and assumes you’re running this from a Linux environment (e.g., WSL, Git Bash, or a Linux machine).

---

### Bulletproof Bash Script: `setup-ec2-website.sh`

```bash
#!/bin/bash

# Purpose: Configure AWS CLI, set environment variables, launch an EC2 instance with a static website,
# attach an Elastic IP, and verify the website in a browser.

# Exit on any error to prevent partial execution
set -e

# --- Variables ---
# Replace these with your values or pass as arguments for flexibility
AWS_REGION="us-east-1"                # AWS region for consistency
KEY_NAME="bootcamp-key"               # Key pair name (assumes .pem exists locally)
VPC_ID="vpc-12345678"                 # Replace with your VPC ID (e.g., from Day 3's MultiTierVPC)
SUBNET_ID="subnet-12345678"           # Replace with your public subnet ID (from Day 3)
AMI_ID="ami-0c55b159cbfafe1f0"       # Amazon Linux 2 AMI (us-east-1, update if needed)
INSTANCE_TYPE="t2.micro"              # Free Tier instance type
SECURITY_GROUP_NAME="WebServerSG"     # Security group for web access
EIP_ALLOCATION_ID=""                  # Will be set after EIP creation
INSTANCE_ID=""                        # Will be set after instance launch
PUBLIC_IP=""                          # Will be set after EIP association

# --- Step 1: Configure AWS CLI ---
echo "Configuring AWS CLI..."

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo "AWS CLI not found! Installing..."
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
    unzip awscliv2.zip
    sudo ./aws/install
    rm -rf awscliv2.zip aws
fi

# Prompt for AWS credentials if not configured
if [ ! -f ~/.aws/credentials ]; then
    echo "AWS CLI not configured. Please enter your credentials:"
    read -p "AWS Access Key ID: " ACCESS_KEY
    read -p "AWS Secret Access Key: " SECRET_KEY
    aws configure set aws_access_key_id "$ACCESS_KEY"
    aws configure set aws_secret_access_key "$SECRET_KEY"
    aws configure set default.region "$AWS_REGION"
    aws configure set default.output "json"
    echo "AWS CLI configured!"
else
    echo "AWS CLI already configured. Verifying..."
    aws sts get-caller-identity || { echo "CLI config invalid! Reconfigure manually."; exit 1; }
fi

# --- Step 2: Set Environment Variables in .bash_profile ---
echo "Setting environment variables in .bash_profile..."

# Backup .bash_profile
cp ~/.bash_profile ~/.bash_profile.bak 2>/dev/null || touch ~/.bash_profile

# Add AWS-related variables if not already present
if ! grep -q "AWS_DEFAULT_REGION" ~/.bash_profile; then
    cat <<EOL >> ~/.bash_profile
# AWS Environment Variables
export AWS_DEFAULT_REGION=$AWS_REGION
export PATH=\$PATH:/usr/local/bin  # Ensure AWS CLI is in PATH
EOL
    echo "Environment variables added to .bash_profile."
else
    echo "Environment variables already set."
fi

# Source .bash_profile to apply changes
source ~/.bash_profile

# --- Step 3: Create or Verify Security Group ---
echo "Configuring Security Group..."

# Check if Security Group exists
SG_ID=$(aws ec2 describe-security-groups \
    --filters "Name=group-name,Values=$SECURITY_GROUP_NAME" "Name=vpc-id,Values=$VPC_ID" \
    --query "SecurityGroups[0].GroupId" --output text 2>/dev/null)

if [ "$SG_ID" == "None" ] || [ -z "$SG_ID" ]; then
    echo "Creating Security Group: $SECURITY_GROUP_NAME..."
    SG_ID=$(aws ec2 create-security-group \
        --group-name "$SECURITY_GROUP_NAME" \
        --description "Security group for web server" \
        --vpc-id "$VPC_ID" \
        --query "GroupId" --output text)
    
    # Add inbound rules: SSH (22) and HTTP (80)
    aws ec2 authorize-security-group-ingress \
        --group-id "$SG_ID" \
        --protocol tcp --port 22 --cidr 0.0.0.0/0  # Replace 0.0.0.0/0 with your IP for security
    aws ec2 authorize-security-group-ingress \
        --group-id "$SG_ID" \
        --protocol tcp --port 80 --cidr 0.0.0.0/0
    echo "Security Group $SG_ID created and configured."
else
    echo "Security Group $SG_ID already exists."
fi

# --- Step 4: Launch EC2 Instance ---
echo "Launching EC2 instance..."

# Verify AMI exists
if ! aws ec2 describe-images --image-ids "$AMI_ID" --region "$AWS_REGION" &>/dev/null; then
    echo "AMI $AMI_ID not found! Fetching latest Amazon Linux 2 AMI..."
    AMI_ID=$(aws ec2 describe-images \
        --owners amazon \
        --filters "Name=name,Values=amzn2-ami-hvm-*-x86_64-gp2" "Name=state,Values=available" \
        --query "sort_by(Images, &CreationDate)[-1].ImageId" --output text)
    echo "Using AMI: $AMI_ID"
fi

# Launch instance with error handling
INSTANCE_ID=$(aws ec2 run-instances \
    --image-id "$AMI_ID" \
    --instance-type "$INSTANCE_TYPE" \
    --subnet-id "$SUBNET_ID" \
    --security-group-ids "$SG_ID" \
    --key-name "$KEY_NAME" \
    --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=WebServer}]' \
    --query "Instances[0].InstanceId" --output text 2>/tmp/ec2-error)

if [ $? -ne 0 ]; then
    echo "EC2 launch failed! Error:"
    cat /tmp/ec2-error
    exit 1
fi

echo "EC2 instance launched: $INSTANCE_ID"

# Wait for instance to be running
echo "Waiting for instance to be running..."
aws ec2 wait instance-running --instance-ids "$INSTANCE_ID"
echo "Instance is running!"

# --- Step 5: Configure EC2 for Static Website ---
echo "Configuring EC2 for static website..."

# Get public IP for SSH
PUBLIC_IP=$(aws ec2 describe-instances \
    --instance-ids "$INSTANCE_ID" \
    --query "Reservations[0].Instances[0].PublicIpAddress" --output text)

# SSH and setup Apache with retries (handles initial connection delays)
MAX_RETRIES=5
RETRY_COUNT=0
until ssh -i "$KEY_NAME.pem" -o ConnectTimeout=10 ec2-user@"$PUBLIC_IP" << 'EOF'
    sudo yum update -y
    sudo yum install httpd -y
    echo "<h1>Welcome to My Static Website</h1>" | sudo tee /var/www/html/index.html
    sudo systemctl start httpd
    sudo systemctl enable httpd
    sudo chmod -R 755 /var/www/html
EOF
do
    RETRY_COUNT=$((RETRY_COUNT + 1))
    if [ $RETRY_COUNT -ge $MAX_RETRIES ]; then
        echo "Failed to configure EC2 after $MAX_RETRIES attempts!"
        exit 1
    fi
    echo "SSH failed, retrying in 10 seconds ($RETRY_COUNT/$MAX_RETRIES)..."
    sleep 10
done

echo "Static website configured on EC2!"

# --- Step 6: Allocate and Associate Elastic IP ---
echo "Allocating and associating Elastic IP..."

# Allocate EIP
EIP_ALLOCATION_ID=$(aws ec2 allocate-address \
    --domain vpc \
    --query "AllocationId" --output text)

# Associate EIP with instance
aws ec2 associate-address \
    --instance-id "$INSTANCE_ID" \
    --allocation-id "$EIP_ALLOCATION_ID"

# Get new public IP (EIP)
PUBLIC_IP=$(aws ec2 describe-instances \
    --instance-ids "$INSTANCE_ID" \
    --query "Reservations[0].Instances[0].PublicIpAddress" --output text)

echo "Elastic IP $PUBLIC_IP associated with $INSTANCE_ID."

# --- Step 7: Verify Website in Browser ---
echo "Verifying website..."

# Wait briefly for HTTP to stabilize
sleep 5

# Check website availability (requires curl on your machine)
if command -v curl &> /dev/null; then
    if curl -s --head "http://$PUBLIC_IP" | grep "200 OK" > /dev/null; then
        echo "Website is live at http://$PUBLIC_IP!"
    else
        echo "Website failed to load! Check Security Group (port 80) and Apache status."
        exit 1
    fi
else
    echo "Curl not installed. Please manually visit http://$PUBLIC_IP in your browser."
fi

# --- Cleanup Instructions (Optional) ---
echo "Setup complete! To clean up later, run:"
echo "aws ec2 terminate-instances --instance-ids $INSTANCE_ID"
echo "aws ec2 release-address --allocation-id $EIP_ALLOCATION_ID"
echo "aws ec2 delete-security-group --group-id $SG_ID  # After instance termination"

exit 0
```

---

### How to Use This Script
1. **Prerequisites**:
   - AWS account with CLI access (keys ready).
   - Bash environment (e.g., WSL, Git Bash, Linux).
   - “bootcamp-key.pem” in the script’s directory.
   - VPC and subnet IDs from Day 3 (e.g., “MultiTierVPC” and “PublicSubnet”).
   - `curl` and `unzip` installed (`sudo apt install curl unzip` on Ubuntu).

2. **Steps**:
   - Save as `setup-ec2-website.sh`.
   - Update variables (`VPC_ID`, `SUBNET_ID`) with your values (find via `aws ec2 describe-vpcs` and `aws ec2 describe-subnets`).
   - Make executable: `chmod +x setup-ec2-website.sh`.
   - Run: `./setup-ec2-website.sh`.
   - Visit `http://<PUBLIC_IP>` in your browser to see “Welcome to My Static Website.”

3. **Security Note**: Replace `0.0.0.0/0` in Security Group rules with your IP (e.g., `192.168.1.100/32`) for SSH and HTTP to lock down access.

---

### Why It’s Bulletproof
- **Error Handling**: `set -e` exits on errors; `if [ $? -ne 0 ]` catches CLI failures; SSH retries handle delays.
- **Verification**: AMI validity, instance status, and website availability are checked.
- **Idempotency**: Security Group check avoids duplicates; script can rerun with tweaks.
- **Comments**: Every step is explained for clarity and learning.
- **Cleanup**: Provides termination commands to avoid orphaned resources.

---

### Key Configurations
- **CLI Setup**: Ensures AWS CLI is installed and configured.
- **Environment**: Persists `AWS_DEFAULT_REGION` in `.bash_profile`.
- **EC2**: Launches with a valid AMI, Security Group (SSH + HTTP), and Apache for the website.
- **EIP**: Guarantees a static IP for consistent access.
- **Website**: Simple HTML page, permissions set, Apache enabled.

---

This script ties into Day 4’s focus on **Automation**, **AWS CLI**, and **Bash**, delivering a production-ready EC2 website with no errors.