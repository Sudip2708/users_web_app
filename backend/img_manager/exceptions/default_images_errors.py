class ImageProcessingError(Exception):
    """Obecná výjimka pro chyby týkající se obrázků."""
    pass

class UnknownImageTypeError(ImageProcessingError):
    """Výjimka pro neznámý typ obrázku."""
    def __init__(self, img_type: str, img_types: str):
        self.img_type = img_type
        self.img_types = img_types
        super().__init__(
            f"Neznámý typ obrázku: '{img_type}'. "
            f"Správné hodnoty: '{img_types}'."
        )

class MissingAttributeError(ImageProcessingError):
    """Výjimka pro chybějící atribut v třídě."""
    def __init__(self, attribute_name: str, class_name: str):
        self.attribute_name = attribute_name
        self.class_name = class_name
        super().__init__(
            f"Atribut '{self.attribute_name}' "
            f"není definován v třídě '{self.class_name}'."
        )

class ImagePathError(ImageProcessingError):
    """Výjimka pro chyby spojené se získáváním cesty k obrázkům."""
    def __init__(self, img_type: str):
        self.img_type = img_type
        super().__init__(
            f"Chyba při získávání cesty k obrázku pro typ: '{img_type}'."
        )

class NonexistentImagePathError(ImageProcessingError):
    """Výjimka pro nenalezení souboru obrázku na dané cestě."""
    def __init__(self, img_type: str):
        self.absolute_path = absolute_path
        super().__init__(
            f"Cesta: '{absolute_path}' neodkazuje na žádný soubor."
        )

class ImageNameError(ImageError):
    """Výjimka pro chyby spojené se získáváním cesty k obrázkům."""
    def __init__(self, img_type: str):
        self.img_type = img_type
        super().__init__(
            f"Chyba při získávání ID velikosti pro typ: '{img_type}'"
        )

class InvalidUserIDError(ValueError):
    """Výjimka pro neplatné ID uživatele."""
    def __init__(self, user_id: int):
        self.user_id = user_id
        super().__init__(
            f"Neplatné ID uživatele: '{user_id}'"
        )
