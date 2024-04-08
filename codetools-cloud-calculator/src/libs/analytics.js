/**
 * Calculates the cost of using Amazon Kinesis.
 *
 * @param {object} params - The parameters for the Amazon Kinesis usage.
 * @param {number} params.dataStreamShards - The number of shards for Kinesis Data Streams.
 * @param {number} params.shardHours - Total hours the shards are running per month.
 * @param {number} params.putPayloadUnits - Total PUT Payload Units for Kinesis Data Streams per month.
 * @param {number} params.dataFirehoseGB - The amount of data processed by Kinesis Data Firehose in gigabytes per month.
 * @param {number} params.dataAnalyticsProcessingUnits - Kinesis Data Analytics Processing Units used per month.
 * @param {number} params.dataTransferOutGB - The amount of data transferred out of Kinesis services in gigabytes per month.
 * @return {number} The total cost of using Amazon Kinesis in USD.
 *
 * Note: The pricing used in this example is simplified and based on generic values. For precise and up-to-date pricing,
 * always consult the official AWS documentation and pricing pages.
 */
export function calculateKinesisCost({
  dataStreamShards,
  shardHours,
  putPayloadUnits,
  dataFirehoseGB,
  dataAnalyticsProcessingUnits,
  dataTransferOutGB,
}) {
  // Cost factors (placeholders, adjust based on current pricing)
  const costPerShardHour = 0.015; // Cost per shard hour for Data Streams
  const costPerPUTPayloadUnit = 0.014; // Cost per million PUT Payload Units for Data Streams
  const costPerGBFirehose = 0.029; // Cost per GB processed by Data Firehose
  const costPerProcessingUnitAnalytics = 0.11; // Cost per Kinesis Data Analytics Processing Unit per hour
  const costPerGBDataTransferOut = 0.09; // Cost per GB of data transferred out

  // Calculating costs
  const dataStreamsCost = dataStreamShards * shardHours * costPerShardHour;
  const putPayloadUnitsCost = (putPayloadUnits / 1000000) * costPerPUTPayloadUnit;
  const dataFirehoseCost = dataFirehoseGB * costPerGBFirehose;
  const dataAnalyticsCost = dataAnalyticsProcessingUnits * costPerProcessingUnitAnalytics;
  const dataTransferOutCost = dataTransferOutGB * costPerGBDataTransferOut;

  // Total cost
  return dataStreamsCost + putPayloadUnitsCost + dataFirehoseCost + dataAnalyticsCost + dataTransferOutCost;
}

//   // Example usage:
//   const kinesisUsage = {
//     dataStreamShards: 2,
//     shardHours: 720, // 2 shards running 24/7 for a 30-day month
//     putPayloadUnits: 5000000, // 5 million PUT Payload Units
//     dataFirehoseGB: 100, // 100 GB processed by Data Firehose
//     dataAnalyticsProcessingUnits: 500, // 500 Kinesis Data Analytics Processing Units
//     dataTransferOutGB: 150 // 150 GB data transferred out
//   };

//   const totalCost = calculateKinesisCost(kinesisUsage);
//   console.log(`Total Amazon Kinesis cost: $${totalCost.toFixed(2)}`);

/**
 * Calculates the cost of using AWS Glue.
 *
 * @param {object} params - The parameters for the AWS Glue usage.
 * @param {number} params.jobDPUHours - The number of Data Processing Units (DPUs) used by Glue jobs per month, multiplied by the hours those DPUs run.
 * @param {number} params.crawlerDPUHours - The number of DPUs used by Glue crawlers per month, multiplied by the hours those DPUs run.
 * @param {number} params.dataCatalogStorageGB - The amount of storage used by the Glue Data Catalog in gigabytes per month, beyond the free tier.
 * @param {number} params.dataCatalogRequests - The number of requests made to the Data Catalog per month, beyond the free tier.
 * @param {number} params.dataBrewRuns - The number of AWS Glue DataBrew job runs per month.
 * @return {number} The total cost of using AWS Glue in USD.
 *
 * Note: The pricing used in this example is simplified and based on generic values. For precise and up-to-date pricing,
 * always consult the official AWS documentation and pricing pages.
 */
export function calculateGlueCost({
  jobDPUHours,
  crawlerDPUHours,
  dataCatalogStorageGB,
  dataCatalogRequests,
  dataBrewRuns,
}) {
  // Cost factors (placeholders, adjust based on current pricing)
  const costPerJobDPUHour = 0.44; // Cost per DPU hour for Glue jobs
  const costPerCrawlerDPUHour = 0.44; // Cost per DPU hour for Glue crawlers
  const costPerGBDataCatalogStorage = 0.01; // Cost per GB of Data Catalog storage per month
  const costPerThousandDataCatalogRequests = 1.0; // Cost per 1,000 requests to the Data Catalog
  const costPerDataBrewRun = 0.48; // Cost per DataBrew job run

  // Calculating costs
  const jobDPUHoursCost = jobDPUHours * costPerJobDPUHour;
  const crawlerDPUHoursCost = crawlerDPUHours * costPerCrawlerDPUHour;
  const dataCatalogStorageCost = dataCatalogStorageGB * costPerGBDataCatalogStorage;
  const dataCatalogRequestsCost = (dataCatalogRequests / 1000) * costPerThousandDataCatalogRequests;
  const dataBrewRunsCost = dataBrewRuns * costPerDataBrewRun;

  // Total cost
  return jobDPUHoursCost + crawlerDPUHoursCost + dataCatalogStorageCost + dataCatalogRequestsCost + dataBrewRunsCost;
}

// // Example usage:
// const glueUsage = {
//   jobDPUHours: 100, // 100 DPU hours for Glue jobs
//   crawlerDPUHours: 50, // 50 DPU hours for Glue crawlers
//   dataCatalogStorageGB: 10, // 10 GB of Data Catalog storage
//   dataCatalogRequests: 100000, // 100,000 Data Catalog requests
//   dataBrewRuns: 200, // 200 DataBrew job runs
// };

// const totalCost = calculateGlueCost(glueUsage);
// console.log(`Total AWS Glue cost: $${totalCost.toFixed(2)}`);

/**
 * Calculates the cost of using AWS Athena.
 *
 * @param {object} params - The parameters for AWS Athena usage.
 * @param {number} params.dataScannedGB - The amount of data scanned by Athena queries in gigabytes.
 * @param {number} params.savedQueries - The number of saved queries, if any additional costs apply.
 * @param {number} params.dataTransferOutGB - The amount of data transferred out of AWS Athena to the internet in gigabytes.
 * @param {number} params.dataTransferRate - The cost per GB for data transfer out in USD.
 * @return {number} The total cost of using AWS Athena in USD.
 *
 * Note: The pricing used in this example is simplified and based on generic values. For precise and up-to-date pricing,
 * always consult the official AWS documentation and pricing pages.
 */
export function calculateAthenaCost({ dataScannedGB, savedQueries = 0, dataTransferOutGB, dataTransferRate }) {
  // Cost factors (placeholders, adjust based on current pricing)
  const costPerGBDataScanned = 5.0; // Cost per GB of data scanned by Athena queries, typically $5 per TB
  const costPerSavedQuery = 0; // Placeholder for any potential costs associated with saved queries
  const savedQueriesCost = savedQueries * costPerSavedQuery;

  // Calculating costs
  const dataScannedCost = dataScannedGB * costPerGBDataScanned;
  const dataTransferCost = dataTransferOutGB * dataTransferRate;

  // Total cost
  return dataScannedCost + savedQueriesCost + dataTransferCost;
}

// Example usage:
// const athenaUsage = {
//   dataScannedGB: 10, // 10 GB of data scanned
//   savedQueries: 0, // Example does not include saved queries cost
//   dataTransferOutGB: 100, // 100 GB data transferred out
//   dataTransferRate: 0.09 // Cost per GB for data transfer out
// };

// const totalCost = calculateAthenaCost(athenaUsage);
// console.log(`Total AWS Athena cost: $${totalCost.toFixed(2)}`);

/**
 * Calculates the cost of using AWS EMR.
 *
 * @param {object} params - The parameters for AWS EMR usage.
 * @param {number} params.masterInstanceHours - The total hours of master instance usage per month.
 * @param {number} params.masterInstanceRate - The hourly rate for the master instance type in USD.
 * @param {number} params.coreInstanceHours - The total hours of core instance usage per month.
 * @param {number} params.coreInstanceRate - The hourly rate for the core instance type in USD.
 * @param {number} params.taskInstanceHours - The total hours of task instance usage per month (optional).
 * @param {number} params.taskInstanceRate - The hourly rate for the task instance type in USD (optional).
 * @param {number} params.ebsVolumeGB - The total size of EBS volumes attached to the instances in gigabytes (optional).
 * @param {number} params.ebsRatePerGBMonth - The monthly cost per GB for the EBS volume in USD (optional).
 * @param {number} params.dataTransferOutGB - The amount of data transferred out of AWS EMR to the internet in gigabytes per month.
 * @param {number} params.dataTransferRate - The cost per GB for data transfer out in USD.
 * @return {number} The total cost of using AWS EMR in USD.
 *
 * Note: The pricing used in this example is simplified and based on generic values. For precise and up-to-date pricing,
 * always consult the official AWS documentation and pricing pages.
 */
export function calculateEMRCost({
  masterInstanceHours,
  masterInstanceRate,
  coreInstanceHours,
  coreInstanceRate,
  taskInstanceHours = 0,
  taskInstanceRate = 0,
  ebsVolumeGB = 0,
  ebsRatePerGBMonth = 0,
  dataTransferOutGB,
  dataTransferRate,
}) {
  // Calculating instance costs
  const masterInstanceCost = masterInstanceHours * masterInstanceRate;
  const coreInstanceCost = coreInstanceHours * coreInstanceRate;
  const taskInstanceCost = taskInstanceHours * taskInstanceRate;

  // Calculating EBS volume cost, if applicable
  const ebsCost = ebsVolumeGB * ebsRatePerGBMonth;

  // Calculating data transfer costs
  const dataTransferCost = dataTransferOutGB * dataTransferRate;

  // Total cost
  return masterInstanceCost + coreInstanceCost + taskInstanceCost + ebsCost + dataTransferCost;
}

// Example usage:
// const emrUsage = {
//   masterInstanceHours: 720, // 1 master instance running 24/7 for a 30-day month
//   masterInstanceRate: 0.2, // Hypothetical rate for the master instance type
//   coreInstanceHours: 1440, // 2 core instances running 24/7 for a 30-day month
//   coreInstanceRate: 0.2, // Hypothetical rate for the core instance type
//   taskInstanceHours: 720, // 1 task instance running 24/7 for a 30-day month (optional)
//   taskInstanceRate: 0.2, // Hypothetical rate for the task instance type (optional)
//   ebsVolumeGB: 1000, // 1 TB of EBS storage (optional)
//   ebsRatePerGBMonth: 0.1, // Hypothetical monthly cost per GB for EBS (optional)
//   dataTransferOutGB: 500, // 500 GB data transferred out
//   dataTransferRate: 0.09 // Cost per GB for data transfer out
// };

// const totalCost = calculateEMRCost(emrUsage);
// console.log(`Total AWS EMR cost: $${totalCost.toFixed(2)}`);

/**
 * Calculates the cost of using AWS OpenSearch.
 *
 * @param {object} params - The parameters for AWS OpenSearch usage.
 * @param {number} params.instanceHours - The total hours of instance usage per month.
 * @param {number} params.instanceTypeRate - The hourly rate for the chosen instance type in USD.
 * @param {number} params.storageGB - The amount of storage used in gigabytes per month.
 * @param {number} params.storageTypeRate - The rate per GB per month for the chosen storage type in USD.
 * @param {number} params.dataTransferOutGB - The amount of data transferred out of OpenSearch in gigabytes per month.
 * @param {number} params.ultraWarmStorageGB - The amount of UltraWarm storage used in gigabytes per month (if applicable).
 * @param {number} params.ultraWarmStorageRate - The rate per GB per month for UltraWarm storage in USD (if applicable).
 * @param {number} params.coldStorageGB - The amount of Cold Storage used in gigabytes per month (if applicable).
 * @param {number} params.coldStorageRate - The rate per GB per month for Cold Storage in USD (if applicable).
 * @return {number} The total cost of using AWS OpenSearch in USD.
 *
 * Note: The pricing used in this example is simplified and based on generic values. For precise and up-to-date pricing,
 * always consult the official AWS documentation and pricing pages.
 */
export function calculateOpenSearchCost({
  instanceHours,
  instanceTypeRate,
  storageGB,
  storageTypeRate,
  dataTransferOutGB,
  ultraWarmStorageGB,
  ultraWarmStorageRate,
  coldStorageGB,
  coldStorageRate,
}) {
  // Cost calculations
  const instanceCost = instanceHours * instanceTypeRate;
  const storageCost = storageGB * storageTypeRate;
  const dataTransferCost = calculateDataTransferCost(dataTransferOutGB); // Placeholder function for data transfer cost calculation
  const ultraWarmCost = ultraWarmStorageGB * ultraWarmStorageRate;
  const coldStorageCost = coldStorageGB * coldStorageRate;

  // Total cost
  return instanceCost + storageCost + dataTransferCost + ultraWarmCost + coldStorageCost;
}

/**
 * Placeholder function to calculate data transfer cost.
 * Implement based on AWS pricing or specific needs.
 * @param {number} dataTransferOutGB - The amount of data transferred out in gigabytes.
 * @return {number} The cost of data transfer in USD.
 */
export function calculateDataTransferCost(dataTransferOutGB) {
  // Placeholder for simplicity. Actual costs can vary based on regions and total volume.
  const costPerGB = 0.09; // Generic rate per GB for data transfer out
  return dataTransferOutGB * costPerGB;
}

// Example usage
// const openSearchUsage = {
//   instanceHours: 720, // 1 instance running 24/7 for a 30-day month
//   instanceTypeRate: 0.1, // Hypothetical rate for a specific instance type
//   storageGB: 500,
//   storageTypeRate: 0.1, // Hypothetical rate per GB for EBS storage
//   dataTransferOutGB: 100,
//   ultraWarmStorageGB: 1000,
//   ultraWarmStorageRate: 0.025,
//   coldStorageGB: 2000,
//   coldStorageRate: 0.015
// };

// const totalCost = calculateOpenSearchCost(openSearchUsage);
// console.log(`Total AWS OpenSearch cost: $${totalCost.toFixed(2)}`);
