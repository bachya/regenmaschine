"""Define API endpoint objects."""
from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING

from typing_extensions import ParamSpec

from regenmaschine.errors import UnknownAPICallError

if TYPE_CHECKING:
    from regenmaschine.controller import Controller

P = ParamSpec("P")


class EndpointManager:
    """Define an object to manage a API endpoints of a certain category."""

    def __init__(self, controller: Controller) -> None:
        """Initialize."""
        self.controller = controller

    @staticmethod
    def raise_on_gen1_controller(func: Callable[..., Awaitable]) -> Callable:
        """Raise an error if a method is called on a 1st generation controller."""

        def decorator(
            inst: type[EndpointManager], *args: P.args, **kwargs: P.kwargs
        ) -> Awaitable:
            if inst.controller.hardware_version == 1:
                raise UnknownAPICallError(
                    f"Can't call {func.__name__} on a 1st generation controller"
                )
            return func(inst, *args, **kwargs)

        return decorator
