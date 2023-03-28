from typing import List

from innova_controls.constants import (
    CMD_FAN_SPEED,
    CMD_NIGHT_MODE,
    CMD_ROTATION,
    CMD_SET_TEMP,
    NIGHT_MODE_OFF,
    NIGHT_MODE_ON,
    ROTATION_OFF,
    ROTATION_ON,
)
from innova_controls.fan_speed import FanSpeed
from innova_controls.innova_device import InnovaDevice
from innova_controls.mode import Mode
from innova_controls.network_functions import NetWorkFunctions


class TwoPointZero(InnovaDevice):
    class Modes(InnovaDevice.Modes):
        HEATING = Mode("set/mode/heating", 0, heat=True)
        COOLING = Mode("set/mode/cooling", 1, cool=True)
        DEHUMIDIFICATION = Mode("set/mode/dehumidification", 3, dehumidify=True)
        FAN_ONLY = Mode("set/mode/fanonly", 4, fan_only=True)
        AUTO = Mode("set/mode/auto", 5, auto=True)

        codes: dict = {
            0: HEATING,
            1: COOLING,
            3: DEHUMIDIFICATION,
            4: FAN_ONLY,
            5: AUTO,
        }

    fan_speeds = {
        0: FanSpeed.AUTO,
        1: FanSpeed.LOW,
        2: FanSpeed.MEDIUM,
        3: FanSpeed.HIGH,
    }
    fan_speeds_reverse: dict = {v: k for k, v in fan_speeds.items()}

    def __init__(self, network_facade: NetWorkFunctions) -> None:
        super().__init__(network_facade)

    @property
    def model(self) -> str:
        return "TwoPointZero (2.0)"

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
    def water_temperature(self) -> float:
        pass

    @property
    def fan_speed(self) -> FanSpeed:
        if "fs" in self._status:
            return self.fan_speeds[self._status["fs"]]
        return FanSpeed.AUTO

    @property
    def supported_fan_speeds(self) -> List[FanSpeed]:
        return list(self.fan_speeds.values())

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

    async def set_temperature(self, temperature: float) -> bool:
        data = {"p_temp": temperature}
        if await self._network_facade.send_command(CMD_SET_TEMP, data=data):
            self._status["sp"] = temperature
            return True
        return False

    async def set_fan_speed(self, speed: FanSpeed) -> bool:
        speed_code = self.fan_speeds_reverse[speed]
        data = {"value": speed_code}
        if await self._network_facade.send_command(CMD_FAN_SPEED, data=data):
            self._status["fs"] = speed_code
            return True
        return False

    @property
    def supports_swing(self) -> bool:
        return True

    async def rotation_on(self) -> bool:
        data = {"value": ROTATION_ON}
        if await self._network_facade.send_command(CMD_ROTATION, data=data):
            self._status["fr"] = ROTATION_ON
            return True
        return False

    async def rotation_off(self) -> bool:
        data = {"value": ROTATION_OFF}
        if await self._network_facade.send_command(CMD_ROTATION, data=data):
            self._status["fr"] = ROTATION_OFF
            return True
        return False

    async def night_mode_on(self) -> bool:
        data = {"value": NIGHT_MODE_ON}
        if await self._network_facade.send_command(CMD_NIGHT_MODE, data=data):
            await self.set_fan_speed(FanSpeed.LOW)
            self._status["nm"] = NIGHT_MODE_ON
            return True
        return False

    async def night_mode_off(self) -> bool:
        data = {"value": NIGHT_MODE_OFF}
        if await self._network_facade.send_command(CMD_NIGHT_MODE, data=data):
            self._status["nm"] = NIGHT_MODE_OFF
            return True
        return False

    async def set_heating(self) -> bool:
        return await self._set_mode(self.Modes.HEATING)

    async def set_cooling(self) -> bool:
        return await self._set_mode(self.Modes.COOLING)

    async def set_dehumidifying(self) -> bool:
        return await self._set_mode(self.Modes.DEHUMIDIFICATION)

    async def set_fan_only(self) -> bool:
        return await self._set_mode(self.Modes.FAN_ONLY)

    async def set_auto(self) -> bool:
        return await self._set_mode(self.Modes.AUTO)
