from camoufox.async_api import AsyncCamoufox
import asyncio

async def main():
    async with AsyncCamoufox(
        os=('windows', 'macos', 'linux'),
        
        humanize=True,
    ) as browser:
        page = await browser.new_page()
        # await page.goto('moz-extension://618b1d5b-9ba1-4081-82e0-f5fa5771f8c3/home.html#onboarding/welcome')
        await asyncio.sleep(500)

asyncio.run(main())