class ImageNameProcessingError(Exception):
    """General exception for image name processing errors."""
    pass

class ExpectedIntegerError(Base64ProcessingError):
    """Výjimka pro případ, že vstupní hodnota není celé číslo"""
    def __init__(self, provided_type: str):
        self.provided_type = provided_type
        super().__init__(
            "Chyba validace vstupních dat třídy ImageNameProcessor. "
            "Vstupní hodnota musí být celé číslo. "
            "Obdržený typ vstupní hodnoty: {provided_type}."
        )

class InvalidAppIDError(ImageNameProcessingError):
    """Výjimka pro případ, že app_id nemá povolenou hodnotu (1-9)."""
    def __init__(self, app_id: int):
        self.app_id = app_id
        super().__init__(
            "Chyba validace vstupních dat třídy ImageNameProcessor. "
            "Hodnota app_ID musí být v rozmezí čísel 1 a 9. "
            f"Obdržená hodnota: {app_id}."
        )

class InvalidSizeIDError(ImageNameProcessingError):
    """Výjimka pro případ, že type_id nemá povolenou hodnotu (0-9)."""
    def __init__(self, type_id: int):
        self.type_id = type_id
        super().__init__(
            "Chyba validace vstupních dat třídy ImageNameProcessor. "
            "Hodnota type_id musí být v rozmezí čísel 0 a 9. "
            f"Obdržená hodnota: {type_id}."
        )


class InvalidUserIDError(ImageNameProcessingError):
    """Výjimka pro případ, že user_id nemá povolenou hodnotu (1<)."""
    def __init__(self, user_id: int):
        self.user_id = user_id
        super().__init__(
            "Chyba validace vstupních dat třídy ImageNameProcessor. "
            "Hodnota user_id musí být kladné číslo. "
            f"Obdržená hodnota: {user_id}."
        )

class InvalidTimestampError(ImageNameProcessingError):
    """Výjimka pro případ, že timestamp není platným datetime formátem."""
    def __init__(self, timestamp: int, original_exception: Exception):
        self.timestamp = timestamp
        self.original_exception = original_exception
        super().__init__(
            "Chyba validace vstupních dat třídy ImageNameProcessor. "
            "Hodnota timestamp musí platný datetime formát. "
            f"Zachycená chyba: {original_exception}."
        )
