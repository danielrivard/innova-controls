from innova_device import InnovaDevice
from network_facade import NetWorkFacade

class AirLeaf(InnovaDevice):

    class Mode(InnovaDevice.Mode):
        AUTO = {"cmd": "set/mode/auto", "code": 0, "status": "auto"}
        HEATING = {"cmd": "set/mode/heating", "code": 3, "status": "heating"}
        COOLING = {"cmd": "set/mode/cooling", "code": 5, "status": "cooling"}
        UNKNOWN = {"code": -1}

    def __init__(self, network_facade: NetWorkFacade) -> None:
        super().__init__(network_facade)