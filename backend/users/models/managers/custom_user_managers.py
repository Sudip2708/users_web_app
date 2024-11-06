"""
Provides CustomUserManager for managing user accounts in Django.

This module contains a custom user manager that extends Django's BaseUserManager
to handle user creation and superuser creation with email as the unique identifier.
"""

from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    """
    Custom user manager for creating users and superusers with email."""

    def create_user(self, email: str, password: str, **extra_fields) -> 'User':
        """
        Create and save a regular user with the given email and password.

        Args:
            email: The user's email address.
            password: The user's password.
            **extra_fields: Additional fields to be saved on the user model.

        Returns:
            The newly created user instance.

        Raises:
            ValueError: If the email or password is not provided.
        """
        if not email:
            raise ValueError("E-mail must be provided.")
        if not password:
            raise ValueError("Password must be provided.")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email: str, password: str, **extra_fields) -> 'User':
        """
        Create and save a superuser with the given email and password.

        Args:
            email: The superuser's email address.
            password: The superuser's password.
            **extra_fields: Additional fields to be saved on the user model.

        Returns:
            The newly created superuser instance.

        Raises:
            ValueError: If is_staff or is_superuser is set to False.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)