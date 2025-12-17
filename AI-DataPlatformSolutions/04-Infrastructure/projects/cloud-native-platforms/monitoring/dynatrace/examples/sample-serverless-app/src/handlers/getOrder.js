/**
 * Get Order Handler
 * 
 * Retrieves an order by ID from DynamoDB.
 */

const { DynamoDBClient } = require('@aws-sdk/client-dynamodb');
const { DynamoDBDocumentClient, GetCommand } = require('@aws-sdk/lib-dynamodb');

// Initialize clients
const dynamoClient = new DynamoDBClient({});
const docClient = DynamoDBDocumentClient.from(dynamoClient);

// Environment variables
const ORDERS_TABLE = process.env.ORDERS_TABLE;

exports.handler = async (event) => {
  const startTime = Date.now();
  
  try {
    const orderId = event.pathParameters?.orderId;
    
    if (!orderId) {
      return {
        statusCode: 400,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          error: 'Bad Request',
          message: 'Order ID is required'
        })
      };
    }
    
    // Log request attribute for Dynatrace
    console.log(`[DT_CUSTOM_PROP] order.id=${orderId}`);
    
    // Get order from DynamoDB
    const result = await docClient.send(new GetCommand({
      TableName: ORDERS_TABLE,
      Key: { orderId }
    }));
    
    const processingTime = Date.now() - startTime;
    console.log(`[DT_METRIC] custom.orders.get_time,environment="${process.env.STAGE}" ${processingTime}`);
    
    if (!result.Item) {
      return {
        statusCode: 404,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          error: 'Not Found',
          message: `Order ${orderId} not found`
        })
      };
    }
    
    return {
      statusCode: 200,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(result.Item)
    };
    
  } catch (error) {
    console.error('Error getting order:', error);
    console.log(`[DT_METRIC] custom.orders.errors,environment="${process.env.STAGE}",operation="get" 1`);
    
    return {
      statusCode: 500,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        error: 'Internal Server Error',
        message: 'Failed to retrieve order'
      })
    };
  }
};

