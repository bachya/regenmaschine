"""Define an object to interact with RainMachine weather parsers."""
import logging
from typing import Any, Awaitable, Callable, Dict, List, cast

_LOGGER: logging.Logger = logging.getLogger(__name__)


class Parser:  # pylint: disable=too-few-public-methods
    """Define a parser object."""

    def __init__(self, request: Callable[..., Awaitable[Dict[str, Any]]]) -> None:
        """Initialize."""
        self._request = request

    async def current(self) -> Dict[str, Any]:
        """Get current diagnostics."""
        data = await self._request("get", "parser")
        return cast(Dict[str, Any], data["parsers"])

    async def post_data(
        self, json_payload: Dict[str, List[Dict[str, Any]]]
    ) -> Dict[str, Any]:
        """Post weather data from an external source.

        Local Weather Push service should be enabled from Settings > Weather >
        Developer tab for RainMachine to consider the values being sent.
        """
        _LOGGER.debug(json_payload)
        return await self._request("post", "parser/data", json=json_payload)
