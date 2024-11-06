import os

def is_debug_mode() -> bool:
    """Check if the application is in debug mode.

    Returns:
        bool: True if in debug mode, False otherwise.
    """
    return os.getenv('DEBUG', 'False').lower() in ('true', '1', 't')
