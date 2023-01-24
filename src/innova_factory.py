from enum import Enum

from airleaf import AirLeaf
from device_manager import DeviceManager
from network_facade import NetWorkFacade
from twopointzero import TwoPointZero


class DeviceType(Enum):
    TWOPOINTZERO = "001"
    AIRLEAF = "002"

class InnovaFactory:
    @staticmethod
    def get_device(device_type: str, network_facade: NetWorkFacade) -> DeviceManager:
        if device_type == DeviceType.TWOPOINTZERO.value:
            return TwoPointZero(network_facade)
        elif device_type == DeviceType.AIRLEAF.value:
            return AirLeaf(network_facade)
