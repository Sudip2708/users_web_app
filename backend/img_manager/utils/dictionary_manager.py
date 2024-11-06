"""
Tento soubor slouží pro navrácení obsahu slovníku jako seznamu nebo řetězce.
"""
import inspect

from backend.shared_utils.decorators.log_method import log_method
from backend.shared_utils.environment.is_debug_mode import is_debug_mode
from img_manager.exceptions.utility_errors import (
    ImgManagerUtilityError,
    InvalidDictionaryTypeError,
    EmptyDictionaryError
)

@log_method
def dictionary_to_string(dictionary) -> str:
    """
    Vrátí řetězec s klíči a hodnotami daného slovníku.

    Formát:
        "{key}: {value}, {key}: {value}, ..."

    Returns:
        str: Řetězec s klíči a hodnotami slovníku.

    Raises:
        ImgManagerUtilityError: Pro chyby zachycené v except větvy.
    """
    try:
        dictionary_list = dictionary_to_list(dictionary)
        return ", ".join(key_value_list)

    except (DictionaryTypeError, EmptyDictionaryError) as e:
        raise ImgManagerUtilityError(
            function_name=inspect.currentframe().f_code.co_name,
        ) from e

@log_method
def dictionary_to_list(dictionary) -> list:
    """
    Vrátí seznam řetězců klíč/hodnota daného slovníku.

    Formát:
        [{key}: {value}, {key}: {value}, ...]

    Returns:
        list: Seznam řetězců klíč/hodnota.

    Raises:
        NoAttributeError: Pokud třída nemá atributy.
        EmptyDictionaryError: Pokud výsledkem je prázdný seznam.
        ImgManagerUtilityError: Pro chyby zachycené v except větvy.

    """
    try:
        debute_mode = is_debug_mode()
        if debute_mode:
            if not isinstance(dictionary, dict):
                raise InvalidDictionaryTypeError(
                    function_name=inspect.currentframe().f_code.co_name,
                    detected_type=type(dictionary).__name__
                )
            if not dictionary:
                raise EmptyDictionaryError(
                    function_name=inspect.currentframe().f_code.co_name
                )

        return [
            f"{key}: {value}"
            for key, value in dictionary.items()
        ]

    except (TypeError, AttributeError, ValueError, MemoryError) as e:
        raise ImgManagerUtilityError(
            function_name=inspect.currentframe().f_code.co_name,
        ) from e
