import os

def delete_file(file_path: str):
    """Smaže soubor, pokud existuje."""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except OSError as e:
        print(f"Varování: Nelze smazat soubor {file_path}: {e}")