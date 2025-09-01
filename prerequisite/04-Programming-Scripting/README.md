# 💻 Programming & Scripting Basics

## 🎯 Overview

Essential programming concepts, scripting skills, and automation fundamentals you need for DevOps work. This covers basic coding principles, common languages, and automation techniques used in modern DevOps practices.

## 📚 Key Concepts

### **What is Programming?**

**Programming** is the process of creating instructions for computers to execute. In DevOps, programming and scripting are essential for automation, infrastructure management, and building tools.

**Why Learn Programming for DevOps?**
- **Automation**: Automate repetitive tasks
- **Infrastructure as Code**: Define infrastructure in code
- **CI/CD Pipelines**: Build and deploy automation
- **Monitoring**: Create custom monitoring scripts
- **Troubleshooting**: Write diagnostic tools

### **Programming vs Scripting**

#### **Programming**
- **Compiled languages**: C, C++, Java, Go
- **Structured**: Complex applications
- **Performance**: Optimized execution
- **Examples**: System tools, applications

#### **Scripting**
- **Interpreted languages**: Python, Bash, PowerShell
- **Quick development**: Rapid prototyping
- **Automation**: Task automation
- **Examples**: DevOps scripts, automation tools

## 🐍 Python Basics

### **Why Python for DevOps?**
- **Easy to learn**: Readable syntax
- **Rich ecosystem**: Libraries for everything
- **Cross-platform**: Works on all operating systems
- **DevOps friendly**: Great for automation and APIs

### **Basic Syntax**

#### **Variables and Data Types**
```python
# Variables
name = "DevOps Engineer"
age = 30
is_expert = True
skills = ["Python", "AWS", "Docker"]

# Data types
string_var = "Hello World"
integer_var = 42
float_var = 3.14
boolean_var = True
list_var = [1, 2, 3, 4, 5]
dict_var = {"key": "value"}
```

#### **Control Structures**
```python
# Conditional statements
if age >= 18:
    print("Adult")
elif age >= 13:
    print("Teenager")
else:
    print("Child")

# Loops
for skill in skills:
    print(f"I know {skill}")

for i in range(5):
    print(f"Count: {i}")

while age < 65:
    age += 1
```

#### **Functions**
```python
def greet(name):
    return f"Hello, {name}!"

def calculate_area(length, width):
    return length * width

# Lambda functions
square = lambda x: x ** 2
```

### **Common DevOps Libraries**

#### **AWS SDK (boto3)**
```python
import boto3

# Create S3 client
s3 = boto3.client('s3')

# List buckets
response = s3.list_buckets()
for bucket in response['Buckets']:
    print(bucket['Name'])
```

#### **Requests (HTTP)**
```python
import requests

# Make HTTP request
response = requests.get('https://api.github.com/users/octocat')
data = response.json()
print(data['name'])
```

#### **Subprocess (System Commands)**
```python
import subprocess

# Run shell command
result = subprocess.run(['ls', '-la'], capture_output=True, text=True)
print(result.stdout)
```

## 🐚 Shell Scripting (Bash)

### **Why Bash for DevOps?**
- **System integration**: Native to Linux/Unix
- **Automation**: Perfect for system tasks
- **CI/CD**: Used in build scripts
- **Server management**: Remote server automation

### **Basic Syntax**

#### **Variables**
```bash
#!/bin/bash

# Variable assignment
NAME="DevOps Engineer"
AGE=30

# Using variables
echo "Hello, $NAME"
echo "Age: ${AGE}"

# Command substitution
CURRENT_DIR=$(pwd)
echo "Current directory: $CURRENT_DIR"
```

#### **Control Structures**
```bash
# Conditional statements
if [ $AGE -ge 18 ]; then
    echo "Adult"
elif [ $AGE -ge 13 ]; then
    echo "Teenager"
else
    echo "Child"
fi

# Loops
for skill in "Python" "AWS" "Docker"; do
    echo "I know $skill"
done

# While loop
count=0
while [ $count -lt 5 ]; do
    echo "Count: $count"
    count=$((count + 1))
done
```

#### **Functions**
```bash
# Function definition
greet() {
    local name=$1
    echo "Hello, $name!"
}

# Function call
greet "World"
```

### **Common DevOps Scripts**

#### **System Information**
```bash
#!/bin/bash

echo "=== System Information ==="
echo "Hostname: $(hostname)"
echo "OS: $(uname -s)"
echo "Kernel: $(uname -r)"
echo "CPU: $(nproc) cores"
echo "Memory: $(free -h | grep Mem | awk '{print $2}')"
```

#### **Backup Script**
```bash
#!/bin/bash

SOURCE_DIR="/var/www"
BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup
tar -czf "$BACKUP_DIR/backup_$DATE.tar.gz" "$SOURCE_DIR"

# Keep only last 7 backups
find "$BACKUP_DIR" -name "backup_*.tar.gz" -mtime +7 -delete
```

## 🔧 Infrastructure as Code

### **What is Infrastructure as Code (IaC)?**
- **Definition**: Managing infrastructure through code
- **Benefits**: Version control, consistency, automation
- **Tools**: Terraform, CloudFormation, Ansible

### **Terraform Example**
```hcl
# AWS provider
provider "aws" {
  region = "us-west-2"
}

# EC2 instance
resource "aws_instance" "web" {
  ami           = "ami-12345678"
  instance_type = "t2.micro"
  
  tags = {
    Name = "WebServer"
  }
}
```

### **Ansible Example**
```yaml
---
- name: Install web server
  hosts: webservers
  tasks:
    - name: Install Apache
      apt:
        name: apache2
        state: present
    
    - name: Start Apache service
      service:
        name: apache2
        state: started
        enabled: yes
```

## 🔄 Automation Concepts

### **Automation Principles**
- **DRY**: Don't Repeat Yourself
- **Modularity**: Break tasks into reusable components
- **Error handling**: Graceful failure management
- **Logging**: Track execution and errors
- **Idempotency**: Safe to run multiple times

### **Common Automation Patterns**

#### **Configuration Management**
```python
import yaml
import json

# Load configuration
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Apply configuration
for service in config['services']:
    deploy_service(service)
```

#### **Health Checks**
```python
import requests
import time

def check_service_health(url):
    try:
        response = requests.get(url, timeout=5)
        return response.status_code == 200
    except:
        return False

# Monitor service
while True:
    if check_service_health('http://localhost:8080'):
        print("Service is healthy")
    else:
        print("Service is down")
    time.sleep(30)
```

## 📊 Data Processing

### **Working with Data**
- **JSON**: API responses, configuration
- **YAML**: Configuration files, documentation
- **CSV**: Logs, reports, data analysis
- **XML**: Legacy systems, SOAP APIs

### **Data Processing Examples**

#### **JSON Processing**
```python
import json

# Parse JSON
data = json.loads('{"name": "John", "age": 30}')

# Create JSON
config = {
    "database": {
        "host": "localhost",
        "port": 5432
    }
}
json.dump(config, open('config.json', 'w'))
```

#### **Log Processing**
```python
import re
from datetime import datetime

def parse_log_line(line):
    pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) - (\w+) - (.+)'
    match = re.match(pattern, line)
    if match:
        return {
            'timestamp': match.group(1),
            'level': match.group(2),
            'message': match.group(3)
        }
    return None
```

## 🧪 Testing

### **Testing Concepts**
- **Unit testing**: Test individual functions
- **Integration testing**: Test component interactions
- **End-to-end testing**: Test complete workflows
- **Test-driven development**: Write tests first

### **Python Testing Example**
```python
import unittest

def add_numbers(a, b):
    return a + b

class TestMath(unittest.TestCase):
    def test_add_numbers(self):
        result = add_numbers(2, 3)
        self.assertEqual(result, 5)
    
    def test_add_negative(self):
        result = add_numbers(-1, 1)
        self.assertEqual(result, 0)

if __name__ == '__main__':
    unittest.main()
```

## 📋 Self-Check Questions

### **Programming Concepts**
1. **Q**: What is the difference between programming and scripting?
   **A**: Programming uses compiled languages for complex apps, scripting uses interpreted languages for automation

2. **Q**: What is a variable?
   **A**: A container that stores data values

3. **Q**: What is a function?
   **A**: A reusable block of code that performs a specific task

### **Python Specific**
4. **Q**: How do you create a list in Python?
   **A**: `my_list = [1, 2, 3, 4, 5]`

5. **Q**: What is the purpose of `if __name__ == '__main__':`?
   **A**: Ensures code only runs when script is executed directly

### **Shell Scripting**
6. **Q**: How do you assign a variable in bash?
   **A**: `VARIABLE="value"`

7. **Q**: What does `$1` refer to in a bash script?
   **A**: The first command line argument

## 🎯 Practice Exercises

### **Beginner Level**
1. **Write a Python script** that lists files in a directory
2. **Create a bash script** that backs up a folder
3. **Write a function** that calculates the area of a circle
4. **Parse a JSON file** and extract specific data

### **Intermediate Level**
1. **Build a web scraper** using Python requests
2. **Create an AWS automation script** using boto3
3. **Write a configuration management script**
4. **Build a monitoring script** that checks service health

### **Advanced Level**
1. **Create a complete CI/CD pipeline** script
2. **Build a log analysis tool** with data visualization
3. **Develop an infrastructure provisioning script**
4. **Create a comprehensive testing framework**

## 🔗 Additional Resources

### **Learning Platforms**
- [Python.org](https://www.python.org/) - Official Python documentation
- [Real Python](https://realpython.com/) - Python tutorials
- [Bash Guide](https://mywiki.wooledge.org/BashGuide) - Bash scripting guide
- [Learn Shell](https://www.learnshell.org/) - Interactive shell tutorial

### **Practice Platforms**
- [HackerRank](https://www.hackerrank.com/) - Programming challenges
- [LeetCode](https://leetcode.com/) - Algorithm problems
- [Codewars](https://www.codewars.com/) - Programming katas
- [Exercism](https://exercism.org/) - Language learning tracks

### **DevOps-Specific Resources**
- [Python for DevOps](https://www.oreilly.com/library/view/python-for-devops/9781492057680/) - Book
- [Automate the Boring Stuff](https://automatetheboringstuff.com/) - Python automation
- [Shell Scripting Tutorial](https://www.shellscript.sh/) - Bash guide

## 🔗 Related Prerequisites

- [Linux & Command Line](../02-Linux-Command-Line/README.md) - Shell scripting environment
- [DevOps Fundamentals](../05-DevOps-Fundamentals/README.md) - Automation concepts
- [Tools & Technologies](../09-Tools-Technologies/README.md) - Programming tools

---

**Ready for the next step?** Move on to [DevOps Fundamentals](../05-DevOps-Fundamentals/README.md) to learn DevOps principles!
