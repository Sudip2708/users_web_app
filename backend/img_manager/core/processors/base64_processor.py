from typing import Dict, Optional
from datetime import datetime
import time

from users.models.services.utils.log_method import log_method
from users.models.services.utils.is_debug_mode import is_debug_mode
from .processor_utils.base64_utils import (
    encode_int_to_base64,
    decode_base64_to_int
)
from .processor_utils.processor_validation_utils import (
    validate_app_id,
    validate_type_id,
    validate_user_id,
    validate_timestamp
)
from .errors.processor_errors import (
    InvalidBase64StringError,
    MissingParametersError,
    EmptyImageNameError,
    DecodedStringTooShortError,
    ExpectedIntegerError
)

class ImageNameProcessor:
    """Processor for generating and decoding image names."""

    @log_method
    def __init__(
        self,
        app_id: Optional[int] = None,
        type_id: Optional[int] = None,
        user_id: Optional[int] = None,
        base64_name: Optional[str] = None
    ) -> None:
        """
        Initialize the ImageNameProcessor instance.

        Args:
            app_id (Optional[int]): Application ID (1-9).
            type_id (Optional[int]): Image size ID (0-9).
            user_id (Optional[int]): User ID (positive integer).
            base64_name (Optional[str]): Base64 encoded image name.

        Raises:
            MissingParametersError: If neither base64_name nor app_id, type_id, and user_id are provided.
        """
        if base64_name:
            self.data = self._decode_image_name(base64_name)
        elif all(param is not None for param in [app_id, type_id, user_id]):
            self.data = {
                "app_id": app_id,
                "type_id": type_id,
                "user_id": user_id,
                "timestamp": int(time.time())
            }
        else:
            raise MissingParametersError()

        self.debug_mode = is_debug_mode()
        self._validate_data()

    @log_method
    def generate_image_name(self) -> str:
        """
        Generate a base64-encoded image name.

        Returns:
            str: Base64 encoded image name.

        Raises:
            EmptyImageNameError: If the generated base64 name is empty.
            GenerateImageNameError: If the method crash.
        """
        try:
            string = (
                f"{self.data['app_id']}"
                f"{self.data['type_id']}"
                f"{self.data['timestamp']}"
                f"{self.data['user_id']}"
            )
            integer = int(string)
            image_name = encode_int_to_base64(integer)

            if self.debug_mode:
                if not image_name:
                    raise EmptyImageNameError()

            return image_name
        except (ValueError, Base64ProcessingError) as e:
            raise GenerateImageNameError() from e

    @staticmethod
    @log_method
    def _decode_image_name(base64_name: str) -> Dict[str, int]:
        """
        Decode a base64 encoded image name.

        Args:
            base64_name (str): Base64 encoded image name.

        Returns:
            Dict[str, int]: Decoded data including app_id, type_id, timestamp, and user_id.

        Raises:
            DecodedStringTooShortError: If the decoded string is too short.
            DekodeImageNameError: If the method crash.
        """
        try:
            decoded_number = decode_base64_to_int(base64_name)
            decoded_string = str(decoded_number)

            if len(decoded_string) < 13:
                raise DecodedStringTooShortError(base64_name, decoded_string)

            return {
                "app_id": int(decoded_string[0]),
                "type_id": int(decoded_string[1]),
                "timestamp": int(decoded_string[2:12]),
                "user_id": int(decoded_string[12:])
            }
        except (Base64ProcessingError, ValueError) as e:
            raise DekodeImageNameError(base64_name) from e

    @log_method
    def _validate_data(self) -> None:
        """
        Validate the decoded data to ensure it meets expected constraints.

        Raises:
            InvalidAppIDError: If app_id is not between 1 and 9.
            InvalidSizeIDError: If type_id is not between 0 and 9.
            InvalidUserIDError: If user_id is not a positive integer.
            InvalidTimestampError: If the timestamp is invalid.
        """
        validate_app_id(self.data['app_id'])
        validate_type_id(self.data['type_id'])
        validate_user_id(self.data['user_id'])
        validate_timestamp(self.data['timestamp'])
