from constants import CMD_FAN_SPEED, CMD_SET_TEMP
from innova_device import InnovaDevice
from network_functions import NetWorkFunctions


class AirLeaf(InnovaDevice):
    class Mode(InnovaDevice.Mode):
        AUTO = {"cmd": "set/mode/auto", "code": 0}
        HEATING = {"cmd": "set/mode/heating", "code": 3}
        COOLING = {"cmd": "set/mode/cooling", "code": 5}

    def __init__(self, network_facade: NetWorkFunctions) -> None:
        super().__init__(network_facade)

    @property
    def ambient_temp(self) -> float:
        if "t" in self._status:
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
    def fan_speed(self) -> int:
        if "fn" in self._status:
            return self._status["fn"]
        return 0

    @property
    def rotation(self) -> bool:
        return False

    @property
    def night_mode(self) -> bool:
        if "fn" in self._status:
            if self._status["fn"] == 2:
                return True
        return False

    async def set_temperature(self, temperature: int) -> bool:
        data = {"p_temp": temperature * 100}
        if await self._network_facade._send_command(CMD_SET_TEMP, data):
            self._status["sp"] = temperature * 100
            return True
        return False

    async def set_fan_speed(self, speed: int) -> bool:
        data = {"value": speed}
        if await self._network_facade._send_command(CMD_FAN_SPEED, data):
            self._status["fn"] = speed
            return True
        return False

    async def rotation_on(self) -> bool:
        return False

    async def rotation_off(self) -> bool:
        return False

    async def night_mode_on(self) -> bool:
        if await self._network_facade._send_command(CMD_FAN_SPEED, {"value": 2}):
            self._status["fn"] = 2
            return True
        return False

    async def night_mode_off(self) -> bool:
        if await self._network_facade._send_command(CMD_FAN_SPEED, {"value": 0}):
            self._status["fn"] = 0
            return True
        return False
