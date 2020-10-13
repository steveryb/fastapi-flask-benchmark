import aiohttp
import requests

from . import constants

_async_session = None
session = None


def get_async_session():
    global _async_session
    if _async_session is None:
        _async_session = aiohttp.ClientSession()
    return _async_session


def get_sync_session():
    global _async_session
    if _async_session is None:
        _async_session = requests.session()
    return _async_session


def make_sync_request(url):
    return get_sync_session().get(url)


async def make_async_request(url):
    session = get_async_session()
    async with session.get(url) as response:
        return await response.text()


def make_sync_wait_request():
    return make_sync_request(constants.WAIT_URL)


async def make_async_wait_request():
    return make_async_request(constants.WAIT_URL)
