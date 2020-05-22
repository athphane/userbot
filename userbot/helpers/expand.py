import requests_async as requests

async def expand_url(url):
    request = await requests.get(f"http://expandurl.com/api/v1/?url={url}")
    expanded = request.text
    if expanded != "false":
        return expanded
    else:
        return None
