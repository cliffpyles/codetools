const { S3Client, PutObjectCommand, HeadObjectCommand } = require("@aws-sdk/client-s3");
const chromium = require("@sparticuz/chromium-min");
const puppeteer = require("puppeteer-core");
const crypto = require("crypto");
const s3Client = new S3Client({ region: process.env.AWS_REGION });
const bucketName = process.env.S3_BUCKET_NAME;

let _page;

async function getBrowser() {
  return puppeteer.launch({
    args: [...chromium.args, "--hide-scrollbars", "--disable-web-security"],
    defaultViewport: chromium.defaultViewport,
    executablePath: await chromium.executablePath(
      `https://github.com/Sparticuz/chromium/releases/download/v121.0.0/chromium-v121.0.0-pack.tar`
    ),
    headless: chromium.headless,
    ignoreHTTPSErrors: true,
  });
}

async function getPage() {
  if (_page) return _page;
  const browser = await getBrowser();
  _page = await browser.newPage();
  return _page;
}

function checkUrl(string) {
  try {
    new URL(string);
  } catch (error) {
    return false;
  }
  return true;
}

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
    // If the command doesn't throw an error, the object exists.
    return true;
  } catch (err) {
    // If the object doesn't exist, an error is thrown.
    return false;
  }
}

async function storeOnS3(key, body) {
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

async function getScreenshot(url, ratio = 1) {
  const page = await getPage();
  await page.goto(url, {
    waitUntil: "domcontentloaded",
  });
  await page.setViewport({
    width: 1000,
    height: 600,
    devicePixelRatio: ratio,
  });
  const file = await page.screenshot();
  return file;
}

exports.screenshotHandler = async (event, context) => {
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
    const s3Response = await storeOnS3(s3Key, screenshot);
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
