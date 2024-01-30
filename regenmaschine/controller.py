"""Define a RainMachine controller class."""
from __future__ import annotations

from collections.abc import Awaitable, Callable
from datetime import datetime, timedelta
from typing import Any

from yarl import URL

from regenmaschine.endpoints.api import API
from regenmaschine.endpoints.diagnostics import Diagnostics
from regenmaschine.endpoints.machine import Machine
from regenmaschine.endpoints.parser import Parser
from regenmaschine.endpoints.program import Program
from regenmaschine.endpoints.provision import Provision
from regenmaschine.endpoints.restriction import Restriction
from regenmaschine.endpoints.stats import Stats
from regenmaschine.endpoints.watering import Watering
from regenmaschine.endpoints.zone import Zone

URL_BASE_LOCAL = "{0}://{1}:{2}/api/4"
URL_BASE_REMOTE = "https://api.rainmachine.com/{0}/api/4"


class Controller:  # pylint: disable=too-few-public-methods,too-many-instance-attributes
    """Define the controller."""

    def __init__(self, request: Callable[..., Awaitable[dict[str, Any]]]) -> None:
        """Initialize.

        Args:
            request: The request method from the Client object.
        """
        self._access_token: str | None = None
        self._access_token_expiration: datetime | None = None
        self._client_request = request
        self._host: str = ""
        self._base_url: URL = URL("")
        self._use_ssl = True
        self.api_version: str = ""
        self.hardware_version: str = ""
        self.mac: str = ""
        self.name: str = ""
        self.software_version: str = ""

        # API endpoints:
        self.api = API(self)
        self.diagnostics = Diagnostics(self)
        self.machine = Machine(self)
        self.parsers = Parser(self)
        self.programs = Program(self)
        self.provisioning = Provision(self)
        self.restrictions = Restriction(self)
        self.stats = Stats(self)
        self.watering = Watering(self)
        self.zones = Zone(self)

    async def request(
        self, method: str, endpoint: str, **kwargs: dict[str, Any]
    ) -> dict[str, Any]:
        """Wrap the generic request method to add access token, etc.

        Args:
            method: An HTTP method.
            endpoint: An API URL endpoint.
            **kwargs: Additional kwargs to send with the request.

        Returns:
            An API response payload.
        """
        return await self._client_request(
            method,
            self._base_url.joinpath(endpoint),
            access_token=self._access_token,
            access_token_expiration=self._access_token_expiration,
            use_ssl=self._use_ssl,
            **kwargs,
        )


class LocalController(Controller):
    """Define a controller accessed over the LAN."""

    def __init__(
        self,
        request: Callable[..., Awaitable[dict[str, Any]]],
        host: str,
        port: int,
        use_ssl: bool = True,
    ) -> None:
        """Initialize.

        Args:
            request: The request method from the Client object.
            host: The IP address or hostname of the controller.
            port: The port that serves the controller's API.
            use_ssl: Whether to use SSL/TLS on the request.
        """
        super().__init__(request)

        if use_ssl:
            self._host = URL_BASE_LOCAL.format("https", host, port)
        else:
            self._host = URL_BASE_LOCAL.format("http", host, port)

        self._base_url = URL(self._host)
        self._use_ssl = use_ssl

    async def login(self, password: str) -> None:
        """Authenticate against the device (locally).

        Args:
            password: The controller password.
        """
        auth_resp = await self._client_request(
            "post",
            self._base_url.joinpath("auth/login"),
            json={"pwd": password, "remember": 1},
        )

        self._access_token: str = auth_resp["access_token"]
        self._access_token_expiration: datetime = datetime.now() + timedelta(
            seconds=int(auth_resp["expires_in"]) - 10
        )


class RemoteController(Controller):
    """Define a controller accessed over RainMachine's cloud."""

    async def login(
        self, stage_1_access_token: str, sprinkler_id: str, password: str
    ) -> None:
        """Authenticate against the device (remotely).

        Args:
            stage_1_access_token: The first-stage access token from the remote cloud.
            sprinkler_id: A unique ID for the controller.
            password: The account password.
        """
        auth_resp: dict = await self._client_request(
            "post",
            URL("https://my.rainmachine.com/devices/login-sprinkler"),
            access_token=stage_1_access_token,
            json={"sprinklerId": sprinkler_id, "pwd": password},
        )

        self._access_token = auth_resp["access_token"]
        self._host = URL_BASE_REMOTE.format(sprinkler_id)
        self._base_url = URL(self._host)
