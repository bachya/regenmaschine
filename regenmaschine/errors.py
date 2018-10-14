"""Define package errors."""


class RainMachineError(Exception):
    """Define a base error."""

    pass


class RequestError(RainMachineError):
    """Define an error related to invalid requests."""

    pass


class UnauthenticatedError(RainMachineError):
    """Define an error for unauthenticated requests."""

    pass
