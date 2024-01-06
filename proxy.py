from .utils import format_proxy_url
from urllib.parse import urlparse
from aiohttp import ClientSession
from aiohttp_proxy import ProxyConnector
from aiohttp.client_exceptions import (
    ClientProxyConnectionError,
    ClientHttpProxyError,
    ClientConnectorError,
    ClientConnectionError,
)
from contextlib import suppress

# from core.utils.logger import log
# log() must be any logging func. Like:
# print() or logging.info() etc.

def log(msg):
    print(msg)


class Proxy:
    def __init__(self, url: str):
        self.url = url
        self.parse_url()
        self.valid: bool = None
        self.aiohttp_type: bool = None
        self.telethon_type: bool = None
        self.convert_to_aiohttp()
        self.convert_to_telethon()

    def parse_url(self):
        self.default_format = format_proxy_url(self.url)
        parsed_url = urlparse(self.default_format)

        self.scheme = parsed_url.scheme
        self.ip = parsed_url.hostname
        self.port = int(parsed_url.port)
        self.username = parsed_url.username
        self.password = parsed_url.password

    async def check_proxy(self) -> bool:
        try:
            if not self.aiohttp_type:
                self.convert_to_aiohttp()
            log.info(f"Checking proxy: {self.url}")
            async with ClientSession(
                connector=ProxyConnector.from_url(self.aiohttp_type)
            ) as session:
                async with session.get("https://ipinfo.io/json") as responce:
                    jsn = await responce.json()
                    if self.ip == str(jsn["ip"]):
                        self.valid = True
                        log.info(f"Proxy {self.url} is valid")
                        return True
                    else:
                        self.valid = False
                        log.warning(f"Proxy {self.url} is invalid")
                        return False

        except (
            ClientProxyConnectionError,
            ClientHttpProxyError,
            ClientConnectorError,
            ClientConnectionError,
        ):
            log.warning(f"Proxy {self.url} is invalid")
            self.valid = False
            return False

    def convert_to_aiohttp(self) -> str:
        self.aiohttp_type = (
            f"{self.scheme}://{self.username}:{self.password}@{self.ip}:{self.port}"
        )

    def convert_to_telethon(self, rdns: bool = True):
        with suppress(ValueError):
            if not self.telethon_type:
                self.telethon_type = {
                    "proxy_type": self.scheme,
                    "addr": self.ip,
                    "port": int(self.port),
                    "username": self.username,
                    "password": self.password,
                    "rdns": rdns,
                }
            return self.telethon_type
