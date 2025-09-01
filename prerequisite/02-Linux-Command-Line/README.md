# 🐧 Linux & Command Line Basics

## 🎯 Overview

Essential Linux command line skills and terminal operations you need to work effectively in DevOps. This covers basic commands, file management, and shell operations that are fundamental to cloud and DevOps work.

## 📚 Key Concepts

### **What is the Command Line?**

**Command Line Interface (CLI)** is a text-based interface for interacting with your computer. It's faster, more powerful, and essential for automation and DevOps work.

**Why Learn CLI?**
- **Automation**: Script repetitive tasks
- **Remote access**: Connect to servers via SSH
- **DevOps tools**: Most DevOps tools are CLI-based
- **Cloud platforms**: AWS CLI, Azure CLI, etc.
- **Server management**: Most servers are Linux-based

### **Shell Basics**

#### **What is a Shell?**
- **Definition**: Program that interprets commands
- **Common shells**: Bash (default), Zsh, Fish
- **Purpose**: Interface between user and operating system

#### **Terminal vs Shell**
- **Terminal**: Application that runs the shell
- **Shell**: Program that executes commands
- **Examples**: Terminal.app (macOS), Windows Terminal, iTerm2

## 🛠️ Essential Commands

### **Navigation Commands**

#### **File System Navigation**
```bash
pwd          # Print working directory (show current location)
ls           # List files and directories
cd           # Change directory
mkdir        # Make directory
rmdir        # Remove empty directory
```

#### **Common Navigation Patterns**
```bash
cd /         # Go to root directory
cd ~         # Go to home directory
cd ..        # Go up one directory
cd -         # Go to previous directory
ls -la       # List all files (including hidden) with details
```

### **File Management**

#### **Viewing Files**
```bash
cat          # Display file content
less         # View file content (scrollable)
head         # Show first 10 lines
tail         # Show last 10 lines
tail -f      # Follow file changes (useful for logs)
```

#### **File Operations**
```bash
cp           # Copy files/directories
mv           # Move/rename files/directories
rm           # Remove files
touch        # Create empty file or update timestamp
```

#### **File Permissions**
```bash
chmod        # Change file permissions
chown        # Change file owner
ls -l        # List with permissions
```

**Permission Examples:**
```bash
chmod +x script.sh    # Make executable
chmod 755 file.txt    # Set specific permissions
chmod 644 file.txt    # Read/write for owner, read for others
```

### **Text Processing**

#### **Search and Filter**
```bash
grep         # Search for text patterns
find         # Find files by name/attributes
which        # Find command location
whereis      # Find command, source, and manual pages
```

#### **Text Manipulation**
```bash
echo         # Print text
sort         # Sort lines
uniq         # Remove duplicate lines
wc           # Count lines, words, characters
cut          # Extract sections from lines
```

### **System Information**

#### **System Commands**
```bash
ps           # Show running processes
top          # Show system resources (interactive)
htop         # Enhanced top (if available)
df           # Show disk space
du           # Show directory size
free         # Show memory usage
```

#### **Network Commands**
```bash
ping         # Test network connectivity
curl         # Transfer data from/to server
wget         # Download files
netstat      # Show network connections
ss           # Show socket statistics
```

## 🔧 Shell Features

### **Command History**
```bash
history      # Show command history
!n           # Execute command number n
!!           # Execute last command
Ctrl+R       # Search command history
```

### **Tab Completion**
- **Press Tab** to auto-complete commands, filenames, paths
- **Press Tab twice** to show all possible completions
- **Essential for efficiency** and avoiding typos

### **Command Chaining**
```bash
command1 && command2    # Run command2 only if command1 succeeds
command1 || command2    # Run command2 only if command1 fails
command1 ; command2     # Run both commands regardless
command1 | command2     # Pipe output from command1 to command2
```

### **Redirection**
```bash
command > file          # Redirect output to file (overwrite)
command >> file         # Redirect output to file (append)
command < file          # Redirect input from file
command 2>&1            # Redirect stderr to stdout
```

## 📁 File System Structure

### **Linux Directory Structure**
```
/                   # Root directory
├── bin/            # Essential binaries
├── boot/           # Boot loader files
├── dev/            # Device files
├── etc/            # Configuration files
├── home/           # User home directories
├── lib/            # Shared libraries
├── media/          # Mount points for removable media
├── mnt/            # Mount points
├── opt/            # Optional applications
├── proc/           # Process information
├── root/           # Root user home
├── run/            # Runtime data
├── sbin/           # System binaries
├── srv/            # Service data
├── sys/            # System information
├── tmp/            # Temporary files
├── usr/            # User programs and data
└── var/            # Variable data (logs, etc.)
```

### **Important Directories for DevOps**
- **/etc/**: Configuration files
- **/var/log/**: System and application logs
- **/home/**: User directories
- **/tmp/**: Temporary files
- **/opt/**: Third-party applications

## 🔍 Working with Files

### **File Types**
- **Regular files**: Text, binary, executable
- **Directories**: Contain other files
- **Symbolic links**: Pointers to other files
- **Device files**: Represent hardware devices

### **File Permissions**
```
-rw-r--r--  1 user group 1234 Jan 1 12:00 file.txt
││││││││││   │ │    │     │   │        │
││││││││││   │ │    │     │   │        └── Filename
││││││││││   │ │    │     │   └────────── Date
││││││││││   │ │    │     └────────────── Size
││││││││││   │ │    └──────────────────── Group
││││││││││   │ └───────────────────────── Owner
││││││││││   └──────────────────────────── Links
│││││││││└──────────────────────────────── Others (read)
││││││││└───────────────────────────────── Others (write)
│││││││└────────────────────────────────── Others (execute)
││││││└─────────────────────────────────── Group (execute)
│││││└──────────────────────────────────── Group (write)
││││└───────────────────────────────────── Group (read)
│││└────────────────────────────────────── Owner (execute)
││└─────────────────────────────────────── Owner (write)
│└──────────────────────────────────────── Owner (read)
└───────────────────────────────────────── File type (- = file, d = directory, l = link)
```

## 🚀 Practical Examples

### **Common DevOps Tasks**

#### **Log Analysis**
```bash
# View recent log entries
tail -n 50 /var/log/application.log

# Search for errors
grep "ERROR" /var/log/application.log

# Monitor log in real-time
tail -f /var/log/application.log
```

#### **File Management**
```bash
# Create backup of configuration
cp /etc/nginx/nginx.conf /etc/nginx/nginx.conf.backup

# Find large files
find /home -type f -size +100M

# Count files in directory
ls -1 | wc -l
```

#### **System Monitoring**
```bash
# Check disk space
df -h

# Check memory usage
free -h

# Check running processes
ps aux | grep nginx
```

## 📋 Self-Check Questions

### **Basic Commands**
1. **Q**: What command shows your current directory?
   **A**: `pwd`

2. **Q**: How do you list all files including hidden ones?
   **A**: `ls -la`

3. **Q**: What does `cd ..` do?
   **A**: Goes up one directory level

### **File Operations**
4. **Q**: How do you copy a file?
   **A**: `cp source destination`

5. **Q**: What command removes a file?
   **A**: `rm filename`

6. **Q**: How do you make a file executable?
   **A**: `chmod +x filename`

### **Text Processing**
7. **Q**: How do you search for text in a file?
   **A**: `grep "text" filename`

8. **Q**: What does `tail -f` do?
   **A**: Follows file changes in real-time

## 🎯 Practice Exercises

### **Beginner Level**
1. **Navigate directories**: Use `cd`, `ls`, `pwd`
2. **Create files and directories**: Use `mkdir`, `touch`
3. **Copy and move files**: Use `cp`, `mv`
4. **View file contents**: Use `cat`, `less`, `head`, `tail`

### **Intermediate Level**
1. **Search for files**: Use `find` and `grep`
2. **Check system resources**: Use `top`, `df`, `free`
3. **Work with permissions**: Use `chmod`, `chown`
4. **Use command chaining**: Use `&&`, `||`, `|`

### **Advanced Level**
1. **Write simple scripts**: Create bash scripts
2. **Process text data**: Use `awk`, `sed`
3. **Network troubleshooting**: Use `ping`, `curl`, `netstat`
4. **System administration**: Monitor processes and logs

## 🔗 Additional Resources

### **Online Terminals**
- [Linux Terminal Online](https://bellard.org/jslinux/)
- [Webminal](https://www.webminal.org/)
- [JSLinux](https://bellard.org/jslinux/)

### **Learning Resources**
- [Linux Journey](https://linuxjourney.com/) - Interactive Linux tutorial
- [Bash Guide](https://mywiki.wooledge.org/BashGuide) - Comprehensive bash guide
- [Linux Command Library](https://linuxcommandlibrary.com/) - Command reference

### **Practice Platforms**
- [OverTheWire Bandit](https://overthewire.org/wargames/bandit/) - Linux security wargame
- [HackerRank Linux Shell](https://www.hackerrank.com/domains/shell) - Shell scripting challenges

## 🔗 Related Prerequisites

- [Cloud Computing Basics](../01-Cloud-Computing-Basics/README.md) - AWS CLI usage
- [Programming & Scripting](../04-Programming-Scripting/README.md) - Shell scripting
- [DevOps Fundamentals](../05-DevOps-Fundamentals/README.md) - Automation concepts

---

**Ready for the next step?** Move on to [Networking Fundamentals](../03-Networking-Fundamentals/README.md) to understand network concepts!
