"""
Tests for the CustomUserManager class.

This module contains unit tests for the CustomUserManager class, covering both
successful scenarios (creating users and superusers) and error cases (missing
email, incorrect superuser flags, etc.).
"""

from django.test import TestCase
from django.core.exceptions import ValidationError
from users.models.custom_user import CustomUser


class CustomUserManagerTests(TestCase):
    """Test cases for CustomUserManager."""

    def test_create_user_success(self):
        """Test successful user creation."""
        user = CustomUser.objects.create_user(
            email="testuser@example.com",
            password="password123",
        )
        self.assertEqual(user.email, "testuser@example.com")
        self.assertTrue(user.check_password("password123"))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_user_no_email(self):
        """Test user creation with no email raises ValueError."""
        with self.assertRaises(ValueError) as context:
            CustomUser.objects.create_user(email=None, password="password123")
        self.assertEqual(str(context.exception), "E-mail must be provided.")

    def test_create_user_no_password(self):
        """Test user creation with no password raises ValueError."""
        with self.assertRaises(ValueError) as context:
            CustomUser.objects.create_user(
                email="testuser@example.com",
                password=None
            )
        self.assertEqual(str(context.exception), "Password must be provided.")

    def test_create_superuser_success(self):
        """Test successful superuser creation."""
        superuser = CustomUser.objects.create_superuser(
            email="admin@example.com",
            password="password123",
            username="adminuser",
            slug="adminuser-slug"
        )
        self.assertEqual(superuser.email, "admin@example.com")
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_active)

    def test_create_superuser_invalid_is_staff(self):
        """Test superuser creation with is_staff=False raises ValueError."""
        with self.assertRaises(ValueError) as context:
            CustomUser.objects.create_superuser(
                email="admin@example.com",
                password="password123",
                is_staff=False
            )
        self.assertEqual(
            str(context.exception), "Superuser must have is_staff=True."
        )

    def test_create_superuser_invalid_is_superuser(self):
        """Test superuser creation with is_superuser=False raises ValueError."""
        with self.assertRaises(ValueError) as context:
            CustomUser.objects.create_superuser(
                email="admin@example.com",
                password="password123",
                is_superuser=False
            )
        self.assertEqual(
            str(context.exception), "Superuser must have is_superuser=True."
        )

    def test_create_user_normalize_email(self):
        """Test email normalization during user creation."""
        user = CustomUser.objects.create_user(
            email="TestUser@EXAMPLE.com",
            password="password123"
        )
        self.assertEqual(user.email, "TestUser@example.com")

    def test_create_superuser_with_extra_fields(self):
        """Test superuser creation with additional fields."""
        superuser = CustomUser.objects.create_superuser(
            email="admin@example.com",
            password="password123",
            first_name="Admin",
            last_name="User"
        )
        self.assertEqual(superuser.first_name, "Admin")
        self.assertEqual(superuser.last_name, "User")

    def test_create_user_with_extra_fields(self):
        """Test user creation with additional fields."""
        user = CustomUser.objects.create_user(
            email="testuser@example.com",
            password="password123",
            first_name="Test",
            last_name="User"
        )
        self.assertEqual(user.first_name, "Test")
        self.assertEqual(user.last_name, "User")