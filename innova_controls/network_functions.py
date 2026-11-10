import asyncio
import logging

from aiohttp import (
    ClientConnectionError,
    ClientResponse,
    ClientSession,
    ServerTimeoutError,
)

from innova_controls.constants import CMD_STATUS, CONNECTION_TIMEOUT

_LOGGER = logging.getLogger(__name__)

RETRY_ATTEMPTS = 2
RETRY_DELAY = 2


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

    async def _request(self, method: str, url: str, **kwargs) -> ClientResponse:
        """Send a request, retrying on connection errors and timeouts.

        The body is read before returning so callers can use json()/text()
        without another network round trip.
        """
        for attempt in range(1, RETRY_ATTEMPTS + 1):
            try:
                r = await self._http_session.request(
                    method,
                    url,
                    headers=self._headers,
                    timeout=CONNECTION_TIMEOUT,
                    **kwargs,
                )
                await r.read()
                return r
            except (ClientConnectionError, asyncio.TimeoutError) as e:
                if attempt == RETRY_ATTEMPTS:
                    raise
                _LOGGER.debug(
                    "Request to %s failed (%s), retrying in %ss", url, e, RETRY_DELAY
                )
                await asyncio.sleep(RETRY_DELAY)

    async def send_command(self, command, data=None, json=None) -> bool:
        cmd_url = f"{self._api_url}/{command}"
        try:
            r = await self._request("POST", cmd_url, data=data, json=json)

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

    async def get_status(self) -> dict:
        status_url = f"{self._api_url}/{CMD_STATUS}"
        try:
            r = await self._request("GET", status_url)
            data: dict = await r.json(content_type=r.content_type)
            if data and data["success"] and "RESULT" in data:
                return data
            else:
                _LOGGER.error(f"Error contacting the unit with response {r.text}")
                return None
        except Exception as e:
            _LOGGER.error(f"Error getting status {status_url}", e)
            return None
