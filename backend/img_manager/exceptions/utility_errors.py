class ImgManagerUtilityError(Exception):
    """Výjimka pro předání dříve zachycených chyb"""
    def __init__(self, function_name: str):
        self.function_name = function_name
        super().__init__(
            f"Chyba zachycená ve funkci {function_name}."
        )

class InvalidDictionaryTypeError(ImgManagerUtilityError):
    """Výjimka pro případ že se nejdná o slovník."""
    def __init__(self, function_name: str, detected_type: str):
        super().__init__(function_name)
        self.detected_type = detected_type
        self.message = (
            f"{self.message} Vstupní objekt není platný typ pro slovník. "
            f"Zjištěný typ: {detected_type}."
        )

class EmptyDictionaryError(ImgManagerUtilityError):
    """Výjimka pro případ že daný slovník nemá žádné klíče a hodnoty."""
    def __init__(self, function_name: str):
        super().__init__(function_name)
        self.message = (
            f"{self.message} Vstupní slovník neobsahuje žádné data."
        )

class InvalidClassTypeError(ImgManagerUtilitiesError):
    """Výjimka pro případ že se nejdná o třídu."""
    def __init__(self, function_name: str, detected_type: str):
        super().__init__(function_name)
        self.detected_type = detected_type
        self.message = (
            f"{self.message} Vstupní objekt není platný typ pro třídu. "
            f"Zjištěný typ: {detected_type}."
        )

class NoAttributeError(ImgManagerUtilitiesError):
    """Výjimka pro případ že daná třída nemá žádný atribut."""
    def __init__(self, function_name: str, class_name: str):
        super().__init__(function_name)
        self.class_name = class_name
        self.message = (
            f"{self.message} Třída {class_name} nemá žádné atributy."
        )