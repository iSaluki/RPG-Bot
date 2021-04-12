const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.goto('https://azgaar.github.io/Fantasy-Map-Generator');
  await new Promise(r => setTimeout(r, 1250));
  await page.screenshot({ path: 'map.png' });
  await browser.close();
})();