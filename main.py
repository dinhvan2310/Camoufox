from camoufox.async_api import AsyncCamoufox
import asyncio
from camoufox.addons import DefaultAddons
from camoufox_utils import profiles
from utils import get_proxies, Proxy, get_config, get_profiles_path, create_profiles
import logging
import CustomFormatter
import logging
import datetime

# Create custom logger logging all five levels
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fmt = '%(asctime)s | %(levelname)8s | %(message)s'
stdout_handler = logging.StreamHandler()
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.setFormatter(CustomFormatter.CustomFormatter(fmt))
today = datetime.date.today()
file_handler = logging.FileHandler('my_app_{}.log'.format(today.strftime('%Y_%m_%d')))
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter(fmt))

# Add both handlers to the logger
logger.addHandler(stdout_handler)
logger.addHandler(file_handler)


async def run_profile(
    proxy: Proxy,
    profile_path: str = '/camoufox/profiles/default',
):
    async with AsyncCamoufox(
        os=('windows', 'macos', 'linux'),
        humanize=True,
        exclude_addons=[DefaultAddons.UBO],
        geoip=True,
        proxy={
            'server': f'{proxy.host}:{proxy.port}',
            'username': f'{proxy.username}',
            'password': f'{proxy.password}',
        },
        persistent_context=True,
        user_data_dir=profile_path,
    ) as browser:
        page = await browser.new_page()
        # await page.goto('https://wallet.litas.io/invite/trandinhvan')
        # await page.locator("//input[@id='repeatedPassword']").click()
        # await page.keyboard.press("Tab")
        # await page.keyboard.press("Tab")
        # await page.keyboard.press("Tab")
        # await page.keyboard.press("Tab")
        # await page.keyboard.press("Tab")

        # await page.keyboard.press("Space")
        await asyncio.sleep(5000)

# asyncio.run(main())

async def main():
    logger.log(logging.INFO, 'Tool auto kèo Litas.io by NEZUKO .....')
    config = get_config()
    proxies_txt = get_proxies()
    proxies = []
    for proxy in proxies_txt:
        proxies.append(Proxy(*proxy.split(':')))

    profiles = get_profiles_path()
    
    logger.log(logging.INFO, f'Found {len(proxies)} proxies')
    logger.log(logging.INFO, f'Found {len(profiles)} profiles')

    if len(profiles) == 0:
        logger.log(logging.WARNING, f'No profiles found, creating {config["num_profiles"]} profiles')
        profiles = await create_profiles(
            config['num_profiles'],
            config['profile_path'],
            proxies,
            config['num_threads']
        )
        logger.log(logging.INFO, f'Created {len(profiles)} profiles, writing to profiles.txt')
        with open('profiles.txt', 'w') as f:
            for profile in profiles:
                f.write(f"{profile}\n")
        logger.log(logging.INFO, 'Profiles written to profiles.txt')
    
    logger.log(logging.INFO, 'Running profiles')

if __name__ == '__main__':
    asyncio.run(main())
