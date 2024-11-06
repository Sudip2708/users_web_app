"""
Tento soubor slouží pro definici aplikací pro vytváření jména profilového obrázku
"""
import inspect
from dataclasses import dataclass

from backend.shared_utils.decorators.log_method import log_method
from img_manager.utils.dictionary_manager import dictionary_to_string
from img_manager.utils.attributes_manager import attributes_to_string
from img_manager.exceptions.config_errors import (
    MissingAttributeError,
    InvalidAttributeTypeError,
    UnknownDictionaryKeyError,
    AppsMapConfigError
)


@dataclass(frozen=True)
class AppsMapConfig:
    """
    Třída sloužící pro definici aplikací pro vytvoření profilového obrázku.

    Attributes:
        IMAGE_APPS_MAP: Slovník s aplikacemi.
    """
    IMAGE_APPS_MAP = {
        0: "Users",
        # Add additional values as needed
    }

    @staticmethod
    @log_method
    def get_image_app(image_app_id: int) -> str:
        """
        Vrátí textovou reprezentaci aplikace v které je obrázek použit.

        Args:
            image_app_id (int): ID aplikace.

        Returns:
            str: Textová reprezentace aplikace.

        Raises:
            MissingAttributeError: Pokud atribut není součástí třídy.
            InvalidAttributeTypeError: Pokud atribut není slovníkem.
            UnknownDictionaryKeyError: Pokud je zadán neexistující klíč.
        """
        try:
            return AppMapsConfig.IMAGE_APPS_MAP[image_app_id]

        except AttributeError as e:
            raise MissingAttributeError(
                method_name=inspect.currentframe().f_code.co_name,
                class_name=AppMapsConfig.__name__,
                attribute_name = 'IMAGE_APPS_MAP',
                allowed_attributes = attributes_to_string(AppsMapConfig)
            ) from e

        except KeyError as e:
            if not isinstance(AppMapsConfig.IMAGE_APPS_MAP, dict):
                raise InvalidAttributeTypeError(
                    method_name=inspect.currentframe().f_code.co_name,
                    class_name=AppMapsConfig.__name__,
                    attribute_name='IMAGE_APPS_MAP',
                    expected_type='dict',
                    actual_type=type(AppMapsConfig.IMAGE_APPS_MAP).__name__
                ) from e

            raise UnknownDictionaryKeyError(
                method_name=inspect.currentframe().f_code.co_name,
                class_name=AppMapsConfig.__name__,
                dictionary_name='IMAGE_APPS_MAP',
                image_app_id=image_app_id,
                allowed_keys=dictionary_to_string(
                    AppsMapConfig.IMAGE_APPS_MAP.items()
                )
            ) from e

