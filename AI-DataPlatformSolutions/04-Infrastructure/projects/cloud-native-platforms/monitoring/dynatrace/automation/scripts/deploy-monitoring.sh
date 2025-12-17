#!/bin/bash
# =============================================================================
# Dynatrace AWS Serverless Monitoring - Deployment Script
# =============================================================================

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# =============================================================================
# Configuration
# =============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

# Default values
ENVIRONMENT="${ENVIRONMENT:-production}"
AWS_REGION="${AWS_REGION:-us-east-1}"
DRY_RUN="${DRY_RUN:-false}"

# =============================================================================
# Functions
# =============================================================================

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_prerequisites() {
    log_info "Checking prerequisites..."
    
    # Check required tools
    local tools=("aws" "terraform" "curl" "jq")
    for tool in "${tools[@]}"; do
        if ! command -v "$tool" &> /dev/null; then
            log_error "$tool is required but not installed."
            exit 1
        fi
    done
    
    # Check environment variables
    local vars=("DT_TENANT_URL" "DT_API_TOKEN" "DT_PAAS_TOKEN")
    for var in "${vars[@]}"; do
        if [[ -z "${!var:-}" ]]; then
            log_error "Environment variable $var is not set."
            exit 1
        fi
    done
    
    # Test Dynatrace API connectivity
    log_info "Testing Dynatrace API connectivity..."
    local status
    status=$(curl -s -o /dev/null -w "%{http_code}" \
        "${DT_TENANT_URL}/api/v2/entities?pageSize=1" \
        -H "Authorization: Api-Token ${DT_API_TOKEN}")
    
    if [[ "$status" != "200" ]]; then
        log_error "Cannot connect to Dynatrace API. HTTP status: $status"
        exit 1
    fi
    
    log_success "Prerequisites check passed."
}

deploy_terraform() {
    log_info "Deploying Terraform infrastructure..."
    
    cd "${PROJECT_ROOT}/infrastructure/terraform"
    
    terraform init -upgrade
    
    if [[ "$DRY_RUN" == "true" ]]; then
        terraform plan \
            -var-file="environments/${ENVIRONMENT}/terraform.tfvars" \
            -var="dynatrace_tenant_url=${DT_TENANT_URL}" \
            -var="dynatrace_api_token=${DT_API_TOKEN}" \
            -var="dynatrace_paas_token=${DT_PAAS_TOKEN}"
    else
        terraform apply \
            -auto-approve \
            -var-file="environments/${ENVIRONMENT}/terraform.tfvars" \
            -var="dynatrace_tenant_url=${DT_TENANT_URL}" \
            -var="dynatrace_api_token=${DT_API_TOKEN}" \
            -var="dynatrace_paas_token=${DT_PAAS_TOKEN}"
    fi
    
    log_success "Terraform deployment completed."
}

deploy_dashboards() {
    log_info "Deploying Dynatrace dashboards..."
    
    for dashboard_file in "${PROJECT_ROOT}/dashboards"/*.json; do
        if [[ -f "$dashboard_file" ]]; then
            local dashboard_name
            dashboard_name=$(jq -r '.dashboardMetadata.name' "$dashboard_file")
            log_info "Deploying dashboard: $dashboard_name"
            
            if [[ "$DRY_RUN" == "true" ]]; then
                log_info "[DRY-RUN] Would deploy: $dashboard_file"
            else
                curl -s -X POST "${DT_TENANT_URL}/api/config/v1/dashboards" \
                    -H "Authorization: Api-Token ${DT_API_TOKEN}" \
                    -H "Content-Type: application/json" \
                    -d @"$dashboard_file" | jq .
            fi
        fi
    done
    
    log_success "Dashboard deployment completed."
}

deploy_alerting() {
    log_info "Deploying alerting configurations..."
    
    # Deploy alerting profiles
    if [[ -f "${PROJECT_ROOT}/configuration/dynatrace-api/alerting-profiles.json" ]]; then
        log_info "Deploying alerting profiles..."
        
        if [[ "$DRY_RUN" != "true" ]]; then
            local profiles
            profiles=$(jq -c '.alertingProfiles[]' "${PROJECT_ROOT}/configuration/dynatrace-api/alerting-profiles.json")
            
            while IFS= read -r profile; do
                curl -s -X POST "${DT_TENANT_URL}/api/config/v1/alertingProfiles" \
                    -H "Authorization: Api-Token ${DT_API_TOKEN}" \
                    -H "Content-Type: application/json" \
                    -d "$profile" | jq .
            done <<< "$profiles"
        fi
    fi
    
    log_success "Alerting configuration deployed."
}

deploy_synthetic_monitors() {
    log_info "Deploying synthetic monitors..."
    
    if [[ -f "${PROJECT_ROOT}/synthetics/monitors/http-monitors.json" ]]; then
        if [[ "$DRY_RUN" != "true" ]]; then
            local monitors
            monitors=$(jq -c '.monitors[]' "${PROJECT_ROOT}/synthetics/monitors/http-monitors.json")
            
            while IFS= read -r monitor; do
                local monitor_name
                monitor_name=$(echo "$monitor" | jq -r '.name')
                log_info "Deploying monitor: $monitor_name"
                
                curl -s -X POST "${DT_TENANT_URL}/api/v1/synthetic/monitors" \
                    -H "Authorization: Api-Token ${DT_API_TOKEN}" \
                    -H "Content-Type: application/json" \
                    -d "$monitor" | jq .
            done <<< "$monitors"
        fi
    fi
    
    log_success "Synthetic monitors deployed."
}

validate_deployment() {
    log_info "Validating deployment..."
    
    # Check AWS integration
    log_info "Checking AWS integration..."
    local aws_count
    aws_count=$(curl -s "${DT_TENANT_URL}/api/config/v1/aws/credentials" \
        -H "Authorization: Api-Token ${DT_API_TOKEN}" | jq '.values | length')
    log_info "AWS integrations configured: $aws_count"
    
    # Check Lambda functions discovered
    log_info "Checking discovered Lambda functions..."
    local lambda_count
    lambda_count=$(curl -s "${DT_TENANT_URL}/api/v2/entities?entitySelector=type(AWS_LAMBDA_FUNCTION)&pageSize=1" \
        -H "Authorization: Api-Token ${DT_API_TOKEN}" | jq '.totalCount')
    log_info "Lambda functions discovered: $lambda_count"
    
    # Check dashboards
    log_info "Checking dashboards..."
    local dashboard_count
    dashboard_count=$(curl -s "${DT_TENANT_URL}/api/config/v1/dashboards" \
        -H "Authorization: Api-Token ${DT_API_TOKEN}" | jq '.dashboards | length')
    log_info "Dashboards configured: $dashboard_count"
    
    log_success "Validation completed."
}

show_help() {
    cat << EOF
Dynatrace AWS Serverless Monitoring - Deployment Script

Usage: $(basename "$0") [OPTIONS] [COMMAND]

Commands:
  all           Deploy all components (default)
  terraform     Deploy Terraform infrastructure only
  dashboards    Deploy dashboards only
  alerting      Deploy alerting configuration only
  synthetic     Deploy synthetic monitors only
  validate      Validate deployment

Options:
  -e, --environment   Environment (dev, staging, production) [default: production]
  -r, --region        AWS region [default: us-east-1]
  -d, --dry-run       Show what would be done without making changes
  -h, --help          Show this help message

Environment Variables Required:
  DT_TENANT_URL       Dynatrace tenant URL
  DT_API_TOKEN        Dynatrace API token
  DT_PAAS_TOKEN       Dynatrace PaaS token

Examples:
  $(basename "$0") all
  $(basename "$0") --environment staging terraform
  $(basename "$0") --dry-run all

EOF
}

# =============================================================================
# Main
# =============================================================================

main() {
    local command="all"
    
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            -e|--environment)
                ENVIRONMENT="$2"
                shift 2
                ;;
            -r|--region)
                AWS_REGION="$2"
                shift 2
                ;;
            -d|--dry-run)
                DRY_RUN="true"
                shift
                ;;
            -h|--help)
                show_help
                exit 0
                ;;
            all|terraform|dashboards|alerting|synthetic|validate)
                command="$1"
                shift
                ;;
            *)
                log_error "Unknown option: $1"
                show_help
                exit 1
                ;;
        esac
    done
    
    echo "=============================================="
    echo "Dynatrace AWS Serverless Monitoring Deployment"
    echo "=============================================="
    echo "Environment: $ENVIRONMENT"
    echo "Region: $AWS_REGION"
    echo "Dry Run: $DRY_RUN"
    echo "=============================================="
    echo ""
    
    check_prerequisites
    
    case $command in
        all)
            deploy_terraform
            deploy_dashboards
            deploy_alerting
            deploy_synthetic_monitors
            validate_deployment
            ;;
        terraform)
            deploy_terraform
            ;;
        dashboards)
            deploy_dashboards
            ;;
        alerting)
            deploy_alerting
            ;;
        synthetic)
            deploy_synthetic_monitors
            ;;
        validate)
            validate_deployment
            ;;
    esac
    
    echo ""
    log_success "Deployment completed successfully!"
}

main "$@"

