/**
 * Calculates the cost of using AWS AppSync.
 *
 * @param {object} params - The parameters for the AWS AppSync usage.
 * @param {number} params.queryAndMutationRequests - The number of query and mutation requests per month.
 * @param {number} params.realTimeUpdateConnections - The number of real-time update connections per month.
 * @param {number} params.realTimeUpdateMinutes - The total minutes these connections are connected per month.
 * @param {number} params.cachedQueryRequests - The number of cached query requests per month.
 * @param {number} params.dataTransferOutGB - The amount of data transferred out in gigabytes per month.
 * @return {number} The total cost of using AWS AppSync in USD.
 *
 * Please note: The pricing used in this example is simplified and based on generic values. For precise and up-to-date pricing,
 * always consult the official AWS documentation and pricing pages.
 */
export function calculateAppSyncCost({
  queryAndMutationRequests,
  realTimeUpdateConnections,
  realTimeUpdateMinutes,
  cachedQueryRequests,
  dataTransferOutGB,
}) {
  // Cost factors (placeholders, adjust based on current pricing)
  const costPerQueryAndMutationRequest = 0.004; // Cost per million queries/mutations
  const costPerRealTimeUpdateConnection = 0.25; // Monthly cost per connection
  const costPerRealTimeUpdateMinute = 0.000002; // Cost per connection minute
  const costPerCachedQueryRequest = 0.002; // Cost per million cached queries
  const costPerGBDataTransferOut = 0.09; // Cost per GB of data transferred out

  // Calculating costs
  const queryAndMutationCost = (queryAndMutationRequests / 1000000) * costPerQueryAndMutationRequest;
  const realTimeUpdateConnectionCost = realTimeUpdateConnections * costPerRealTimeUpdateConnection;
  const realTimeUpdateMinuteCost = realTimeUpdateMinutes * costPerRealTimeUpdateMinute;
  const cachedQueryCost = (cachedQueryRequests / 1000000) * costPerCachedQueryRequest;
  const dataTransferOutCost = dataTransferOutGB * costPerGBDataTransferOut;

  // Total cost
  return (
    queryAndMutationCost +
    realTimeUpdateConnectionCost +
    realTimeUpdateMinuteCost +
    cachedQueryCost +
    dataTransferOutCost
  );
}

// Example usage:
const appSyncUsage = {
  queryAndMutationRequests: 5000000,
  realTimeUpdateConnections: 100,
  realTimeUpdateMinutes: 30000,
  cachedQueryRequests: 2000000,
  dataTransferOutGB: 50,
};

const totalCost = calculateAppSyncCost(appSyncUsage);
console.log(`Total AWS AppSync cost: $${totalCost.toFixed(2)}`);
