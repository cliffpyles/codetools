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
function calculateKinesisCost({
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
function calculateGlueCost({ jobDPUHours, crawlerDPUHours, dataCatalogStorageGB, dataCatalogRequests, dataBrewRuns }) {
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
