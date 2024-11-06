import os
from django.core.exceptions import ValidationError

def validate_file_size(file_path: str, min_mb, max_mb) -> None:
    """
    Metoda ověří, zda má obrázek správnou velikost.

    Args:
        image_path: Absolutní cesta k obrázku.
        min_mb: Minimální velikost obrázku pro ověření (MB).
        max_mb: Maximální velikost obrázku pro ověření (MB).

    Raises:
        ValidationError: Pokud obrázek nevyhovuje nastaveným limitům.
    """
    min_size_bytes = min_mb * 1024 * 1024
    max_size_bytes = max_mb * 1024 * 1024
    file_size = os.path.getsize(image_path)
    if image_size < min_size_bytes:
        raise ValidationError(
            f"Velikost obrázku nesmí být menší než {min_mb} MB.")
    elif image_size > max_size_bytes:
        raise ValidationError(
            f"Velikost obrázku nesmí překročit {max_mb} MB.")