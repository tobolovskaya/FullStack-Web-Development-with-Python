import platform

import aiohttp
import asyncio
from uuid import uuid4


async def main():
    async with aiohttp.ClientSession() as session:
        async with session.post('http://localhost:5000', data={"message": "Hello world!"}, ssl=False) as response:

            print("Status:", response.status)
            html = await response.text()
            return f"Body: {html}"


if __name__ == "__main__":
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    r = asyncio.run(main())
    print(r)