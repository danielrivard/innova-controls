import logging
from abc import ABC, abstractmethod
from typing import List

from innova_controls.constants import (
    CMD_POWER_OFF,
    CMD_POWER_ON,
    MAX_TEMP,
    MIN_TEMP,
    UNKNOWN_MODE,
)
from innova_controls.fan_speed import FanSpeed
from innova_controls.mode import Mode
from innova_controls.network_functions import NetWorkFunctions

_LOGGER = logging.getLogger(__name__)


class InnovaDevice(ABC):
    class Modes(ABC):
        codes: dict = None

        @classmethod
        def get_supported_modes(cls) -> List[Mode]:
            return cls.codes.values()

        @classmethod
        def get_mode(cls, code: int) -> Mode:
            if code in cls.codes:
                return cls.codes[code]
            else:
                return UNKNOWN_MODE

    def __init__(self, network_facade: NetWorkFunctions) -> None:
        super().__init__()
        self._network_facade = network_facade
        self._data = {}
        self._status = {}

    def set_data(self, data: dict) -> None:
        self._data = data
        if self._data["success"] and "RESULT" in self._data:
            # We don't need the password, so obfuscate it to avoid exposing it in logs
            self._data["RESULT"]["pwd"] = "__OBFUSCATED__"
            _LOGGER.debug(f"Received: {self._data}")
            self._status = self._data["RESULT"]
        else:
            _LOGGER.error("Error contacting the unit with response")

    @property
    @abstractmethod
    def ambient_temp(self) -> float:
        pass

    @property
    @abstractmethod
    def target_temperature(self) -> float:
        pass

    @property
    @abstractmethod
    def fan_speed(self) -> FanSpeed:
        pass

    @property
    @abstractmethod
    def supported_fan_speeds(self) -> List[FanSpeed]:
        pass

    @property
    @abstractmethod
    def rotation(self) -> bool:
        pass

    @property
    @abstractmethod
    def night_mode(self) -> bool:
        pass

    @property
    @abstractmethod
    def temperature_step(self) -> float:
        pass

    @abstractmethod
    async def set_temperature(self, temperature: int) -> bool:
        pass

    @abstractmethod
    async def set_fan_speed(self, speed: FanSpeed) -> bool:
        pass

    @abstractmethod
    async def rotation_on(self) -> bool:
        pass

    @abstractmethod
    async def rotation_off(self) -> bool:
        pass

    @abstractmethod
    async def night_mode_on(self) -> bool:
        pass

    @abstractmethod
    async def night_mode_off(self) -> bool:
        pass

    @abstractmethod
    async def set_heating(self) -> bool:
        pass

    @abstractmethod
    async def set_cooling(self) -> bool:
        pass

    @abstractmethod
    async def set_dehumidifying(self) -> bool:
        pass

    @abstractmethod
    async def set_fan_only(self) -> bool:
        pass

    @abstractmethod
    async def set_auto(self) -> bool:
        pass

    async def _set_mode(self, mode: Mode) -> bool:
        if await self._network_facade._send_command(mode.command):
            self._status["ps"] = 1
            self._status["wm"] = mode.code
            return True
        return False

    @property
    def min_temperature(self) -> int:
        return MIN_TEMP

    @property
    def max_temperature(self) -> int:
        return MAX_TEMP

    @property
    def power(self) -> bool:
        if "ps" in self._status:
            return self._status["ps"] == 1
        return False

    @property
    def mode(self) -> Mode:
        if "wm" in self._status:
            return self.Modes.get_mode(self._status["wm"])
        else:
            return UNKNOWN_MODE

    async def power_on(self) -> bool:
        if await self._network_facade._send_command(CMD_POWER_ON):
            self._status["ps"] = 1
            return True
        return False

    async def power_off(self) -> bool:
        if await self._network_facade._send_command(CMD_POWER_OFF):
            self._status["ps"] = 0
            return True
        return False

    @property
    def name(self) -> str:
        if "setup" in self._data and "name" in self._data["setup"]:
            return self._data["setup"]["name"]
        return None

    @property
    def serial(self) -> str:
        if "setup" in self._data and "serial" in self._data["setup"]:
            return self._data["setup"]["serial"]
        return None

    @property
    def uid(self) -> str:
        if "UID" in self._data:
            return self._data["UID"]
        return None

    @property
    def software_version(self) -> str:
        if "sw" in self._data and "V" in self._data["sw"]:
            return self._data["sw"]["V"]
        return None

    @property
    def ip_address(self) -> str:
        if "net" in self._data and "ip" in self._data["net"]:
            return self._data["net"]["ip"]
        return None

    @property
    def supports_target_temp(self) -> bool:
        return True

    @property
    def supports_swing(self) -> bool:
        return False

    @property
    def supports_fan(self) -> bool:
        return True

    @property
    def supports_preset(self) -> bool:
        return True
