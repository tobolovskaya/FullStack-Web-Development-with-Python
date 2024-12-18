import platform

import aiohttp
import asyncio


async def main():

    session = aiohttp.ClientSession()
    response = await session.get('https://python.org')

    print("Status:", response.status)
    print("Content-type:", response.headers['content-type'])

    html = await response.text()
    response.close()

    await session.close()
    return f"Body: {html[:15]}..."


if __name__ == "__main__":
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    r = asyncio.run(main())
    print(r)