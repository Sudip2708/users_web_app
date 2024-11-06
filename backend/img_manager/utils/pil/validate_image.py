import logging
from PIL import Image
from django.core.exceptions import ValidationError

def validate_image_format(image_path: str) -> None:
    """Validate that the file at the given path is a valid image.

    This function attempts to open and verify the image using PIL (Python
    Imaging Library). If the image is invalid or cannot be opened, it logs
    an error and raises a ValidationError.

    Args:
        image_path (str): The file path to the image to be validated. This
            should be an absolute path or a path relative to the current
            working directory.

    Raises:
        ValidationError: If the file is not a valid image or cannot be opened.

    Example:
        >>> try:
        ...     validate_image_format('path/to/image.jpg')
        ...     print("Image is valid")
        ... except ValidationError:
        ...     print("Image is invalid")

    Note:
        This function does not return the opened image. It only validates
        the image format.
    """
    try:
        with Image.open(image_path) as img:
            img.verify()
    except (IOError, SyntaxError) as e:
        logging.error(f"Failed to validate image: {image_path}", exc_info=True)
        raise ValidationError("The uploaded file is not a valid image.") from e