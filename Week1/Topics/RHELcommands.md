## ✅ 1. RHEL(Red Hat Enterprise Linux) Command Cheat Sheet (Essential for Admins)

### 🔹 File & Directory Management
```bash
ls -l             # Long listing format
cd /path          # Change directory
pwd               # Print working directory
mkdir dirname     # Create directory
rm file           # Remove file
rm -r dirname     # Remove directory recursively
cp src dest       # Copy files or directories
mv src dest       # Move or rename files
```

### 🔹 File Viewing & Editing
```bash
cat file.txt             # View content
less file.txt            # View with scroll
tail -n 100 logfile.log  # Last 100 lines
head file.txt            # First few lines
vi file.txt              # Open file with vim
nano file.txt            # Open file with nano
```

### 🔹 System Info
```bash
uname -r           # Kernel version
df -h              # Disk usage (human-readable)
free -m            # Memory usage
top                # Processes
uptime             # Load average and uptime
whoami             # Logged-in user
```

### 🔹 User & Permissions
```bash
useradd newuser         # Create user
passwd newuser          # Set password
chmod 755 file          # Set permissions
chown user:group file   # Change ownership
```

### 🔹 Package & System Management
```bash
dnf install pkg         # Install a package
dnf remove pkg          # Remove a package
dnf update              # Update system
systemctl status sshd   # Check service
systemctl restart sshd  # Restart service
```

---

## 🔐 2. Server Hardening Tips

### 🔸 SSH Hardening
- Disable root login:
  ```bash
  /etc/ssh/sshd_config → PermitRootLogin no
  ```
- Change SSH port from 22:
  ```bash
  Port 2222
  ```
- Enable key-based auth, disable password:
  ```bash
  PasswordAuthentication no
  ```

### 🔸 SELinux
```bash
getenforce             # Check status
setenforce 1           # Set to Enforcing
vi /etc/selinux/config # Set SELINUX=enforcing
```

Use `semanage` (from `policycoreutils-python-utils`) to manage SELinux rules:
```bash
semanage port -l       # List managed ports
semanage port -a -t ssh_port_t -p tcp 2222
```

### 🔸 Firewall (firewalld)
```bash
firewall-cmd --state
firewall-cmd --list-all
firewall-cmd --add-service=http --permanent
firewall-cmd --reload
```

---

## 🔎 3. Log Analysis & Troubleshooting

### 🔸 System Logs
```bash
journalctl               # View system logs
journalctl -xe           # View latest critical logs
journalctl -u nginx      # Logs for nginx service
```

### 🔸 Log Files to Know
| File Path                 | Purpose                        |
|---------------------------|--------------------------------|
| `/var/log/messages`       | General system log             |
| `/var/log/secure`         | Auth logs                      |
| `/var/log/boot.log`       | Boot-time messages             |
| `/var/log/cron`           | Cron job logs                  |
| `/var/log/dnf.log`        | Yum/DNF transaction logs       |
| `/var/log/httpd/*`        | Apache logs                    |
| `/var/log/audit/audit.log`| SELinux and auditd events      |

### 🔸 grep + less = 💪
```bash
grep "error" /var/log/messages | less
```

---

## 🔧 4. Common Troubleshooting Scenarios

### 🔹 Boot Issues
```bash
journalctl -xb         # Boot-related errors
```
- Check `/etc/fstab` for invalid entries
- Use `dracut` to rebuild initramfs if kernel/initrd is broken

### 🔹 DNS Not Resolving
```bash
cat /etc/resolv.conf
ping google.com
dig example.com
```

### 🔹 Network Down
```bash
ip a                   # Interface status
nmcli dev status       # NetworkManager devices
systemctl restart NetworkManager
```

### 🔹 Service Crashes or Fails to Start
```bash
systemctl status service
journalctl -u service
```

Example:
```bash
systemctl restart nginx
journalctl -u nginx
```

---
