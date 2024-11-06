class Base64ProcessingError(Exception):
    """General exception for image name processing errors."""
    pass

class ExpectedIntegerError(Base64ProcessingError):
    """Výjimka pro případ, že vstupní hodnota není celé číslo."""
    def __init__(self, provided_type: str):
        self.provided_type = provided_type
        super().__init__(
            f"Chyba při převodu čísla {provided_type} na base64 řetězec. "
            "Vstupní hodnota musí být celé číslo."
        )

class ExpectedPositiveIntegerError(Base64ProcessingError):
    """Výjimka pro případ, že vstupní hodnota není kladné číslo."""
    def __init__(self, integer: int):
        self.integer = integer
        super().__init__(
            f"Chyba při převodu čísla {integer} na base64 řetězec. "
            "Vstupní hodnota musí být kladné číslo."
        )

class EmptyOutputError(Base64ProcessingError):
    """Výjimka pro případ, že by výsledkem převodu byl prázdný řetězec."""
    def __init__(self, integer: int):
        self.integer = integer
        super().__init__(
            f"Chyba při převodu čísla {integer} na base64 řetězec. "
            "Výsledný řetězec je prázdný."
        )

class EncodeIntToBase64Error(Base64ProcessingError):
    """Výjimka pro případ pokud funkce encode_int_to_base64 selže."""
    def __init__(self, integer: int, original_exception: Exception):
        self.integer = integer
        self.original_exception = original_exception
        super().__init__(
            f"Chyba při převodu čísla {integer} na base64 řetězec. "
            f"Zachycená chyba: {original_exception}."
        )

class ExpectedStringError(Base64ProcessingError):
    """Výjimka pro případ že vstupní hodnota není řetězec."""
    def __init__(self, provided_type: str):
        self.base64_string = base64_string
        super().__init__(
            f"Chyba při převodu base64 řetězce {base64_string} na číslo. "
            "Vstupní hodnota musí být řetězec."
        )

class EmptyStringError(Base64ProcessingError):
    """Výjimka pro případ, kdy vstupní hodnota je prázdný řetězec."""
    def __init__(self):
        self.base64_string = base64_string
        super().__init__(
            f"Chyba při převodu base64 řetězce {base64_string} na číslo. "
            "Vstupní hodnota nemůže být prázdný řetězec."
        )

class NegativeIntegerOutputError(ImageNameProcessingError):
    """Výjimka pro případ že výsledkem funkce je záporné číslo."""
    def __init__(self, base64_string: str, decoded_int: int):
        self.base64_string = base64_string
        self.decoded_int = decoded_int
        super().__init__(
            f"Chyba při převodu base64 řetězce {base64_string} na číslo. "
            f"Výsledkem nemůže být záporné číslo: {decoded_int}"
        )

class DecodeBase64ToStringError(ImageNameProcessingError):
    """Výjimka pro případ selhání převodu base64 formátu na celé číslo."""
    def __init__(self, integer: int, original_exception: Exception):
        self.integer = integer
        self.original_exception = original_exception
        super().__init__(
            f"Chyba při převodu base64 řetězce {base64_string} na číslo."
            f"Zachycená chyba: {original_exception}."
        )