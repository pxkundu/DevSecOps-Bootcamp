# AWS CloudFormation - Infrastructure as Code

## 🏗️ Overview
AWS CloudFormation is a service that helps you model and set up AWS resources using infrastructure as code. This section provides practical guides for using CloudFormation in DevSecOps workflows.

## 📁 Directory Structure

```
cloudformation/
├── README.md
├── templates/
│   ├── basic-infrastructure/
│   ├── security-focused/
│   ├── multi-tier-apps/
│   └── serverless/
├── stacks/
│   ├── dev/
│   ├── staging/
│   └── production/
└── scripts/
    ├── deploy.sh
    ├── validate.sh
    └── cleanup.sh
```

## 🛠️ Essential CloudFormation Templates

### 1. Basic VPC Template
```yaml
# templates/basic-infrastructure/vpc.yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: 'Basic VPC with public and private subnets'

Parameters:
  Environment:
    Type: String
    Default: dev
    AllowedValues: [dev, staging, prod]
    Description: Environment name
  
  VpcCIDR:
    Type: String
    Default: 10.0.0.0/16
    Description: CIDR block for VPC

Resources:
  VPC:
    Type: AWS::EC2::VPC
    Properties:
      CidrBlock: !Ref VpcCIDR
      EnableDnsHostnames: true
      EnableDnsSupport: true
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-vpc'
        - Key: Environment
          Value: !Ref Environment

  InternetGateway:
    Type: AWS::EC2::InternetGateway
    Properties:
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-igw'

  InternetGatewayAttachment:
    Type: AWS::EC2::VPCGatewayAttachment
    Properties:
      InternetGatewayId: !Ref InternetGateway
      VpcId: !Ref VPC

  PublicSubnet1:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref VPC
      AvailabilityZone: !Select [0, !GetAZs '']
      CidrBlock: 10.0.1.0/24
      MapPublicIpOnLaunch: true
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-public-subnet-1'

  PublicSubnet2:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref VPC
      AvailabilityZone: !Select [1, !GetAZs '']
      CidrBlock: 10.0.2.0/24
      MapPublicIpOnLaunch: true
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-public-subnet-2'

  PrivateSubnet1:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref VPC
      AvailabilityZone: !Select [0, !GetAZs '']
      CidrBlock: 10.0.11.0/24
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-private-subnet-1'

  PrivateSubnet2:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref VPC
      AvailabilityZone: !Select [1, !GetAZs '']
      CidrBlock: 10.0.12.0/24
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-private-subnet-2'

  PublicRouteTable:
    Type: AWS::EC2::RouteTable
    Properties:
      VpcId: !Ref VPC
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-public-rt'

  DefaultPublicRoute:
    Type: AWS::EC2::Route
    DependsOn: InternetGatewayAttachment
    Properties:
      RouteTableId: !Ref PublicRouteTable
      DestinationCidrBlock: 0.0.0.0/0
      GatewayId: !Ref InternetGateway

  PublicSubnet1RouteTableAssociation:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
      RouteTableId: !Ref PublicRouteTable
      SubnetId: !Ref PublicSubnet1

  PublicSubnet2RouteTableAssociation:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
      RouteTableId: !Ref PublicRouteTable
      SubnetId: !Ref PublicSubnet2

Outputs:
  VPCId:
    Description: VPC ID
    Value: !Ref VPC
    Export:
      Name: !Sub '${Environment}-VPC-ID'

  PublicSubnet1:
    Description: Public Subnet 1
    Value: !Ref PublicSubnet1
    Export:
      Name: !Sub '${Environment}-PublicSubnet1'

  PublicSubnet2:
    Description: Public Subnet 2
    Value: !Ref PublicSubnet2
    Export:
      Name: !Sub '${Environment}-PublicSubnet2'

  PrivateSubnet1:
    Description: Private Subnet 1
    Value: !Ref PrivateSubnet1
    Export:
      Name: !Sub '${Environment}-PrivateSubnet1'

  PrivateSubnet2:
    Description: Private Subnet 2
    Value: !Ref PrivateSubnet2
    Export:
      Name: !Sub '${Environment}-PrivateSubnet2'
```

### 2. Security-Focused Template
```yaml
# templates/security-focused/security-groups.yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: 'Security groups for DevSecOps environment'

Parameters:
  Environment:
    Type: String
    Default: dev
    AllowedValues: [dev, staging, prod]

  VpcId:
    Type: AWS::EC2::VPC::Id
    Description: VPC ID

Resources:
  WebSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupName: !Sub '${Environment}-web-sg'
      GroupDescription: Security group for web servers
      VpcId: !Ref VpcId
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 80
          ToPort: 80
          CidrIp: 0.0.0.0/0
          Description: HTTP access
        - IpProtocol: tcp
          FromPort: 443
          ToPort: 443
          CidrIp: 0.0.0.0/0
          Description: HTTPS access
        - IpProtocol: tcp
          FromPort: 22
          ToPort: 22
          CidrIp: 10.0.0.0/16
          Description: SSH access from VPC
      SecurityGroupEgress:
        - IpProtocol: -1
          CidrIp: 0.0.0.0/0
          Description: All outbound traffic
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-web-sg'
        - Key: Environment
          Value: !Ref Environment

  DatabaseSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupName: !Sub '${Environment}-db-sg'
      GroupDescription: Security group for database
      VpcId: !Ref VpcId
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 3306
          ToPort: 3306
          SourceSecurityGroupId: !Ref WebSecurityGroup
          Description: MySQL access from web servers
        - IpProtocol: tcp
          FromPort: 5432
          ToPort: 5432
          SourceSecurityGroupId: !Ref WebSecurityGroup
          Description: PostgreSQL access from web servers
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-db-sg'
        - Key: Environment
          Value: !Ref Environment

  ALBSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupName: !Sub '${Environment}-alb-sg'
      GroupDescription: Security group for Application Load Balancer
      VpcId: !Ref VpcId
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 80
          ToPort: 80
          CidrIp: 0.0.0.0/0
          Description: HTTP access
        - IpProtocol: tcp
          FromPort: 443
          ToPort: 443
          CidrIp: 0.0.0.0/0
          Description: HTTPS access
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-alb-sg'
        - Key: Environment
          Value: !Ref Environment
```

### 3. EKS Cluster Template
```yaml
# templates/kubernetes/eks-cluster.yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: 'EKS cluster for DevSecOps'

Parameters:
  Environment:
    Type: String
    Default: dev
    AllowedValues: [dev, staging, prod]

  NodeInstanceType:
    Type: String
    Default: t3.medium
    AllowedValues: [t3.small, t3.medium, t3.large, t3.xlarge]

  NodeGroupDesiredCapacity:
    Type: Number
    Default: 2
    MinValue: 1
    MaxValue: 10

  VpcId:
    Type: AWS::EC2::VPC::Id

  SubnetIds:
    Type: List<AWS::EC2::Subnet::Id>
    Description: List of subnet IDs for the EKS cluster

Resources:
  EKSClusterRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: eks.amazonaws.com
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/AmazonEKSClusterPolicy

  EKSNodeGroupRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: ec2.amazonaws.com
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy
        - arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy
        - arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly

  EKSCluster:
    Type: AWS::EKS::Cluster
    Properties:
      Name: !Sub '${Environment}-eks-cluster'
      Version: '1.27'
      RoleArn: !GetAtt EKSClusterRole.Arn
      ResourcesVpcConfig:
        SecurityGroupIds:
          - !Ref EKSClusterSecurityGroup
        SubnetIds: !Ref SubnetIds
        EndpointConfig:
          PublicAccess: true
          PrivateAccess: true
      Logging:
        ClusterLogging:
          EnabledTypes:
            - api
            - audit
            - authenticator
            - controllerManager
            - scheduler

  EKSClusterSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: Security group for EKS cluster
      VpcId: !Ref VpcId
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 443
          ToPort: 443
          CidrIp: 0.0.0.0/0
          Description: HTTPS access to EKS API server
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-eks-cluster-sg'

  EKSNodeGroup:
    Type: AWS::EKS::Nodegroup
    Properties:
      ClusterName: !Ref EKSCluster
      NodeRole: !GetAtt EKSNodeGroupRole.Arn
      InstanceTypes:
        - !Ref NodeInstanceType
      ScalingConfig:
        DesiredSize: !Ref NodeGroupDesiredCapacity
        MaxSize: 10
        MinSize: 1
      Subnets: !Ref SubnetIds
      UpdateConfig:
        MaxUnavailablePercentage: 25
      Tags:
        Environment: !Ref Environment

Outputs:
  EKSClusterName:
    Description: EKS Cluster Name
    Value: !Ref EKSCluster
    Export:
      Name: !Sub '${Environment}-EKS-Cluster-Name'

  EKSClusterEndpoint:
    Description: EKS Cluster Endpoint
    Value: !GetAtt EKSCluster.Endpoint
    Export:
      Name: !Sub '${Environment}-EKS-Cluster-Endpoint'

  EKSClusterArn:
    Description: EKS Cluster ARN
    Value: !GetAtt EKSCluster.Arn
    Export:
      Name: !Sub '${Environment}-EKS-Cluster-ARN'
```

## 🚀 Deployment Scripts

### 1. Deploy Script
```bash
#!/bin/bash
# scripts/deploy.sh

set -e

# Configuration
STACK_NAME="devsecops-infrastructure"
TEMPLATE_FILE="templates/basic-infrastructure/vpc.yaml"
PARAMETERS_FILE="stacks/dev/parameters.json"
REGION="us-west-2"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Deploying CloudFormation stack: $STACK_NAME${NC}"

# Validate template
echo "Validating CloudFormation template..."
aws cloudformation validate-template \
    --template-body file://$TEMPLATE_FILE \
    --region $REGION

if [ $? -eq 0 ]; then
    echo -e "${GREEN}Template validation successful${NC}"
else
    echo -e "${RED}Template validation failed${NC}"
    exit 1
fi

# Check if stack exists
if aws cloudformation describe-stacks --stack-name $STACK_NAME --region $REGION >/dev/null 2>&1; then
    echo "Stack exists. Updating..."
    aws cloudformation update-stack \
        --stack-name $STACK_NAME \
        --template-body file://$TEMPLATE_FILE \
        --parameters file://$PARAMETERS_FILE \
        --capabilities CAPABILITY_IAM \
        --region $REGION
else
    echo "Stack does not exist. Creating..."
    aws cloudformation create-stack \
        --stack-name $STACK_NAME \
        --template-body file://$TEMPLATE_FILE \
        --parameters file://$PARAMETERS_FILE \
        --capabilities CAPABILITY_IAM \
        --region $REGION
fi

# Wait for stack operation to complete
echo "Waiting for stack operation to complete..."
aws cloudformation wait stack-update-complete \
    --stack-name $STACK_NAME \
    --region $REGION

if [ $? -eq 0 ]; then
    echo -e "${GREEN}Stack operation completed successfully${NC}"
    
    # Display outputs
    echo "Stack outputs:"
    aws cloudformation describe-stacks \
        --stack-name $STACK_NAME \
        --region $REGION \
        --query 'Stacks[0].Outputs'
else
    echo -e "${RED}Stack operation failed${NC}"
    exit 1
fi
```

### 2. Validation Script
```bash
#!/bin/bash
# scripts/validate.sh

set -e

TEMPLATE_FILE=$1
REGION=${2:-us-west-2}

if [ -z "$TEMPLATE_FILE" ]; then
    echo "Usage: $0 <template-file> [region]"
    echo "Example: $0 templates/basic-infrastructure/vpc.yaml us-west-2"
    exit 1
fi

echo "Validating CloudFormation template: $TEMPLATE_FILE"

# Validate template
aws cloudformation validate-template \
    --template-body file://$TEMPLATE_FILE \
    --region $REGION

if [ $? -eq 0 ]; then
    echo "✅ Template validation successful"
else
    echo "❌ Template validation failed"
    exit 1
fi

# Check for common issues
echo "Checking for common issues..."

# Check for hardcoded values
if grep -q "hardcoded" $TEMPLATE_FILE; then
    echo "⚠️  Warning: Found potential hardcoded values"
fi

# Check for missing parameters
if grep -q "Ref:" $TEMPLATE_FILE && ! grep -q "Parameters:" $TEMPLATE_FILE; then
    echo "⚠️  Warning: Template uses Ref but no Parameters section found"
fi

# Check for security groups without egress rules
if grep -q "AWS::EC2::SecurityGroup" $TEMPLATE_FILE; then
    if ! grep -q "SecurityGroupEgress" $TEMPLATE_FILE; then
        echo "⚠️  Warning: Security groups found without egress rules"
    fi
fi

echo "✅ Validation complete"
```

### 3. Cleanup Script
```bash
#!/bin/bash
# scripts/cleanup.sh

set -e

STACK_NAME=$1
REGION=${2:-us-west-2}

if [ -z "$STACK_NAME" ]; then
    echo "Usage: $0 <stack-name> [region]"
    echo "Example: $0 devsecops-infrastructure us-west-2"
    exit 1
fi

echo "Cleaning up CloudFormation stack: $STACK_NAME"

# Check if stack exists
if ! aws cloudformation describe-stacks --stack-name $STACK_NAME --region $REGION >/dev/null 2>&1; then
    echo "Stack does not exist: $STACK_NAME"
    exit 1
fi

# Delete stack
echo "Deleting stack..."
aws cloudformation delete-stack \
    --stack-name $STACK_NAME \
    --region $REGION

# Wait for deletion to complete
echo "Waiting for stack deletion to complete..."
aws cloudformation wait stack-delete-complete \
    --stack-name $STACK_NAME \
    --region $REGION

if [ $? -eq 0 ]; then
    echo "✅ Stack deleted successfully"
else
    echo "❌ Stack deletion failed"
    exit 1
fi
```

## 📋 Best Practices

### 1. Template Organization
- Use nested stacks for complex infrastructure
- Separate templates by environment (dev, staging, prod)
- Use parameters for environment-specific values
- Include comprehensive outputs for cross-stack references

### 2. Security Best Practices
- Use IAM roles instead of access keys
- Implement least privilege access
- Enable CloudTrail for audit logging
- Use security groups with minimal required access
- Encrypt sensitive data at rest and in transit

### 3. Cost Optimization
- Use appropriate instance types
- Implement auto-scaling
- Use spot instances for non-critical workloads
- Regular cleanup of unused resources
- Monitor costs with AWS Cost Explorer

### 4. Monitoring and Logging
- Enable CloudWatch logging
- Set up monitoring and alerting
- Use AWS Config for compliance monitoring
- Implement centralized logging

## 🧪 Hands-On Examples

### Example 1: Deploy a Web Application
```bash
# 1. Create VPC
./scripts/deploy.sh vpc-stack templates/basic-infrastructure/vpc.yaml

# 2. Create security groups
./scripts/deploy.sh security-stack templates/security-focused/security-groups.yaml

# 3. Deploy EKS cluster
./scripts/deploy.sh eks-stack templates/kubernetes/eks-cluster.yaml

# 4. Deploy application
kubectl apply -f k8s/manifests/
```

### Example 2: Environment-Specific Deployment
```bash
# Deploy to different environments
./scripts/deploy.sh dev-infrastructure templates/basic-infrastructure/vpc.yaml stacks/dev/
./scripts/deploy.sh staging-infrastructure templates/basic-infrastructure/vpc.yaml stacks/staging/
./scripts/deploy.sh prod-infrastructure templates/basic-infrastructure/vpc.yaml stacks/production/
```

## 📚 Learning Resources

### Official Documentation
- [AWS CloudFormation User Guide](https://docs.aws.amazon.com/cloudformation/)
- [CloudFormation Template Reference](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/)
- [CloudFormation Best Practices](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/best-practices.html)

### Community Resources
- [AWS CloudFormation Samples](https://github.com/awslabs/aws-cloudformation-templates)
- [CloudFormation Registry](https://aws.amazon.com/cloudformation/registry/)
- [Stack Overflow CloudFormation](https://stackoverflow.com/questions/tagged/aws-cloudformation)

---

**Ready to master AWS CloudFormation?** Start with the basic VPC template and work your way up to complex multi-tier applications!
