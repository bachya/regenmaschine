"""Define API endpoint objects."""

from __future__ import annotations

from collections.abc import Callable, Coroutine
from typing import TYPE_CHECKING, Any, Concatenate, TypeVar

from typing_extensions import ParamSpec

from regenmaschine.errors import UnknownAPICallError

if TYPE_CHECKING:
    from regenmaschine.controller import Controller

_P = ParamSpec("_P")
_T = TypeVar("_T", bound=dict | list | str)
_ManagerT = TypeVar("_ManagerT", bound="EndpointManager")


class EndpointManager:  # pylint: disable=too-few-public-methods
    """Define an object to manage a API endpoints of a certain category."""

    def __init__(self, controller: Controller) -> None:
        """Initialize.

        Args:
            controller: A Controller subclass.
        """
        self.controller = controller

    @staticmethod
    def raise_on_gen1_controller(
        func: Callable[Concatenate[_ManagerT, _P], Coroutine[Any, Any, _T]],
    ) -> Callable[Concatenate[_ManagerT, _P], Coroutine[Any, Any, _T]]:
        """Raise an error if a method is called on a 1st generation controller.

        Args:
            func: The callable to decorate.

        Returns:
            The decorated callable.
        """

        def decorator(
            inst: _ManagerT, *args: _P.args, **kwargs: _P.kwargs
        ) -> Coroutine[Any, Any, _T]:
            if inst.controller.hardware_version == "1":
                raise UnknownAPICallError(
                    f"Can't call {func.__name__} on a 1st generation controller"
                )
            return func(inst, *args, **kwargs)

        return decorator
