Terraform is an open-source Infrastructure as Code (IaC) software tool developed by HashiCorp. It allows you to define and manage infrastructure resources in a declarative way using code, making it easier to provision, modify, and version infrastructure across various cloud providers and on-premises environments. Terraform is widely used in DevOps practices to automate infrastructure management, ensuring consistency, repeatability, and scalability.

Here’s a detailed breakdown of Terraform and its key aspects:

---

### **What is Terraform?**
Terraform enables you to describe your infrastructure as code using a declarative configuration language (primarily HashiCorp Configuration Language, or HCL, though it also supports JSON). Instead of manually provisioning resources through a cloud provider’s UI or writing custom scripts, you define your desired infrastructure state in Terraform configuration files, and Terraform handles provisioning and managing those resources for you.

Terraform supports a wide range of providers, including:
- Cloud providers: AWS, Azure, Google Cloud Platform (GCP), DigitalOcean, etc.
- Infrastructure services: Kubernetes, Docker, VMware, etc.
- SaaS providers: GitHub, Datadog, etc.

---

### **Key Concepts in Terraform**
1. **Providers**:
   - Providers are plugins that Terraform uses to interact with APIs of various platforms (e.g., AWS, Azure, GCP).
   - Example: The AWS provider allows Terraform to manage AWS resources like EC2 instances, S3 buckets, and VPCs.
   - You define a provider in your configuration:
     ```hcl
     provider "aws" {
       region = "us-east-1"
     }
     ```

2. **Resources**:
   - Resources are the individual components of your infrastructure (e.g., a virtual machine, a database, a network).
   - Example: Define an AWS EC2 instance:
     ```hcl
     resource "aws_instance" "example" {
       ami           = "ami-0c55b159cbfafe1f0"
       instance_type = "t2.micro"
     }
     ```

3. **State**:
   - Terraform maintains a state file (`terraform.tfstate`) that tracks the current state of your infrastructure.
   - This file maps your configuration to the real-world resources Terraform manages.
   - State can be stored locally or remotely (e.g., in S3, Terraform Cloud, or Consul) to enable collaboration and persistence.

4. **Modules**:
   - Modules are reusable, self-contained packages of Terraform configurations.
   - They help you organize and reuse code. For example, you can create a module for a VPC and reuse it across projects.
   - Example: Calling a module:
     ```hcl
     module "vpc" {
       source = "terraform-aws-modules/vpc/aws"
       version = "3.14.0"
       # Module inputs
       vpc_cidr = "10.0.0.0/16"
     }
     ```

5. **Variables and Outputs**:
   - Variables allow you to parameterize your configurations.
     ```hcl
     variable "instance_type" {
       default = "t2.micro"
     }
     ```
   - Outputs return values from your infrastructure after deployment.
     ```hcl
     output "instance_ip" {
       value = aws_instance.example.public_ip
     }
     ```

6. **Plan and Apply**:
   - Terraform operates in a two-step process:
     - `terraform plan`: Generates an execution plan showing what changes will be made to reach the desired state.
     - `terraform apply`: Applies the changes to provision or modify resources.

---

### **How Terraform Works**
Terraform follows a declarative approach:
1. **Write Configuration Files**:
   - You define your infrastructure in `.tf` files using HCL (or JSON).
   - Example: A simple configuration to create an AWS S3 bucket:
     ```hcl
     provider "aws" {
       region = "us-east-1"
     }

     resource "aws_s3_bucket" "my_bucket" {
       bucket = "my-unique-bucket-name-123"
       acl    = "private"
     }
     ```

2. **Initialize the Project**:
   - Run `terraform init` to download the necessary provider plugins and set up the working directory.

3. **Create an Execution Plan**:
   - Run `terraform plan` to see what Terraform will do to match your desired state (create, update, or destroy resources).

4. **Apply Changes**:
   - Run `terraform apply` to provision the resources. Terraform will interact with the provider’s API (e.g., AWS) to create the resources.

5. **Manage Changes**:
   - If you update your configuration (e.g., change the S3 bucket’s ACL), Terraform will detect the drift and apply the necessary changes on the next `terraform apply`.

---

### **Benefits of Terraform**
- **Infrastructure as Code**: Define infrastructure in version-controlled files, enabling collaboration, audits, and repeatability.
- **Multi-Cloud Support**: Works with multiple cloud providers and services, allowing you to manage hybrid or multi-cloud environments.
- **State Management**: Tracks the state of your infrastructure, making it easy to modify or destroy resources.
- **Idempotency**: Terraform ensures that applying the same configuration multiple times produces the same result.
- **Community and Ecosystem**: Large community support, with thousands of modules available in the Terraform Registry.

---

### **Terraform Workflow Example**
Let’s walk through a simple example of creating an AWS EC2 instance.

1. **Create a Configuration File** (`main.tf`):
   ```hcl
   provider "aws" {
     region = "us-east-1"
   }

   resource "aws_instance" "example" {
     ami           = "ami-0c55b159cbfafe1f0"  # Amazon Linux 2 AMI
     instance_type = "t2.micro"

     tags = {
       Name = "example-instance"
     }
   }

   output "instance_public_ip" {
     value = aws_instance.example.public_ip
   }
   ```

2. **Initialize Terraform**:
   ```bash
   terraform init
   ```

3. **Plan the Changes**:
   ```bash
   terraform plan
   ```
   Terraform will show that it plans to create an EC2 instance.

4. **Apply the Changes**:
   ```bash
   terraform apply
   ```
   Confirm with `yes`, and Terraform will create the EC2 instance. The public IP will be outputted.

5. **Destroy Resources (Optional)**:
   To clean up:
   ```bash
   terraform destroy
   ```

---

### **Terraform in Relation to Your Project**
In your current project (a Dockerized Nginx server with a SaaS task manager), Terraform can be used to:
- **Provision Infrastructure**: If your Docker containers are hosted on a cloud provider (e.g., AWS EC2, ECS, or EKS), Terraform can provision the underlying infrastructure (e.g., EC2 instances, VPCs, or Kubernetes clusters).
- **Manage Networking**: Define and manage the networking setup, such as load balancers or DNS records (e.g., for `partha.snehith-dev.com`).
- **Automate Deployment**: Combine Terraform with CI/CD pipelines to automate infrastructure provisioning and updates.

For example, you could use Terraform to:
- Deploy an EC2 instance to run your Docker containers.
- Set up an Application Load Balancer (ALB) to handle traffic to your domain without needing to specify ports (instead of using Nginx as a reverse proxy directly).
- Manage DNS records for `partha.snehith-dev.com` in Route 53.

---

### **Terraform vs. Other Tools**
- **Terraform vs. Ansible**:
  - Terraform is declarative and focuses on provisioning infrastructure (e.g., creating cloud resources).
  - Ansible is imperative and focuses on configuration management (e.g., installing software, configuring servers).
- **Terraform vs. CloudFormation**:
  - CloudFormation is AWS-specific, while Terraform is provider-agnostic.
  - Terraform has a more mature ecosystem for multi-cloud setups.
- **Terraform vs. Pulumi**:
  - Terraform uses HCL, while Pulumi uses general-purpose languages like JavaScript, TypeScript, or Python.
  - Terraform has a larger community and more mature ecosystem.

---

### **Best Practices for Terraform**
1. **Use Modules**: Break down your infrastructure into reusable modules for better organization.
2. **Store State Remotely**: Use remote backends (e.g., S3 with locking via DynamoDB) to enable team collaboration and avoid state file corruption.
3. **Version Control**: Store your Terraform code in Git to track changes and collaborate.
4. **Use Variables**: Parameterize your configurations to make them reusable and adaptable.
5. **Plan Before Apply**: Always run `terraform plan` to review changes before applying them.
6. **Secure Secrets**: Avoid hardcoding secrets in your Terraform files. Use tools like HashiCorp Vault, AWS Secrets Manager, or environment variables.

---

### **Learning Resources**
- **Official Documentation**: [terraform.io](https://www.terraform.io/docs)
- **Terraform Registry**: Browse providers and modules at [registry.terraform.io](https://registry.terraform.io)
- **HashiCorp Learn**: Free tutorials at [learn.hashicorp.com](https://learn.hashicorp.com/terraform)
- **Books**: "Terraform: Up & Running" by Yevgeniy Brikman is a great resource for beginners.

---

Terraform is a powerful tool that can greatly simplify infrastructure management, especially for projects like yours that involve cloud deployments.

---

How to start learning Terraform using a Windows Subsystem for Linux (WSL) environment with AWS as the cloud provider. This guide will cover installation, setup, basic commands, and a simple project to get you started. 

By the end, you'll have Terraform installed on WSL, configured to work with AWS, and you'll deploy a basic AWS EC2 instance as a hands-on project.

---

### Step 1: Set Up WSL and Install Terraform

#### 1.1 Ensure WSL is Installed
WSL allows you to run a Linux environment on Windows. If you don’t have WSL installed:
1. Open PowerShell as Administrator and run:
   ```powershell
   wsl --install
   ```
   This installs WSL 2 and the default Ubuntu distribution. If you prefer a different distro (e.g., Debian), you can install it from the Microsoft Store.
2. Restart your machine if prompted.
3. Launch WSL by opening a terminal and typing:
   ```powershell
   wsl
   ```
   You’ll be in a Linux shell (e.g., Ubuntu).

#### 1.2 Update WSL
Inside the WSL terminal, ensure your system is up to date:
```bash
sudo apt update && sudo apt upgrade -y
```

#### 1.3 Install Terraform
Terraform provides a binary that you can install on WSL. Follow these steps:
1. **Install Prerequisites**:
   You’ll need `unzip` and `curl`:
   ```bash
   sudo apt install unzip curl -y
   ```

2. **Download Terraform**:
   Terraform is distributed as a single binary. Download the latest version for Linux (amd64 for most WSL setups). As of March 16, 2025, check the latest version on the [Terraform downloads page](https://www.terraform.io/downloads.html). For example, to download version 1.7.0 (adjust as needed):
   ```bash
   curl -O https://releases.hashicorp.com/terraform/1.7.0/terraform_1.7.0_linux_amd64.zip
   ```

3. **Unzip and Install**:
   Unzip the downloaded file and move the binary to a location in your PATH (e.g., `/usr/local/bin`):
   ```bash
   unzip terraform_1.7.0_linux_amd64.zip
   sudo mv terraform /usr/local/bin/
   ```

4. **Verify Installation**:
   Check that Terraform is installed:
   ```bash
   terraform -v
   ```
   You should see the version (e.g., `Terraform v1.7.0`).

---

### Step 2: Set Up AWS Credentials
Terraform needs access to your AWS account to manage resources. You’ll configure AWS credentials on WSL.

#### 2.1 Install the AWS CLI
1. Install the AWS CLI to manage your credentials:
   ```bash
   sudo apt install awscli -y
   ```

2. Verify the installation:
   ```bash
   aws --version
   ```

#### 2.2 Configure AWS Credentials
1. Generate AWS Access Keys:
   - Log in to the AWS Management Console.
   - Go to **IAM > Users > [Your User] > Security credentials**.
   - Create an access key and download the `Access Key ID` and `Secret Access Key`.

2. Configure AWS CLI:
   Run the following command and provide your credentials:
   ```bash
   aws configure
   ```
   - **AWS Access Key ID**: Enter your access key.
   - **AWS Secret Access Key**: Enter your secret key.
   - **Default region name**: Enter your preferred region (e.g., `us-east-1`).
   - **Default output format**: Enter `json` (or leave as default).

   This creates a credentials file at `~/.aws/credentials` and a config file at `~/.aws/config`.

3. Test AWS CLI:
   Verify that your credentials work by listing S3 buckets (or another AWS command):
   ```bash
   aws s3 ls
   ```
   If configured correctly, this should list your S3 buckets (or return an empty response if you have none).

#### 2.3 (Optional) Use AWS IAM Role (Best Practice)
For production, it’s better to use an IAM role or temporary credentials instead of long-term access keys. If you’re using an EC2 instance with an IAM role, Terraform can automatically use those credentials. For this learning setup, access keys are fine.

---

### Step 3: Learn Basic Terraform Commands
Before diving into a project, let’s go over the core Terraform commands you’ll use:
- `terraform init`: Initializes a Terraform working directory by downloading provider plugins.
- `terraform plan`: Creates an execution plan showing what Terraform will do to reach the desired state.
- `terraform apply`: Applies the changes to provision or modify resources.
- `terraform destroy`: Destroys all resources managed by Terraform in the current configuration.
- `terraform fmt`: Formats your Terraform configuration files to follow style conventions.
- `terraform validate`: Validates your configuration for syntax errors.

---

### Step 4: Create a Simple Terraform Project
Let’s create a simple project to deploy an AWS EC2 instance using Terraform. This will help you understand the workflow.

#### 4.1 Set Up a Project Directory
1. Create a new directory for your project:
   ```bash
   mkdir terraform-aws-ec2
   cd terraform-aws-ec2
   ```

2. Create a file named `main.tf`:
   ```bash
   touch main.tf
   ```

#### 4.2 Write Your Terraform Configuration
Open `main.tf` in a text editor (e.g., `nano` or `vim`):
```bash
nano main.tf
```

Add the following configuration to create an EC2 instance:
```hcl
# Specify the provider and region
provider "aws" {
  region = "us-east-1"
}

# Define an EC2 instance resource
resource "aws_instance" "example" {
  ami           = "ami-0c55b159cbfafe1f0"  # Amazon Linux 2 AMI (us-east-1)
  instance_type = "t2.micro"

  tags = {
    Name = "terraform-example-instance"
  }
}

# Output the public IP of the instance
output "instance_public_ip" {
  value = aws_instance.example.public_ip
}
```

**Notes**:
- The AMI ID (`ami-0c55b159cbfafe1f0`) is for Amazon Linux 2 in `us-east-1`. AMIs are region-specific, so if you’re using a different region, find the appropriate AMI ID in the AWS EC2 console under "Launch Instance."
- `t2.micro` is a free-tier instance type, suitable for learning.

#### 4.3 Initialize the Project
Run the following to download the AWS provider plugin:
```bash
terraform init
```
You should see output indicating that Terraform has initialized and downloaded the provider.

#### 4.4 Plan the Deployment
Run:
```bash
terraform plan
```
Terraform will show a plan indicating it will create an EC2 instance and output its public IP. Review the plan to ensure it looks correct.

#### 4.5 Apply the Configuration
Run:
```bash
terraform apply
```
- Terraform will show the plan again and prompt for confirmation.
- Type `yes` and press Enter.
- Terraform will create the EC2 instance. Once complete, it will output the public IP of the instance.

#### 4.6 Verify in AWS Console
- Log in to the AWS Management Console.
- Go to **EC2 > Instances**.
- You should see a new instance named `terraform-example-instance`.

#### 4.7 Clean Up
When you’re done, destroy the resources to avoid incurring charges:
```bash
terraform destroy
```
- Confirm with `yes`.
- Terraform will delete the EC2 instance.

---

### Step 5: Expand the Project (Optional Enhancements)
To make the project more useful, let’s add a security group to allow SSH access to the EC2 instance and make the configuration more reusable with variables.

1. **Update `main.tf`**:
   Replace the contents of `main.tf` with this enhanced version:
   ```hcl
   provider "aws" {
     region = "us-east-1"
   }

   # Define variables
   variable "instance_type" {
     default = "t2.micro"
   }

   variable "ami" {
     default = "ami-0c55b159cbfafe1f0"  # Amazon Linux 2 in us-east-1
   }

   # Create a security group to allow SSH
   resource "aws_security_group" "allow_ssh" {
     name        = "allow_ssh"
     description = "Allow SSH inbound traffic"

     ingress {
       from_port   = 22
       to_port     = 22
       protocol    = "tcp"
       cidr_blocks = ["0.0.0.0/0"]  # Allow from anywhere (for learning; restrict in production)
     }

     egress {
       from_port   = 0
       to_port     = 0
       protocol    = "-1"
       cidr_blocks = ["0.0.0.0/0"]
     }
   }

   # Create an EC2 instance
   resource "aws_instance" "example" {
     ami           = var.ami
     instance_type = var.instance_type
     vpc_security_group_ids = [aws_security_group.allow_ssh.id]

     tags = {
       Name = "terraform-example-instance"
     }
   }

   # Output the public IP
   output "instance_public_ip" {
     value = aws_instance.example.public_ip
   }
   ```

2. **Reinitialize (if needed)**:
   If new provider features are used, reinitialize:
   ```bash
   terraform init
   ```

3. **Apply the Changes**:
   ```bash
   terraform plan
   terraform apply
   ```
   This will create an EC2 instance with a security group allowing SSH access.

4. **SSH into the Instance**:
   - Use the public IP output by Terraform.
   - SSH using the default user for Amazon Linux (`ec2-user`):
     ```bash
     ssh -i <your-private-key.pem> ec2-user@<instance_public_ip>
     ```
   - Note: You’ll need to create or use an existing key pair and associate it with the EC2 instance by adding a `key_name` attribute to the `aws_instance` resource.

5. **Destroy When Done**:
   ```bash
   terraform destroy
   ```

---

### Step 6: Best Practices for Learning Terraform
1. **Organize Your Code**:
   - Split your configuration into multiple files (e.g., `variables.tf`, `outputs.tf`, `main.tf`).
   - Use modules for reusable components (e.g., a module for EC2 instances).

2. **Use Remote State**:
   - For real projects, store your state file remotely to enable collaboration and prevent data loss. Example with S3:
     ```hcl
     terraform {
       backend "s3" {
         bucket = "my-terraform-state-bucket"
         key    = "state/terraform.tfstate"
         region = "us-east-1"
       }
     }
     ```
   - You’ll need to create the S3 bucket first and configure it for state storage.

3. **Version Control**:
   - Store your Terraform code in a Git repository (e.g., GitHub) to track changes.

4. **Secure Credentials**:
   - Avoid hardcoding AWS credentials. Use the AWS CLI configuration or environment variables:
     ```bash
     export AWS_ACCESS_KEY_ID="your_access_key"
     export AWS_SECRET_ACCESS_KEY="your_secret_key"
     export AWS_DEFAULT_REGION="us-east-1"
     ```

---

### Step 7: Next Steps for Learning
- **Explore More Resources**:
  - Create an S3 bucket, VPC, or RDS database with Terraform.
  - Example for an S3 bucket:
    ```hcl
    resource "aws_s3_bucket" "example" {
      bucket = "my-unique-bucket-name-123"
      acl    = "private"
    }
    ```

- **Learn Modules**:
  - Use the Terraform Registry to find pre-built modules (e.g., for VPCs): [registry.terraform.io](https://registry.terraform.io).

- **Integrate with Your Project**:
  - Use Terraform to provision an EC2 instance or ECS cluster to run your Dockerized Nginx and task manager services.
  - Example: Deploy your `docker-compose.yml` to an EC2 instance and use Terraform to manage the instance.

- **Follow Tutorials**:
  - HashiCorp Learn: [learn.hashicorp.com](https://learn.hashicorp.com/terraform)
  - AWS Terraform Guides: Search for “Terraform AWS tutorials” for hands-on labs.

---

### Troubleshooting
- **Terraform Init Fails**:
  - Ensure you have internet access in WSL.
  - Check for typos in `main.tf`.
- **AWS Authentication Errors**:
  - Verify your credentials with `aws s3 ls`.
  - Ensure your IAM user has permissions (e.g., `AmazonEC2FullAccess` for this project).
- **EC2 Instance Not Accessible**:
  - Check the security group rules.
  - Ensure the instance is in a public subnet with an internet gateway.

---

By following this guide, we’ve installed Terraform on WSL, configured it to work with AWS, learned basic commands, and deployed a simple EC2 instance.

---

Here We will convert a Cloudformation template to Terraform template:

Converting a CloudFormation template to Terraform involves translating the declarative syntax from JSON/YAML (CloudFormation) to HashiCorp Configuration Language (HCL) used by Terraform. 

The provided CloudFormation template sets up a Jenkins Master-Slave architecture with a VPC, subnets, security groups, IAM roles, and EC2 instances. Below is the equivalent Terraform template, with explanations for key differences and adaptations.

---

### Terraform Template

Create a file named `main.tf` and add the following content:

```hcl
# Define provider configuration
provider "aws" {
  region = "us-east-1" # Adjust region as needed
}

# Define input variables
variable "key_name" {
  description = "Name of the EC2 key pair"
  type        = string
}

variable "instance_type" {
  description = "Instance type for EC2 instances"
  type        = string
  default     = "t3.medium"
}

variable "jenkins_secret_id" {
  description = "Secrets Manager secret ID for SSH key"
  type        = string
  default     = "github-ssh-key"
}

# VPC
resource "aws_vpc" "jenkins_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name = "JenkinsVPC"
  }
}

# Public Subnet
resource "aws_subnet" "public_subnet" {
  vpc_id                  = aws_vpc.jenkins_vpc.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true

  tags = {
    Name = "PublicSubnet"
  }
}

# Private Subnet
resource "aws_subnet" "private_subnet" {
  vpc_id     = aws_vpc.jenkins_vpc.id
  cidr_block = "10.0.2.0/24"

  tags = {
    Name = "PrivateSubnet"
  }
}

# Internet Gateway
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.jenkins_vpc.id
}

# Attach Internet Gateway to VPC
resource "aws_internet_gateway_attachment" "gateway_attachment" {
  internet_gateway_id = aws_internet_gateway.igw.id
  vpc_id              = aws_vpc.jenkins_vpc.id
}

# Public Route Table
resource "aws_route_table" "public_route_table" {
  vpc_id = aws_vpc.jenkins_vpc.id
}

# Public Route
resource "aws_route" "public_route" {
  route_table_id         = aws_route_table.public_route_table.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.igw.id
}

# Associate Public Route Table with Public Subnet
resource "aws_route_table_association" "public_subnet_association" {
  subnet_id      = aws_subnet.public_subnet.id
  route_table_id = aws_route_table.public_route_table.id
}

# Elastic IP for NAT Gateway
resource "aws_eip" "nat_eip" {
  domain = "vpc"
}

# NAT Gateway
resource "aws_nat_gateway" "nat_gateway" {
  allocation_id = aws_eip.nat_eip.id
  subnet_id     = aws_subnet.public_subnet.id
}

# Private Route Table
resource "aws_route_table" "private_route_table" {
  vpc_id = aws_vpc.jenkins_vpc.id
}

# Private Route
resource "aws_route" "private_route" {
  route_table_id         = aws_route_table.private_route_table.id
  destination_cidr_block = "0.0.0.0/0"
  nat_gateway_id         = aws_nat_gateway.nat_gateway.id
}

# Associate Private Route Table with Private Subnet
resource "aws_route_table_association" "private_subnet_association" {
  subnet_id      = aws_subnet.private_subnet.id
  route_table_id = aws_route_table.private_route_table.id
}

# Security Group for Jenkins Master
resource "aws_security_group" "jenkins_master_sg" {
  name        = "JenkinsMasterSG"
  description = "Security group for Jenkins Master"
  vpc_id      = aws_vpc.jenkins_vpc.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Security Group for Jenkins Slave
resource "aws_security_group" "jenkins_slave_sg" {
  name        = "JenkinsSlaveSG"
  description = "Security group for Jenkins Slave"
  vpc_id      = aws_vpc.jenkins_vpc.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# IAM Role for Jenkins Instances
resource "aws_iam_role" "jenkins_role" {
  name = "JenkinsRole"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
}

# IAM Policy for Jenkins Role
resource "aws_iam_policy" "jenkins_policy" {
  name = "JenkinsPolicy"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "ecr:*",
          "secretsmanager:GetSecretValue"
        ]
        Resource = "*"
      }
    ]
  })
}

# Attach Policy to Role
resource "aws_iam_role_policy_attachment" "jenkins_policy_attachment" {
  role       = aws_iam_role.jenkins_role.name
  policy_arn = aws_iam_policy.jenkins_policy.arn
}

# IAM Instance Profile
resource "aws_iam_instance_profile" "jenkins_profile" {
  name = "JenkinsInstanceProfile"
  role = aws_iam_role.jenkins_role.name
}

# EBS Volume for Jenkins Master
resource "aws_ebs_volume" "jenkins_master_ebs" {
  availability_zone = aws_instance.jenkins_master.availability_zone
  size              = 20
  type              = "gp3"

  tags = {
    Name = "JenkinsMasterEBS"
  }
}

# EBS Volume Attachment for Jenkins Master
resource "aws_volume_attachment" "jenkins_master_volume_attachment" {
  device_name = "/dev/xvdf"
  volume_id   = aws_ebs_volume.jenkins_master_ebs.id
  instance_id = aws_instance.jenkins_master.id
}

# Jenkins Master EC2 Instance
resource "aws_instance" "jenkins_master" {
  ami                    = "ami-08b5b3a93ed654d19" # Amazon Linux 2 in us-east-1
  instance_type          = var.instance_type
  key_name               = var.key_name
  subnet_id              = aws_subnet.private_subnet.id
  vpc_security_group_ids = [aws_security_group.jenkins_master_sg.id]
  iam_instance_profile   = aws_iam_instance_profile.jenkins_profile.name

  user_data = base64encode(templatefile("user-data-master.tftpl", {
    jenkins_secret_id = var.jenkins_secret_id
  }))

  tags = {
    Name = "JenkinsMaster"
  }
}

# Jenkins Slave EC2 Instance
resource "aws_instance" "jenkins_slave" {
  ami                    = "ami-08b5b3a93ed654d19" # Amazon Linux 2 in us-east-1
  instance_type          = var.instance_type
  key_name               = var.key_name
  subnet_id              = aws_subnet.public_subnet.id
  vpc_security_group_ids = [aws_security_group.jenkins_slave_sg.id]
  iam_instance_profile   = aws_iam_instance_profile.jenkins_profile.name

  user_data = base64encode(templatefile("user-data-slave.tftpl", {
    master_private_ip = aws_instance.jenkins_master.private_ip
  }))

  tags = {
    Name = "JenkinsSlave"
  }
}

# Output values
output "master_public_ip" {
  description = "Public IP of Jenkins Master"
  value       = aws_instance.jenkins_master.public_ip
}

output "slave_public_ip" {
  description = "Public IP of Jenkins Slave"
  value       = aws_instance.jenkins_slave.public_ip
}

output "jenkins_url" {
  description = "Jenkins URL"
  value       = "http://${aws_instance.jenkins_master.public_ip}:8080"
}
```

---

### Additional Files

#### `user-data-master.tftpl`
Create a separate file named `user-data-master.tftpl` for the Jenkins Master user data script:
```hcl
#!/bin/bash
yum update -y
sudo dnf install java-17-amazon-corretto -y
yum install -y awscli git
wget -O /etc/yum.repos.d/jenkins.repo https://pkg.jenkins.io/redhat-stable/jenkins.repo
rpm --import https://pkg.jenkins.io/redhat-stable/jenkins.io.key
yum install -y jenkins
systemctl start jenkins
systemctl enable jenkins
mkfs.ext4 /dev/xvdf
mkdir -p /var/lib/jenkins
mount /dev/xvdf /var/lib/jenkins
chown jenkins:jenkins /var/lib/jenkins
mkdir -p /var/lib/jenkins/.ssh
aws secretsmanager get-secret-value --secret-id ${jenkins_secret_id} --region us-east-1 --query SecretString --output text > /var/lib/jenkins/.ssh/id_rsa
chmod 600 /var/lib/jenkins/.ssh/id_rsa
ssh-keyscan -H github.com >> /var/lib/jenkins/.ssh/known_hosts
chown -R jenkins:jenkins /var/lib/jenkins/.ssh
systemctl restart jenkins
```

#### `user-data-slave.tftpl`
Create a file named `user-data-slave.tftpl` for the Jenkins Slave user data script:
```hcl
#!/bin/bash
yum update -y
sudo dnf install java-17-amazon-corretto docker -y
systemctl start docker
systemctl enable docker
usermod -aG docker ec2-user
mkdir -p /home/ec2-user/jenkins
cd /home/ec2-user/jenkins
curl -O http://${master_private_ip}:8080/jnlpJars/agent.jar
java -jar agent.jar -jnlpUrl http://${master_private_ip}:8080/computer/slave1/jenkins-agent.jnlp -secret REPLACE_WITH_SECRET -workDir /home/ec2-user/jenkins
```

---

### Key Differences and Adaptations

1. **Provider Configuration**:
   - CloudFormation doesn’t require a provider block, but Terraform does. The `aws` provider is explicitly defined with a region.

2. **Variables**:
   - CloudFormation uses `Parameters`, while Terraform uses `variable` blocks. The variables are defined with defaults and descriptions for clarity.

3. **Resource Naming**:
   - Terraform requires unique resource names (e.g., `aws_vpc.jenkins_vpc` instead of just `VPC`). These names are used to reference resources within the configuration.

4. **User Data**:
   - CloudFormation uses `Fn::Base64` and `!Sub` for user data scripts. Terraform uses `base64encode` and `templatefile` to handle dynamic scripting. Separate `.tftpl` files are used to manage user data scripts, with variables injected during rendering.

5. **IAM Policy**:
   - In CloudFormation, the IAM policy is embedded in the `JenkinsRole` resource. In Terraform, it’s split into a separate `aws_iam_policy` resource and attached via `aws_iam_role_policy_attachment` for better modularity.

6. **Dependencies**:
   - Terraform automatically handles dependencies based on resource references (e.g., `aws_instance.jenkins_master.availability_zone` for the EBS volume). CloudFormation uses `!Ref` and `!GetAtt`, which are implicit in Terraform’s dependency graph.

7. **Outputs**:
   - CloudFormation uses `Outputs`, while Terraform uses `output` blocks. The structure is similar, providing values like public IPs and URLs.

8. **Security Group Egress**:
   - Terraform requires an explicit `egress` block for security groups, while CloudFormation implies open egress by default. An egress rule is added to allow all traffic out.

---

### Steps to Use the Terraform Template

1. **Initialize the Project**:
   ```bash
   terraform init
   ```
   This downloads the AWS provider.

2. **Set Variables**:
   - Provide the `key_name` variable when applying (e.g., via a `terraform.tfvars` file or command-line variables). Create a `terraform.tfvars` file:
     ```hcl
     key_name = "your-key-pair-name"
     ```
   - Or pass it during `apply`: `-var 'key_name=your-key-pair-name'`.

3. **Plan the Deployment**:
   ```bash
   terraform plan -var 'key_name=your-key-pair-name'
   ```

4. **Apply the Configuration**:
   ```bash
   terraform apply -var 'key_name=your-key-pair-name'
   ```
   Confirm with `yes`.

5. **Verify**:
   - Check the AWS Console for the VPC, subnets, security groups, and EC2 instances.
   - Access the Jenkins Master at the outputted `jenkins_url`.

6. **Clean Up**:
   ```bash
   terraform destroy -var 'key_name=your-key-pair-name'
   ```

---

### Notes and Considerations
- **AMI ID**: The AMI (`ami-08b5b3a93ed654d19`) is region-specific (us-east-1). Adjust it for other regions using the AWS EC2 console.
- **Secret Management**: The Jenkins secret (`github-ssh-key`) is retrieved from AWS Secrets Manager. Ensure the secret exists and contains the SSH key.
- **Security**: The security group allows inbound traffic from `0.0.0.0/0` for ports 22 and 8080. For production, restrict `cidr_blocks` to specific IPs.
- **Slave Agent Secret**: The `REPLACE_WITH_SECRET` placeholder in the slave user data requires a real secret from the Jenkins Master. You’ll need to retrieve this manually or automate it (e.g., via a post-deployment script).
- **EBS Attachment**: The EBS volume is attached to `/dev/xvdf`. Ensure this device is available and not in use by the AMI.

---

