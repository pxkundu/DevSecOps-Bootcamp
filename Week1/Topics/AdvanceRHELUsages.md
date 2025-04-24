Let's get into the **pro admin toolkit** with:

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
