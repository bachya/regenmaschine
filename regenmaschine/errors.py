"""Define package errors."""


class RainMachineError(Exception):
    """Define a base error."""

    pass


class RequestError(RainMachineError):
    """Define an error related to invalid requests."""

    pass


class TokenExpiredError(RainMachineError):
    """Define an error for expired access tokens that can't be refreshed."""

    pass
