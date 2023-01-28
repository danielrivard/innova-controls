import asyncio

import aiohttp
from innova_controls.fan_speed import FanSpeed

from innova_controls.innova import Innova


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
        print(f"Fan Speed: {innova.fan_speed.name}")
        print(f"Rotation: {innova.rotation}")
        print(f"Night Mode: {innova.night_mode}")
        modes = []
        print (innova.supported_modes)
        for mode in innova.supported_modes:
            if mode.is_cooling:
                modes.append("HVACMode.COOL")
            elif mode.is_heating:
                modes.append("HVACMode.HEAT")
            elif mode.is_dehumidifying:
                modes.append("HVACMode.DRY")
            elif mode.is_fan_only:
                modes.append("HVACMode.FAN_ONLY")
            elif mode.is_auto:
                modes.append("HVACMode.HEAT_COOL")
        print(modes)
        print(innova.supported_fan_speeds)

        # await innova.set_fan_speed(FanSpeed.AUTO)
        # print(innova.fan_speed)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
