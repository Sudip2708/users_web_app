from typing import Any
import base64

from users.models.services.utils.log_method import log_method
from users.models.services.utils.is_debug_mode import is_debug_mode
from .base64_utils_errors import (
    ExpectedStringError,
    NegativeIntegerOutputError,
    InvalidBase64StringError,
)

@log_method
def decode_base64_to_int(base64_string: str) -> int:
    """Decodes a base64 string to an integer.

    Args:
        base64_string (str): The base64 string to decode.

    Returns:
        int: The decoded integer.

    Raises:
        EmptyBase64StringError: If the base64 string is empty.
        DecodeNegativeIntegerError: If the integer is negative.
        InvalidBase64StringError: If the base64 string is invalid.
    """
    debug_mode = is_debug_mode()

    if debug_mode:
        if not isinstance(base64_string, str):
            raise ExpectedStringError(type(base64_string).__name__)
        if not base64_string:
            raise EmptyStringError()

    try:
        padding = '=' * (-len(base64_string) % 4)
        padded_string = base64_string + padding
        decoded_bytes = base64.urlsafe_b64decode(padded_string)
        decoded_int = int.from_bytes(decoded_bytes, byteorder='big')

        if debug_mode:
            if decoded_int < 0:
                raise NegativeIntegerOutputError(base64_string, decoded_int)

        return decoded_int
    except (base64.binascii.Error, TypeError, ValueError) as e:
        raise DecodeBase64ToStringError(base64_string) from e


