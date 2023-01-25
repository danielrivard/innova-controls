import aiohttp
import asyncio

from innova_controls import Innova

async def main():

    async with aiohttp.ClientSession() as session:
        innova = Innova(session, '192.168.1.20', None, None)

        result = await innova.async_update()
        print(f"Ambient: {innova.ambient_temp}")
        # await innova.set_temperature(19)
        print(f"Target: {innova.target_temperature}")
        print(f"Name: {innova.name}")
        print(f"Current Mode: {innova.mode}")
        print(f"Powered on: {innova.power}")


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
