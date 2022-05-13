import logging
from enum import Enum

import requests

CMD_STATUS = "status"

CMD_POWER_ON = "power/on"
CMD_POWER_OFF = "power/off"

CMD_SET_TEMP = "set/setpoint"

CMD_ROTATION = "set/feature/rotation"
ROTATION_ON = 0
ROTATION_OFF = 7

CMD_FAN_SPEED = "set/fan"

MIN_TEMP = 16
MAX_TEMP = 31


class Mode(Enum):
    COOLING = {"cmd": "set/mode/cooling", "code": 1, "status": "cooling"}
    HEATING = {"cmd": "set/mode/heating", "code": 2, "status": "heating"}
    DEHUMIDIFICATION = {
        "cmd": "set/mode/dehumidification",
        "code": 3,
        "status": "dehumidification",
    }
    FAN_ONLY = {"cmd": "set/mode/fanonly", "code": 4, "status": "fanonly"}
    AUTO = {"cmd": "set/mode/auto", "code": 5, "status": "auto"}
    UNKNOWN = {}


class Innova:
    """This is a class to control Innova heat pump units over http

    Attributes:
        For Local Mode
        host: str
            IP address of the Innova unit on the local network.
            If omitted, cloud mode is assumed

        For Cloud Mode (both serial and uid are mandatory)
        serial: str
            Serial number of the Innova unit (usually looks like INXXXXXXX)
        uid: str)
            The MAC address of the Innova unit. 
    """
    def __init__(self, host: str = None, serial: str = None, uid: str = None):
        self._LOGGER = logging.getLogger(__name__)
        if host is not None:
            # Setup for local mode
            self._api_url = f"http://{host}/api/v/1"
            self._headers = None
        else:
            # Setup for cloud mode
            self._api_url = "http://innovaenergie.cloud/api/v/1/"
            self._headers = {
                'X-serial': serial,
                'X-UID': uid
            }
        self._data = {}
        self._status = {}

    def __send_command(self, command, data=None) -> bool:
        cmd_url = f"{self._api_url}/{command}"
        try:
            r = requests.post(cmd_url, data=data, headers=self._headers)

            if r.status_code == 200:
                if r.json()["success"]:
                    return True
            return False
        except requests.exceptions.ConnectTimeout:
            return False
        except requests.exceptions.ConnectionError:
            return False
        except Exception as e:
            self._LOGGER.error("Error while sending command", e)

    def update(self):
        status_url = f"{self._api_url}/{CMD_STATUS}"
        try:
            r = requests.get(status_url, headers=self._headers)
            self._data = r.json()
            if "RESULT" in self._data:
                self._status = self._data["RESULT"]
        except Exception as e:
            self._LOGGER.error("Error getting status", e)

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
        return MIN_TEMP

    @property
    def max_temperature(self) -> int:
        return MAX_TEMP

    @property
    def power(self) -> bool:
        if "ps" in self._status:
            return self._status["ps"] == 1
        return False

    @property
    def mode(self) -> Mode:
        if "wm" in self._status:
            for mode in Mode:
                if self._status["wm"] == mode.value["code"]:
                    return mode
        return Mode.UNKNOWN

    @property
    def rotation(self) -> bool:
        if "fr" in self._status:
            if self._status["fr"] == ROTATION_ON:
                return True
        return False

    @property
    def fan_speed(self) -> int:
        if "fs" in self._status:
            return self._status["fs"]
        return 0

    @property
    def name(self) -> str:
        if "setup" in self._data and "name" in self._data["setup"]:
            return self._data["setup"]["name"]
        return None

    @property
    def id(self) -> str:
        if "setup" in self._data and "serial" in self._data["setup"]:
            return self._data["setup"]["serial"]
        return None

    def power_on(self):
        if self.__send_command(CMD_POWER_ON):
            self._status["ps"] = 1

    def power_off(self):
        if self.__send_command(CMD_POWER_OFF):
            self._status["ps"] = 0

    def rotation_on(self):
        if self.__send_command(CMD_ROTATION, {"value": ROTATION_ON}):
            self._status["fr"] = ROTATION_ON

    def rotation_off(self):
        if self.__send_command(CMD_ROTATION, {"value": ROTATION_OFF}):
            self._status["fr"] = ROTATION_OFF

    def set_temperature(self, temperature: int):
        data = {"p_temp": temperature}
        if self.__send_command(CMD_SET_TEMP, data):
            self._status["sp"] = temperature

    def set_fan_speed(self, speed: int):
        data = {"value": speed}
        if self.__send_command(CMD_FAN_SPEED, data):
            self._status["fs"] = speed

    def set_mode(self, mode: Mode):
        if self.__send_command(mode.value["cmd"]):
            self._status["wm"] = mode.value["code"]
