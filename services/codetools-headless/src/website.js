const { createHash, getPublicUrl, uploadToS3 } = require("./utils/storage");
const { checkUrl } = require("./utils/validation");
const { downloadPage } = require("./utils/browser");
exports.handler = async (event, context) => {
  const { url, mode = "content" } = event?.queryStringParameters || {};

  if (!url) {
    return { statusCode: 400, body: "No url query specified." };
  }
  if (!checkUrl(url)) {
    return { statusCode: 400, body: "Invalid url query specified." };
  }

  const hash = createHash(url);
  const s3Key = `downloads/${hash}/index.html`;

  try {
    const content = await downloadPage(url, mode);
    await uploadToS3(s3Key, content);

    const publicUrl = await getPublicUrl(s3Key);

    return {
      statusCode: 200,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: "Content downloaded and stored on S3", url: publicUrl, path: s3Key }),
    };
  } catch (error) {
    console.error(error);
    return {
      statusCode: 500,
      body: JSON.stringify({ error: "The server encountered an error." }),
    };
  }
};
