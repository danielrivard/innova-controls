from device_manager import DeviceManager
from network_facade import NetWorkFacade


class TwoPointZero(DeviceManager):

    def __init__(self, network_facade: NetWorkFacade) -> None:
        super().__init__(network_facade)