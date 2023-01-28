from enum import Enum

from innova_controls.airleaf import AirLeaf
from innova_controls.innova_device import InnovaDevice
from innova_controls.network_functions import NetWorkFunctions
from innova_controls.twopointzero import TwoPointZero


class DeviceType(Enum):
    TWOPOINTZERO = "001"
    AIRLEAF = "002"


class InnovaFactory:
    @staticmethod
    def get_device(device_type: str, network_facade: NetWorkFunctions) -> InnovaDevice:
        if device_type == DeviceType.TWOPOINTZERO.value:
            return TwoPointZero(network_facade)
        elif device_type == DeviceType.AIRLEAF.value:
            return AirLeaf(network_facade)
