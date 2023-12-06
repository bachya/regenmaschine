"""Define API endpoint objects."""
from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING, Generic, TypeVar

from typing_extensions import ParamSpec

from regenmaschine.errors import UnknownAPICallError

if TYPE_CHECKING:
    from regenmaschine.controller import Controller

_P = ParamSpec("_P")
_T = TypeVar("_T", dict, list, str)


class EndpointManager(Generic[_P, _T]):  # pylint: disable=too-few-public-methods
    """Define an object to manage a API endpoints of a certain category."""

    def __init__(self, controller: Controller) -> None:
        """Initialize.

        Args:
            controller: A Controller subclass.
        """
        self.controller = controller

    @staticmethod
    def raise_on_gen1_controller(
        func: Callable[..., Awaitable[_T]],
    ) -> Callable[..., Awaitable[_T]]:
        """Raise an error if a method is called on a 1st generation controller.

        Args:
            func: The callable to decorate.

        Returns:
            The decorated callable.
        """

        def decorator(
            inst: type[EndpointManager], *args: _P.args, **kwargs: _P.kwargs
        ) -> Awaitable[_T]:
            if inst.controller.hardware_version == "1":
                raise UnknownAPICallError(
                    f"Can't call {func.__name__} on a 1st generation controller"
                )
            return func(inst, *args, **kwargs)

        return decorator
