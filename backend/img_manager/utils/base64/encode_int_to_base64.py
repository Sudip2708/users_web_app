from typing import Any
import base64

from users.models.services.utils.log_method import log_method
from users.models.services.utils.is_debug_mode import is_debug_mode
from .base64_utils_errors import (
    ExpectedIntegerError,
    ExpectedPositiveIntegerError,
    EmptyOutputError,
)

@log_method
def encode_int_to_base64(integer: int) -> str:
    """
    Encode an integer into a base64 string.

    Args:
        integer (int): The integer to be encoded.

    Returns:
        str: The base64-encoded string without padding.

    Raises:
        ExpectedIntegerError: If an expected integer is not provided.
        ExpectedPositiveIntegerError: If the integer is negative.
        EncodeIntToBase64Error: If encoding fails.
    """
    debug_mode = is_debug_mode()

    if debug_mode:
        if not isinstance(integer, int):
            raise ExpectedIntegerError(type(integer).__name__)
        if integer < 0:
            raise ExpectedPositiveIntegerError(integer)

    try:
        byte_length = (integer.bit_length() + 7) // 8
        bytes_data = integer.to_bytes(byte_length, byteorder='big')
        encoded = base64.urlsafe_b64encode(bytes_data)
        base64_str = encoded.decode('utf-8').rstrip('=')

        if debug_mode:
            if not base64_str:
                raise EmptyOutputError(integer)

        return base64_str

    except (OverflowError, TypeError, ValueError) as e:
        raise EncodeIntToBase64Error(integer) from e



