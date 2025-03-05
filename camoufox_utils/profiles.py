from camoufox.async_api import AsyncCamoufox
import asyncio
from camoufox.addons import DefaultAddons
from utils import get_proxies, get_config, Proxy

async def create_profile(proxy: Proxy, profile_path_folder: str, profile_name_prefix: str, index: int):
    async with AsyncCamoufox(
        os=('windows', 'macos', 'linux'),
        exclude_addons=[DefaultAddons.UBO],
        geoip=True,
        proxy={
            'server': f'{proxy.host}:{proxy.port}',
            'username': f'{proxy.username}',
            'password': f'{proxy.password}',
        },
        persistent_context=True,
        user_data_dir=f'/{profile_path_folder}/{profile_name_prefix}_{index}',
        headless=True,
    ) as camoufox:
        page = await camoufox.new_page()

async def create_profiles(
    proxies: list,
    number_of_threads: int,
    profile_path_folder: str = '/camoufox/profiles',
    profile_name_prefix: str = 'profile',
):
    tasks = []
    for i, proxy in enumerate(proxies):
        if i >= number_of_threads:
            await asyncio.gather(*tasks)
            tasks = []
        tasks.append(create_profile(proxy, profile_path_folder, profile_name_prefix, i))

    if tasks:
        await asyncio.gather(*tasks)
    
if __name__ == '__main__':
    proxies_txt = get_proxies()
    proxies = []
    for proxy in proxies_txt:
        proxies.append(Proxy(*proxy.split(':')))

    config = get_config()
    asyncio.run(create_profiles(proxies, config['number_of_threads']))