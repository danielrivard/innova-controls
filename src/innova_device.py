import logging
from abc import ABC, abstractmethod
from enum import Enum

from constants import CMD_POWER_OFF, CMD_POWER_ON, MAX_TEMP, MIN_TEMP
from network_functions import NetWorkFunctions

_LOGGER = logging.getLogger(__name__)


class InnovaDevice(ABC):
    class Mode(Enum):
        pass

    class UnknownMode(Mode):
        UNKNOWN = {"code": -1}

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
    def fan_speed(self) -> int:
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
    async def set_fan_speed(self, speed: int) -> bool:
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
            for mode in self.Mode:
                if self._status["wm"] == mode.value["code"]:
                    return mode
        return self.UnknownMode.UNKNOWN

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

    async def set_mode(self, mode: Mode) -> bool:
        if await self._network_facade._send_command(mode.value["cmd"]):
            self._status["ps"] = 1
            self._status["wm"] = mode.value["code"]
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
