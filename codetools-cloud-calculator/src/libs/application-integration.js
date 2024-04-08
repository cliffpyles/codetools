/**
 * Calculates the cost of using AWS EventBridge.
 *
 * @param {object} params - The parameters for AWS EventBridge usage.
 * @param {number} params.eventsPut - The number of events put to EventBridge per month.
 * @param {number} params.customEventBuses - The number of custom event buses used per month, beyond the free tier.
 * @param {number} params.customEventBusesHours - The total hours that custom event buses are running per month.
 * @param {number} params.schemaRegistryRequests - The number of Schema Registry API requests per month, beyond the free tier.
 * @param {number} params.dataTransferOutGB - The amount of data transferred out of EventBridge in gigabytes per month.
 * @return {number} The total cost of using AWS EventBridge in USD.
 *
 * Note: The pricing used in this example is simplified and based on generic values. For precise and up-to-date pricing,
 * always consult the official AWS documentation and pricing pages.
 */
export function calculateEventBridgeCost({
  eventsPut,
  customEventBuses,
  customEventBusesHours,
  schemaRegistryRequests,
  dataTransferOutGB,
}) {
  // Cost factors (placeholders, adjust based on current pricing)
  const costPerEventPut = 1.0 / 1000000; // Cost per million events put to EventBridge
  const costPerCustomEventBusHour = 0.02; // Cost per custom event bus hour
  const costPerSchemaRegistryRequest = 1.0 / 1000000; // Cost per million Schema Registry API requests
  const costPerGBDataTransferOut = 0.09; // Cost per GB of data transferred out

  // Calculating costs
  const eventsPutCost = eventsPut * costPerEventPut;
  const customEventBusesCost = customEventBuses * customEventBusesHours * costPerCustomEventBusHour;
  const schemaRegistryRequestsCost = schemaRegistryRequests * costPerSchemaRegistryRequest;
  const dataTransferOutCost = dataTransferOutGB * costPerGBDataTransferOut;

  // Total cost
  return eventsPutCost + customEventBusesCost + schemaRegistryRequestsCost + dataTransferOutCost;
}

// // Example usage:
// const eventBridgeUsage = {
//   eventsPut: 5000000, // 5 million events put to EventBridge
//   customEventBuses: 2, // 2 custom event buses
//   customEventBusesHours: 720, // 2 buses running 24/7 for a 30-day month
//   schemaRegistryRequests: 1000000, // 1 million Schema Registry API requests
//   dataTransferOutGB: 50 // 50 GB data transferred out
// };

// const totalCost = calculateEventBridgeCost(eventBridgeUsage);
// console.log(`Total AWS EventBridge cost: $${totalCost.toFixed(2)}`);

/**
 * Calculates the cost of using AWS Step Functions.
 *
 * @param {object} params - The parameters for the AWS Step Functions usage.
 * @param {number} params.standardTransitions - The number of state transitions for Standard workflows.
 * @param {number} params.expressTransitions - The number of state transitions for Express workflows.
 * @param {number} params.expressGbSeconds - The total GB-seconds used by Express workflows, calculated as the memory size allocated times the duration in seconds.
 * @return {number} The total cost of using AWS Step Functions in USD.
 *
 * Note: The pricing used in this example is simplified and based on generic values. For precise and up-to-date pricing,
 * always consult the official AWS documentation and pricing pages.
 */
export function calculateStepFunctionsCost({ standardTransitions, expressTransitions, expressGbSeconds }) {
  // Cost factors (placeholders, adjust based on current pricing)
  const costPerStandardTransition = 0.025 / 1000; // Cost per 1,000 state transitions for Standard workflows
  const costPerExpressTransition = 0.000001; // Cost per state transition for Express workflows
  const costPerGbSecondExpress = 0.0000166667; // Cost per GB-second for Express workflows

  // Calculating costs
  const standardTransitionsCost = standardTransitions * costPerStandardTransition;
  const expressTransitionsCost = expressTransitions * costPerExpressTransition;
  const expressGbSecondsCost = expressGbSeconds * costPerGbSecondExpress;

  // Total cost
  return standardTransitionsCost + expressTransitionsCost + expressGbSecondsCost;
}

// // Example usage:
// const stepFunctionsUsage = {
//   standardTransitions: 4000, // 4,000 state transitions for Standard workflows
//   expressTransitions: 1000000, // 1,000,000 state transitions for Express workflows
//   expressGbSeconds: 5000 // 5,000 GB-seconds for Express workflows
// };

// const totalCost = calculateStepFunctionsCost(stepFunctionsUsage);
// console.log(`Total AWS Step Functions cost: $${totalCost.toFixed(2)}`);

/**
 * Calculates the cost of using Amazon SQS (Simple Queue Service).
 *
 * @param {Object} options - The input options for the calculation.
 * @param {number} options.requests - The number of requests (API calls).
 * @param {string} options.region - The AWS region code.
 * @returns {number} The total cost in USD.
 */
export function calculateSQSCost({ requests, region }) {
  // Example regional pricing factors (costs could vary, use the latest pricing)
  const regionalPricing = {
    "us-east-1": {
      requestCostPerMillion: 0.4, // Standard Queue
      // For FIFO Queue, pricing might differ
    },
    // Add other regions as needed
  };

  const pricing = regionalPricing[region] || regionalPricing["us-east-1"];

  // Calculate the requests cost
  const requestCost = (requests / 1e6) * pricing.requestCostPerMillion;

  // Total cost
  const totalCost = requestCost;

  return totalCost;
}

/**
 * Calculates the cost of using Amazon SNS (Simple Notification Service).
 *
 * @param {Object} options - The input options for the calculation.
 * @param {number} options.requests - The number of Publish requests.
 * @param {number} options.smsMessages - The number of SMS messages sent.
 * @param {string} options.region - The AWS region code.
 * @returns {number} The total cost in USD.
 */
export function calculateSNSCost({ requests, smsMessages, region }) {
  // Example regional pricing for US-East-1 (costs could vary, use the latest pricing)
  const regionalPricing = {
    "us-east-1": {
      requestCostPerMillion: 0.5, // Cost per 1 million Publish requests
      smsMessageCost: 0.00645, // Cost per SMS message (this can vary widely by destination country)
    },
    // Add other regions and pricing as needed
  };

  const pricing = regionalPricing[region] || regionalPricing["us-east-1"];

  // Calculate the requests cost
  const requestCost = (requests / 1e6) * pricing.requestCostPerMillion;

  // Calculate the SMS messages cost
  const smsMessageCost = smsMessages * pricing.smsMessageCost;

  // Total cost
  const totalCost = requestCost + smsMessageCost;

  return totalCost;
}

// Example usage for SQS
// console.log(`Total Amazon SQS cost: $${calculateSQSCost({
//     requests: 2000000, // 2 million requests
//     region: 'us-east-1'
// }).toFixed(4)}`);

// Example usage for SNS
// console.log(`Total Amazon SNS cost: $${calculateSNSCost({
//     requests: 1000000, // 1 million Publish requests
//     smsMessages: 5000, // 5,000 SMS messages
//     region: 'us-east-1'
// }).toFixed(4)}`);
