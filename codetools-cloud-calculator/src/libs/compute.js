/**
 * Calculates the cost of using AWS EC2.
 *
 * @param {object} params - The parameters for AWS EC2 usage.
 * @param {number} params.instanceHours - The total hours of instance usage per month.
 * @param {number} params.instanceRate - The hourly rate for the chosen instance type in USD.
 * @param {number} params.numberOfInstances - The number of instances of the specified type.
 * @param {number} params.ebsVolumeGB - The total size of EBS volumes attached to the instances in gigabytes.
 * @param {number} params.ebsRatePerGBMonth - The monthly cost per GB for the EBS volume in USD.
 * @param {number} params.dataTransferOutGB - The amount of data transferred out of AWS EC2 to the internet in gigabytes per month.
 * @param {number} params.dataTransferRate - The cost per GB for data transfer out in USD.
 * @return {number} The total cost of using AWS EC2 in USD.
 *
 * Note: The pricing used in this example is simplified and based on generic values. For precise and up-to-date pricing,
 * always consult the official AWS documentation and pricing pages.
 */
export function calculateEC2Cost({
  instanceHours,
  instanceRate,
  numberOfInstances,
  ebsVolumeGB,
  ebsRatePerGBMonth,
  dataTransferOutGB,
  dataTransferRate,
}) {
  // Calculating instance costs
  const instanceCost = instanceHours * instanceRate * numberOfInstances;

  // Calculating EBS volume cost
  const ebsCost = ebsVolumeGB * ebsRatePerGBMonth;

  // Calculating data transfer costs
  const dataTransferCost = dataTransferOutGB * dataTransferRate;

  // Total cost
  return instanceCost + ebsCost + dataTransferCost;
}

// Example usage:
// const ec2Usage = {
//   instanceHours: 720, // 1 instance running 24/7 for a 30-day month
//   instanceRate: 0.1, // Hypothetical rate for a specific instance type
//   numberOfInstances: 2, // 2 instances running
//   ebsVolumeGB: 1000, // 1 TB of EBS storage
//   ebsRatePerGBMonth: 0.1, // Hypothetical monthly cost per GB for EBS
//   dataTransferOutGB: 500, // 500 GB data transferred out
//   dataTransferRate: 0.09 // Cost per GB for data transfer out
// };

// const totalCost = calculateEC2Cost(ec2Usage);
// console.log(`Total AWS EC2 cost: $${totalCost.toFixed(2)}`);

/**
 * Calculates the cost of using AWS Lambda.
 *
 * @param {Object} options - The input options for the calculation.
 * @param {number} options.numRequests - The number of requests.
 * @param {number} options.executionTime - The average execution time per request in milliseconds.
 * @param {number} options.memorySize - The memory allocated per request in GB.
 * @param {number} options.provisionedConcurrentExecutions - The number of provisioned concurrent executions.
 * @param {string} options.region - The AWS region code.
 * @returns {number} The total cost in USD.
 */
export function calculateLambdaCost({
  numRequests,
  executionTime,
  memorySize,
  provisionedConcurrentExecutions,
  region,
}) {
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
