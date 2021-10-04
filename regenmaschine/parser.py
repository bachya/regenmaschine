"""Define an object to interact with RainMachine weather parsers."""
from typing import Any, Awaitable, Callable, Dict, List, cast


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
        self, payload: Dict[str, List[Dict[str, Any]]]
    ) -> Dict[str, Any]:
        """Post weather data from an external source.

        Reference API Documentation for details:
        https://rainmachine.docs.apiary.io/#reference/weather-services/parserdata/post
        """
        return await self._request("post", "parser/data", json=payload)
