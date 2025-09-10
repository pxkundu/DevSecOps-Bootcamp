# Pulumi - Modern Infrastructure as Code

## 🚀 Overview
Pulumi is a modern Infrastructure as Code platform that allows you to use familiar programming languages to define and deploy cloud infrastructure. This section provides practical guides for using Pulumi in DevSecOps workflows.

## 📁 Directory Structure

```
pulumi/
├── README.md
├── projects/
│   ├── aws-typescript/
│   ├── aws-python/
│   ├── azure-typescript/
│   └── gcp-python/
├── shared/
│   ├── components/
│   ├── libraries/
│   └── utilities/
└── scripts/
    ├── deploy.sh
    ├── destroy.sh
    └── preview.sh
```

## 🛠️ Essential Pulumi Projects

### 1. AWS TypeScript Project
```typescript
// projects/aws-typescript/index.ts
import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";

// Configuration
const config = new pulumi.Config();
const environment = config.get("environment") || "dev";
const vpcCidr = config.get("vpcCidr") || "10.0.0.0/16";

// VPC
const vpc = new aws.ec2.Vpc("main-vpc", {
    cidrBlock: vpcCidr,
    enableDnsHostnames: true,
    enableDnsSupport: true,
    tags: {
        Name: `${environment}-vpc`,
        Environment: environment,
    },
});

// Internet Gateway
const internetGateway = new aws.ec2.InternetGateway("main-igw", {
    vpcId: vpc.id,
    tags: {
        Name: `${environment}-igw`,
        Environment: environment,
    },
});

// Public Subnets
const publicSubnet1 = new aws.ec2.Subnet("public-subnet-1", {
    vpcId: vpc.id,
    cidrBlock: "10.0.1.0/24",
    availabilityZone: "us-west-2a",
    mapPublicIpOnLaunch: true,
    tags: {
        Name: `${environment}-public-subnet-1`,
        Environment: environment,
    },
});

const publicSubnet2 = new aws.ec2.Subnet("public-subnet-2", {
    vpcId: vpc.id,
    cidrBlock: "10.0.2.0/24",
    availabilityZone: "us-west-2b",
    mapPublicIpOnLaunch: true,
    tags: {
        Name: `${environment}-public-subnet-2`,
        Environment: environment,
    },
});

// Private Subnets
const privateSubnet1 = new aws.ec2.Subnet("private-subnet-1", {
    vpcId: vpc.id,
    cidrBlock: "10.0.11.0/24",
    availabilityZone: "us-west-2a",
    tags: {
        Name: `${environment}-private-subnet-1`,
        Environment: environment,
    },
});

const privateSubnet2 = new aws.ec2.Subnet("private-subnet-2", {
    vpcId: vpc.id,
    cidrBlock: "10.0.12.0/24",
    availabilityZone: "us-west-2b",
    tags: {
        Name: `${environment}-private-subnet-2`,
        Environment: environment,
    },
});

// Route Table for Public Subnets
const publicRouteTable = new aws.ec2.RouteTable("public-rt", {
    vpcId: vpc.id,
    tags: {
        Name: `${environment}-public-rt`,
        Environment: environment,
    },
});

// Default route for public subnets
const publicRoute = new aws.ec2.Route("public-route", {
    routeTableId: publicRouteTable.id,
    destinationCidrBlock: "0.0.0.0/0",
    gatewayId: internetGateway.id,
});

// Associate public subnets with route table
const publicSubnet1Association = new aws.ec2.RouteTableAssociation("public-subnet-1-association", {
    subnetId: publicSubnet1.id,
    routeTableId: publicRouteTable.id,
});

const publicSubnet2Association = new aws.ec2.RouteTableAssociation("public-subnet-2-association", {
    subnetId: publicSubnet2.id,
    routeTableId: publicRouteTable.id,
});

// Security Groups
const webSecurityGroup = new aws.ec2.SecurityGroup("web-sg", {
    name: `${environment}-web-sg`,
    description: "Security group for web servers",
    vpcId: vpc.id,
    ingress: [
        {
            protocol: "tcp",
            fromPort: 80,
            toPort: 80,
            cidrBlocks: ["0.0.0.0/0"],
            description: "HTTP access",
        },
        {
            protocol: "tcp",
            fromPort: 443,
            toPort: 443,
            cidrBlocks: ["0.0.0.0/0"],
            description: "HTTPS access",
        },
        {
            protocol: "tcp",
            fromPort: 22,
            toPort: 22,
            cidrBlocks: [vpcCidr],
            description: "SSH access from VPC",
        },
    ],
    egress: [
        {
            protocol: "-1",
            fromPort: 0,
            toPort: 0,
            cidrBlocks: ["0.0.0.0/0"],
            description: "All outbound traffic",
        },
    ],
    tags: {
        Name: `${environment}-web-sg`,
        Environment: environment,
    },
});

// EKS Cluster
const eksClusterRole = new aws.iam.Role("eks-cluster-role", {
    assumeRolePolicy: JSON.stringify({
        Version: "2012-10-17",
        Statement: [
            {
                Action: "sts:AssumeRole",
                Effect: "Allow",
                Principal: {
                    Service: "eks.amazonaws.com",
                },
            },
        ],
    }),
    managedPolicyArns: ["arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"],
});

const eksNodeGroupRole = new aws.iam.Role("eks-nodegroup-role", {
    assumeRolePolicy: JSON.stringify({
        Version: "2012-10-17",
        Statement: [
            {
                Action: "sts:AssumeRole",
                Effect: "Allow",
                Principal: {
                    Service: "ec2.amazonaws.com",
                },
            },
        ],
    }),
    managedPolicyArns: [
        "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy",
        "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy",
        "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly",
    ],
});

const eksCluster = new aws.eks.Cluster("eks-cluster", {
    name: `${environment}-eks-cluster`,
    roleArn: eksClusterRole.arn,
    version: "1.27",
    vpcConfig: {
        subnetIds: [publicSubnet1.id, publicSubnet2.id, privateSubnet1.id, privateSubnet2.id],
        securityGroupIds: [webSecurityGroup.id],
        endpointConfig: {
            publicAccess: true,
            privateAccess: true,
        },
    },
    tags: {
        Name: `${environment}-eks-cluster`,
        Environment: environment,
    },
});

const eksNodeGroup = new aws.eks.NodeGroup("eks-nodegroup", {
    clusterName: eksCluster.name,
    nodeRoleArn: eksNodeGroupRole.arn,
    subnetIds: [privateSubnet1.id, privateSubnet2.id],
    instanceTypes: ["t3.medium"],
    scalingConfig: {
        desiredSize: 2,
        maxSize: 10,
        minSize: 1,
    },
    updateConfig: {
        maxUnavailablePercentage: 25,
    },
    tags: {
        Environment: environment,
    },
});

// Outputs
export const vpcId = vpc.id;
export const vpcCidrBlock = vpc.cidrBlock;
export const publicSubnetIds = [publicSubnet1.id, publicSubnet2.id];
export const privateSubnetIds = [privateSubnet1.id, privateSubnet2.id];
export const eksClusterName = eksCluster.name;
export const eksClusterEndpoint = eksCluster.endpoint;
export const eksClusterArn = eksCluster.arn;
```

### 2. AWS Python Project
```python
# projects/aws-python/__main__.py
import pulumi
import pulumi_aws as aws

# Configuration
config = pulumi.Config()
environment = config.get("environment") or "dev"
vpc_cidr = config.get("vpcCidr") or "10.0.0.0/16"

# VPC
vpc = aws.ec2.Vpc("main-vpc",
    cidr_block=vpc_cidr,
    enable_dns_hostnames=True,
    enable_dns_support=True,
    tags={
        "Name": f"{environment}-vpc",
        "Environment": environment,
    }
)

# Internet Gateway
internet_gateway = aws.ec2.InternetGateway("main-igw",
    vpc_id=vpc.id,
    tags={
        "Name": f"{environment}-igw",
        "Environment": environment,
    }
)

# Public Subnets
public_subnet_1 = aws.ec2.Subnet("public-subnet-1",
    vpc_id=vpc.id,
    cidr_block="10.0.1.0/24",
    availability_zone="us-west-2a",
    map_public_ip_on_launch=True,
    tags={
        "Name": f"{environment}-public-subnet-1",
        "Environment": environment,
    }
)

public_subnet_2 = aws.ec2.Subnet("public-subnet-2",
    vpc_id=vpc.id,
    cidr_block="10.0.2.0/24",
    availability_zone="us-west-2b",
    map_public_ip_on_launch=True,
    tags={
        "Name": f"{environment}-public-subnet-2",
        "Environment": environment,
    }
)

# Private Subnets
private_subnet_1 = aws.ec2.Subnet("private-subnet-1",
    vpc_id=vpc.id,
    cidr_block="10.0.11.0/24",
    availability_zone="us-west-2a",
    tags={
        "Name": f"{environment}-private-subnet-1",
        "Environment": environment,
    }
)

private_subnet_2 = aws.ec2.Subnet("private-subnet-2",
    vpc_id=vpc.id,
    cidr_block="10.0.12.0/24",
    availability_zone="us-west-2b",
    tags={
        "Name": f"{environment}-private-subnet-2",
        "Environment": environment,
    }
)

# Route Table for Public Subnets
public_route_table = aws.ec2.RouteTable("public-rt",
    vpc_id=vpc.id,
    tags={
        "Name": f"{environment}-public-rt",
        "Environment": environment,
    }
)

# Default route for public subnets
public_route = aws.ec2.Route("public-route",
    route_table_id=public_route_table.id,
    destination_cidr_block="0.0.0.0/0",
    gateway_id=internet_gateway.id
)

# Associate public subnets with route table
public_subnet_1_association = aws.ec2.RouteTableAssociation("public-subnet-1-association",
    subnet_id=public_subnet_1.id,
    route_table_id=public_route_table.id
)

public_subnet_2_association = aws.ec2.RouteTableAssociation("public-subnet-2-association",
    subnet_id=public_subnet_2.id,
    route_table_id=public_route_table.id
)

# Security Groups
web_security_group = aws.ec2.SecurityGroup("web-sg",
    name=f"{environment}-web-sg",
    description="Security group for web servers",
    vpc_id=vpc.id,
    ingress=[
        aws.ec2.SecurityGroupIngressArgs(
            protocol="tcp",
            from_port=80,
            to_port=80,
            cidr_blocks=["0.0.0.0/0"],
            description="HTTP access",
        ),
        aws.ec2.SecurityGroupIngressArgs(
            protocol="tcp",
            from_port=443,
            to_port=443,
            cidr_blocks=["0.0.0.0/0"],
            description="HTTPS access",
        ),
        aws.ec2.SecurityGroupIngressArgs(
            protocol="tcp",
            from_port=22,
            to_port=22,
            cidr_blocks=[vpc_cidr],
            description="SSH access from VPC",
        ),
    ],
    egress=[
        aws.ec2.SecurityGroupEgressArgs(
            protocol="-1",
            from_port=0,
            to_port=0,
            cidr_blocks=["0.0.0.0/0"],
            description="All outbound traffic",
        ),
    ],
    tags={
        "Name": f"{environment}-web-sg",
        "Environment": environment,
    }
)

# EKS Cluster
eks_cluster_role = aws.iam.Role("eks-cluster-role",
    assume_role_policy="""{
        "Version": "2012-10-17",
        "Statement": [
            {
                "Action": "sts:AssumeRole",
                "Effect": "Allow",
                "Principal": {
                    "Service": "eks.amazonaws.com"
                }
            }
        ]
    }""",
    managed_policy_arns=["arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"]
)

eks_nodegroup_role = aws.iam.Role("eks-nodegroup-role",
    assume_role_policy="""{
        "Version": "2012-10-17",
        "Statement": [
            {
                "Action": "sts:AssumeRole",
                "Effect": "Allow",
                "Principal": {
                    "Service": "ec2.amazonaws.com"
                }
            }
        ]
    }""",
    managed_policy_arns=[
        "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy",
        "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy",
        "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly",
    ]
)

eks_cluster = aws.eks.Cluster("eks-cluster",
    name=f"{environment}-eks-cluster",
    role_arn=eks_cluster_role.arn,
    version="1.27",
    vpc_config=aws.eks.ClusterVpcConfigArgs(
        subnet_ids=[public_subnet_1.id, public_subnet_2.id, private_subnet_1.id, private_subnet_2.id],
        security_group_ids=[web_security_group.id],
        endpoint_config=aws.eks.ClusterVpcConfigEndpointConfigArgs(
            public_access=True,
            private_access=True,
        ),
    ),
    tags={
        "Name": f"{environment}-eks-cluster",
        "Environment": environment,
    }
)

eks_nodegroup = aws.eks.NodeGroup("eks-nodegroup",
    cluster_name=eks_cluster.name,
    node_role_arn=eks_nodegroup_role.arn,
    subnet_ids=[private_subnet_1.id, private_subnet_2.id],
    instance_types=["t3.medium"],
    scaling_config=aws.eks.NodeGroupScalingConfigArgs(
        desired_size=2,
        max_size=10,
        min_size=1,
    ),
    update_config=aws.eks.NodeGroupUpdateConfigArgs(
        max_unavailable_percentage=25,
    ),
    tags={
        "Environment": environment,
    }
)

# Outputs
pulumi.export("vpc_id", vpc.id)
pulumi.export("vpc_cidr_block", vpc.cidr_block)
pulumi.export("public_subnet_ids", [public_subnet_1.id, public_subnet_2.id])
pulumi.export("private_subnet_ids", [private_subnet_1.id, private_subnet_2.id])
pulumi.export("eks_cluster_name", eks_cluster.name)
pulumi.export("eks_cluster_endpoint", eks_cluster.endpoint)
pulumi.export("eks_cluster_arn", eks_cluster.arn)
```

### 3. Azure TypeScript Project
```typescript
// projects/azure-typescript/index.ts
import * as pulumi from "@pulumi/pulumi";
import * as azure from "@pulumi/azure";

// Configuration
const config = new pulumi.Config();
const environment = config.get("environment") || "dev";
const location = config.get("location") || "West US 2";

// Resource Group
const resourceGroup = new azure.core.ResourceGroup("main-rg", {
    name: `${environment}-rg`,
    location: location,
    tags: {
        Environment: environment,
    },
});

// Virtual Network
const virtualNetwork = new azure.network.VirtualNetwork("main-vnet", {
    name: `${environment}-vnet`,
    resourceGroupName: resourceGroup.name,
    location: resourceGroup.location,
    addressSpaces: ["10.0.0.0/16"],
    tags: {
        Environment: environment,
    },
});

// Subnets
const publicSubnet = new azure.network.Subnet("public-subnet", {
    name: "public-subnet",
    resourceGroupName: resourceGroup.name,
    virtualNetworkName: virtualNetwork.name,
    addressPrefixes: ["10.0.1.0/24"],
});

const privateSubnet = new azure.network.Subnet("private-subnet", {
    name: "private-subnet",
    resourceGroupName: resourceGroup.name,
    virtualNetworkName: virtualNetwork.name,
    addressPrefixes: ["10.0.2.0/24"],
});

// Network Security Group
const networkSecurityGroup = new azure.network.NetworkSecurityGroup("main-nsg", {
    name: `${environment}-nsg`,
    resourceGroupName: resourceGroup.name,
    location: resourceGroup.location,
    securityRules: [
        {
            name: "AllowHTTP",
            priority: 100,
            direction: "Inbound",
            access: "Allow",
            protocol: "Tcp",
            sourcePortRange: "*",
            destinationPortRange: "80",
            sourceAddressPrefix: "*",
            destinationAddressPrefix: "*",
        },
        {
            name: "AllowHTTPS",
            priority: 110,
            direction: "Inbound",
            access: "Allow",
            protocol: "Tcp",
            sourcePortRange: "*",
            destinationPortRange: "443",
            sourceAddressPrefix: "*",
            destinationAddressPrefix: "*",
        },
        {
            name: "AllowSSH",
            priority: 120,
            direction: "Inbound",
            access: "Allow",
            protocol: "Tcp",
            sourcePortRange: "*",
            destinationPortRange: "22",
            sourceAddressPrefix: "10.0.0.0/16",
            destinationAddressPrefix: "*",
        },
    ],
    tags: {
        Environment: environment,
    },
});

// Associate NSG with subnets
const publicSubnetNsgAssociation = new azure.network.SubnetNetworkSecurityGroupAssociation("public-subnet-nsg-association", {
    subnetId: publicSubnet.id,
    networkSecurityGroupId: networkSecurityGroup.id,
});

const privateSubnetNsgAssociation = new azure.network.SubnetNetworkSecurityGroupAssociation("private-subnet-nsg-association", {
    subnetId: privateSubnet.id,
    networkSecurityGroupId: networkSecurityGroup.id,
});

// AKS Cluster
const aksCluster = new azure.containerservice.KubernetesCluster("aks-cluster", {
    name: `${environment}-aks-cluster`,
    location: resourceGroup.location,
    resourceGroupName: resourceGroup.name,
    dnsPrefix: `${environment}-aks`,
    defaultNodePool: {
        name: "default",
        nodeCount: 2,
        vmSize: "Standard_D2s_v3",
        vnetSubnetId: privateSubnet.id,
    },
    identity: {
        type: "SystemAssigned",
    },
    networkProfile: {
        networkPlugin: "azure",
        serviceCidr: "10.1.0.0/16",
        dnsServiceIp: "10.1.0.10",
    },
    tags: {
        Environment: environment,
    },
});

// Outputs
export const resourceGroupName = resourceGroup.name;
export const virtualNetworkName = virtualNetwork.name;
export const publicSubnetId = publicSubnet.id;
export const privateSubnetId = privateSubnet.id;
export const aksClusterName = aksCluster.name;
export const aksClusterFqdn = aksCluster.fqdn;
export const aksClusterKubeConfig = aksCluster.kubeConfigRaw;
```

## 🚀 Deployment Scripts

### 1. Deploy Script
```bash
#!/bin/bash
# scripts/deploy.sh

set -e

# Configuration
PROJECT_DIR=$1
STACK_NAME=$2
ENVIRONMENT=${3:-dev}

if [ -z "$PROJECT_DIR" ] || [ -z "$STACK_NAME" ]; then
    echo "Usage: $0 <project-directory> <stack-name> [environment]"
    echo "Example: $0 projects/aws-typescript devsecops-stack dev"
    exit 1
fi

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Deploying Pulumi stack: $STACK_NAME${NC}"

# Change to project directory
cd "$PROJECT_DIR"

# Check if Pulumi is installed
if ! command -v pulumi &> /dev/null; then
    echo -e "${RED}Pulumi is not installed. Please install it first.${NC}"
    exit 1
fi

# Login to Pulumi (if not already logged in)
if ! pulumi whoami &> /dev/null; then
    echo "Please login to Pulumi:"
    pulumi login
fi

# Create or select stack
if pulumi stack ls | grep -q "$STACK_NAME"; then
    echo "Stack exists. Selecting..."
    pulumi stack select "$STACK_NAME"
else
    echo "Creating new stack..."
    pulumi stack init "$STACK_NAME"
fi

# Set configuration
pulumi config set environment "$ENVIRONMENT"

# Preview changes
echo "Previewing changes..."
pulumi preview

# Deploy
echo "Deploying..."
pulumi up --yes

if [ $? -eq 0 ]; then
    echo -e "${GREEN}Deployment completed successfully${NC}"
    
    # Display outputs
    echo "Stack outputs:"
    pulumi stack output
else
    echo -e "${RED}Deployment failed${NC}"
    exit 1
fi
```

### 2. Destroy Script
```bash
#!/bin/bash
# scripts/destroy.sh

set -e

# Configuration
PROJECT_DIR=$1
STACK_NAME=$2

if [ -z "$PROJECT_DIR" ] || [ -z "$STACK_NAME" ]; then
    echo "Usage: $0 <project-directory> <stack-name>"
    echo "Example: $0 projects/aws-typescript devsecops-stack"
    exit 1
fi

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Destroying Pulumi stack: $STACK_NAME${NC}"

# Change to project directory
cd "$PROJECT_DIR"

# Select stack
pulumi stack select "$STACK_NAME"

# Confirm destruction
read -p "Are you sure you want to destroy the stack? (yes/no): " confirm
if [ "$confirm" != "yes" ]; then
    echo "Destruction cancelled"
    exit 0
fi

# Destroy stack
echo "Destroying stack..."
pulumi destroy --yes

if [ $? -eq 0 ]; then
    echo -e "${GREEN}Stack destroyed successfully${NC}"
else
    echo -e "${RED}Stack destruction failed${NC}"
    exit 1
fi
```

### 3. Preview Script
```bash
#!/bin/bash
# scripts/preview.sh

set -e

# Configuration
PROJECT_DIR=$1
STACK_NAME=$2

if [ -z "$PROJECT_DIR" ] || [ -z "$STACK_NAME" ]; then
    echo "Usage: $0 <project-directory> <stack-name>"
    echo "Example: $0 projects/aws-typescript devsecops-stack"
    exit 1
fi

# Change to project directory
cd "$PROJECT_DIR"

# Select stack
pulumi stack select "$STACK_NAME"

# Preview changes
echo "Previewing changes..."
pulumi preview
```

## 📋 Best Practices

### 1. Project Organization
- Use separate projects for different environments
- Organize code into reusable components
- Use configuration for environment-specific values
- Implement proper error handling

### 2. Security Best Practices
- Use IAM roles and policies
- Implement least privilege access
- Encrypt sensitive data
- Use secure defaults
- Regular security audits

### 3. Cost Optimization
- Use appropriate resource types
- Implement auto-scaling
- Regular cleanup of unused resources
- Monitor costs
- Use spot instances where appropriate

### 4. Monitoring and Logging
- Enable CloudWatch/Application Insights
- Set up monitoring and alerting
- Implement centralized logging
- Use Pulumi's built-in monitoring

## 🧪 Hands-On Examples

### Example 1: Deploy AWS Infrastructure
```bash
# Deploy AWS TypeScript project
./scripts/deploy.sh projects/aws-typescript devsecops-aws dev

# Deploy AWS Python project
./scripts/deploy.sh projects/aws-python devsecops-aws-python dev
```

### Example 2: Deploy Azure Infrastructure
```bash
# Deploy Azure TypeScript project
./scripts/deploy.sh projects/azure-typescript devsecops-azure dev
```

### Example 3: Multi-Environment Deployment
```bash
# Deploy to different environments
./scripts/deploy.sh projects/aws-typescript devsecops-dev dev
./scripts/deploy.sh projects/aws-typescript devsecops-staging staging
./scripts/deploy.sh projects/aws-typescript devsecops-prod prod
```

## 📚 Learning Resources

### Official Documentation
- [Pulumi Documentation](https://www.pulumi.com/docs/)
- [Pulumi AWS Provider](https://www.pulumi.com/registry/packages/aws/)
- [Pulumi Azure Provider](https://www.pulumi.com/registry/packages/azure-native/)
- [Pulumi GCP Provider](https://www.pulumi.com/registry/packages/gcp/)

### Community Resources
- [Pulumi Examples](https://github.com/pulumi/examples)
- [Pulumi Community](https://www.pulumi.com/community/)
- [Stack Overflow Pulumi](https://stackoverflow.com/questions/tagged/pulumi)

---

**Ready to master Pulumi?** Start with the AWS TypeScript project and work your way up to complex multi-cloud deployments!
