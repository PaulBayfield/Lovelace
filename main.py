from Lovelace import Bot

import asyncio


from os import environ
from dotenv import load_dotenv
from aiohttp import ClientSession


load_dotenv(dotenv_path=f".env")


async def main():
    client = Bot()

    async with ClientSession() as session:
        async with client:
            client.session = session
            client.ssl = False
            await client.run()
            await client.start(environ["TOKEN"], reconnect=True)


asyncio.run(main())
