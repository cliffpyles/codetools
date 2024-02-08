const { getScreenshot } = require("./utils/browser");
const { createHash, checkIfScreenshotExists, saveToS3 } = require("./utils/storage");
const { checkUrl } = require("./utils/validation");

exports.handler = async (event, context) => {
  const { url, ratio, force } = event?.queryStringParameters || {};

  if (!url) {
    return { statusCode: 400, body: "No url query specified." };
  }
  if (!checkUrl(url)) {
    return { statusCode: 400, body: "Invalid url query specified." };
  }

  const hash = createHash(url);
  const s3Key = `screenshots/${hash}.png`;

  try {
    const exists = await checkIfScreenshotExists(s3Key);
    if (exists && !force) {
      return {
        statusCode: 200,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: "Screenshot already exists", path: s3Key }),
      };
    }

    const screenshot = await getScreenshot(url, ratio);
    const s3Response = await saveToS3(s3Key, screenshot);
    return {
      statusCode: 200,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: "Screenshot taken and stored on S3", s3Response, path: s3Key }),
    };
  } catch (error) {
    console.error(error);
    return {
      statusCode: 500,
      body: JSON.stringify({ error: "The server encountered an error." }),
    };
  }
};
