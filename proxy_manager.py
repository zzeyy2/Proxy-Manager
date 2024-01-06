from . import Proxy, utils
from typing import List, NoReturn
from pathlib import Path
from secrets import choice
from telethon import TelegramClient


class ProxyManager:
    def __init__(self, proxies_file_path: Path):
        self.proxies_file_path = proxies_file_path
        self.proxies: List[Proxy]

    async def read_proxies_file(self) -> NoReturn:
        self.proxies = [
            Proxy(url) for url in await utils.read_proxy_file(self.proxies_file_path)
        ]

    def get_random_proxy(self) -> Proxy:
        return choice(self.proxies)

    async def check_proxies(self) -> NoReturn:
        self.proxies = [proxy for proxy in self.proxies if await proxy.check_proxy()]

    async def get_proxies_for_clients(
        self, clients: List[TelegramClient]
    ) -> List[Proxy]:
        await self.check_proxies()
        return await utils.get_proxies_for_clients(len(clients), self.proxies)
