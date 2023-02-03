import logging

from aiohttp import ClientConnectionError, ClientSession, ServerTimeoutError
from retry import retry

from innova_controls.constants import CMD_STATUS, CONNECTION_TIMEOUT

_LOGGER = logging.getLogger(__name__)


class NetWorkFunctions:
    def __init__(
        self,
        http_session: ClientSession,
        host: str = None,
        serial: str = None,
        uid: str = None,
    ) -> None:

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

    @retry(exceptions=Exception, tries=2, delay=2, logger=_LOGGER, log_traceback=True)
    async def send_command(self, command, data=None, json=None) -> bool:
        cmd_url = f"{self._api_url}/{command}"
        try:
            r = await self._http_session.post(
                cmd_url,
                data=data,
                json=json,
                headers=self._headers,
                timeout=CONNECTION_TIMEOUT,
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
    async def get_status(self) -> dict:
        status_url = f"{self._api_url}/{CMD_STATUS}"
        try:
            r = await self._http_session.get(
                status_url, headers=self._headers, timeout=CONNECTION_TIMEOUT
            )
            data: dict = await r.json(content_type=r.content_type)
            if data and data["success"] and "RESULT" in data:
                return data
            else:
                _LOGGER.error(f"Error contacting the unit with response {r.text}")
                return None
        except Exception as e:
            _LOGGER.error(f"Error getting status {status_url}", e)
            return None
