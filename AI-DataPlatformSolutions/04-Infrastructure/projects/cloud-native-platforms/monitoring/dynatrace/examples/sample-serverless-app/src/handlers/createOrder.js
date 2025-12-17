/**
 * Create Order Handler
 * 
 * Creates a new order and sends it to the processing queue.
 * Includes Dynatrace custom metrics and request attributes.
 */

const { DynamoDBClient } = require('@aws-sdk/client-dynamodb');
const { DynamoDBDocumentClient, PutCommand } = require('@aws-sdk/lib-dynamodb');
const { SQSClient, SendMessageCommand } = require('@aws-sdk/client-sqs');
const { v4: uuidv4 } = require('uuid');

// Initialize clients
const dynamoClient = new DynamoDBClient({});
const docClient = DynamoDBDocumentClient.from(dynamoClient);
const sqsClient = new SQSClient({});

// Environment variables
const ORDERS_TABLE = process.env.ORDERS_TABLE;
const ORDERS_QUEUE_URL = process.env.ORDERS_QUEUE_URL;

/**
 * Add custom request attribute for Dynatrace
 * These appear in distributed traces for easier debugging
 */
const addDynatraceAttribute = (key, value) => {
  // Dynatrace automatically captures these when set on the request
  if (process.env.DT_TENANT) {
    console.log(`[DT_CUSTOM_PROP] ${key}=${value}`);
  }
};

/**
 * Log custom metric for Dynatrace
 * Format: [DT_METRIC] metric_name,dimensions value
 */
const logMetric = (name, value, dimensions = {}) => {
  const dimStr = Object.entries(dimensions)
    .map(([k, v]) => `${k}="${v}"`)
    .join(',');
  console.log(`[DT_METRIC] ${name}${dimStr ? ',' + dimStr : ''} ${value}`);
};

exports.handler = async (event) => {
  const startTime = Date.now();
  
  try {
    // Parse request body
    const body = JSON.parse(event.body || '{}');
    
    // Validate required fields
    if (!body.customerId || !body.items || !Array.isArray(body.items)) {
      return {
        statusCode: 400,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          error: 'Invalid request',
          message: 'customerId and items array are required'
        })
      };
    }
    
    // Generate order ID and calculate total
    const orderId = uuidv4();
    const orderTotal = body.items.reduce((sum, item) => {
      return sum + (item.price || 10) * (item.quantity || 1);
    }, 0);
    
    // Create order object
    const order = {
      orderId,
      customerId: body.customerId,
      items: body.items,
      total: orderTotal,
      status: 'PENDING',
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    };
    
    // Add Dynatrace custom attributes
    addDynatraceAttribute('order.id', orderId);
    addDynatraceAttribute('order.customer_id', body.customerId);
    addDynatraceAttribute('order.total', orderTotal);
    addDynatraceAttribute('order.items_count', body.items.length);
    
    // Save to DynamoDB
    await docClient.send(new PutCommand({
      TableName: ORDERS_TABLE,
      Item: order
    }));
    
    console.log(`Order ${orderId} saved to DynamoDB`);
    
    // Send to processing queue
    await sqsClient.send(new SendMessageCommand({
      QueueUrl: ORDERS_QUEUE_URL,
      MessageBody: JSON.stringify({
        orderId,
        action: 'PROCESS_ORDER'
      }),
      MessageAttributes: {
        OrderId: {
          DataType: 'String',
          StringValue: orderId
        },
        CustomerId: {
          DataType: 'String',
          StringValue: body.customerId
        }
      }
    }));
    
    console.log(`Order ${orderId} sent to processing queue`);
    
    // Calculate processing time
    const processingTime = Date.now() - startTime;
    
    // Log custom metrics for Dynatrace
    logMetric('custom.orders.created', 1, {
      environment: process.env.STAGE,
      customer_id: body.customerId
    });
    
    logMetric('custom.orders.value', orderTotal, {
      environment: process.env.STAGE,
      currency: 'USD'
    });
    
    logMetric('custom.orders.processing_time', processingTime, {
      environment: process.env.STAGE,
      operation: 'create'
    });
    
    // Return success response
    return {
      statusCode: 201,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message: 'Order created successfully',
        order: {
          orderId: order.orderId,
          status: order.status,
          total: order.total,
          createdAt: order.createdAt
        }
      })
    };
    
  } catch (error) {
    console.error('Error creating order:', error);
    
    // Log error metric
    logMetric('custom.orders.errors', 1, {
      environment: process.env.STAGE,
      error_type: error.name || 'Unknown',
      operation: 'create'
    });
    
    return {
      statusCode: 500,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        error: 'Internal server error',
        message: 'Failed to create order'
      })
    };
  }
};

