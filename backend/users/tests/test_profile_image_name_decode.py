"""
This file contains tests for functions that decode user profile image names.

The TestProfileImageNameDecode class inherits from `unittest.TestCase`
and implements individual tests for the following functions:

* `decode_profile_image_name`
* `get_image_app_info`
* `get_image_type_info`
* `format_image_creation_date`
* `retrieve_user_info`

The tests cover both successful and failure scenarios and verify the behavior
of the functions under various conditions.

Mock objects are used for `CustomUser.objects.get` and `decode_image_name`
to simplify testing.
"""

import unittest
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

from django.core.exceptions import ObjectDoesNotExist

from users.models.utils.profile_image_name_decode import (
    ConfigSettings,
    decode_profile_image_name,
    get_image_app_info,
    get_image_type_info,
    format_image_creation_date,
    retrieve_user_info,
)


class TestProfileImageNameDecode(unittest.TestCase):
    """Test cases for profile image name decoding utilities."""

    _file_path = 'users.models.utils.profile_image_name_decode'

    def setUp(self):
        """Set up test fixtures."""
        self.mock_user = MagicMock()
        self.mock_user.id = 1
        self.mock_user.username = "test_user"
        self.mock_user.email = "test@example.com"
        self.mock_user.last_login = datetime(2024, 9, 20, 14, 0, 0)
        self.file_path = 'users.models.utils.profile_image_name_decode'

    @patch(f'{_file_path}.CustomUser.objects.get')
    @patch(f'{_file_path}.decode_image_name')
    def test_decode_profile_image_name(self, mock_decode, mock_get_user):
        """Test successful decoding of profile image name."""
        mock_decode.return_value = {
            'app_id': 1,
            'type_id': 0,
            'timestamp': 1726664971,
            'user_id': 1
        }
        mock_get_user.return_value = self.mock_user

        result = decode_profile_image_name('dummy_encoded_name')

        self.assertIn("Decoded image details for: dummy_encoded_name", result)
        self.assertIn("Image App: Users", result)
        self.assertIn("Image Type: Profile picture - master", result)
        self.assertIn("Created: 2024-09-18 13:09:31", result)
        self.assertIn("User ID: 1", result)
        self.assertIn("Username: test_user", result)
        self.assertIn("User email: test@example.com", result)
        self.assertIn("Last Login: 2024-09-20 14:00:00", result)

    @patch(f'{_file_path}.CustomUser.objects.get')
    @patch(f'{_file_path}.decode_image_name')
    def test_decode_profile_image_name_error(self, mock_decode, mock_get_user):
        """Test error handling in profile image name decoding."""
        mock_decode.side_effect = ValueError("Invalid input")
        mock_get_user.return_value = self.mock_user

        result = decode_profile_image_name('invalid_encoded_name')

        self.assertIn("Error decoding image name: Invalid input", result)

    def test_get_image_app_info_known(self):
        """Test retrieval of known image app info."""
        result = get_image_app_info(1)

        self.assertEqual(result, "Users")

    def test_get_image_app_info_unknown(self):
        """Test retrieval of unknown image app info."""
        result = get_image_app_info(99)

        self.assertEqual(result, "Unknown App")

    def test_get_image_type_info_known(self):
        """Test retrieval of known image type info."""
        result = get_image_type_info(0)

        self.assertIn("Profile picture - master", result)

    def test_get_image_type_info_unknown(self):
        """Test retrieval of unknown image type info."""
        result = get_image_type_info(99)

        self.assertEqual(result, "Unknown image type")

    def test_format_image_creation_date_inder(self):
        """Test formatting of valid image creation date."""
        result = format_image_creation_date(1632150000)

        self.assertEqual(result, "2021-09-20 15:00:00")

    def test_format_image_creation_date_below_minimum(self):
        """Test formatting of image creation date set below minimum."""
        below_minimum_date = ConfigSettings.DATE_MIN - timedelta(days=1)
        timestamp_format = below_minimum_date.timestamp()

        result = format_image_creation_date(timestamp_format)

        self.assertIn("Date is out of the setting boundaries", result)
        self.assertIn("Acquired date", result)

    def test_format_image_creation_above_maximum(self):
        """Test formatting of image creation date set above maximum."""
        above_maximum_date = ConfigSettings.DATE_MAX + timedelta(days=1)
        timestamp_format = above_maximum_date.timestamp()

        result = format_image_creation_date(timestamp_format)

        self.assertIn("Date is out of the setting boundaries", result)
        self.assertIn("Acquired date", result)

    def test_format_image_creation_date_invalid(self):
        """Test formatting of invalid image creation date."""
        result = format_image_creation_date('invalid')

        self.assertIn("Invalid timestamp format!", result)

    @patch(f'{_file_path}.CustomUser.objects.get')
    def test_retrieve_user_info_existing(self, mock_get):
        """Test retrieval of existing user info."""
        mock_get.return_value = self.mock_user

        result = retrieve_user_info(123)

        self.assertIn("User ID: 1", result)
        self.assertIn("Username: test_user", result)
        self.assertIn("User email: test@example.com", result)
        self.assertIn("Last Login: 2024-09-20 14:00:00", result)

    def test_user_not_found(self):
        """Test handling of non-existent user."""
        user_id = 9999999999

        result = retrieve_user_info(user_id)

        self.assertIn(f"User: User with ID {user_id} not found.", result)
