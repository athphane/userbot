import aiohttp


class Spacex:
    @staticmethod
    async def get(latest_or_next):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://api.spacexdata.com/v3/launches/{latest_or_next}"
            ) as resp:
                data = await resp.json()
        return data

    async def latest(self):
        return await self.get("latest")

    async def next(self):
        return await self.get("next")
