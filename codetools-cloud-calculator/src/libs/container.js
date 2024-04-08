/**
 * Placeholder for Amazon ECS (Elastic Container Service) Cost Calculation
 */

/**
 * Placeholder for Amazon ECR (Elastic Container Registry) Cost Calculation
 */

/**
 * Calculates the cost of using Amazon EKS (Elastic Kubernetes Service).
 *
 * @param {Object} options - The input options for the calculation.
 * @param {number} options.clusterHours - The total hours the cluster is running.
 * @param {number} options.workerNodeHours - The total hours all worker nodes are running.
 * @param {number} options.workerNodevCPU - The total vCPUs across all worker nodes.
 * @param {number} options.workerNodeGB - The total memory (GB) across all worker nodes.
 * @param {string} options.region - The AWS region code.
 * @returns {number} The total cost in USD.
 */
export function calculateEKSCost({ clusterHours, workerNodeHours, workerNodevCPU, workerNodeGB, region }) {
  // Example regional pricing factors (costs could vary, use the latest pricing)
  const regionalPricing = {
    "us-east-1": {
      clusterCostPerHour: 0.1,
      workerNodeCostPerHourPerCPU: 0.04,
      workerNodeCostPerHourPerGB: 0.002,
    },
    // Add other regions as needed
  };

  const pricing = regionalPricing[region] || regionalPricing["us-east-1"];

  // Calculate the cluster cost
  const clusterCost = clusterHours * pricing.clusterCostPerHour;

  // Calculate the worker nodes cost
  const workerNodesCPUCost = workerNodeHours * workerNodevCPU * pricing.workerNodeCostPerHourPerCPU;
  const workerNodesMemoryCost = workerNodeHours * workerNodeGB * pricing.workerNodeCostPerHourPerGB;

  // Total cost
  const totalCost = clusterCost + workerNodesCPUCost + workerNodesMemoryCost;

  return totalCost;
}

// console.log(
//   `Total Amazon EKS cost: $${calculateEKSCost({
//     clusterHours: 720, // 1 month
//     workerNodeHours: 1440, // 2 nodes for 1 month
//     workerNodevCPU: 8, // 4 vCPUs per node
//     workerNodeGB: 32, // 16 GB per node
//     region: "us-east-1",
//   }).toFixed(4)}`
// );
