import asyncio
import aiohttp


async def wait_api_ready(url: str) -> None:
    """Waiting for the fastapi application to launch.

    Args:
        url (str): FastAPI app url.
    """
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                async with session.get(url=url) as response:
                    if response.status == 200:
                        return
            except aiohttp.ClientError:
                pass

            await asyncio.sleep(0.2)
