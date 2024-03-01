"""Define common test utilities."""

import os

TEST_ACCESS_TOKEN = "12345abcdef"  # noqa: S105
TEST_API_VERSION = "4.5.0"
TEST_EMAIL = "user@host.com"
TEST_HOST = "192.168.1.100"
TEST_HW_VERSION = "3"
TEST_MAC = "ab:cd:ef:12:34:56"
TEST_NAME = "My House"
TEST_PASSWORD = "the_password_123"  # noqa: S105
TEST_PORT = 8081
TEST_SPRINKLER_ID = "12345abcde"
TEST_SW_VERSION = "4.0.925"
TEST_TOTP_CODE = 123456
TEST_URL = f"https://{TEST_HOST}:{TEST_PORT}"


def load_fixture(filename: str) -> str:
    """Load a fixture.

    Args:
        filename: The filename of the fixtures/ file to load.

    Returns:
        A string containing the contents of the file.
    """
    path = os.path.join(os.path.dirname(__file__), "fixtures", filename)
    with open(path, encoding="utf-8") as fptr:
        return fptr.read()
