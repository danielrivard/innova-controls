from enum import Enum
from typing import List

from innova_controls.constants import CMD_SET_TEMP
from innova_controls.fan_speed import FanSpeed
from innova_controls.innova_device import InnovaDevice
from innova_controls.mode import Mode
from innova_controls.network_functions import NetWorkFunctions


class AirLeaf(InnovaDevice):
    class Modes(InnovaDevice.Modes):
        AUTO = Mode("set/mode/auto", 0, auto=True)
        HEATING = Mode("set/mode/heating", 3, heat=True)
        COOLING = Mode("set/mode/cooling", 5, cool=True)

        codes: dict = {
            0: AUTO,
            3: HEATING,
            5: COOLING,
        }

    class Function(Enum):
        AUTO = {"cmd": "set/function/auto", "code": 1, "fan": FanSpeed.AUTO}
        NIGHT = {"cmd": "set/function/night", "code": 2, "fan": None}
        MIN = {"cmd": "set/function/min", "code": 3, "fan": FanSpeed.LOW}
        MAX = {"cmd": "set/function/max", "code": 4, "fan": FanSpeed.HIGH}

        codes = {1: AUTO, 2: NIGHT, 3: MIN, 4: MAX, "fan": None}

    def __init__(self, network_facade: NetWorkFunctions) -> None:
        super().__init__(network_facade)

    @property
    def temperature_step(self) -> float:
        return 0.5

    @property
    def ambient_temp(self) -> float:
        if "ta" in self._status:
            return self._status["ta"] / 10
        else:
            return 0

    @property
    def target_temperature(self) -> float:
        if "sp" in self._status:
            return self._status["sp"] / 10
        else:
            return 0

    @property
    def water_temperature(self) -> float:
        if "tw" in self._status:
            return self._status["tw"] / 10
        else:
            return 0

    @property
    def fan_speed(self) -> FanSpeed:
        if "fn" in self._status:
            fn = self.Function.codes.value[self._status["fn"]]
            # Night is not really a fan speed, and is handled by preset
            # so, let fan be labeled as AUTO in this case.
            if fn == self.Function.NIGHT:
                fn = FanSpeed.AUTO
            return fn["fan"]
        return FanSpeed.AUTO

    @property
    def supported_fan_speeds(self) -> List[FanSpeed]:
        speeds: List[FanSpeed] = []
        for function in self.Function:
            if "fan" in function.value and function.value["fan"] is not None:
                speeds.append(function.value["fan"])
        return speeds

    @property
    def rotation(self) -> bool:
        return False

    @property
    def night_mode(self) -> bool:
        if "fn" in self._status:
            if self._status["fn"] == self.Function.NIGHT.value["code"]:
                return True
        return False

    async def set_temperature(self, temperature: int) -> bool:
        data = {"p_temp": temperature * 100}
        if await self._network_facade._send_command(CMD_SET_TEMP, data):
            self._status["sp"] = temperature * 100
            return True
        return False

    async def set_fan_speed(self, speed: FanSpeed) -> bool:
        command: str = None
        code: int = None
        for function in self.Function:
            if speed == function.value["fan"]:
                command = function.value["cmd"]
                code = function.value["code"]
                break

        if command and await self._network_facade._send_command(command):
            self._status["fn"] = code
            return True
        return False

    async def rotation_on(self) -> bool:
        return False

    async def rotation_off(self) -> bool:
        return False

    async def night_mode_on(self) -> bool:
        if await self._network_facade._send_command(self.Function.NIGHT.value["cmd"]):
            self._status["fn"] = self.Function.NIGHT.value["code"]
            return True
        return False

    async def night_mode_off(self) -> bool:
        if await self._network_facade._send_command(self.Function.AUTO.value["cmd"]):
            self._status["fn"] = self.Function.AUTO.value["code"]
            return True
        return False

    async def set_heating(self) -> bool:
        return await super()._set_mode(self.Modes.HEATING)

    async def set_cooling(self) -> bool:
        return await super()._set_mode(self.Modes.COOLING)

    async def set_auto(self) -> bool:
        return await super()._set_mode(self.Modes.AUTO)

    async def set_dehumidifying(self) -> bool:
        pass

    async def set_fan_only(self) -> bool:
        pass
