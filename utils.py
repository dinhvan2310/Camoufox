import json
from concurrent.futures import ThreadPoolExecutor
import asyncio
from camoufox.sync_api import Camoufox
from camoufox.addons import DefaultAddons
import logging

def log_decorator(func):
    def wrapper(*args, **kwargs):
        logging.info(f"Calling function '{func.__name__}' with arguments {args} and keyword arguments {kwargs}")
        result = func(*args, **kwargs)
        logging.info(f"Function '{func.__name__}' returned {result}")
        return result
    return wrapper

logging.basicConfig(level=logging.INFO)

class Proxy:
    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    def __str__(self):
        return f"{self.host}:{self.port}:{self.username}:{self.password}"

@log_decorator
def get_config():
    with open('config.json', 'r') as file:
        return json.load(file)

@log_decorator
def get_proxies():
    with open('proxies.txt', 'r') as file:
        proxies = file.readlines()
        return [proxy.strip() for proxy in proxies]

@log_decorator
def get_profiles_path():
    with open('profiles.txt', 'r') as file:
        profiles = file.readlines()
        if not profiles:
            return []
        return [profile.strip() for profile in profiles]

@log_decorator
def create_profile(proxy: Proxy, profile_path: str, profile_name: str):
    print(f'Creating profile {profile_name} with proxy {proxy}')
    with Camoufox(
        os=('windows', 'macos', 'linux'),
        exclude_addons=[DefaultAddons.UBO],
        geoip=True,
        proxy={
            'server': f'{proxy.host}:{proxy.port}',
            'username': f'{proxy.username}',
            'password': f'{proxy.password}',
        },
        persistent_context=True,
        user_data_dir=f'/{profile_path}/{profile_name}',
        headless=True,
    ) as camoufox:
        page = camoufox.new_page()

@log_decorator  
async def create_profiles(
    num_profiles: int = 0,
    profile_path: str = 'camoufox/profiles',
    proxies: list[Proxy] = [],
    num_threads: int = 10
):
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        loop = asyncio.get_event_loop()
        tasks = []
        for i in range(num_profiles):
            if i >= len(proxies):
                break
            tasks.append(loop.run_in_executor(executor, create_profile, proxies[i], profile_path, f'profile_{i}'))
        await asyncio.gather(*tasks)
    return [f'/{profile_path}/profile_{i}' for i in range(num_profiles)]