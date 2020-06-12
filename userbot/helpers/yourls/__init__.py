import time
from hashlib import md5

from userbot import YOURLS_KEY, YOURLS_URL


class Yourls:
    def __init__(self):
        self.token = YOURLS_KEY
        self.url = YOURLS_URL

    def signature(self):
        time = self.time()
        return time, md5(f"{time}{self.token}".encode('utf-8')).hexdigest()

    @staticmethod
    def time():
        return int(time.time())

    def base_url(self):
        time, signature = self.signature()
        return f"{self.url}?timestamp={time}&signature={signature}&action="

    def shorten(self, url):
        pass
