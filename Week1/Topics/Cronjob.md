# Cronjob Automation in WSL: Comprehensive Documentation

## Table of Contents
1. [Introduction](#1-introduction)
2. [Setting Up Cron in WSL](#2-setting-up-cron-in-wsl)
3. [Basic Cronjob Operations](#3-basic-cronjob-operations)
   - [Running a Text File Every 5 Minutes](#31-running-a-text-file-every-5-minutes)
   - [Logging Date/Time Every Friday at 10:00 AM](#32-logging-datetime-every-friday-at-1000-am)
   - [Updating a Text File Every 5 Minutes for Today Only](#33-updating-a-text-file-every-5-minutes-for-today-only)
   - [Deleting All Cronjobs](#34-deleting-all-cronjobs)
4. [AWS Integration with Cronjobs](#4-aws-integration-with-cronjobs)
   - [Creating an EC2 Instance with MySQL and HTML Page](#41-creating-an-ec2-instance-with-mysql-and-html-page)
   - [Starting/Stopping EC2 on Workdays](#42-startingstopping-ec2-on-workdays)
5. [Real-World Use Cases for Fortune 100 Companies](#5-real-world-use-cases-for-fortune-100-companies)
6. [Best Practices and Troubleshooting](#6-best-practices-and-troubleshooting)
7. [Conclusion](#7-conclusion)

---

## 1. Introduction
Cronjobs are a powerful way to schedule repetitive tasks in Linux environments like Windows Subsystem for Linux (WSL). This documentation covers cronjob setup, AWS integration, and practical examples based on your queries. All paths are relative to your WSL home directory: `/home/artha_undu`.

---

## 2. Setting Up Cron in WSL
WSL doesn’t run cron by default, so you must install and start it manually. To automate this on WSL startup:

### Commands
```bash
# Install cron
sudo apt update
sudo apt install cron

# Start cron manually
sudo service cron start

# Create a startup script for persistence
echo '#!/bin/bash
sudo service cron start
' > /home/artha_undu/.wsl_startup.sh

# Make it executable
chmod +x /home/artha_undu/.wsl_startup.sh

# Add to ~/.bashrc for automatic execution on WSL start
echo "~/home/artha_undu/.wsl_startup.sh" >> /home/artha_undu/.bashrc
```

### Notes
- Restart WSL (`wsl --shutdown` from Windows CMD) to test persistence.
- Check cron status: `sudo service cron status`.

---

## 3. Basic Cronjob Operations

### 3.1 Running a Text File Every 5 Minutes
**Objective**: Execute a script every 5 minutes.

**Script**: `/home/artha_undu/script.txt`
```bash
#!/bin/bash
echo "Task executed at $(date)" >> /home/artha_undu/log.txt
```

**Commands**
```bash
chmod +x /home/artha_undu/script.txt
(crontab -l 2>/dev/null; echo "*/5 * * * * /bin/bash /home/artha_undu/script.txt") | crontab -
crontab -l
```

**Cron Expression**: `*/5 * * * *` (every 5 minutes).

---

### 3.2 Logging Date/Time Every Friday at 10:00 AM
**Objective**: Log the current date and time to a file every Friday at 10:00 AM.

**Script**: `/home/artha_undu/log_datetime.sh`
```bash
#!/bin/bash
date >> /home/artha_undu/datetime.log
```

**Commands**
```bash
chmod +x /home/artha_undu/log_datetime.sh
(crontab -l 2>/dev/null; echo "0 10 * * 5 /bin/bash /home/artha_undu/log_datetime.sh") | crontab -
crontab -l
```

**Cron Expression**: `0 10 * * 5` (10:00 AM every Friday; 5 = Friday).

---

### 3.3 Updating a Text File Every 5 Minutes for Today Only
**Objective**: Append date/time to a file every 5 minutes, but only on February 27, 2025.

**Script**: `/home/artha_undu/update_text.sh`
```bash
#!/bin/bash
if [ "$(date +%Y-%m-%d)" = "2025-02-27" ]; then
    echo "$(date)" >> /home/artha_undu/myfile.txt
fi
```

**Commands**
```bash
chmod +x /home/artha_undu/update_text.sh
(crontab -l 2>/dev/null; echo "*/5 * * * * /bin/bash /home/artha_undu/update_text.sh") | crontab -
crontab -l
```

**Cron Expression**: `*/5 * * * *` (every 5 minutes, with script logic limiting to today).

---

### 3.4 Deleting All Cronjobs
**Objective**: Remove all cronjobs for the current user.

**Commands**
```bash
crontab -r
crontab -l  # Should return "no crontab for artha_undu"
```

**Note**: This only affects your user’s cronjobs, not system-wide ones.

---

## 4. AWS Integration with Cronjobs

### 4.1 Creating an EC2 Instance with MySQL and HTML Page
**Objective**: Launch a free-tier EC2 instance, install MySQL and Apache, and display date/time on an HTML page.
shell script that creates an AWS EC2 instance (free tier), installs MySQL server, sets up an HTML page to display the current time and date, and configures cronjobs to start the instance every workday at 9 AM and shut it down at 5 PM. This assumes you have AWS CLI configured in your WSL environment (e.g., at `/home/artha_undu`) with appropriate permissions.

### Shell Script: `setup_ec2.sh`

```bash
#!/bin/bash

# Variables
KEY_NAME="artha-key"
SECURITY_GROUP="artha-sg"
AMI_ID="ami-0c55b159cbfafe1f0"  # Amazon Linux 2 AMI (update for your region)
INSTANCE_TYPE="t2.micro"       # Free tier eligible
HTML_FILE="/var/www/html/index.html"
SUBNET_ID="subnet-xxxxxxxx"    # Replace with your subnet ID
IAM_ROLE="ec2-role"            # Optional: Replace with your IAM role if needed

# Step 1: Create a key pair (if not already created)
aws ec2 create-key-pair --key-name $KEY_NAME --query 'KeyMaterial' --output text > $KEY_NAME.pem
chmod 400 $KEY_NAME.pem

# Step 2: Create a security group and allow SSH (22) and HTTP (80)
aws ec2 create-security-group --group-name $SECURITY_GROUP --description "SG for EC2 with SSH and HTTP"
aws ec2 authorize-security-group-ingress --group-name $SECURITY_GROUP --protocol tcp --port 22 --cidr 0.0.0.0/0
aws ec2 authorize-security-group-ingress --group-name $SECURITY_GROUP --protocol tcp --port 80 --cidr 0.0.0.0/0

# Step 3: Launch EC2 instance with user data to install MySQL, Apache, and set up HTML page
USER_DATA=$(cat << 'EOF' | base64
#!/bin/bash
yum update -y
yum install -y httpd mysql-server
systemctl start httpd
systemctl enable httpd
systemctl start mysqld
systemctl enable mysqld
echo "<html><body><h1>Current Date and Time: $(date)</h1></body></html>" > /var/www/html/index.html
EOF
)

INSTANCE_ID=$(aws ec2 run-instances \
  --image-id $AMI_ID \
  --instance-type $INSTANCE_TYPE \
  --key-name $KEY_NAME \
  --security-groups $SECURITY_GROUP \
  --subnet-id $SUBNET_ID \
  --user-data "$USER_DATA" \
  --query 'Instances[0].InstanceId' \
  --output text)

echo "EC2 Instance ID: $INSTANCE_ID"

# Step 4: Save instance ID to a file for cronjob use
echo $INSTANCE_ID > /home/artha_undu/instance_id.txt

# Step 5: Create start/stop scripts for cronjobs
cat << 'EOF' > /home/artha_undu/start_ec2.sh
#!/bin/bash
INSTANCE_ID=$(cat /home/artha_undu/instance_id.txt)
aws ec2 start-instances --instance-ids $INSTANCE_ID
EOF

cat << 'EOF' > /home/artha_undu/stop_ec2.sh
#!/bin/bash
INSTANCE_ID=$(cat /home/artha_undu/instance_id.txt)
aws ec2 stop-instances --instance-ids $INSTANCE_ID
EOF

# Make scripts executable
chmod +x /home/artha_undu/start_ec2.sh
chmod +x /home/artha_undu/stop_ec2.sh

# Step 6: Set up cronjobs for workdays (Monday-Friday) at 9 AM and 5 PM
(crontab -l 2>/dev/null; echo "0 9 * * 1-5 /bin/bash /home/artha_undu/start_ec2.sh") | crontab -
(crontab -l 2>/dev/null; echo "0 17 * * 1-5 /bin/bash /home/artha_undu/stop_ec2.sh") | crontab -

# Verify cronjobs
crontab -l

echo "EC2 setup complete. Cronjobs scheduled for 9 AM start and 5 PM stop on workdays."
```

### How to Use:
1. ** Prerequisites**:
   - AWS CLI installed and configured in WSL (`aws configure` with your credentials).
   - Replace `SUBNET_ID` with your actual subnet ID (find it in AWS VPC console).
   - Update `AMI_ID` if needed (check AWS EC2 console for a free-tier-eligible Amazon Linux 2 AMI in your region).

2. **Save and Run**:
   - Save the script as `setup_ec2.sh` in `/home/artha_undu/`.
   - Make it executable: `chmod +x /home/artha_undu/setup_ec2.sh`.
   - Run it: `./setup_ec2.sh`.

3. **What It Does**:
   - Creates a key pair (`artha-key.pem`) for SSH access.
   - Sets up a security group allowing SSH (port 22) and HTTP (port 80).
   - Launches a `t2.micro` EC2 instance with a user-data script that:
     - Installs Apache (`httpd`) and MySQL server.
     - Starts both services.
     - Creates an `index.html` file showing the date/time at instance launch.
   - Saves the instance ID for cronjob use.
   - Creates `start_ec2.sh` and `stop_ec2.sh` scripts to control the instance.
   - Schedules cronjobs to start at 9 AM and stop at 5 PM, Monday through Friday.

4. **Cronjob Details**:
   - `0 9 * * 1-5`: Runs at 9:00 AM, Monday-Friday.
   - `0 17 * * 1-5`: Runs at 5:00 PM (17:00), Monday-Friday.

5. **Verification**:
   - Check cronjobs: `crontab -l`.
   - Get the instance’s public IP after it starts: `aws ec2 describe-instances --instance-ids $(cat /home/artha_undu/instance_id.txt) --query 'Reservations[0].Instances[0].PublicIpAddress' --output text`.
   - Visit `http://<public-ip>` in a browser to see the date/time (note: it’s static from launch time unless refreshed by another script).

### Notes:
- **Cron Service**: Ensure cron is running (`sudo service cron start`). Use the earlier startup script method for persistence.
- **Dynamic Time**: The HTML page shows the time at instance launch. To update it dynamically, add a cronjob on the EC2 instance itself (via user-data or SSH).
- **Cleanup**: After testing, terminate the instance (`aws ec2 terminate-instances --instance-ids $(cat /home/artha_undu/instance_id.txt)`) and delete the security group/key pair to avoid charges.

Run this in your WSL terminal at `/home/artha_undu` to set everything up!

---

## 5. Real-World Use Cases for Fortune 100 Companies
These examples reflect automation needs in large enterprises.

 Top 5 real-world use cases for cronjobs and scripts tailored to Fortune 100 companies, along with example scripts. These use cases reflect common automation needs in large-scale enterprises like Walmart, Amazon, Apple, ExxonMobil, or UnitedHealth Group, leveraging my knowledge of their operational scale and tech reliance as of February 27, 2025.

---

### 1. Daily Database Backup
**Use Case**: Fortune 100 companies manage massive datasets (e.g., customer transactions at Amazon or Walmart). Cronjobs automate daily backups to ensure data integrity and disaster recovery.

**Script**: `backup_db.sh`
```bash
#!/bin/bash
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
DB_NAME="company_db"
BACKUP_DIR="/home/artha_undu/backups"
mysqldump -u root -p'password' $DB_NAME > $BACKUP_DIR/$DB_NAME_$TIMESTAMP.sql
aws s3 cp $BACKUP_DIR/$DB_NAME_$TIMESTAMP.sql s3://company-backups/
```

**Cronjob**: Run daily at 2 AM
```bash
0 2 * * * /bin/bash /home/artha_undu/backup_db.sh
```

---

### 2. System Health Monitoring and Alerts
**Use Case**: Companies like Apple or Alphabet monitor server health (e.g., disk space, CPU usage) to prevent downtime. Cronjobs check metrics and email alerts if thresholds are breached.

**Script**: `check_health.sh`
```bash
#!/bin/bash
DISK_USAGE=$(df -h / | awk 'NR==2 {print $5}' | cut -d'%' -f1)
if [ $DISK_USAGE -gt 80 ]; then
    echo "Disk usage at $DISK_USAGE% on $(date)" | mail -s "ALERT: High Disk Usage" admin@company.com
fi
```

**Cronjob**: Run hourly
```bash
0 * * * * /bin/bash /home/artha_undu/check_health.sh
```

---

### 3. Inventory Sync Across Warehouses
**Use Case**: Retail giants like Walmart sync inventory data across warehouses to optimize stock levels. Cronjobs run scripts to pull data from APIs and update databases.

**Script**: `sync_inventory.sh`
```bash
#!/bin/bash
curl -o /home/artha_undu/inventory.json "https://api.company.com/inventory"
mysql -u root -p'password' company_db < /home/artha_undu/update_inventory.sql
aws s3 sync /home/artha_undu/inventory.json s3://inventory-sync/
```

**Cronjob**: Run every 15 minutes
```bash
*/15 * * * * /bin/bash /home/artha_undu/sync_inventory.sh
```

---

### 4. Automated Financial Reporting
**Use Case**: Financial firms like Berkshire Hathaway or healthcare giants like UnitedHealth Group generate daily revenue reports for stakeholders. Cronjobs process data and upload reports to secure storage.

**Script**: `generate_report.sh`
```bash
#!/bin/bash
REPORT_FILE="/home/artha_undu/daily_report_$(date +%Y%m%d).csv"
echo "Date,Revenue" > $REPORT_FILE
mysql -u root -p'password' -e "SELECT DATE(NOW()), SUM(revenue) FROM sales" company_db >> $REPORT_FILE
aws s3 cp $REPORT_FILE s3://company-reports/
```

**Cronjob**: Run daily at 6 AM
```bash
0 6 * * * /bin/bash /home/artha_undu/generate_report.sh
```

---

### 5. Log Rotation and Cleanup
**Use Case**: Tech-heavy firms like Amazon or Alphabet manage server logs to maintain performance. Cronjobs rotate logs and delete old ones to free up space.

**Script**: `rotate_logs.sh`
```bash
#!/bin/bash
LOG_DIR="/var/log/company_app"
find $LOG_DIR -name "*.log" -mtime +7 -exec rm {} \;
tar -czf $LOG_DIR/archive_$(date +%Y%m%d).tar.gz $LOG_DIR/*.log
aws s3 mv $LOG_DIR/archive_$(date +%Y%m%d).tar.gz s3://log-archives/
```

**Cronjob**: Run weekly on Sunday at midnight
```bash
0 0 * * 0 /bin/bash /home/artha_undu/rotate_logs.sh
```

---

### Setup Instructions:
1. Save each script in `/home/artha_undu/` (your WSL path).
2. Make them executable: `chmod +x /home/artha_undu/<script_name>.sh`.
3. Add cronjobs via `crontab -e` in WSL.
4. Ensure dependencies (e.g., `mysql`, `aws cli`, `curl`) are installed and configured.
5. Start cron: `sudo service cron start` (add to `~/.wsl_startup.sh` for persistence).

These use cases align with Fortune 100 needs for scalability, reliability, and automation, leveraging cloud storage (AWS S3) and database operations common in their tech stacks. Adjust credentials, paths, or APIs as needed for your environment!

---

## 6. Best Practices and Troubleshooting

### Best Practices
- **Script Permissions**: Always `chmod +x` scripts.
- **Full Paths**: Use absolute paths (e.g., `/bin/bash`) in cronjobs.
- **Logging**: Redirect output (`>> /path/to/log 2>&1`) for debugging.
- **AWS Credentials**: Store securely as env variables (e.g., via `set-aws-keys.sh`).
- **Cleanup**: Remove unused cronjobs and AWS resources to avoid costs.

### Troubleshooting
- **Cron Not Running**: `sudo service cron status`.
- **Job Not Executing**: Check syntax with `crontab -l` and logs.
- **AWS Errors**: Verify credentials (`aws sts get-caller-identity`) and permissions.
- **WSL Restart**: Use `wsl --shutdown` to reset environment.

---

## 7. Conclusion
This documentation provides a robust foundation for cronjob automation in WSL, from basic scheduling to AWS-integrated tasks and enterprise use cases. Save scripts in `/home/artha_undu/`, adjust paths/credentials as needed, and leverage this guide for scalable automation projects.

--- 
