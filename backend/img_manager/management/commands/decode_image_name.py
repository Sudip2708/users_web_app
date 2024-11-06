"""
This module contains a Django management command for decoding base64-encoded
profile image names.

For detailed usage instructions, refer to the docstring of the Command class.
"""

from django.core.management.base import BaseCommand
from users.models.utils.image_name_decode import ImageNameDecoder

class Command(BaseCommand):
    """
    Decodes a base64-encoded profile image name and prints detailed user
    information.

    This command decodes a base64-encoded profile image name to retrieve
    detailed user information, such as the application name, image type,
    creation date, and user details including ID, username, email,
    and last login.

    Args:
        encoded_image_name (str): The base64-encoded image name to decode.

    Example usage:
        To use this command, run the following in your terminal:

        ```bash
        $ python manage.py decode_image_name {encoded_image_name}
        ```

        For example:
        ```bash
        $ python manage.py decode_image_name 7Nnen9k
        ```

    Output:
        The decoded image name details will be printed to the console,
        including:
        - Application name
        - Image type
        - Creation date
        - User information (ID, username, email, last login)

    Note:
        This command internally uses the `decode_profile_image_name` function
        to decode the input string and display the result.
    """

    help = 'Decode base64 image name and print user info'

    def add_arguments(self, parser):
        parser.add_argument('encoded_image_name', type=str)

    def handle(self, *args, **kwargs):
        encoded_image_name = kwargs['encoded_image_name']
        result = ImageNameDecoder.decode(encoded_image_name)
        self.stdout.write(self.style.SUCCESS(result))
