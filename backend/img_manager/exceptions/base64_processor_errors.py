class ImageNameProcessingError(Exception):
    """General exception for image name processing errors."""
    pass

class MissingParametersError(ImageNameProcessingError):
    """Výjimka pro případ, že nejsou dodány potřebné vstupní údaje."""
    def __init__(self):
        super().__init__(
            "Chyba inicializace třídy ImageNameProcessor. "
            "Nebyl zadán žádný parametr. "
            "Pro inicializaci třýdy musí být zadán buď base64_name parametr, "
            "nebo tyto tři údaje: app_id, type_id, user_id."
        )

class EmptyImageNameError(ImageNameProcessingError):
    """Pokud metoda generate_image_name nevrátí žádnou hodnotu."""
    def __init__(self):
        super().__init__(
            "Chyba při vytváření jména nového obrázku. "
            "Metoda pro vytvoření jména encode_int_to_base64 "
            "vrátila prázdnou hodnotu. "
        )

class GenerateImageNameError(ImageNameProcessingError):
    """Výjimka pro případ pokud metoda generate_image_name selže."""
    def __init__(self, original_exception: Exception):
        self.original_exception = original_exception
        super().__init__(
            f"Chyba při vytváření jména nového obrázku"
            f"Zachycená chyba: {original_exception}."
        )

class DecodedStringTooShortError(ImageNameProcessingError):
    """Výjimka pro případ že dekodované číslo je příliš krátké (<13 znaků)"""
    def __init__(self, base64_name: str, decoded_string: str):
        self.decoded_string = decoded_string
        super().__init__(
            f"Chyba při dekodování vstupního base 64 řetězce: {base64_name}. "
            "Funkce decode_base64_to_int nevrátila hodnotu "
            f"s minimálním počtem znaků (13): {decoded_string}."
        )

class DekodeImageNameError(ImageNameProcessingError):
    """Výjimka pro případ pokud metoda _decode_image_name selže."""
    def __init__(self, base64_name: str, original_exception: Exception):
        self.base64_name = base64_name
        self.original_exception = original_exception
        super().__init__(
            f"Chyba při dekodování vstupního base 64 řetězce: {base64_name}. "
            f"Zachycená chyba: {original_exception}."
        )
