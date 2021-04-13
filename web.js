const puppeteer = require('puppeteer');
var myArgs = process.argv.slice(2);


(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.goto('https://azgaar.github.io/Fantasy-Map-Generator');
  await new Promise(r => setTimeout(r, 2000));
  for (let i= 0; i < myArgs.length; i++){
    await page.$eval('button[id='+myArgs[i]+']', el => el.click());
  }
  await page.screenshot({ path: 'cache/map.png' });
  await browser.close();
})();