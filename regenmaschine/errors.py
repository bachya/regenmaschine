"""Define package errors."""
from __future__ import annotations

from typing import Any

from aiohttp import ClientResponse
from aiohttp.client_exceptions import ClientError
from yarl import URL


class RainMachineError(Exception):
    """Define a base error."""

    pass


class RequestError(RainMachineError):
    """Define an error related to invalid requests."""

    pass


class TokenExpiredError(RequestError):
    """Define an error for expired access tokens that can't be refreshed."""

    pass


class UnknownAPICallError(RequestError):
    """Define an error for an unknown API call."""

    pass


class UnvalidatedEmailError(RequestError):
    """Define an error for unvalidated email addresses."""

    pass


LOCAL_ERROR_CODE_EXCEPTION_MAPPING = {
    2: TokenExpiredError,
    13: UnknownAPICallError,
}

REMOTE_ERROR_CODE_EXCEPTION_MAPPING = {
    1: UnvalidatedEmailError("The email has not been validated"),
}


def _raise_local_api_error(url: URL, error_code: int, message: str) -> None:
    """Raise the appropriate error for a remote error code.

    Args:
        url: The URL that raised the exception:
        error_code: The RainMachine error code.
        message: The RainMachine error message.

    Raises:
        exc: A RequestError subclass.
    """
    exc: RequestError
    try:
        exc_obj = LOCAL_ERROR_CODE_EXCEPTION_MAPPING[error_code]
        exc = exc_obj(message)
    except KeyError:
        exc = RequestError(
            f"Unknown error returned for {url}: {error_code} -> {message}"
        )
    raise exc


def _raise_remote_api_error(url: URL, error_code: int) -> None:
    """Raise the appropriate error for a remote error code.

    Args:
        url: The URL that raised the exception:
        error_code: The RainMachine error code.

    Raises:
        exc: A RequestError subclass.
    """
    exc: RequestError
    try:
        exc = REMOTE_ERROR_CODE_EXCEPTION_MAPPING[error_code]
    except KeyError:
        exc = RequestError(f"Unknown error code returned for {url}: {error_code}")
    raise exc


def raise_for_error(resp: ClientResponse, data: dict[str, Any] | None) -> None:
    """Raise an error from the remote API if necessary.

    Args:
        resp: The aiohttp ClientResponse that generated the exception.
        data: An optional API response payload.

    Raises:
        RequestError: Raised when any error occurs.
    """
    if data:
        if data.get("errorType") and data["errorType"] > 0:
            # RainMachine's remote cloud uses "errorType" to show errors, so if we find
            # that, we assume we need to raise a remote error:
            _raise_remote_api_error(resp.url, data["errorType"])

        if data.get("statusCode") and data["statusCode"] != 200:
            # RainMachine's local cloud uses "statusCode" to show errors, so if we find
            # that, we assume we need to raise a local error:
            _raise_local_api_error(resp.url, data["statusCode"], data["message"])
    else:
        try:
            resp.raise_for_status()
        except ClientError as err:
            raise RequestError(f"Error while requesting {resp.url}: {err}") from err
