#!/bin/bash
# =============================================================================
# Dynatrace AWS Serverless Monitoring - Validation Script
# =============================================================================

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Counters
PASS=0
FAIL=0
WARN=0

# =============================================================================
# Functions
# =============================================================================

check_pass() {
    echo -e "${GREEN}✓${NC} $1"
    ((PASS++))
}

check_fail() {
    echo -e "${RED}✗${NC} $1"
    ((FAIL++))
}

check_warn() {
    echo -e "${YELLOW}⚠${NC} $1"
    ((WARN++))
}

# =============================================================================
# Validation Checks
# =============================================================================

echo "=============================================="
echo "Dynatrace AWS Serverless Monitoring Validation"
echo "=============================================="
echo ""

# Check environment variables
echo "1. Environment Variables"
echo "------------------------"

if [[ -n "${DT_TENANT_URL:-}" ]]; then
    check_pass "DT_TENANT_URL is set"
else
    check_fail "DT_TENANT_URL is not set"
fi

if [[ -n "${DT_API_TOKEN:-}" ]]; then
    check_pass "DT_API_TOKEN is set"
else
    check_fail "DT_API_TOKEN is not set"
fi

if [[ -n "${DT_PAAS_TOKEN:-}" ]]; then
    check_pass "DT_PAAS_TOKEN is set"
else
    check_fail "DT_PAAS_TOKEN is not set"
fi

echo ""

# Check API connectivity
echo "2. API Connectivity"
echo "-------------------"

if [[ -n "${DT_TENANT_URL:-}" ]] && [[ -n "${DT_API_TOKEN:-}" ]]; then
    status=$(curl -s -o /dev/null -w "%{http_code}" \
        "${DT_TENANT_URL}/api/v2/entities?pageSize=1" \
        -H "Authorization: Api-Token ${DT_API_TOKEN}" 2>/dev/null || echo "000")
    
    if [[ "$status" == "200" ]]; then
        check_pass "Dynatrace API is accessible (HTTP $status)"
    else
        check_fail "Dynatrace API returned HTTP $status"
    fi
else
    check_fail "Cannot test API - credentials not set"
fi

echo ""

# Check AWS integration
echo "3. AWS Integration"
echo "------------------"

if [[ -n "${DT_TENANT_URL:-}" ]] && [[ -n "${DT_API_TOKEN:-}" ]]; then
    aws_response=$(curl -s "${DT_TENANT_URL}/api/config/v1/aws/credentials" \
        -H "Authorization: Api-Token ${DT_API_TOKEN}" 2>/dev/null || echo "{}")
    
    aws_count=$(echo "$aws_response" | jq -r '.values | length' 2>/dev/null || echo "0")
    
    if [[ "$aws_count" -gt 0 ]]; then
        check_pass "AWS integration configured ($aws_count connections)"
    else
        check_warn "No AWS integrations found"
    fi
fi

echo ""

# Check Lambda functions
echo "4. Lambda Functions"
echo "-------------------"

if [[ -n "${DT_TENANT_URL:-}" ]] && [[ -n "${DT_API_TOKEN:-}" ]]; then
    lambda_response=$(curl -s "${DT_TENANT_URL}/api/v2/entities?entitySelector=type(AWS_LAMBDA_FUNCTION)&pageSize=1" \
        -H "Authorization: Api-Token ${DT_API_TOKEN}" 2>/dev/null || echo "{}")
    
    lambda_count=$(echo "$lambda_response" | jq -r '.totalCount' 2>/dev/null || echo "0")
    
    if [[ "$lambda_count" -gt 0 ]]; then
        check_pass "Lambda functions discovered: $lambda_count"
    else
        check_warn "No Lambda functions discovered yet"
    fi
fi

echo ""

# Check monitored services
echo "5. Monitored Services"
echo "---------------------"

if [[ -n "${DT_TENANT_URL:-}" ]] && [[ -n "${DT_API_TOKEN:-}" ]]; then
    services_response=$(curl -s "${DT_TENANT_URL}/api/v2/entities?entitySelector=type(SERVICE)&pageSize=1" \
        -H "Authorization: Api-Token ${DT_API_TOKEN}" 2>/dev/null || echo "{}")
    
    services_count=$(echo "$services_response" | jq -r '.totalCount' 2>/dev/null || echo "0")
    
    if [[ "$services_count" -gt 0 ]]; then
        check_pass "Services being monitored: $services_count"
    else
        check_warn "No services discovered yet"
    fi
fi

echo ""

# Check dashboards
echo "6. Dashboards"
echo "-------------"

if [[ -n "${DT_TENANT_URL:-}" ]] && [[ -n "${DT_API_TOKEN:-}" ]]; then
    dashboards_response=$(curl -s "${DT_TENANT_URL}/api/config/v1/dashboards" \
        -H "Authorization: Api-Token ${DT_API_TOKEN}" 2>/dev/null || echo "{}")
    
    dashboards_count=$(echo "$dashboards_response" | jq -r '.dashboards | length' 2>/dev/null || echo "0")
    
    if [[ "$dashboards_count" -gt 0 ]]; then
        check_pass "Dashboards configured: $dashboards_count"
    else
        check_warn "No dashboards configured"
    fi
fi

echo ""

# Check active problems
echo "7. Active Problems"
echo "------------------"

if [[ -n "${DT_TENANT_URL:-}" ]] && [[ -n "${DT_API_TOKEN:-}" ]]; then
    problems_response=$(curl -s "${DT_TENANT_URL}/api/v2/problems?problemSelector=status(\"open\")" \
        -H "Authorization: Api-Token ${DT_API_TOKEN}" 2>/dev/null || echo "{}")
    
    problems_count=$(echo "$problems_response" | jq -r '.totalCount' 2>/dev/null || echo "0")
    
    if [[ "$problems_count" == "0" ]]; then
        check_pass "No active problems"
    else
        check_warn "Active problems: $problems_count"
    fi
fi

echo ""

# Summary
echo "=============================================="
echo "Validation Summary"
echo "=============================================="
echo -e "${GREEN}Passed:${NC} $PASS"
echo -e "${RED}Failed:${NC} $FAIL"
echo -e "${YELLOW}Warnings:${NC} $WARN"
echo ""

if [[ $FAIL -gt 0 ]]; then
    echo -e "${RED}Validation failed. Please fix the issues above.${NC}"
    exit 1
else
    echo -e "${GREEN}Validation completed successfully!${NC}"
    exit 0
fi

