from enum import Enum
from innova_device import InnovaDevice
from network_facade import NetWorkFacade


class TwoPointZero(InnovaDevice):

    class Mode(InnovaDevice.Mode):
        HEATING = {"cmd": "set/mode/heating", "code": 0, "status": "heating"}
        COOLING = {"cmd": "set/mode/cooling", "code": 1, "status": "cooling"}
        DEHUMIDIFICATION = {
            "cmd": "set/mode/dehumidification",
            "code": 3,
            "status": "dehumidification",
        }
        FAN_ONLY = {"cmd": "set/mode/fanonly", "code": 4, "status": "fanonly"}
        AUTO = {"cmd": "set/mode/auto", "code": 5, "status": "auto"}
        UNKNOWN = {"code": -1}

    def __init__(self, network_facade: NetWorkFacade) -> None:
        super().__init__(network_facade)