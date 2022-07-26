import logging
from enum import Enum

from aiohttp import ClientConnectionError, ClientSession, ServerTimeoutError
from retry import retry

_CMD_STATUS = "status"

_CMD_POWER_ON = "power/on"
_CMD_POWER_OFF = "power/off"

_CMD_SET_TEMP = "set/setpoint"

_CMD_ROTATION = "set/feature/rotation"
_ROTATION_ON = 0
_ROTATION_OFF = 7

_CMD_FAN_SPEED = "set/fan"

_CMD_NIGHT_MODE = "set/feature/night"
_NIGHT_MODE_ON = 1
_NIGHT_MODE_OFF = 0

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
    UNKNOWN = {"code": -1}


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

    def __init__(
        self,
        http_session: ClientSession,
        host: str = None,
        serial: str = None,
        uid: str = None,
    ):
        _LOGGER.info(
            f"Initialize Innova Controls with host={host}, "
            "serial={serial}, uid={uid}"
        )
        self._http_session = http_session

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
    async def _send_command(self, command, data=None) -> bool:
        cmd_url = f"{self._api_url}/{command}"
        try:
            r = await self._http_session.post(
                cmd_url, data=data, headers=self._headers, timeout=_CONNECTION_TIMEOUT
            )

            if r.status == 200:
                result = await r.json(content_type=r.content_type)
                if result["success"]:
                    return True
            return False
        except ServerTimeoutError:
            return False
        except ClientConnectionError:
            return False
        except Exception as e:
            _LOGGER.error(f"Error while sending command {cmd_url}", e)
            return False

    @retry(exceptions=Exception, tries=2, delay=2, logger=_LOGGER, log_traceback=True)
    async def async_update(self) -> bool:
        status_url = f"{self._api_url}/{_CMD_STATUS}"
        try:
            r = await self._http_session.get(
                status_url, headers=self._headers, timeout=_CONNECTION_TIMEOUT
            )
            self._data: dict = await r.json(content_type=r.content_type)
            if self._data["success"] and "RESULT" in self._data:
                # We don't need the password, so obfuscate it to avoid exposing it in logs
                self._data["RESULT"]["pwd"] = "__OBFUSCATED__"
                _LOGGER.debug(f"Status {status_url} received: {self._data}")
                self._status = self._data["RESULT"]
                return True
            else:
                _LOGGER.error(f"Error contacting the unit with response {r.text}")
                return False
        except Exception as e:
            _LOGGER.error(f"Error getting status {status_url}", e)
            return False

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
    def night_mode(self) -> bool:
        if "nm" in self._status:
            if self._status["nm"] == _NIGHT_MODE_ON:
                return True
        return False

    @property
    def name(self) -> str:
        if "setup" in self._data and "name" in self._data["setup"]:
            return self._data["setup"]["name"]
        return None

    @property
    def serial(self) -> str:
        if "setup" in self._data and "serial" in self._data["setup"]:
            return self._data["setup"]["serial"]
        return None

    @property
    def uid(self) -> str:
        if "UID" in self._data:
            return self._data["UID"]
        return None

    @property
    def software_version(self) -> str:
        if "sw" in self._data and "V" in self._data["sw"]:
            return self._data["sw"]["V"]
        return None

    @property
    def ip_address(self) -> str:
        if "net" in self._data and "ip" in self._data["net"]:
            return self._data["net"]["ip"]
        return None

    async def power_on(self) -> bool:
        if await self._send_command(_CMD_POWER_ON):
            self._status["ps"] = 1
            return True
        return False

    async def power_off(self) -> bool:
        if await self._send_command(_CMD_POWER_OFF):
            self._status["ps"] = 0
            return True
        return False

    async def rotation_on(self) -> bool:
        if await self._send_command(_CMD_ROTATION, {"value": _ROTATION_ON}):
            self._status["fr"] = _ROTATION_ON
            return True
        return False

    async def rotation_off(self) -> bool:
        if await self._send_command(_CMD_ROTATION, {"value": _ROTATION_OFF}):
            self._status["fr"] = _ROTATION_OFF
            return True
        return False

    async def night_mode_on(self) -> bool:
        if await self._send_command(_CMD_NIGHT_MODE, {"value": _NIGHT_MODE_ON}):
            self._status["nm"] = _NIGHT_MODE_ON
            return True
        return False

    async def night_mode_off(self) -> bool:
        if await self._send_command(_CMD_NIGHT_MODE, {"value": _NIGHT_MODE_OFF}):
            self._status["nm"] = _NIGHT_MODE_OFF
            return True
        return False

    async def set_temperature(self, temperature: int) -> bool:
        data = {"p_temp": temperature}
        if await self._send_command(_CMD_SET_TEMP, data):
            self._status["sp"] = temperature
            return True
        return False

    async def set_fan_speed(self, speed: int) -> bool:
        data = {"value": speed}
        if await self._send_command(_CMD_FAN_SPEED, data):
            self._status["fs"] = speed
            return True
        return False

    async def set_mode(self, mode: Mode) -> bool:
        if await self._send_command(mode.value["cmd"]):
            self._status["wm"] = mode.value["code"]
            return True
        return False
