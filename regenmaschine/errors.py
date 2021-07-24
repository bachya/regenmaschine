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


ERROR_CODES = {1: "The email has not been validated"}


def raise_remote_error(error_code: int) -> None:
    """Raise the appropriate error with a remote error code."""
    try:
        error = next((v for k, v in ERROR_CODES.items() if k == error_code))
        raise RequestError(error)
    except StopIteration:
        raise RequestError(
            f"Unknown remote error code returned: {error_code}"
        ) from None
