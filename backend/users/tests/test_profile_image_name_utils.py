"""
This file contains tests for image name generation and decoding functions.

The TestProfileImageNameUtils class inherits from `unittest.TestCase`
and implements individual tests for the functions:

* `generate_image_name`
* `decode_image_name`

The tests cover various input values and verify the correctness of the output.

Different test scenarios are used, including boundary values and invalid inputs.
"""

import unittest
import time

from ..models.utils.profile_image_name_utils import generate_image_name
from ..models.utils.profile_image_name_utils import decode_image_name

class TestProfileImageNameUtils(unittest.TestCase):
    """Test cases for profile image name utilities."""

    def test_generate_valid_input(self):
        """Test generating a name with valid inputs."""
        name = generate_image_name(5, 3, 1234)

        self.assertIsInstance(name, str)
        self.assertTrue(len(name) > 0)

    def test_generate_invalid_app_id(self):
        """Test generating a name with an invalid app_id."""
        with self.assertRaises(ValueError):
            generate_image_name(0, 3, 1)
        with self.assertRaises(ValueError):
            generate_image_name(10, 3, 12)
        with self.assertRaises(ValueError):
            generate_image_name(-1, 3, 123)

    def test_generate_invalid_type_id(self):
        """Test generating a name with an invalid type_id."""
        with self.assertRaises(ValueError):
            generate_image_name(5, 10, 1)
        with self.assertRaises(ValueError):
            generate_image_name(5, -1, 12)

    def test_generate_invalid_user_id(self):
        """Test generating a name with an invalid user_id."""
        with self.assertRaises(ValueError):
            generate_image_name(5, 3, 0)
        with self.assertRaises(ValueError):
            generate_image_name(5, 3, -1)

    def test_decode_valid_input(self):
        """Test decoding a valid input."""
        app_id, type_id, user_id = 5, 3, 1234
        name = generate_image_name(app_id, type_id, user_id)
        decoded = decode_image_name(name)

        self.assertIsInstance(decoded, dict)
        self.assertEqual(decoded['app_id'], app_id)
        self.assertEqual(decoded['type_id'], type_id)
        self.assertEqual(decoded['user_id'], user_id)
        self.assertTrue(abs(decoded['timestamp'] - int(time.time())) < 10)
        # Tolerance of 10 seconds

    def test_decode_invalid_input(self):
        """Test decoding an invalid input."""
        with self.assertRaises(ValueError):
            decode_image_name("invalid_base64_string")

    def test_boundary_minimal_values(self):
        """Test boundary minimal values."""
        min_name = generate_image_name(1, 0, 1)
        min_decoded = decode_image_name(min_name)

        self.assertEqual(min_decoded['app_id'], 1)
        self.assertEqual(min_decoded['type_id'], 0)
        self.assertEqual(min_decoded['user_id'], 1)

    def test_boundary_maximal_values(self):
        """Test boundary maximal values."""
        max_32_bit_number = 2 ** 32 - 1
        max_name = generate_image_name(9, 9, max_32_bit_number)
        max_decoded = decode_image_name(max_name)

        self.assertEqual(max_decoded['app_id'], 9)
        self.assertEqual(max_decoded['type_id'], 9)
        self.assertEqual(max_decoded['user_id'], max_32_bit_number)

