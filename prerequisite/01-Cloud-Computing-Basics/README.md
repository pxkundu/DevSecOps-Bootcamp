# ☁️ Cloud Computing Basics

## 🎯 Overview

Essential cloud computing concepts and AWS fundamentals you need to understand before starting the DevSecOps bootcamp. This covers the foundational knowledge required for working with cloud platforms.

## 📚 Key Concepts

### **What is Cloud Computing?**

**Cloud Computing** is the delivery of computing services (servers, storage, databases, networking, software) over the internet ("the cloud") on a pay-as-you-go basis.

**Key Characteristics:**
- **On-demand self-service** - Provision resources automatically
- **Broad network access** - Access from anywhere via internet
- **Resource pooling** - Shared resources across multiple customers
- **Rapid elasticity** - Scale up/down quickly
- **Measured service** - Pay only for what you use

### **Cloud Service Models**

#### **1. Infrastructure as a Service (IaaS)**
- **What**: Virtual machines, storage, networking
- **Examples**: AWS EC2, Google Compute Engine, Azure VMs
- **You manage**: OS, applications, data
- **Provider manages**: Hardware, networking, virtualization

#### **2. Platform as a Service (PaaS)**
- **What**: Development platforms, databases, middleware
- **Examples**: AWS Elastic Beanstalk, Google App Engine, Heroku
- **You manage**: Applications, data
- **Provider manages**: OS, runtime, middleware

#### **3. Software as a Service (SaaS)**
- **What**: Complete applications
- **Examples**: Gmail, Salesforce, Dropbox
- **You manage**: Data, user access
- **Provider manages**: Everything else

## 🚀 AWS Fundamentals

### **AWS Global Infrastructure**

#### **Regions**
- **Definition**: Geographic areas with multiple data centers
- **Examples**: us-east-1 (N. Virginia), eu-west-1 (Ireland), ap-southeast-1 (Singapore)
- **Key Point**: Choose region closest to users for low latency

#### **Availability Zones (AZs)**
- **Definition**: Isolated data centers within a region
- **Purpose**: High availability and fault tolerance
- **Example**: us-east-1a, us-east-1b, us-east-1c

#### **Edge Locations**
- **Definition**: Content delivery network (CDN) points
- **Purpose**: Cache content closer to users
- **Service**: CloudFront

### **Core AWS Services**

#### **Compute Services**
- **EC2 (Elastic Compute Cloud)**: Virtual servers
- **Lambda**: Serverless functions
- **ECS/EKS**: Container services
- **Auto Scaling**: Automatic scaling

#### **Storage Services**
- **S3 (Simple Storage Service)**: Object storage
- **EBS (Elastic Block Store)**: Block storage for EC2
- **EFS (Elastic File System)**: File storage
- **Glacier**: Long-term archival storage

#### **Database Services**
- **RDS**: Managed relational databases
- **DynamoDB**: NoSQL database
- **ElastiCache**: In-memory caching
- **Redshift**: Data warehouse

#### **Networking Services**
- **VPC (Virtual Private Cloud)**: Private network
- **Route 53**: DNS service
- **CloudFront**: Content delivery
- **API Gateway**: API management

#### **Security Services**
- **IAM (Identity and Access Management)**: User and permission management
- **KMS (Key Management Service)**: Encryption key management
- **CloudTrail**: API logging
- **GuardDuty**: Threat detection

## 🔑 Essential AWS Terminology

### **Account & Billing**
- **AWS Account**: Your subscription to AWS services
- **Root User**: Account owner with full access
- **IAM User**: Individual user account
- **Billing**: Pay-as-you-go model
- **Free Tier**: Limited free usage for new accounts

### **Resource Management**
- **Resource**: Any AWS service component (EC2 instance, S3 bucket, etc.)
- **Tag**: Key-value pair for organizing resources
- **ARN (Amazon Resource Name)**: Unique identifier for resources
- **Region**: Geographic location for resources

### **Security Concepts**
- **Access Key**: Credentials for programmatic access
- **Secret Key**: Password for access key
- **Role**: Temporary permissions for AWS services
- **Policy**: JSON document defining permissions
- **Security Group**: Virtual firewall for EC2 instances

## 💰 AWS Pricing Model

### **Pay-as-You-Go**
- **No upfront costs**
- **Pay only for what you use**
- **No long-term commitments**

### **Cost Factors**
- **Compute**: Instance hours, instance type
- **Storage**: Data stored, data transfer
- **Network**: Data transfer out, requests
- **Services**: API calls, features used

### **Cost Optimization**
- **Right-sizing**: Choose appropriate instance types
- **Reserved Instances**: Discount for 1-3 year commitments
- **Spot Instances**: Use spare capacity at discount
- **Auto Scaling**: Scale down when not needed

## 🛠️ Getting Started with AWS

### **Account Setup**
1. **Create AWS Account**: Sign up at aws.amazon.com
2. **Set up Billing**: Add payment method
3. **Create IAM User**: Don't use root user for daily work
4. **Enable MFA**: Multi-factor authentication for security

### **Access Methods**
- **AWS Console**: Web-based management interface
- **AWS CLI**: Command-line interface
- **SDKs**: Software development kits for programming
- **CloudFormation**: Infrastructure as code

### **Best Practices**
- **Use IAM roles** instead of access keys when possible
- **Enable CloudTrail** for audit logging
- **Use tags** for resource organization
- **Set up billing alerts** to monitor costs
- **Follow security best practices** from AWS Well-Architected Framework

## 📋 Self-Check Questions

### **Basic Concepts**
1. **Q**: What are the three main cloud service models?
   **A**: IaaS, PaaS, SaaS

2. **Q**: What is the difference between a region and an availability zone?
   **A**: Region is geographic area, AZ is isolated data center within region

3. **Q**: What does "pay-as-you-go" mean in cloud computing?
   **A**: Pay only for resources you use, no upfront costs

### **AWS Specific**
4. **Q**: What is the purpose of IAM?
   **A**: Manage users, groups, and permissions for AWS resources

5. **Q**: What service would you use for object storage?
   **A**: Amazon S3

6. **Q**: What is a VPC?
   **A**: Virtual Private Cloud - your private network in AWS

## 🎯 Next Steps

### **Practice Exercises**
1. **Create an AWS account** and explore the console
2. **Set up IAM user** with appropriate permissions
3. **Create an S3 bucket** and upload a file
4. **Launch an EC2 instance** (free tier eligible)
5. **Set up billing alerts** to monitor costs

### **Additional Learning**
- [AWS Free Tier](https://aws.amazon.com/free/) - Practice with free services
- [AWS Documentation](https://docs.aws.amazon.com/) - Official guides
- [AWS Training](https://aws.amazon.com/training/) - Free and paid courses
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/) - Best practices

## 🔗 Related Prerequisites

- [Linux & Command Line](../02-Linux-Command-Line/README.md) - Terminal skills for AWS CLI
- [Networking Fundamentals](../03-Networking-Fundamentals/README.md) - Network concepts for VPC
- [Security Basics](../06-Security-Basics/README.md) - Security concepts for IAM and security groups

---

**Ready for the next step?** Move on to [Linux & Command Line](../02-Linux-Command-Line/README.md) to learn essential terminal skills!
