/**
 * Process Order Handler
 * 
 * Processes orders from SQS queue (async processing).
 * Updates order status in DynamoDB.
 */

const { DynamoDBClient } = require('@aws-sdk/client-dynamodb');
const { DynamoDBDocumentClient, UpdateCommand, GetCommand } = require('@aws-sdk/lib-dynamodb');

// Initialize clients
const dynamoClient = new DynamoDBClient({});
const docClient = DynamoDBDocumentClient.from(dynamoClient);

// Environment variables
const ORDERS_TABLE = process.env.ORDERS_TABLE;

/**
 * Simulate order processing (payment, inventory, etc.)
 */
const processOrderLogic = async (order) => {
  // Simulate processing time (100-500ms)
  const processingTime = Math.floor(Math.random() * 400) + 100;
  await new Promise(resolve => setTimeout(resolve, processingTime));
  
  // Simulate occasional processing failures (5% failure rate)
  if (Math.random() < 0.05) {
    throw new Error('Payment processing failed');
  }
  
  return {
    success: true,
    processingTime
  };
};

exports.handler = async (event) => {
  const startTime = Date.now();
  const results = {
    processed: 0,
    failed: 0,
    errors: []
  };
  
  console.log(`Processing ${event.Records.length} orders from SQS`);
  
  for (const record of event.Records) {
    try {
      const message = JSON.parse(record.body);
      const { orderId } = message;
      
      if (!orderId) {
        console.error('Missing orderId in message');
        results.failed++;
        continue;
      }
      
      console.log(`[DT_CUSTOM_PROP] order.id=${orderId}`);
      console.log(`Processing order: ${orderId}`);
      
      // Get current order
      const orderResult = await docClient.send(new GetCommand({
        TableName: ORDERS_TABLE,
        Key: { orderId }
      }));
      
      if (!orderResult.Item) {
        console.error(`Order ${orderId} not found`);
        results.failed++;
        continue;
      }
      
      const order = orderResult.Item;
      
      // Update status to PROCESSING
      await docClient.send(new UpdateCommand({
        TableName: ORDERS_TABLE,
        Key: { orderId },
        UpdateExpression: 'SET #status = :status, updatedAt = :updatedAt',
        ExpressionAttributeNames: {
          '#status': 'status'
        },
        ExpressionAttributeValues: {
          ':status': 'PROCESSING',
          ':updatedAt': new Date().toISOString()
        }
      }));
      
      // Process the order
      const processingResult = await processOrderLogic(order);
      
      // Update status to COMPLETED
      await docClient.send(new UpdateCommand({
        TableName: ORDERS_TABLE,
        Key: { orderId },
        UpdateExpression: 'SET #status = :status, updatedAt = :updatedAt, processedAt = :processedAt',
        ExpressionAttributeNames: {
          '#status': 'status'
        },
        ExpressionAttributeValues: {
          ':status': 'COMPLETED',
          ':updatedAt': new Date().toISOString(),
          ':processedAt': new Date().toISOString()
        }
      }));
      
      console.log(`Order ${orderId} processed successfully`);
      
      // Log metrics
      console.log(`[DT_METRIC] custom.orders.processed,environment="${process.env.STAGE}",status="success" 1`);
      console.log(`[DT_METRIC] custom.orders.processing_duration,environment="${process.env.STAGE}" ${processingResult.processingTime}`);
      
      results.processed++;
      
    } catch (error) {
      console.error('Error processing order:', error);
      
      // Try to update order status to FAILED
      try {
        const message = JSON.parse(record.body);
        if (message.orderId) {
          await docClient.send(new UpdateCommand({
            TableName: ORDERS_TABLE,
            Key: { orderId: message.orderId },
            UpdateExpression: 'SET #status = :status, updatedAt = :updatedAt, errorMessage = :error',
            ExpressionAttributeNames: {
              '#status': 'status'
            },
            ExpressionAttributeValues: {
              ':status': 'FAILED',
              ':updatedAt': new Date().toISOString(),
              ':error': error.message
            }
          }));
        }
      } catch (updateError) {
        console.error('Failed to update order status:', updateError);
      }
      
      // Log error metric
      console.log(`[DT_METRIC] custom.orders.processed,environment="${process.env.STAGE}",status="failed" 1`);
      console.log(`[DT_METRIC] custom.orders.errors,environment="${process.env.STAGE}",operation="process" 1`);
      
      results.failed++;
      results.errors.push({
        orderId: JSON.parse(record.body)?.orderId,
        error: error.message
      });
      
      // Re-throw to trigger DLQ
      throw error;
    }
  }
  
  const totalTime = Date.now() - startTime;
  console.log(`[DT_METRIC] custom.orders.batch_time,environment="${process.env.STAGE}" ${totalTime}`);
  console.log(`Batch processing complete. Processed: ${results.processed}, Failed: ${results.failed}`);
  
  return {
    batchItemFailures: results.errors.map(e => ({
      itemIdentifier: e.orderId
    }))
  };
};

