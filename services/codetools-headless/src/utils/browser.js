const chromium = require("@sparticuz/chromium-min");
const puppeteer = require("puppeteer-core");

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

async function downloadPage(url, mode) {
  try {
    const page = await getPage();
    await page.goto(url, { waitUntil: "networkidle0" });
    let artifact;

    if (mode === "snapshot") {
      const cdp = await page.target().createCDPSession();
      const { data } = await cdp.send("Page.captureSnapshot", { format: "mhtml" });
      artifact = data;
    } else if (mode === "content") {
      artifact = await page.content();
    } else {
      artifact = await page.content();
    }
    console.log(`Page downloaded successfully `);

    return artifact;
  } catch (err) {
    console.error("Error downloading page:", err);
    throw err;
  }
}

module.exports = { getPage, getScreenshot, downloadPage };
