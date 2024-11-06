"""
Tento soubor slouží pro navrácení atributů třídy jako seznamu nebo řetězce.
"""
import inspect

from backend.shared_utils.decorators.log_method import log_method
from backend.shared_utils.environment.is_debug_mode import is_debug_mode
from img_manager.exceptions.utility_errors import (
    ImgManagerUtilityError,
    InvalidClassTypeError,
    NoAttributeError
)

@log_method
def attributes_to_string(cls) -> str:
    """
    Vrátí řetězec názvů všech atributů dané třídy.

    Formát:
        "{attribute1}, {attribute2}, ..."

    Returns:
        str: Řetězec s názvy atributů třídy.

    Raises:
        ImgManagerUtilityError: Pro chyby zachycené v except větvy.
    """
    try:
        attributes_list = attributes_to_list(cls)
        return ", ".join(attributes_list)

    except (InvalidClassTypeError, NoAttributeError) as e:
        raise ImgManagerUtilityError(
            function_name=inspect.currentframe().f_code.co_name
        ) from e

@log_method
def attributes_to_list(cls) -> list:
    """
    Vrátí seznam názvů všech atributů dané třídy.

    Formát:
        [{attribute1}, {attribute2}, ...]

    Returns:
        list: Seznam názvů atributů třídy.

    Raises:
        NoAttributeError: Pokud třída nemá atributy.
        TypeError: Pokud atributy nejsou správně strukturovány.
        ImgManagerUtilityError: Pro chyby zachycené v except větvy.
    """

    try:
        debute_mode = is_debug_mode()
        if debute_mode:
            if not isinstance(cls, type):
                raise InvalidClassTypeError(
                    function_name=inspect.currentframe().f_code.co_name,
                    detected_type=type(cls).__name__
                )

        attribute_names_list = [
            key for key in vars(cls)
            if not key.startswith('__')
        ]

        if debute_mode:
            if not attribute_names_list:
                raise ClassHasNoAttributeError(
                    function_name=inspect.currentframe().f_code.co_name,
                    class_name=cls.__name__
                )

        return attribute_names

    except (TypeError, AttributeError, ValueError, MemoryError) as e:
        raise ImgManagerUtilityError(
            function_name=inspect.currentframe().f_code.co_name,
        ) from e
