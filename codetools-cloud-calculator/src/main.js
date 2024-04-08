/**
 * Extends the AWS Lambda cost calculation to include free tier benefits,
 * provisioned concurrency, and regional pricing differences.
 *
 * @param {Object} options - The input options for the calculation.
 * @param {number} options.numRequests - The number of requests.
 * @param {number} options.executionTime - The average execution time per request in milliseconds.
 * @param {number} options.memorySize - The memory allocated per request in GB.
 * @param {number} options.provisionedConcurrentExecutions - The number of provisioned concurrent executions.
 * @param {string} options.region - The AWS region code.
 * @returns {number} The total cost in USD.
 */
function calculateLambdaCost({ numRequests, executionTime, memorySize, provisionedConcurrentExecutions, region }) {
  // Regional pricing factors - could be extended with actual region-based pricing
  const regionalPricing = {
    "us-east-1": {
      requestCostPerMillion: 0.2,
      costPerGBSecond: 0.0000166667,
      provisionedConcurrentExecutionCost: 0.00005,
    },
    // Add other regions as needed
  };

  // Use pricing for the provided region, default to 'us-east-1' if not found
  const { requestCostPerMillion, costPerGBSecond, provisionedConcurrentExecutionCost } =
    regionalPricing[region] || regionalPricing["us-east-1"];

  // Free tier allowances
  const FREE_REQUESTS = 1000000;
  const FREE_COMPUTE_GB_SECONDS = 400000;

  // Calculate the total compute time in seconds
  const executionTimeInSeconds = executionTime / 1000;
  const totalComputeSeconds = numRequests * executionTimeInSeconds;

  // Calculate the total compute GB-seconds
  const totalComputeGBSeconds = totalComputeSeconds * memorySize;

  // Adjust for free tier
  const billableRequests = Math.max(0, numRequests - FREE_REQUESTS);
  const billableComputeGBSeconds = Math.max(0, totalComputeGBSeconds - FREE_COMPUTE_GB_SECONDS);

  // Calculate the cost for requests beyond the free tier
  const requestCost = (billableRequests / 1e6) * requestCostPerMillion;

  // Calculate the compute cost beyond the free tier
  const computeCost = billableComputeGBSeconds * costPerGBSecond;

  // Calculate the cost of provisioned concurrency
  const provisionedConcurrencyCost =
    provisionedConcurrentExecutions * provisionedConcurrentExecutionCost * 3600 * 24 * 30; // Assuming a full month

  // Calculate the total cost
  const totalCost = requestCost + computeCost + provisionedConcurrencyCost;

  return totalCost;
}

// Example usage:
// const cost = calculateLambdaCost({
//     numRequests: 2000000, // 2 million requests
//     executionTime: 500, // 500 milliseconds average execution time
//     memorySize: 0.5, // 512 MB or 0.5 GB memory allocated
//     provisionedConcurrentExecutions: 10, // 10 provisioned concurrency
//     region: 'us-east-1' // AWS region
// });

// console.log(`Total AWS Lambda cost: $${cost.toFixed(4)}`);
