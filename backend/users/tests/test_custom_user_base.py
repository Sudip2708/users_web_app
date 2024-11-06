"""
Tests for the CustomUser model.

This module contains unit tests for the CustomUser model, covering various
aspects such as username generation, slug creation, email uniqueness, and
default profile image settings.
"""

from django.test import TestCase
from django.utils.text import slugify
from django.db.utils import IntegrityError
from users.models.custom_user import CustomUser


class CustomUserBaseTests(TestCase):
    """Test cases for the CustomUser model."""

    def setUp(self):
        """Initialize test data before each test."""
        self.user = CustomUser.objects.create_user(
            email="testuser@example.com",
            password="password123",
        )

    def test_unique_email(self):
        """
        Test that creating a user with an existing email raises IntegrityError.
        """
        with self.assertRaises(IntegrityError):
            CustomUser.objects.create_user(
                email="testuser@example.com",
                password="password123",
            )

    def test_username_generating(self):
        """Test if username is correctly generated from email."""
        base_username = self.user.email.split('@')[0].lower()
        self.assertEqual(self.user.username, base_username)

    def test_username_lowercase(self):
        """Test that username is converted to lowercase."""
        user = CustomUser.objects.create_user(
            email="John.Doe@example.com",
            password="password123",
        )
        self.assertEqual(user.username, "john.doe")

    def test_username_uniqueness(self):
        """Test if username generation always produces unique usernames."""
        user1 = CustomUser.objects.create_user(
            email="testuser@different_provider1.com",
            password="password123",
        )
        user2 = CustomUser.objects.create_user(
            email="testuser@different_provider2.com",
            password="password123",
        )
        user3 = CustomUser.objects.create_user(
            email="testuser@different_provider3.com",
            password="password123",
        )
        self.assertEqual(user1.username, "testuser1")
        self.assertEqual(user2.username, "testuser2")
        self.assertEqual(user3.username, "testuser3")

    def test_username_change_and_slug_change(self):
        """Test changing username and its effect on slug."""
        user = CustomUser.objects.create_user(
            email="testuser1@example.com",
            password="password123",
        )
        old_username = user.username
        new_username = "new_username"
        user.username = new_username
        user.save()
        self.assertEqual(user.username, new_username)
        self.assertEqual(user.slug, slugify(new_username))
        user.username = old_username
        user.save()
        self.assertEqual(user.username, old_username)
        self.assertEqual(user.slug, slugify(old_username))

    def test_slug_generating(self):
        """Test if slug is correctly generated from username."""
        generate_slug = slugify(self.user.username)
        self.assertEqual(self.user.slug, generate_slug)

    def test_slug_reset_after_change(self):
        """Test if slug field resets to original value after change."""
        generate_slug = slugify(self.user.username)
        self.user.slug = "new_slug"
        self.user.save()
        self.assertEqual(self.user.slug, generate_slug)

    def test_user_str_method(self):
        """Test the __str__ method of the CustomUser model."""
        self.assertEqual(str(self.user), self.user.slug)

    def test_is_active_default(self):
        """Test that is_active is True by default."""
        self.assertTrue(self.user.is_active)

    def test_is_staff_default(self):
        """Test that is_staff is False by default."""
        self.assertFalse(self.user.is_staff)

    def test_is_superuser_default(self):
        """Test that is_superuser is False by default."""
        self.assertFalse(self.user.is_superuser)
        
    # def test_profile_image_default(self):
    #     """Test if profile image has the correct default value."""
    #     self.assertEqual(self.user.profile_image, 'users/profile_pics/default_400x400.png')

    # def test_profile_image_thumbnail_default(self):
    #     """Test if profile image thumbnail has the correct default value."""
    #     self.assertEqual(self.user.profile_image_thumbnail, 'users/profile_pics/default_64x64.png')

    # def test_email_case_insensitivity(self):
    #     """Test that email addresses are treated as case-insensitive."""
    #     with self.assertRaises(IntegrityError):
    #         CustomUser.objects.create_user(
    #             email="TestUser@Example.com",
    #             password="password123",
    #         )

    # def test_username_max_length(self):
    #     """Test that username doesn't exceed the maximum length."""
    #     long_email = 'a' * 150 + '@example.com'
    #     user = CustomUser.objects.create_user(
    #         email=long_email,
    #         password="password123",
    #     )
    #     self.assertLessEqual(len(user.username), 150)  # Assuming max_length is 150


# Další testy, které byste mohli zvážit (v závislosti na vašich konkrétních požadavcích):
#
# Test pro ověření, že heslo není uloženo v čitelné podobě.
# Test pro ověření, že uživatel může změnit své heslo.
# Test pro ověření funkčnosti metody get_full_name(), pokud ji máte implementovanou.
# Test pro ověření, že nelze vytvořit uživatele s neplatnou e-mailovou adresou.