#!/bin/bash

# Wait for EKS deployment
echo "Waiting for pods to be ready..."
kubectl wait --for=condition=ready pod -l app=crm-ui -n crm-us --timeout=300s
kubectl wait --for=condition=ready pod -l app=tracking-ui -n supply-us --timeout=300s

# Get LoadBalancer URLs
CRM_UI_URL=$(kubectl get svc crm-ui -n crm-us -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')
TRACKING_UI_URL=$(kubectl get svc tracking-ui -n supply-us -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')

# Test CRM Order Placement
echo "Placing order via crm-ui..."
ORDER_RESPONSE=$(curl -s -X POST "http://$CRM_UI_URL/orders" \
  -d "productId=prod-001&quantity=5" \
  -H "X-API-Key: default-key")
ORDER_ID=$(echo "$ORDER_RESPONSE" | grep -o '"id":"[^"]*' | cut -d'"' -f4)
if [ -z "$ORDER_ID" ]; then
  echo "Failed to place order"
  exit 1
fi
echo "Order placed: $ORDER_ID"

# Test Inventory Sync (assumes order-service updates inventory)
echo "Checking inventory sync..."
INVENTORY_RESPONSE=$(curl -s "http://$CRM_UI_URL/orders/$ORDER_ID" -H "X-API-Key: default-key")
if ! echo "$INVENTORY_RESPONSE" | grep -q "quantity"; then
  echo "Inventory sync failed"
  exit 1
fi
echo "Inventory synced"

# Test Tracking UI
echo "Checking tracking UI..."
TRACKING_RESPONSE=$(curl -s "http://$TRACKING_UI_URL/shipments/ship-$ORDER_ID" -H "X-API-Key: default-key")
if ! echo "$TRACKING_RESPONSE" | grep -q "shipmentId"; then
  echo "Tracking UI failed"
  exit 1
fi
echo "Tracking UI validated"

echo "Full flow test passed!"
exit 0
