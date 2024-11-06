from datetime import datetime
from typing import Dict, Any, Optional

from django.core.exceptions import ObjectDoesNotExist

from users.models.custom_user import CustomUser
from ..image_name.config import ImageNameConfig
from ..image_name.processor import ImageNameProcessor

class ImageNameDecoder:
    """
    A class for decoding and retrieving information from encoded profile image names.

    This class processes a base64 encoded image name, extracts relevant information,
    and provides methods to retrieve decoded details about the image and associated user.

    The class is designed for use in a development environment and returns all results
    as formatted strings, including error messages.

    Example:
        info = ProfileImageInfoDecoder.decode("encoded_image_name_here")
        print(info)
    """

    @staticmethod
    def decode(base64_name: str) -> str:
        """
        Decode the given base64 image name and return all relevant information.

        This static method creates an instance of ProfileImageInfoDecoder and
        returns the decoded information as a formatted string.

        Args:
            base64_name (str): The base64 encoded image name to be processed.

        Returns:
            str: A formatted string containing all decoded information or error messages.
        """
        decoder = ProfileImageInfoDecoder(base64_name)
        return decoder._get_decoded_info()

    def __init__(self, base64_name: str):
        """
        Initialize the ProfileImageInfoDecoder with a base64 encoded image name.

        Args:
            base64_name (str): The base64 encoded image name to be processed.
        """
        self.base64_name = base64_name
        self.data: Optional[Dict[str, Any]] = None
        self.config: Optional[ImageNameConfig] = None

        # Initialize configuration attributes
        self.image_app_map: Dict[int, str] = {}
        self.image_type_map: Dict[int, str] = {}
        self.date_time_format: str = ""
        self.date_format: str = ""
        self.date_min: datetime = datetime.min
        self.date_max: datetime = datetime.max

        try:
            self.data = ImageNameProcessor(base64_name).data
            self.config = ImageNameConfig()

            # Set configuration attributes
            self.image_app_map = self.config.IMAGE_APP_MAP
            self.image_type_map = self.config.IMAGE_TYPE_MAP
            self.date_time_format = self.config.DATE_TIME_FORMAT
            self.date_format = self.config.DATE_FORMAT
            self.date_min = self.config.DATE_MIN
            self.date_max = self.config.DATE_MAX
        except Exception as e:
            self.error = f"Error processing base64 name: {e}"

    def _get_decoded_info(self) -> str:
        """
        Retrieve all decoded information about the image and user.

        Returns:
            str: A formatted string containing all decoded information or error messages.
        """
        if hasattr(self, 'error'):
            return self._get_error_message()

        intro = self._get_intro()
        app = self._get_image_app_info()
        image_type = self._get_image_type_info()
        date = self._format_image_creation_date()
        user = self._retrieve_user_info()
        return f"{intro}{app}{image_type}{date}{user}{'=' * 50}\n"

    def _get_error_message(self) -> str:
        """Generate an error message when decoding fails."""
        return (
            f"\n{'=' * 50}\n"
            f"Error decoding image name: {self.base64_name}\n"
            f"{'-' * 50}\n"
            f"{self.error}\n"
            f"{'=' * 50}\n"
        )

    def _get_intro(self) -> str:
        """Generate an introductory string for the decoded information."""
        return (
            f"\n{'=' * 50}\n"
            f"Decoded image details for the base64 name: {self.base64_name}\n"
            f"{'-' * 50}\n"
        )

    def _get_image_app_info(self) -> str:
        """Retrieve information about the image application."""
        intro = "Image App: "
        try:
            app_id = self.data['app_id']
            app = self.image_app_map[app_id]
            return f"{intro}{app}\n"
        except (KeyError, TypeError, ValueError) as e:
            return f"{intro}Error retrieving app name: {e}\n"

    def _get_image_type_info(self) -> str:
        """Retrieve information about the image type."""
        intro = "Image Type: "
        try:
            type_id = self.data['type_id']
            image_type = self.image_type_map[type_id]
            return f"{intro}{image_type}\n"
        except (KeyError, TypeError, ValueError) as e:
            return f"{intro}Error retrieving image type: {e}\n"

    def _retrieve_user_info(self) -> str:
        """Retrieve information about the associated user."""
        intro = "User: "
        try:
            user_id = self.data['user_id']
            user = CustomUser.objects.get(pk=user_id)
            last_login_date = user.last_login.strftime(self.date_time_format)
            return (
                f"{intro}\n"
                f"- User ID: {user.id}\n"
                f"- Username: {user.username}\n"
                f"- User email: {user.email}\n"
                f"- Last Login: {last_login_date}\n"
            )
        except ObjectDoesNotExist:
            return f"{intro}User with ID {user_id} does not exist.\n"
        except (KeyError, AttributeError, TypeError, ValueError) as e:
            return f"{intro}Error retrieving user info: {e}\n"

    def _format_image_creation_date(self) -> str:
        """Format and validate the image creation date."""
        intro = "Created: "
        try:
            timestamp = self.data['timestamp']
            datetime_transfer = datetime.utcfromtimestamp(timestamp)

            if self.date_min < datetime_transfer < self.date_max:
                date = datetime_transfer.strftime(self.date_time_format)
                return f"{intro}{date}\n"
            else:
                date = datetime_transfer.strftime(self.date_format)
                return (
                    f"{intro}Date {date} is outside the valid range "
                    f"({self.date_min.strftime(self.date_format)} - "
                    f"{self.date_max.strftime(self.date_format)}).\n"
                )
        except (KeyError, AttributeError, TypeError, ValueError, OSError) as e:
            return f"{intro}Error retrieving creation date: {e}\n"