import platform

import aiohttp
import asyncio


async def index(session):
    url = 'https://python.org'
    async with session.get(url) as response:
        print("Status:", response.status)
        print("Content-type:", response.headers['content-type'])

        html = await response.text()
        return f"Body: {html[:15]}..."


async def doc(session):
    url = "https://www.python.org/doc/"
    async with session.get(url) as response:
        print("Status:", response.status)
        print("Content-type:", response.headers['content-type'])

        html = await response.text()
        return f"Body: {html[:15]}..."


async def main():
    async with aiohttp.ClientSession() as session:
        result = await asyncio.gather(index(session), doc(session))
        return result


if __name__ == "__main__":
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    r = asyncio.run(main())
    print(r)