from datetime import datetime

from .processor_errors import (
    ExpectedIntegerError,
    InvalidAppIDError,
    InvalidSizeIDError,
    InvalidUserIDError,
    InvalidTimestampError,
)

@log_method
def validate_app_id(app_id: int) -> None:
    """
    Validate the app_id.

    Args:
        app_id (int): The app ID to validate.

    Raises:
        ExpectedIntegerError: If app_id is not an integer.
        InvalidAppIDError: If app_id is not between 1 and 9.
    """
    if not isinstance(app_id, int):
        raise ExpectedIntegerError(type(app_id).__name__)
    if not 1 <= app_id <= 9:
        raise InvalidAppIDError(app_id)

@log_method
def validate_type_id(type_id: int) -> None:
    """
    Validate the type_id.

    Args:
        type_id (int): The size ID to validate.

    Raises:
        ExpectedIntegerError: If type_id is not an integer.
        InvalidSizeIDError: If type_id is not between 0 and 9.
    """
    if not isinstance(type_id, int):
        raise ExpectedIntegerError(type(type_id).__name__)
    if not 0 <= type_id <= 9:
        raise InvalidSizeIDError(type_id)

@log_method
def validate_user_id(user_id: int) -> None:
    """
    Validate the user_id.

    Args:
        user_id (int): The user ID to validate.

    Raises:
        ExpectedIntegerError: If user_id is not an integer.
        InvalidUserIDError: If user_id is not a positive integer.
    """
    if not isinstance(user_id, int):
        raise ExpectedIntegerError(type(user_id).__name__)
    if user_id <= 0:
        raise InvalidUserIDError(user_id)

@log_method
def validate_timestamp(timestamp: int) -> None:
    """
    Validate the timestamp.

    Args:
        timestamp (int): The timestamp to validate.

    Raises:
        InvalidTimestampError: If the timestamp is invalid.
    """
    try:
        datetime.utcfromtimestamp(timestamp)
    except (OSError, OverflowError, TypeError, ValueError) as e:
        raise InvalidTimestampError(timestamp) from e