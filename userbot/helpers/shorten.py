from userbot import YOURLS_URL, YOURLS_KEY

from yourls import YOURLSClient
from yourls.exceptions import YOURLSURLExistsError, YOURLSKeywordExistsError
import aiohttp


async def shorten_url(url, keyword):
    if not YOURLS_URL or not YOURLS_KEY:
        return "API ERROR"
    
    url_checked = await url_check(url)
    if url_checked:
        yourls = YOURLSClient(YOURLS_URL, signature=YOURLS_KEY)
        try:
            shorturl = yourls.shorten(url, keyword).shorturl
            result = shorturl
        except YOURLSURLExistsError:
            shorturl = yourls.expand(url)
            result = shorturl
        except YOURLSKeywordExistsError:
            result = "KEYWORD Exists"
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
