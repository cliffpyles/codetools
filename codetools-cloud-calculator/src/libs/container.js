/**
 * Placeholder for Amazon ECR (Elastic Container Registry) Cost Calculation
 */

/**
 * Calculates the cost of using AWS ECS (Elastic Container Service).
 *
 * @param {object} params - The parameters for AWS ECS usage.
 * @param {number} params.ec2InstanceHours - The total hours of EC2 instance usage for ECS per month (for EC2 launch type).
 * @param {number} params.ec2InstanceRate - The hourly rate for the EC2 instances used by ECS in USD (for EC2 launch type).
 * @param {number} params.fargatevCPUHours - The total hours of vCPU used by Fargate tasks per month (for Fargate launch type).
 * @param {number} params.fargateMemoryGBHours - The total hours of memory in GB used by Fargate tasks per month (for Fargate launch type).
 * @param {number} params.fargatevCPURate - The cost per vCPU hour for Fargate tasks in USD.
 * @param {number} params.fargateMemoryRate - The cost per GB hour for memory used by Fargate tasks in USD.
 * @param {number} params.ebsVolumeGB - The total size of EBS volumes attached to the EC2 instances in gigabytes (optional for EC2 launch type).
 * @param {number} params.ebsRatePerGBMonth - The monthly cost per GB for the EBS volume in USD (optional for EC2 launch type).
 * @param {number} params.dataTransferOutGB - The amount of data transferred out of AWS ECS to the internet in gigabytes per month.
 * @param {number} params.dataTransferRate - The cost per GB for data transfer out in USD.
 * @return {number} The total cost of using AWS ECS in USD.
 *
 * Note: The pricing used in this example is simplified and based on generic values. For precise and up-to-date pricing,
 * always consult the official AWS documentation and pricing pages.
 */
function calculateECSCost({
  ec2InstanceHours,
  ec2InstanceRate,
  fargatevCPUHours,
  fargateMemoryGBHours,
  fargatevCPURate,
  fargateMemoryRate,
  ebsVolumeGB = 0,
  ebsRatePerGBMonth = 0,
  dataTransferOutGB,
  dataTransferRate,
}) {
  // Calculating costs for EC2 launch type
  const ec2Cost = ec2InstanceHours * ec2InstanceRate;
  const ebsCost = ebsVolumeGB * ebsRatePerGBMonth;

  // Calculating costs for Fargate launch type
  const fargatevCPUCost = fargatevCPUHours * fargatevCPURate;
  const fargateMemoryCost = fargateMemoryGBHours * fargateMemoryRate;

  // Calculating data transfer costs
  const dataTransferCost = dataTransferOutGB * dataTransferRate;

  // Total cost
  return ec2Cost + ebsCost + fargatevCPUCost + fargateMemoryCost + dataTransferCost;
}

// Example usage:
// const ecsUsage = {
//   ec2InstanceHours: 720, // 1 EC2 instance running 24/7 for a 30-day month
//   ec2InstanceRate: 0.25, // Hourly rate for the EC2 instance
//   fargatevCPUHours: 100, // 100 vCPU hours used by Fargate
//   fargateMemoryGBHours: 200, // 200 GB hours of memory used by Fargate
//   fargatevCPURate: 0.04, // Cost per vCPU hour for Fargate
//   fargateMemoryRate: 0.004, // Cost per GB hour for memory used by Fargate
//   ebsVolumeGB: 500, // 500 GB of EBS storage (optional for EC2 launch type)
//   ebsRatePerGBMonth: 0.1, // Monthly cost per GB for EBS
//   dataTransferOutGB: 100, // 100 GB data transferred out
//   dataTransferRate: 0.09 // Cost per GB for data transfer out
// };

// const totalCost = calculateECSCost(ecsUsage);
// console.log(`Total AWS ECS cost: $${totalCost.toFixed(2)}`);

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
