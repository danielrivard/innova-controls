import asyncio

import aiohttp

from innova_controls import Innova


async def main():

    async with aiohttp.ClientSession() as session:
        innova = Innova(session, "192.168.1.20", None, None)

        await innova.async_update()
        print(f"Ambient: {innova.ambient_temp}")
        # await innova.set_temperature(19)
        print(f"Temperature Step: {innova.temperature_step}")
        print(f"Target: {innova.target_temperature}")
        print(f"Name: {innova.name}")
        print(f"Current Mode: {innova.mode}")
        print(f"Powered: {innova.power}")
        print(f"Fan Speed: {innova.fan_speed}")
        print(f"Rotation: {innova.rotation}")
        print(f"Night Mode: {innova.night_mode}")


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
