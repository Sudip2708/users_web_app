from PIL import Image
from django.core.exceptions import ValidationError

def validate_tuple_with_two_integers(size: tuple):
    """
    Validátor tuple a zda obsahuje dvě celočíselné hodnoty.

    Uprčeno pro ověření tuple hodnot, které mají splňovat tyto podmínky.
    Například pro nastavení DPI a nebo Velikosti obrázku.

    Args:
        tuple: Tuple který má být ověřen.
    """
    if not isinstance(size, tuple) or len(size) != 2:
        raise ValueError(
            "Parametr 'size' musí být tuple se dvěma hodnotami.")

    if not all(isinstance(dim, int) for dim in size):
        raise ValueError("Obě hodnoty v 'size' musí být celočíselné.")

def resize_image(self, image: Image.Image, size: tuple) -> Image.Image:
    """
    Metoda pro změnu velikosti obrázku podle daného rozměru.

    Args:
        image: Obrázek otevřený v PIL.
        size: Tuple pro nastavení velikosti obrázku.

    Returns:
        Obrázek se změněnou velikostí.

    Raises:
        ValueError: Pokud se jedná o špatné hodnoty pro nastavení velikosti.
    """
    try:
        validate_tuple_with_two_integers(size)
        return image.resize(size, Image.LANCZOS)
    except Exception as e:
        raise ValueError(f"Chyba při změně velikosti obrázku: {e}")