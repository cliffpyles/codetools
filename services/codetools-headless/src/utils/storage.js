const crypto = require("crypto");
const { PassThrough } = require("stream");
const { S3Client, PutObjectCommand, HeadObjectCommand, GetObjectCommand } = require("@aws-sdk/client-s3");
const { Upload } = require("@aws-sdk/lib-storage");
const { getSignedUrl } = require("@aws-sdk/s3-request-presigner");
const s3Client = new S3Client({ region: process.env.AWS_REGION });
const bucketName = process.env.S3_BUCKET_NAME;

function createHash(input) {
  return crypto.createHash("sha256").update(input).digest("hex");
}

async function checkIfScreenshotExists(key) {
  try {
    await s3Client.send(
      new HeadObjectCommand({
        Bucket: bucketName,
        Key: key,
      })
    );
    return true;
  } catch (err) {
    return false;
  }
}

async function saveToS3(key, body) {
  const command = new PutObjectCommand({
    Bucket: bucketName,
    Key: key,
    Body: body,
  });
  try {
    const response = await s3Client.send(command);
    return response;
  } catch (err) {
    console.error("Error storing object in S3:", err);
    throw err;
  }
}

async function streamToS3(key, bodyStream) {
  try {
    const upload = new Upload({
      client: s3Client,
      params: {
        Bucket: bucketName,
        Key: key,
        Body: bodyStream,
      },
    });

    await upload.done();
    console.log(`Stream upload completed successfully to ${key}`);
  } catch (err) {
    console.error("Error streaming object to S3:", err);
    throw err;
  }
}

async function uploadToS3(key, body) {
  const pass = new PassThrough();
  const uploadPromise = streamToS3(key, pass);
  pass.write(body);
  pass.end();
  await uploadPromise;
}

async function getPublicUrl(s3Key) {
  const presignedUrl = await getSignedUrl(
    s3Client,
    new GetObjectCommand({
      Bucket: bucketName,
      Key: s3Key,
    }),
    { expiresIn: 3600 }
  ); // URL expires in 1 hour

  return presignedUrl;
}

module.exports = { createHash, checkIfScreenshotExists, saveToS3, uploadToS3, getPublicUrl };
