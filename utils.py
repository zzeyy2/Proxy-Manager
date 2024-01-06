import aiofiles
from typing import Union
from pathlib import Path


async def read_proxy_file(file_path: Union[str, Path]):
    async with aiofiles.open(file_path, "r", encoding="utf-8") as async_file:
        return [_.rstrip() for _ in (await async_file.read()).split("\n")]


async def get_proxies_for_clients(clients_len: int, proxies: list = []):
    try:
        for _ in range(clients_len - len(proxies)):
            proxies.append(proxies[_ % len(proxies)])

        return proxies
    except ZeroDivisionError:
        return None


def process_scheme(scheme: str) -> str:
    if "//" not in scheme or r"\\" not in scheme:
        scheme = f'{scheme}{":" if not ":" in scheme else ""}//'
    scheme = scheme.replace("https", "http")
    return scheme


def format_proxy_url(url):
    if "@" in url:
        url_splitted = url.split("//")
        scheme = url_splitted[0]
        url_splitted = url_splitted[1].split("@")
        for part in url_splitted:
            if part.count(".") >= 3:
                ip_port = part
            else:
                login_pass = part
        formatted_url = f"{process_scheme(scheme)}{login_pass}@{ip_port}"
    else:
        url_splitted = url.split(":")
        scheme = url_splitted[0]
        url_splitted = [
            f"{url_splitted[-4]}:{url_splitted[-3]}",
            f"{url_splitted[-2]}:{url_splitted[-1]}",
        ]
        for part in url_splitted:
            if part.count(".") >= 3:
                ip_port = part
            else:
                login_pass = part

        formatted_url = f"{process_scheme(scheme)}{login_pass}@{ip_port}"

    return formatted_url
