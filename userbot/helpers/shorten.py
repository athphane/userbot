from userbot import YOURLS_URL, YOURLS_KEY

from yourls import YOURLSClient
import aiohttp


async def shorten_url(url, keyword):
    if not YOURLS_URL or not YOURLS_KEY:
        return "API ERROR"

    if url_check(url):
        yourls = YOURLSClient(YOURLS_URL, signature=YOURLS_KEY)

    try:
        shorturl = yourls.shorten(url, keyword).shorturl
    except yourls.exceptions.YOURLSURLExistsError:
        shorturl = yourls.expand(url)
        result = shorturl
    else:
        result = "INVALID URL"

    return result


async def url_check(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                return resp.status == 200
    except aiohttp.ClientError:
        return False
