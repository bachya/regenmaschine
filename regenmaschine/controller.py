"""Define a RainMachine controller class."""
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from regenmaschine.client import Client


class Controller:
    """Define the controller."""

    def __init__(self, client: Client) -> None:
        """Initialize."""
        self._client = client
