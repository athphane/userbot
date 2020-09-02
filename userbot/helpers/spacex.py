import aiohttp


class Spacex:
    @staticmethod
    async def get_latest():
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.spacexdata.com/v3/launches/latest") as resp:
                data = await resp.json()
        return data

    @staticmethod
    async def get_next():
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.spacexdata.com/v3/launches/next") as resp:
                data = await resp.json()
        return data
