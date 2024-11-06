from dataclasses import dataclass, field
from typing import Dict
from pathlib import Path

from users.models.services.utils.log_method import log_method
from .constants import ProfileImageConfig
from ..errors.default_images_errors import (
    MissingAttributeError,
    UnknownImageTypeError
)

@dataclass(frozen=True)
class ProfileImagePaths:
    """
    Definuje cesty pro ukládání a načítání profilových obrázků uživatelů.

    Attributes:
        PATH_FROM_MEDIA (Path): Relativní cesta od media adresáře k profilovým obrázkům.
        DEFAULT_IMAGES_PATH (Dict[str, Path]): Slovník cest k výchozím obrázkům pro různé typy.
    """
    PATH_FROM_MEDIA: Path = Path('users/profile_images/')
    DEFAULT_IMAGES_PATH: Dict[str, Path] = field(default_factory=lambda: {
        'master': Path('images/profile_image_default_master[400x400].jpg'),
        'thumbnail': Path('images/profile_image_default_thumbnail[64x64].jpg'),
    })

    @log_method
    def get_path_from_media(self) -> int:
        """
        Vrátí cestu ze složky media ke kořenové složce pro profilové obrázky.

        Returns:
            Path: Cesta ze media do základní složky pro profilové obrázky.

        Raises:
            MissingAttributeError: Pokud by atribut nebyl součástí třídy.
        """
        try:
            return self.PATH_FROM_MEDIA

        except AttributeError as e:
            class_name = self.__class__.__name__
            raise MissingAttributeError('PATH_FROM_MEDIA', class_name) from e
        
    @log_method
    def get_default_image_path(self, img_type: str) -> Path:
        """
        Vrátí cestu k výchozímu obrázku pro daný typ.

        Args:
            img_type (str): Typ obrázku ('master' nebo 'thumbnail').

        Returns:
            Path: Cesta k výchozímu obrázku.

        Raises:
            MissingAttributeError: Pokud by atribut nebyl součástí třídy.
            UnknownImageTypeError: Pokud je zadán neznámý typ obrázku.
        """
        try:
            return self.DEFAULT_IMAGES_PATH[img_type]

        except AttributeError as e:
            class_name = self.__class__.__name__
            attribute_name = 'DEFAULT_IMAGES_PATH'
            raise MissingAttributeError(attribute_name, class_name) from e

        except KeyError as e:
            allowed_image_types = ProfileImageConfig.get_img_types_str()
            raise UnknownImageTypeError(img_type, allowed_image_types) from e

    @log_method
    def get_profile_images_rel_path(self, img_type: str) -> int:
        """
        Vrátí relativní cestu do složky s profilovými obrázky.

        Returns:
            Path: Relativní cestu do složky s profilovými obrázky..

        Raises:
            MissingAttributeError: Pokud by atribut nebyl součástí třídy.
        """
        try:
            return self.PATH_FROM_MEDIA / img_type

        except AttributeError as e:
            class_name = self.__class__.__name__
            raise MissingAttributeError('PATH_FROM_MEDIA', class_name) from e

    @log_method
    def get_profile_images_abs_path(self, img_type: str) -> int:
        """
        Vrátí absolutní cestu do složky s profilovými obrázky.

        Returns:
            Path: Absolutní cestu do složky s profilovými obrázky.
        """
        try:
            relative_path = self.get_profile_images_rel_path(img_type)
            return Path(settings.MEDIA_ROOT) / relative_path

        except ... as e:
            pass