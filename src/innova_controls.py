import logging

from aiohttp import ClientSession

from innova_device import InnovaDevice
from innova_factory import InnovaFactory
from network_facade import NetWorkFacade

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

    def __init__(self,
        http_session: ClientSession,
        host: str = None,
        serial: str = None,
        uid: str = None,
    ):
        _LOGGER.info(
            f"Initialize Innova Controls with host={host}, "
            "serial={serial}, uid={uid}"
        )

        self._network_facade = NetWorkFacade(http_session, host, serial, uid)
        self._device_manager: InnovaDevice = None

    async def async_update(self) -> bool:
        data: dict = await self._network_facade.get_status()

        if data:
            if self._device_manager is None:
                self._device_manager = InnovaFactory.get_device(data["deviceType"], self._network_facade)
            self._device_manager.set_data(data) 
            _LOGGER.debug(f"Received: {data}")
            return True
        else:
            _LOGGER.error(f"Error retrieving unit status")
            return False

    @property
    def ambient_temp(self) -> int:
        if self._device_manager:
            return self._device_manager.ambient_temp
        return 0

    @property
    def target_temperature(self) -> int:
        if self._device_manager:
            return self._device_manager.target_temperature
        return 0

    @property
    def min_temperature(self) -> int:
        if self._device_manager:
            return self._device_manager.min_temperature
        return 0

    @property
    def max_temperature(self) -> int:
        if self._device_manager:
            return self._device_manager.max_temperature
        return 0

    @property
    def power(self) -> bool:
        if self._device_manager:
            return self._device_manager.power
        return False

    @property
    def mode(self) -> InnovaDevice.Mode:
        if self._device_manager:
            return self._device_manager.mode
        return InnovaDevice.Mode.UNKNOWN

    @property
    def rotation(self) -> bool:
        if self._device_manager:
            return self._device_manager.rotation
        return False

    @property
    def fan_speed(self) -> int:
        if self._device_manager:
            return self._device_manager.fan_speed
        return 0

    @property
    def night_mode(self) -> bool:
        if self._device_manager:
            return self._device_manager.night_mode
        return False

    @property
    def name(self) -> str:
        if self._device_manager:
            return self._device_manager.name
        return None

    @property
    def serial(self) -> str:
        if self._device_manager:
            return self._device_manager.serial
        return None

    @property
    def uid(self) -> str:
        if self._device_manager:
            return self._device_manager.uid
        return None

    @property
    def software_version(self) -> str:
        if self._device_manager:
            return self._device_manager.software_version
        return None

    @property
    def ip_address(self) -> str:
        if self._device_manager:
            return self._device_manager.ip_address
        return None

    async def power_on(self) -> bool:
        if self._device_manager:
            return await self._device_manager.power_on()
        return False

    async def power_off(self) -> bool:
        if self._device_manager:
            return await self._device_manager.power_off()
        return False

    async def rotation_on(self) -> bool:
        if self._device_manager:
            return await self._device_manager.rotation_on()
        return False

    async def rotation_off(self) -> bool:
        if self._device_manager:
            return await self._device_manager.rotation_off()
        return False

    async def night_mode_on(self) -> bool:
        if self._device_manager:
            return await self._device_manager.night_mode_on()
        return False

    async def night_mode_off(self) -> bool:
        if self._device_manager:
            return await self._device_manager.night_mode_off()
        return False

    async def set_temperature(self, temperature: int) -> bool:
        if self._device_manager:
            return await self._device_manager.set_temperature(temperature)
        return False

    async def set_fan_speed(self, speed: int) -> bool:
        if self._device_manager:
            return await self._device_manager.set_fan_speed(speed)
        return False

    async def set_mode(self, mode: InnovaDevice.Mode) -> bool:
        if self._device_manager:
            return await self._device_manager.set_mode(mode)
        return False
