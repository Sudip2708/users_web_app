from pathlib import Path
import os
from typing import List

def list_files_in_directory(directory_path: Path) -> List[str]:
    """
    Retrieves a list of file names in the specified directory.

    Args:
        directory_path (Path): The path to the directory.

    Returns:
        List[str]: A list of file names (including extensions) in the directory.

    Raises:
        FileNotFoundError: If the specified path does not exist.
        NotADirectoryError: If the specified path is a file, not a directory.
        PermissionError: If there are insufficient permissions to access the directory.
        OSError: For other issues with accessing files or the directory.
    """
    try:

        all_items = os.listdir(directory_path)
        files = [
            item for item in all_items
            if (directory_path / item).is_file()
        ]
        return files

    except FileNotFoundError:
        text = "Error: The specified path was not found."
        raise ListFileError(directory_path, text)
    except NotADirectoryError:
        text = "Error: The specified path refers to a file, not a directory."
        raise ListFileError(directory_path, text)
    except PermissionError:
        text = "Error: Insufficient permissions to access the directory or files."
        raise ListFileError(directory_path, text)
    except OSError:
        text = "Error: Problem accessing files or the directory."
        raise ListFileError(directory_path, text)

class UtilityError(Exception):
    """Obecná výjimka pro chyby týkající se obrázků."""
    pass

class ListFileError(UtilityError):
    """Výjimka pro neznámý typ obrázku."""
    self.directory_path = directory_path
    self.text = text
    super().__init__(f"{text} Path: {directory_path}")