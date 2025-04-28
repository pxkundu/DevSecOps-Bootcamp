#!/bin/bash

# deploy-istio-bookinfo-part1.sh
# Part 1: Sets up AWS Load Balancer Controller, Istio, and configures istio-ingressgateway as LoadBalancer
# Exits after initiating LoadBalancer creation to allow async provisioning

set -e
set -o pipefail

ERROR_LOG=""
WARNING_LOG=""
cleanup_triggered=false

cleanup() {
    if [ "$cleanup_triggered" = true ]; then
        return
    fi
    cleanup_triggered=true
    echo "ERROR or WARNING detected. Cleaning up resources..."
    echo "Uninstalling Istio..."
    istioctl uninstall --purge -y 2>/dev/null || true
    kubectl delete namespace istio-system --ignore-not-found=true 2>/dev/null || true
    echo "Removing sidecar injection label..."
    kubectl label namespace default istio-injection- --ignore-not-found=true 2>/dev/null || true
    rm -rf "$WORK_DIR" 2>/dev/null || true
    echo "Cleanup complete."
    echo "Summary:"
    echo "Errors: $ERROR_LOG"
    echo "Warnings: $WARNING_LOG"
    exit 1
}

exec 3>&1
exec 2> >(while read -r line; do
    if [[ "$line" =~ "error" || "$line" =~ "Error" ]]; then
        ERROR_LOG+="$line\n"
        cleanup
    elif [[ "$line" =~ "warning" || "$line" =~ "Warning" ]]; then
        WARNING_LOG+="$line\n"
        cleanup
    else
        echo "$line" >&3
    fi
done)

log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1"
}

log "Checking prerequisites..."
command -v kubectl >/dev/null 2>&1 || { log "kubectl is required"; ERROR_LOG="kubectl not found"; cleanup; }
command -v curl >/dev/null 2>&1 || { log "curl is required"; ERROR_LOG="curl not found"; cleanup; }
command -v jq >/dev/null 2>&1 || { log "jq is required"; ERROR_LOG="jq not found"; cleanup; }
command -v helm >/dev/null 2>&1 || { log "helm is required"; ERROR_LOG="helm not found"; cleanup; }
kubectl cluster-info >/dev/null 2>&1 || { log "kubectl cannot connect to cluster"; ERROR_LOG="kubectl cluster access failed"; cleanup; }

log "Checking Kubernetes version..."
K8S_VERSION=$(kubectl version -o json | jq -r '.serverVersion.gitVersion' | cut -d'+' -f1)
if [ -z "$K8S_VERSION" ]; then
    log "Failed to retrieve Kubernetes version"
    ERROR_LOG="kubectl version retrieval failed"
    cleanup
fi
log "Kubernetes version: $K8S_VERSION"
K8S_MAJOR=$(echo "$K8S_VERSION" | cut -d'.' -f1 | tr -d 'v')
K8S_MINOR=$(echo "$K8S_VERSION" | cut -d'.' -f2)

case "$K8S_MAJOR.$K8S_MINOR" in
    "1.28")
        ISTIO_VERSION="1.22.3"
        ;;
    "1.27")
        ISTIO_VERSION="1.21.3"
        ;;
    "1.29" | "1.30" | "1.31")
        ISTIO_VERSION="1.25.2"
        ;;
    *)
        log "Unsupported Kubernetes version: $K8S_VERSION"
        ERROR_LOG="Unsupported Kubernetes version: $K8S_VERSION"
        cleanup
        ;;
esac
log "Selected Istio version: $ISTIO_VERSION"

WORK_DIR="$HOME/istio-bookinfo"
ISTIO_DIR="$HOME/istio-$ISTIO_VERSION"
mkdir -p "$WORK_DIR" || { log "Failed to create $WORK_DIR"; ERROR_LOG="mkdir $WORK_DIR failed"; cleanup; }
cd "$WORK_DIR" || { log "Failed to cd to $WORK_DIR"; ERROR_LOG="cd $WORK_DIR failed"; cleanup; }

log "Setting up AWS Load Balancer Controller..."
# Check if controller is running
if ! kubectl get pods -n kube-system -l app.kubernetes.io/name=aws-load-balancer-controller | grep -q Running; then
    log "AWS Load Balancer Controller not found or not running. Installing..."
    # Add EKS chart repository
    helm repo add eks https://aws.github.io/eks-charts || { log "Failed to add EKS Helm repo"; ERROR_LOG="Helm repo add failed"; cleanup; }
    helm repo update || { log "Failed to update Helm repos"; ERROR_LOG="Helm repo update failed"; cleanup; }

    # Get cluster name (prompt user if needed)
    CLUSTER_NAME=$(kubectl config view -o jsonpath='{.clusters[0].name}' | sed 's/.*://')
    if [ -z "$CLUSTER_NAME" ]; then
        log "Could not detect EKS cluster name. Please provide it."
        read -p "Enter EKS cluster name: " CLUSTER_NAME
        if [ -z "$CLUSTER_NAME" ]; then
            log "Cluster name required"
            ERROR_LOG="Cluster name missing"
            cleanup
        fi
    fi

    # Install controller
    helm upgrade --install aws-load-balancer-controller eks/aws-load-balancer-controller \
        -n kube-system \
        --set clusterName="$CLUSTER_NAME" \
        --set serviceAccount.create=true \
        --set serviceAccount.name=aws-load-balancer-controller || { log "Failed to install AWS Load Balancer Controller"; ERROR_LOG="Controller install failed"; cleanup; }

    # Wait for controller pods to be ready
    log "Waiting for AWS Load Balancer Controller pods..."
    timeout 300 bash -c 'while ! kubectl get pods -n kube-system -l app.kubernetes.io/name=aws-load-balancer-controller | grep -q "1/1.*Running"; do sleep 5; done' || {
        log "AWS Load Balancer Controller pods not ready"
        ERROR_LOG="Controller pods not ready"
        cleanup
    }
else
    log "AWS Load Balancer Controller already running."
fi

log "Verifying IAM permissions..."
# Create or update IAM policy for the controller
IAM_POLICY_ARN=$(aws iam list-policies --query "Policies[?PolicyName=='AWSLoadBalancerControllerIAMPolicy'].Arn" --output text 2>/dev/null)
if [ -z "$IAM_POLICY_ARN" ]; then
    log "Creating IAM policy for AWS Load Balancer Controller..."
    POLICY_DOCUMENT=$(cat <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "iam:CreateServiceLinkedRole",
                "ec2:DescribeAccountAttributes",
                "ec2:DescribeAddresses",
                "ec2:DescribeAvailabilityZones",
                "ec2:DescribeInternetGateways",
                "ec2:DescribeVpcs",
                "ec2:DescribeSubnets",
                "ec2:DescribeSecurityGroups",
                "ec2:DescribeInstances",
                "ec2:DescribeNetworkInterfaces",
                "ec2:DescribeTags",
                "ec2:GetCoipPoolUsage",
                "ec2:DescribeCoipPools",
                "elasticloadbalancing:DescribeLoadBalancers",
                "elasticloadbalancing:DescribeLoadBalancerAttributes",
                "elasticloadbalancing:DescribeListeners",
                "elasticloadbalancing:DescribeListenerCertificates",
                "elasticloadbalancing:DescribeSSLPolicies",
                "elasticloadbalancing:DescribeRules",
                "elasticloadbalancing:DescribeTargetGroups",
                "elasticloadbalancing:DescribeTargetGroupAttributes",
                "elasticloadbalancing:DescribeTargetHealth",
                "elasticloadbalancing:DescribeTags"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "cognito-idp:DescribeUserPoolClient",
                "acm:ListCertificates",
                "acm:DescribeCertificate",
                "iam:ListServerCertificates",
                "iam:GetServerCertificate",
                "waf-regional:GetWebACL",
                "waf-regional:GetWebACLForResource",
                "waf-regional:AssociateWebACL",
                "waf-regional:DisassociateWebACL",
                "wafv2:GetWebACL",
                "wafv2:GetWebACLForResource",
                "wafv2:AssociateWebACL",
                "wafv2:DisassociateWebACL",
                "shield:GetSubscriptionState",
                "shield:DescribeProtection",
                "shield:CreateProtection",
                "shield:DeleteProtection"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "ec2:AuthorizeSecurityGroupIngress",
                "ec2:RevokeSecurityGroupIngress"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "ec2:CreateSecurityGroup"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "ec2:CreateTags"
            ],
            "Resource": "arn:aws:ec2:*:*:security-group/*",
            "Condition": {
                "StringEquals": {
                    "ec2:CreateAction": "CreateSecurityGroup"
                },
                "Null": {
                    "aws:RequestTag/elbv2.k8s.aws/cluster": "false",
                    "aws:RequestTag/ingress.k8s.aws/stack": "false",
                    "aws:RequestTag/ingress.k8s.aws/resource": "false"
                }
            }
        },
        {
            "Effect": "Allow",
            "Action": [
                "ec2:CreateTags",
                "ec2:DeleteTags"
            ],
            "Resource": "arn:aws:ec2:*:*:security-group/*",
            "Condition": {
                "Null": {
                    "aws:RequestTag/elbv2.k8s.aws/cluster": "true",
                    "aws:RequestTag/ingress.k8s.aws/stack": "true",
                    "aws:RequestTag/ingress.k8s.aws/resource": "true",
                    "aws:ResourceTag/elbv2.k8s.aws/cluster": "false",
                    "aws:ResourceTag/ingress.k8s.aws/stack": "false",
                    "aws:ResourceTag/ingress.k8s.aws/resource": "false"
                }
            }
        },
        {
            "Effect": "Allow",
            "Action": [
                "ec2:AuthorizeSecurityGroupIngress",
                "ec2:RevokeSecurityGroupIngress",
                "ec2:DeleteSecurityGroup"
            ],
            "Resource": "*",
            "Condition": {
                "Null": {
                    "aws:ResourceTag/elbv2.k8s.aws/cluster": "false",
                    "aws:ResourceTag/ingress.k8s.aws/stack": "false",
                    "aws:ResourceTag/ingress.k8s.aws/resource": "false"
                }
            }
        },
        {
            "Effect": "Allow",
            "Action": [
                "elasticloadbalancing:CreateLoadBalancer",
                "elasticloadbalancing:CreateTargetGroup"
            ],
            "Resource": "*",
            "Condition": {
                "Null": {
                    "aws:RequestTag/elbv2.k8s.aws/cluster": "false",
                    "aws:RequestTag/ingress.k8s.aws/stack": "false",
                    "aws:RequestTag/ingress.k8s.aws/resource": "false"
                }
            }
        },
        {
            "Effect": "Allow",
            "Action": [
                "elasticloadbalancing:CreateListener",
                "elasticloadbalancing:DeleteListener",
                "elasticloadbalancing:CreateRule",
                "elasticloadbalancing:DeleteRule"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "elasticloadbalancing:AddTags",
                "elasticloadbalancing:RemoveTags"
            ],
            "Resource": [
                "arn:aws:elasticloadbalancing:*:*:targetgroup/*",
                "arn:aws:elasticloadbalancing:*:*:loadbalancer/net/*",
                "arn:aws:elasticloadbalancing:*:*:loadbalancer/app/*"
            ],
            "Condition": {
                "Null": {
                    "aws:RequestTag/elbv2.k8s.aws/cluster": "true",
                    "aws:RequestTag/ingress.k8s.aws/stack": "true",
                    "aws:RequestTag/ingress.k8s.aws/resource": "true",
                    "aws:ResourceTag/elbv2.k8s.aws/cluster": "false",
                    "aws:ResourceTag/ingress.k8s.aws/stack": "false",
                    "aws:ResourceTag/ingress.k8s.aws/resource": "false"
                }
            }
        },
        {
            "Effect": "Allow",
            "Action": [
                "elasticloadbalancing:AddTags",
                "elasticloadbalancing:RemoveTags"
            ],
            "Resource": [
                "arn:aws:elasticloadbalancing:*:*:listener/net/*",
                "arn:aws:elasticloadbalancing:*:*:listener/app/*",
                "arn:aws:elasticloadbalancing:*:*:listener-rule/net/*",
                "arn:aws:elasticloadbalancing:*:*:listener-rule/app/*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "elasticloadbalancing:ModifyLoadBalancerAttributes",
                "elasticloadbalancing:SetIpAddressType",
                "elasticloadbalancing:SetSecurityGroups",
                "elasticloadbalancing:SetSubnets",
                "elasticloadbalancing:DeleteLoadBalancer",
                "elasticloadbalancing:ModifyTargetGroup",
                "elasticloadbalancing:ModifyTargetGroupAttributes",
                "elasticloadbalancing:DeleteTargetGroup"
            ],
            "Resource": "*",
            "Condition": {
                "Null": {
                    "aws:ResourceTag/elbv2.k8s.aws/cluster": "false",
                    "aws:ResourceTag/ingress.k8s.aws/stack": "false",
                    "aws:ResourceTag/ingress.k8s.aws/resource": "false"
                }
            }
        },
        {
            "Effect": "Allow",
            "Action": [
                "elasticloadbalancing:RegisterTargets",
                "elasticloadbalancing:DeregisterTargets"
            ],
            "Resource": "arn:aws:elasticloadbalancing:*:*:targetgroup/*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "elasticloadbalancing:SetWebAcl",
                "elasticloadbalancing:ModifyListener",
                "elasticloadbalancing:AddListenerCertificates",
                "elasticloadbalancing:RemoveListenerCertificates",
                "elasticloadbalancing:ModifyRule"
            ],
            "Resource": "*"
        }
    ]
}
EOF
    )
    IAM_POLICY_ARN=$(aws iam create-policy --policy-name AWSLoadBalancerControllerIAMPolicy --policy-document "$POLICY_DOCUMENT" --query 'Policy.Arn' --output text 2>/dev/null) || {
        log "Failed to create IAM policy"
        ERROR_LOG="IAM policy creation failed"
        cleanup
    }
fi

# Attach policy to service account (assumes IRSA or manual role attachment)
log "Ensure the aws-load-balancer-controller service account has the IAM policy $IAM_POLICY_ARN attached."
log "If using IRSA, update the service account annotation with the role ARN in the AWS console or via eksctl."
log "Manually verify IAM role attachment if not using IRSA."

log "Verifying subnet tags..."
# Check for public subnets with proper tags
SUBNETS=$(aws ec2 describe-subnets --filters "Name=tag:kubernetes.io/cluster/$CLUSTER_NAME,Values=shared" --query 'Subnets[].SubnetId' --output text)
if [ -z "$SUBNETS" ]; then
    log "No subnets tagged with kubernetes.io/cluster/$CLUSTER_NAME=shared found."
    log "Tag at least two public subnets with this key-value pair in the AWS console."
    ERROR_LOG="Missing subnet tags"
    cleanup
fi

log "Downloading Istio $ISTIO_VERSION..."
if [ ! -d "$ISTIO_DIR" ]; then
    curl -L "https://github.com/istio/istio/releases/download/$ISTIO_VERSION/istio-$ISTIO_VERSION-linux-amd64.tar.gz" | tar xz -C "$HOME" || { log "Failed to download Istio"; ERROR_LOG="Istio download failed"; cleanup; }
fi
cd "$ISTIO_DIR" || { log "Failed to cd to $ISTIO_DIR"; ERROR_LOG="cd $ISTIO_DIR failed"; cleanup; }
export PATH="$PWD/bin:$PATH"
command -v istioctl >/dev/null 2>&1 || { log "istioctl not found"; ERROR_LOG="istioctl not found"; cleanup; }

log "Installing Istio..."
istioctl install --set profile=demo -y || { log "Istio installation failed"; ERROR_LOG="Istio install failed"; cleanup; }

log "Verifying Istio pods..."
sleep 10
if ! kubectl get pods -n istio-system | grep -E "istiod|istio-ingressgateway|istio-egressgateway" | grep -q Running; then
    log "Istio pods not running"
    ERROR_LOG="Istio pods not running"
    cleanup
fi

log "Enabling sidecar injection..."
kubectl label namespace default istio-injection=enabled --overwrite || { log "Failed to label namespace"; ERROR_LOG="Namespace labeling failed"; cleanup; }

log "Configuring istio-ingressgateway as LoadBalancer..."
kubectl -n istio-system patch svc istio-ingressgateway -p '{
  "metadata": {
    "annotations": {
      "service.beta.kubernetes.io/aws-load-balancer-type": "external",
      "service.beta.kubernetes.io/aws-load-balancer-nlb-target-type": "ip",
      "service.beta.kubernetes.io/aws-load-balancer-scheme": "internet-facing"
    }
  }
}' || { log "Failed to patch istio-ingressgateway"; ERROR_LOG="Ingressgateway patch failed"; cleanup; }

log "Saving state for Part 2..."
echo "ISTIO_VERSION=$ISTIO_VERSION" > "$WORK_DIR/state.conf"
echo "WORK_DIR=$WORK_DIR" >> "$WORK_DIR/state.conf"
echo "ISTIO_DIR=$ISTIO_DIR" >> "$WORK_DIR/state.conf"
echo "CLUSTER_NAME=$CLUSTER_NAME" >> "$WORK_DIR/state.conf"

log "Part 1 complete! LoadBalancer creation initiated."
echo "Wait for the LoadBalancer DNS to be assigned. Check status with:"
echo "  kubectl -n istio-system get svc istio-ingressgateway -o jsonpath='{.status.loadBalancer.ingress[0].hostname}'"
echo "If status remains <pending>, check controller logs:"
echo "  kubectl logs -n kube-system -l app.kubernetes.io/name=aws-load-balancer-controller"
echo "Verify subnet tags and IAM permissions. Once DNS is available, run deploy-istio-bookinfo-part2.sh."

exit 0
