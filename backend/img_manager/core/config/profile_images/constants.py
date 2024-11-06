"""
Tento soubor slouží k definici konstant pro profilové obrázky uživatele.
"""
import inspect
from dataclasses import dataclass, field
from typing import Dict, Tuple

from backend.shared_utils.decorators.log_method import log_method
from img_manager.exceptions.config_errors import (
    MissingAttributeError,
    # InvalidAttributeTypeError,
    # UnknownDictionaryKeyError,
    # AppsMapConfigError
)

@dataclass(frozen=True)
class ProfileImageConfig():
    """
    Definuje konfiguraci pro zpracování profilových obrázků uživatelů.

    Attributes:
        APP_ID (int): Identifikátor aplikace.
        IMAGE_TYPE (Dict[int, str]: Textová reprezentace jednotlivých typů profilových obrázků.
        ALLOWED_TYPES (List[str]): Seznam povolených typů profilových obrázků.
        TYPE_ID (Dict[str, int]): Slovník ID pro různé velikosti obrázků.
        SIZE (Dict[str, Tuple[int, int]]): Slovník rozměrů pro různé typy obrázků.
    """
    APP_ID: int = 0
    IMAGE_TYPE: Dict[str, str] = field(default_factory=lambda: {
        0: "Profile picture - master - 400 x 400 - 72 dpi",
        1: "Profile picture - thumbnail - 64 x 64 - 72 dpi",
    })
    ALLOWED_TYPES: List[str] = ['master', 'thumbnail']
    TYPE_ID: Dict[str, int] = field(default_factory=lambda: {
        'master': 0,
        'thumbnail': 1,
    })
    SIZE: Dict[str, Tuple[int, int]] = field(default_factory=lambda: {
        'master': (400, 400),
        'thumbnail': (64, 64),
    })

    @staticmethod
    @log_method
    def get_app_id() -> int:
        """
        Vrátí ID aplikace v ktré je obrázek použit (0=CustomUser).

        Returns:
            int: Identifikátor aplikace.

        Raises:
            MissingAttributeError: Pokud by atribut nebyl součástí třídy.
        """
        try:
            return ProfileImageConfig.APP_ID

        except AttributeError as e:
            raise MissingAttributeError(
                method_name=inspect.currentframe().f_code.co_name,
                class_name=AppMapsConfig.__name__,
                attribute_name = 'IMAGE_APPS_MAP',
                allowed_attributes = AppsMapConfig._image_apps_attribute_names()
            ) from e

    @staticmethod
    @log_method
    def get_img_types_list() -> List[str]:
        """
        Vrátí seznam povolených typů obrázků.

        Returns:
            List[str]: Seznam povolených typů obrázků.

        Raises:
            MissingAttributeError: Pokud by atribut nebyl součástí třídy.
        """
        try:
            return ProfileImageConfig.ALLOWED_IMAGE_TYPES
        except AttributeError as e:
            class_name = ProfileImageConfig.__class__.__name__
            attribute_name = 'ALLOWED_IMAGE_TYPES'
            raise MissingAttributeError(attribute_name, class_name) from e

    @staticmethod
    @log_method
    def get_img_types_str() -> str:
        """
        Vrátí řetězec povolených typů obrázků.

        Returns:
            str: Řetězec povolených typů obrázků.

        Raises:
            MissingAttributeError: Pokud by atribut nebyl součástí třídy.
        """
        try:
            return ", ".join(ProfileImageConfig.ALLOWED_IMAGE_TYPES)
        except AttributeError as e:
            class_name = ProfileImageConfig.__class__.__name__
            attribute_name = 'ALLOWED_IMAGE_TYPES'
            raise MissingAttributeError(attribute_name, class_name) from e



    @staticmethod
    @log_method
    def get_type_id(img_type: str) -> int:
        """
        Vrátí ID velikosti pro daný typ obrázku.

        Args:
            img_type (str): Typ obrázku ('master' nebo 'thumbnail').

        Returns:
            int: ID velikosti obrázku.

        Raises:
            MissingAttributeError: Pokud by atribut nebyl součástí třídy.
            UnknownImageTypeError: Pokud je zadán neznámý typ obrázku.
        """
        try:
            return ProfileImageConfig.TYPE_ID[img_type]

        except AttributeError as e:
            class_name = ProfileImageConfig.__class__.__name__
            raise MissingAttributeError('TYPE_ID', class_name) from e

        except KeyError as e:
            allowed_image_types = ProfileImageConfig.get_img_types_str
            raise UnknownImageTypeError(img_type, allowed_image_types) from e

    @staticmethod
    @log_method
    def get_size(img_type: str) -> Tuple[int, int]:
        """
        Vrátí rozměry pro daný typ obrázku.

        Args:
            img_type (str): Typ obrázku ('master' nebo 'thumbnail').

        Returns:
            Tuple[int, int]: Rozměry obrázku (šířka, výška).

        Raises:
            MissingAttributeError: Pokud by atribut nebyl součástí třídy.
            UnknownImageTypeError: Pokud je zadán neznámý typ obrázku.
        """
        try:
            return ProfileImageConfig.SIZE[img_type]

        except AttributeError as e:
            class_name = ProfileImageConfig.__class__.__name__
            raise MissingAttributeError('SIZE', class_name) from e

        except KeyError:
            allowed_image_types = ProfileImageConfig.get_img_types_str
            raise UnknownImageTypeError(img_type, allowed_image_types) from e


