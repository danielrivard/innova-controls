import logging
from typing import List

from aiohttp import ClientSession

from innova_controls.constants import UNKNOWN_MODE
from innova_controls.fan_speed import FanSpeed
from innova_controls.innova_device import InnovaDevice
from innova_controls.innova_factory import InnovaFactory
from innova_controls.mode import Mode
from innova_controls.network_functions import NetWorkFunctions

_LOGGER = logging.getLogger(__name__)


class Innova:
    """This is a class to control Innova heat pump units over http

    Attributes:
        For Local Mode
        host: str
            IP address of the Innova unit on the local network.
            If omitted, cloud mode is assumed

        For Cloud Mode (both serial and uid are mandatory)
        serial: str
            Serial number of the Innova unit (usually looks like INXXXXXXX)
        uid: str)
            The MAC address of the Innova unit.
    """

    def __init__(
        self,
        http_session: ClientSession,
        host: str = None,
        serial: str = None,
        uid: str = None,
    ):
        _LOGGER.info(
            f"Initialize Innova Controls with host={host}, "
            "serial={serial}, uid={uid}"
        )

        self._network_facade = NetWorkFunctions(http_session, host, serial, uid)
        self._innova_device: InnovaDevice = None

    async def async_update(self) -> bool:
        data: dict = await self._network_facade.get_status()

        if data:
            if self._innova_device is None:
                self._innova_device = InnovaFactory.get_device(
                    data["deviceType"], self._network_facade
                )
            self._innova_device.set_data(data)
            _LOGGER.debug(f"Received: {data}")
            return True
        else:
            _LOGGER.error(f"Error retrieving unit status")
            return False

    @property
    def ambient_temp(self) -> float:
        if self._innova_device:
            return self._innova_device.ambient_temp
        return 0

    @property
    def target_temperature(self) -> float:
        if self._innova_device:
            return self._innova_device.target_temperature
        return 0

    @property
    def temperature_step(self) -> float:
        if self._innova_device:
            return self._innova_device.temperature_step
        return 1.0

    @property
    def min_temperature(self) -> float:
        if self._innova_device:
            return self._innova_device.min_temperature
        return 0

    @property
    def max_temperature(self) -> float:
        if self._innova_device:
            return self._innova_device.max_temperature
        return 0

    @property
    def power(self) -> bool:
        if self._innova_device:
            return self._innova_device.power
        return False

    @property
    def mode(self) -> Mode:
        if self._innova_device:
            return self._innova_device.mode
        return UNKNOWN_MODE

    @property
    def supported_modes(self) -> List[Mode]:
        if self._innova_device:
            return list(self._innova_device.Modes.get_supported_modes())
        return []

    @property
    def rotation(self) -> bool:
        if self._innova_device:
            return self._innova_device.rotation
        return False

    @property
    def fan_speed(self) -> FanSpeed:
        if self._innova_device:
            return self._innova_device.fan_speed
        return 0

    @property
    def supported_fan_speeds(self) -> List[FanSpeed]:
        if self._innova_device:
            return self._innova_device.supported_fan_speeds
        return []

    @property
    def night_mode(self) -> bool:
        if self._innova_device:
            return self._innova_device.night_mode
        return False

    @property
    def name(self) -> str:
        if self._innova_device:
            return self._innova_device.name
        return None

    @property
    def serial(self) -> str:
        if self._innova_device:
            return self._innova_device.serial
        return None

    @property
    def uid(self) -> str:
        if self._innova_device:
            return self._innova_device.uid
        return None

    @property
    def software_version(self) -> str:
        if self._innova_device:
            return self._innova_device.software_version
        return None

    @property
    def ip_address(self) -> str:
        if self._innova_device:
            return self._innova_device.ip_address
        return None

    async def power_on(self) -> bool:
        if self._innova_device:
            return await self._innova_device.power_on()
        return False

    async def power_off(self) -> bool:
        if self._innova_device:
            return await self._innova_device.power_off()
        return False

    async def rotation_on(self) -> bool:
        if self._innova_device:
            return await self._innova_device.rotation_on()
        return False

    async def rotation_off(self) -> bool:
        if self._innova_device:
            return await self._innova_device.rotation_off()
        return False

    async def night_mode_on(self) -> bool:
        if self._innova_device:
            return await self._innova_device.night_mode_on()
        return False

    async def night_mode_off(self) -> bool:
        if self._innova_device:
            return await self._innova_device.night_mode_off()
        return False

    async def set_temperature(self, temperature: float) -> bool:
        if self._innova_device:
            return await self._innova_device.set_temperature(temperature)
        return False

    async def set_fan_speed(self, speed: FanSpeed) -> bool:
        if self._innova_device:
            return await self._innova_device.set_fan_speed(speed)
        return False

    async def set_heating(self) -> bool:
        return await self._innova_device.set_heating()

    async def set_cooling(self) -> bool:
        return await self._innova_device.set_cooling()

    async def set_dehumidifying(self) -> bool:
        return await self._innova_device.set_dehumidifying()

    async def set_fan_only(self) -> bool:
        return await self._innova_device.set_fan_only()

    async def set_auto(self) -> bool:
        return await self._innova_device.set_auto()

    @property
    def supports_target_temp(self) -> bool:
        return self._innova_device.supports_target_temp

    @property
    def supports_swing(self) -> bool:
        return self._innova_device.supports_swing

    @property
    def supports_fan(self) -> bool:
        return self._innova_device.supports_fan

    @property
    def supports_preset(self) -> bool:
        return self._innova_device.supports_preset
