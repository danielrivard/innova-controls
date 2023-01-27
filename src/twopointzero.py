from enum import Enum

from constants import (
    CMD_FAN_SPEED,
    CMD_NIGHT_MODE,
    CMD_ROTATION,
    CMD_SET_TEMP,
    NIGHT_MODE_OFF,
    NIGHT_MODE_ON,
    ROTATION_OFF,
    ROTATION_ON,
)
from innova_device import InnovaDevice
from network_functions import NetWorkFunctions


class TwoPointZero(InnovaDevice):
    class Mode(InnovaDevice.Mode):
        HEATING = {"cmd": "set/mode/heating", "code": 0}
        COOLING = {"cmd": "set/mode/cooling", "code": 1}
        DEHUMIDIFICATION = {"cmd": "set/mode/dehumidification", "code": 3}
        FAN_ONLY = {"cmd": "set/mode/fanonly", "code": 4}
        AUTO = {"cmd": "set/mode/auto", "code": 5}

    def __init__(self, network_facade: NetWorkFunctions) -> None:
        super().__init__(network_facade)

    @property
    def temperature_step(self) -> float:
        return 1.0

    @property
    def ambient_temp(self) -> float:
        if "t" in self._status:
            return self._status["t"]
        else:
            return 0

    @property
    def target_temperature(self) -> float:
        if "sp" in self._status:
            return self._status["sp"]
        else:
            return 0

    @property
    def fan_speed(self) -> int:
        if "fs" in self._status:
            return self._status["fs"]
        return 0

    @property
    def rotation(self) -> bool:
        if "fr" in self._status:
            if self._status["fr"] == ROTATION_ON:
                return True
        return False

    @property
    def night_mode(self) -> bool:
        if "nm" in self._status:
            if self._status["nm"] == NIGHT_MODE_ON:
                return True
        return False

    async def set_temperature(self, temperature: int) -> bool:
        data = {"p_temp": temperature}
        if await self._network_facade._send_command(CMD_SET_TEMP, data):
            self._status["sp"] = temperature
            return True
        return False

    async def set_fan_speed(self, speed: int) -> bool:
        data = {"value": speed}
        if await self._network_facade._send_command(CMD_FAN_SPEED, data):
            self._status["fs"] = speed
            return True
        return False

    @property
    def supports_swing(self) -> bool:
        return True

    async def rotation_on(self) -> bool:
        if await self._network_facade._send_command(
            CMD_ROTATION, {"value": ROTATION_ON}
        ):
            self._status["fr"] = ROTATION_ON
            return True
        return False

    async def rotation_off(self) -> bool:
        if await self._network_facade._send_command(
            CMD_ROTATION, {"value": ROTATION_OFF}
        ):
            self._status["fr"] = ROTATION_OFF
            return True
        return False

    async def night_mode_on(self) -> bool:
        if await self._network_facade._send_command(
            CMD_NIGHT_MODE, {"value": NIGHT_MODE_ON}
        ):
            self._status["nm"] = NIGHT_MODE_ON
            return True
        return False

    async def night_mode_off(self) -> bool:
        if await self._network_facade._send_command(
            CMD_NIGHT_MODE, {"value": NIGHT_MODE_OFF}
        ):
            self._status["nm"] = NIGHT_MODE_OFF
            return True
        return False
