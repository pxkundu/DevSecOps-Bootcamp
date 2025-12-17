/**
 * List Orders Handler
 * 
 * Lists orders with optional pagination and customer filtering.
 */

const { DynamoDBClient } = require('@aws-sdk/client-dynamodb');
const { DynamoDBDocumentClient, ScanCommand, QueryCommand } = require('@aws-sdk/lib-dynamodb');

// Initialize clients
const dynamoClient = new DynamoDBClient({});
const docClient = DynamoDBDocumentClient.from(dynamoClient);

// Environment variables
const ORDERS_TABLE = process.env.ORDERS_TABLE;

exports.handler = async (event) => {
  const startTime = Date.now();
  
  try {
    const queryParams = event.queryStringParameters || {};
    const customerId = queryParams.customerId;
    const limit = parseInt(queryParams.limit) || 20;
    
    let result;
    
    if (customerId) {
      // Query by customer ID using GSI
      console.log(`[DT_CUSTOM_PROP] query.customer_id=${customerId}`);
      
      result = await docClient.send(new QueryCommand({
        TableName: ORDERS_TABLE,
        IndexName: 'CustomerIndex',
        KeyConditionExpression: 'customerId = :customerId',
        ExpressionAttributeValues: {
          ':customerId': customerId
        },
        Limit: limit
      }));
    } else {
      // Scan all orders
      result = await docClient.send(new ScanCommand({
        TableName: ORDERS_TABLE,
        Limit: limit
      }));
    }
    
    const processingTime = Date.now() - startTime;
    console.log(`[DT_METRIC] custom.orders.list_time,environment="${process.env.STAGE}" ${processingTime}`);
    console.log(`[DT_METRIC] custom.orders.list_count,environment="${process.env.STAGE}" ${result.Items?.length || 0}`);
    
    return {
      statusCode: 200,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        orders: result.Items || [],
        count: result.Items?.length || 0,
        lastEvaluatedKey: result.LastEvaluatedKey
      })
    };
    
  } catch (error) {
    console.error('Error listing orders:', error);
    console.log(`[DT_METRIC] custom.orders.errors,environment="${process.env.STAGE}",operation="list" 1`);
    
    return {
      statusCode: 500,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        error: 'Internal Server Error',
        message: 'Failed to list orders'
      })
    };
  }
};

