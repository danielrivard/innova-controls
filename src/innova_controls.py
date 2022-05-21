import logging
from enum import Enum

import requests
from retry import retry

_CMD_STATUS = "status"

_CMD_POWER_ON = "power/on"
_CMD_POWER_OFF = "power/off"

_CMD_SET_TEMP = "set/setpoint"

_CMD_ROTATION = "set/feature/rotation"
_ROTATION_ON = 0
_ROTATION_OFF = 7

_CMD_FAN_SPEED = "set/fan"

_MIN_TEMP = 16
_MAX_TEMP = 31

_CONNECTION_TIMEOUT = 20

_LOGGER = logging.getLogger(__name__)


class Mode(Enum):
    HEATING = {"cmd": "set/mode/heating", "code": 0, "status": "heating"}
    COOLING = {"cmd": "set/mode/cooling", "code": 1, "status": "cooling"}
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
        _LOGGER.info(
            f"Initialize Innova Controls with host={host}, "
            "serial={serial}, uid={uid}"
        )
        if host is not None:
            # Setup for local mode
            _LOGGER.debug("Setting up local mode")
            self._api_url = f"http://{host}/api/v/1"
            self._headers = None
        else:
            # Setup for cloud mode
            _LOGGER.debug("Setting up cloud mode")
            self._api_url = "http://innovaenergie.cloud/api/v/1"
            self._headers = {"X-serial": serial, "X-UID": uid}
        self._data = {}
        self._status = {}

    @retry(exceptions=Exception, tries=2, delay=2, logger=_LOGGER, log_traceback=True)
    def __send_command(self, command, data=None) -> bool:
        cmd_url = f"{self._api_url}/{command}"
        try:
            r = requests.post(
                cmd_url, data=data, headers=self._headers, timeout=_CONNECTION_TIMEOUT
            )

            if r.status_code == 200:
                if r.json()["success"]:
                    return True
            return False
        except requests.exceptions.ConnectTimeout:
            return False
        except requests.exceptions.ConnectionError:
            return False
        except Exception as e:
            _LOGGER.error("Error while sending command", e)
            return False

    def update(self):
        status_url = f"{self._api_url}/{_CMD_STATUS}"
        try:
            r = requests.get(
                status_url, headers=self._headers, timeout=_CONNECTION_TIMEOUT
            )
            self._data = r.json()
            if "RESULT" in self._data:
                self._status = self._data["RESULT"]
        except Exception as e:
            _LOGGER.error("Error getting status", e)

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
        return _MIN_TEMP

    @property
    def max_temperature(self) -> int:
        return _MAX_TEMP

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
            if self._status["fr"] == _ROTATION_ON:
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
        if self.__send_command(_CMD_POWER_ON):
            self._status["ps"] = 1

    def power_off(self):
        if self.__send_command(_CMD_POWER_OFF):
            self._status["ps"] = 0

    def rotation_on(self):
        if self.__send_command(_CMD_ROTATION, {"value": _ROTATION_ON}):
            self._status["fr"] = _ROTATION_ON

    def rotation_off(self):
        if self.__send_command(_CMD_ROTATION, {"value": _ROTATION_OFF}):
            self._status["fr"] = _ROTATION_OFF

    def set_temperature(self, temperature: int):
        data = {"p_temp": temperature}
        if self.__send_command(_CMD_SET_TEMP, data):
            self._status["sp"] = temperature

    def set_fan_speed(self, speed: int):
        data = {"value": speed}
        if self.__send_command(_CMD_FAN_SPEED, data):
            self._status["fs"] = speed

    def set_mode(self, mode: Mode):
        if self.__send_command(mode.value["cmd"]):
            self._status["wm"] = mode.value["code"]
