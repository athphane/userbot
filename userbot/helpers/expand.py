import requests

def expand_url(url):
    expanded = requests.get(f"http://expandurl.com/api/v1/?url={url}").text
    return expanded if expanded != "false" else None
