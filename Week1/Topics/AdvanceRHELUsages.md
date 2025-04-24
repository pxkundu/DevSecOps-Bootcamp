Let's get into the **Linux pro admin toolkit** with:

- 🛠️ **Performance Tuning**
- 📊 **Monitoring Tools**
- 🛡️ **Automated Security Audits / Scripts**

---

## 🛠️ 1. Performance Tuning in RHEL

### 🔹 System Resource Monitoring
```bash
top               # Real-time process monitoring
htop              # Advanced version (requires install)
iotop             # Disk I/O usage (install if needed)
vmstat 1          # Memory, CPU, I/O stats every 1 sec
```

### 🔹 CPU & Memory Tuning

#### Enable tuned and apply performance profile:
```bash
dnf install tuned
systemctl enable --now tuned
tuned-adm profile performance
```

#### Check current profile:
```bash
tuned-adm active
```

### 🔹 Kernel Parameters (via sysctl)
Adjust networking, memory limits, etc.

```bash
# View all current values
sysctl -a

# Temporarily set a value
sysctl -w net.ipv4.ip_forward=1

# Persistent config in:
vi /etc/sysctl.conf
```

Common tuning options:
```bash
vm.swappiness = 10
fs.file-max = 2097152
net.core.somaxconn = 1024
```

---

## 📊 2. Monitoring Tools

### 🔸 Native Tools
- `top`, `free`, `iostat`, `vmstat`, `netstat`, `ss`
- `dstat`: Combines vmstat, netstat, iostat (install with `dnf install dstat`)
- `sar` from `sysstat`: Historical system metrics
  ```bash
  dnf install sysstat
  sar -u 1 3           # CPU usage every 1s for 3 times
  ```

### 🔸 Web-based Monitoring
#### 🔹 Cockpit (Official RHEL Web Interface)
```bash
dnf install cockpit
systemctl enable --now cockpit.socket
```
Access via: `https://<server-ip>:9090`

#### 🔹 Netdata (Real-time, full-stack monitoring)
```bash
bash <(curl -Ss https://my-netdata.io/kickstart.sh)
```

---

## 🛡️ 3. Automated Security Audits & Hardening

### 🔸 Lynis (Linux Audit Tool)
```bash
dnf install epel-release
dnf install lynis
lynis audit system
```

### 🔸 OpenSCAP (Red Hat Certified Tool)
```bash
dnf install scap-security-guide openscap-scanner
oscap xccdf eval --profile xccdf_org.ssgproject.content_profile_standard \
--results scan.xml --report scan.html \
/usr/share/xml/scap/ssg/content/ssg-rhel9-ds.xml
```

Check report at `scan.html`

### 🔸 Basic Security Hardening Script
Here’s a simplified script example:

```bash
#!/bin/bash

# Disable root SSH login
sed -i 's/^PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config

# Disable password auth
sed -i 's/^PasswordAuthentication.*/PasswordAuthentication no/' /etc/ssh/sshd_config

# Enable UFW or firewalld
systemctl enable --now firewalld
firewall-cmd --set-default-zone=public
firewall-cmd --add-service=ssh --permanent
firewall-cmd --reload

# Set audit rules
echo "-w /etc/passwd -p wa" >> /etc/audit/rules.d/audit.rules
echo "-w /etc/shadow -p wa" >> /etc/audit/rules.d/audit.rules

# Enforce SELinux
sed -i 's/^SELINUX=.*/SELINUX=enforcing/' /etc/selinux/config

# Update system
dnf update -y
```

Make executable:
```bash
chmod +x secure-server.sh
./secure-server.sh
```
---

## 📦 4. Custom Scripts Collection

---

### 🗄️ A. **Backup Script** (Daily File Backup with `tar` and Timestamp)

**`daily_backup.sh`**
```bash
#!/bin/bash

BACKUP_SRC="/home"                  # What to back up
BACKUP_DEST="/backups"             # Where to save
DATE=$(date +%Y-%m-%d_%H-%M)
HOSTNAME=$(hostname -s)

mkdir -p $BACKUP_DEST

tar -czf $BACKUP_DEST/${HOSTNAME}_home_backup_$DATE.tar.gz $BACKUP_SRC

echo "Backup completed on $DATE" >> /var/log/backup.log
```

**🔁 Cron example (daily at 2AM):**
```bash
0 2 * * * /usr/local/bin/daily_backup.sh
```

---

### 🔔 B. **Alert Script** (Disk Usage Threshold Notification)

**`disk_alert.sh`**
```bash
#!/bin/bash

THRESHOLD=80
EMAIL="admin@example.com"

df -h | grep '^/dev/' | while read line; do
  USAGE=$(echo $line | awk '{print $5}' | tr -d '%')
  MOUNT=$(echo $line | awk '{print $6}')
  if [ $USAGE -ge $THRESHOLD ]; then
    echo "Disk usage warning on $MOUNT: $USAGE%" | mail -s "Disk Alert on $(hostname)" $EMAIL
  fi
done
```

**📧 Requirements:**
- `mailx` package for sending emails: `dnf install mailx`

---

### 🔄 C. **Patching Script** (Automated Package Update)

**`patch_system.sh`**
```bash
#!/bin/bash

echo "[$(date)] Starting system update..." >> /var/log/patch.log
dnf update -y >> /var/log/patch.log 2>&1
echo "[$(date)] Update complete." >> /var/log/patch.log
```

**📆 Cron suggestion (weekly patch every Sunday at 3 AM):**
```bash
0 3 * * 0 /usr/local/bin/patch_system.sh
```

---

### 🧪 D. **Basic Health Check Script**

**`health_check.sh`**
```bash
#!/bin/bash

HOST=$(hostname)
DATE=$(date)
REPORT="/tmp/health_report.txt"

echo "Health Check for $HOST - $DATE" > $REPORT
echo "Uptime:" >> $REPORT
uptime >> $REPORT
echo -e "\nDisk Usage:" >> $REPORT
df -h >> $REPORT
echo -e "\nMemory Usage:" >> $REPORT
free -m >> $REPORT
echo -e "\nTop 5 Memory Consumers:" >> $REPORT
ps -eo pid,ppid,cmd,%mem,%cpu --sort=-%mem | head -n 6 >> $REPORT

cat $REPORT | mail -s "Health Report - $HOST" admin@example.com
```

---

### 📦 E. **Simple File Integrity Checker (using md5sum)**

**`file_integrity.sh`**
```bash
#!/bin/bash

FILE="/etc/passwd"
HASH_FILE="/var/log/passwd.hash"

if [ ! -f $HASH_FILE ]; then
    md5sum $FILE > $HASH_FILE
    echo "Initial hash created."
else
    OLD_HASH=$(cat $HASH_FILE | awk '{print $1}')
    NEW_HASH=$(md5sum $FILE | awk '{print $1}')
    if [ "$OLD_HASH" != "$NEW_HASH" ]; then
        echo "WARNING: File integrity check failed for $FILE" | mail -s "File Change Alert" admin@example.com
    fi
fi
```

---

### 💡 Recommendations

- Place scripts in `/usr/local/bin/` or `/opt/scripts/`
- Set proper permissions: `chmod +x scriptname.sh`
- Create log files in `/var/log/` or a custom dir (`/var/log/custom/`)
- Use `systemd` timers for more control over cron if needed

---

You're thinking like a DevOps pro now — love it. Let's build out a **set of dynamic and interactive scripts** to help set up cloud integrations (AWS, GCP, and Azure) on Linux systems, following **best practices** and **industry standards**.

---

## ☁️ 5. Cloud Integration Scripts for Linux

We'll create **bash-based setup scripts** that:

- Prompt for required inputs (dynamic & interactive)
- Install required CLI tools (AWS CLI, GCloud SDK, Azure CLI)
- Set up secure credentials handling
- Validate configuration
- Can be reused and extended

---

### 🔹 A. **AWS Integration Script**

**`aws_setup.sh`**
```bash
#!/bin/bash

echo "==== AWS CLI Setup ===="
read -p "Enter AWS Access Key ID: " AWS_ACCESS_KEY_ID
read -sp "Enter AWS Secret Access Key: " AWS_SECRET_ACCESS_KEY
echo
read -p "Enter AWS Default Region (e.g. us-east-1): " AWS_REGION
read -p "Enter Output format (json, yaml, text): " AWS_OUTPUT

# Install AWS CLI if missing
if ! command -v aws &> /dev/null; then
    echo "Installing AWS CLI..."
    dnf install -y unzip curl
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
    unzip awscliv2.zip
    ./aws/install
fi

# Configure AWS CLI
mkdir -p ~/.aws
cat > ~/.aws/credentials <<EOF
[default]
aws_access_key_id = $AWS_ACCESS_KEY_ID
aws_secret_access_key = $AWS_SECRET_ACCESS_KEY
EOF

cat > ~/.aws/config <<EOF
[default]
region = $AWS_REGION
output = $AWS_OUTPUT
EOF

echo "✅ AWS CLI configured and ready."
aws sts get-caller-identity
```

---

### 🔹 B. **GCP Integration Script**

**`gcp_setup.sh`**
```bash
#!/bin/bash

echo "==== GCP SDK Setup ===="

read -p "Enter your GCP project ID: " PROJECT_ID

# Install gcloud SDK
if ! command -v gcloud &> /dev/null; then
    echo "Installing Google Cloud SDK..."
    dnf install -y dnf-plugins-core
    tee -a /etc/yum.repos.d/google-cloud-sdk.repo << EOM
[google-cloud-sdk]
name=Google Cloud SDK
baseurl=https://packages.cloud.google.com/yum/repos/cloud-sdk-el9-x86_64
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://packages.cloud.google.com/yum/doc/yum-key.gpg
       https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg
EOM

    dnf install -y google-cloud-sdk
fi

# Init and auth
echo "Launching browser-based auth..."
gcloud init
gcloud config set project $PROJECT_ID

echo "✅ GCP configured. Current config:"
gcloud config list
```

---

### 🔹 C. **Azure Integration Script**

**`azure_setup.sh`**
```bash
#!/bin/bash

echo "==== Azure CLI Setup ===="

# Install Azure CLI
if ! command -v az &> /dev/null; then
    echo "Installing Azure CLI..."
    rpm --import https://packages.microsoft.com/keys/microsoft.asc
    dnf install -y https://packages.microsoft.com/config/rhel/9.0/packages-microsoft-prod.rpm
    dnf install -y azure-cli
fi

# Login
az login

echo "✅ Azure CLI configured. Subscriptions:"
az account list --output table
```

---

## 📌 Security & Best Practices

- Use IAM roles or managed identities where possible (especially on cloud VMs)
- Avoid hardcoding secrets; use environment variables or secret managers
- Rotate keys regularly
- Validate CLI versions (`aws --version`, `gcloud version`, `az version`)
- Use CLI profiles for multiple accounts

---
