import asyncio
import time
from pyppeteer import launch

async def main():
    browser = await launch()
    page = await browser.newPage()
    await page.goto('https://azgaar.github.io/Fantasy-Map-Generator')
    time.sleep(10)
    try:
        await page.click("button.ui-button.ui-corner-all.ui-widget")
    except:
        return
    time.sleep(20)
    await page.screenshot({'path': 'example.png'})
    await browser.close()

asyncio.get_event_loop().run_until_complete(main())