from abc import ABC
from enum import Enum
import logging
from network_facade import NetWorkFacade

_CMD_POWER_ON = "power/on"
_CMD_POWER_OFF = "power/off"

_CMD_SET_TEMP = "set/setpoint"

_CMD_ROTATION = "set/feature/rotation"
_ROTATION_ON = 0
_ROTATION_OFF = 7

_CMD_FAN_SPEED = "set/fan"

_CMD_NIGHT_MODE = "set/feature/night"
_NIGHT_MODE_ON = 1
_NIGHT_MODE_OFF = 0

_MIN_TEMP = 16
_MAX_TEMP = 31

_LOGGER = logging.getLogger(__name__)


class InnovaDevice(ABC):

    class Mode(Enum):
        pass


    def __init__(self, network_facade: NetWorkFacade) -> None:
        super().__init__()
        self._network_facade = network_facade
        self._data = {}
        self._status = {}

    def set_data(self, data: dict) -> None:
        self._data = data
        # We don't need the password, so obfuscate it to avoid exposing it in logs
        self._data["RESULT"]["pwd"] = "__OBFUSCATED__"
        _LOGGER.debug(f"Received: {self._data}")
        self._status = self._data["RESULT"]

    @property
    def ambient_temp(self) -> int:
        if "t" in self._status:
            return self._status["t"]
        else:
            return 0

    @property
    def target_temperature(self) -> int:
        if "sp" in self._status:
            return self._status["sp"]
        else:
            return 0

    @property
    def min_temperature(self) -> int:
        return _MIN_TEMP

    @property
    def max_temperature(self) -> int:
        return _MAX_TEMP

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
        return self.Mode.UNKNOWN

    @property
    def rotation(self) -> bool:
        if "fr" in self._status:
            if self._status["fr"] == _ROTATION_ON:
                return True
        return False

    @property
    def fan_speed(self) -> int:
        if "fs" in self._status:
            return self._status["fs"]
        return 0

    @property
    def night_mode(self) -> bool:
        if "nm" in self._status:
            if self._status["nm"] == _NIGHT_MODE_ON:
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

    async def power_on(self) -> bool:
        if await self._network_facade._send_command(_CMD_POWER_ON):
            self._status["ps"] = 1
            return True
        return False

    async def power_off(self) -> bool:
        if await self._network_facade._send_command(_CMD_POWER_OFF):
            self._status["ps"] = 0
            return True
        return False

    async def rotation_on(self) -> bool:
        if await self._network_facade._send_command(_CMD_ROTATION, {"value": _ROTATION_ON}):
            self._status["fr"] = _ROTATION_ON
            return True
        return False

    async def rotation_off(self) -> bool:
        if await self._network_facade._send_command(_CMD_ROTATION, {"value": _ROTATION_OFF}):
            self._status["fr"] = _ROTATION_OFF
            return True
        return False

    async def night_mode_on(self) -> bool:
        if await self._network_facade._send_command(_CMD_NIGHT_MODE, {"value": _NIGHT_MODE_ON}):
            self._status["nm"] = _NIGHT_MODE_ON
            return True
        return False

    async def night_mode_off(self) -> bool:
        if await self._network_facade._send_command(_CMD_NIGHT_MODE, {"value": _NIGHT_MODE_OFF}):
            self._status["nm"] = _NIGHT_MODE_OFF
            return True
        return False

    async def set_temperature(self, temperature: int) -> bool:
        data = {"p_temp": temperature}
        if await self._network_facade._send_command(_CMD_SET_TEMP, data):
            self._status["sp"] = temperature
            return True
        return False

    async def set_fan_speed(self, speed: int) -> bool:
        data = {"value": speed}
        if await self._network_facade._send_command(_CMD_FAN_SPEED, data):
            self._status["fs"] = speed
            return True
        return False

    async def set_mode(self, mode: Mode) -> bool:
        if await self._network_facade._send_command(mode.value["cmd"]):
            self._status["ps"] = 1
            self._status["wm"] = mode.value["code"]
            return True
        return False
