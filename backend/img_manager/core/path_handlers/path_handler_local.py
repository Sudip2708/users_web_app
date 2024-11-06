from pathlib import Path
from django.conf import settings
from django.core.files.storage import default_storage
import os

from users.models.services.utils.log_method import log_method
from users.models.services.utils.is_debug_mode import is_debug_mode
from .protocols.path_handler_protocol import PathHandlerProtocol
from .constants.image_paths import ImagePaths
from .constants.image_config import ImageConfig


from .utils.generate_image_name import generate_image_name
from .errors.default_images_errors import (
    UnknownImageTypeError,
    NonexistentImagePathError,
    ImagePathError,
    InvalidUserIDError,
    ImageNameError
)

class PathHandlerLocal(PathHandlerProtocol):
    """
    Implementace PathHandlerProtocol pro lokální správu cest k profilovým obrázkům.

    Tato třída poskytuje konkrétní implementaci pro vytváření a správu cest
    k profilovým obrázkům uživatelů v lokálním souborovém systému.
    """

    def __init__(self) -> None:
        """Inicializuje PathHandlerLocal s cestami a konfigurací."""
        self.paths = ImagePaths()
        self.config = ImageConfig()
        self.image_types_list = self.config.get_img_types_list()
        self.image_types_str = self.config.get_img_types_str()
        self.debug_mode = is_debug_mode()

    @log_method
    def get_absolute_default(self, img_type: str) -> Path:
        """Vrátí absolutní cestu k defaultnímu obrázku."""

        if self.debug_mode:
            if img_type not in self.image_types_list:
                raise UnknownImageTypeError(img_type, self.image_types_str)

        try:
            relative_path = self.paths.get_default_image_path(img_type)
            absolute_path = Path(settings.STATIC_ROOT) / relative_path
            if self.debug_mode:
                if not absolute_path.exists():
                    raise NonexistentImagePathError(absolute_path)
            return absolute_path

        except ImageProcessingError as e:
            raise ImagePathError(img_type) from e

    @log_method
    def create_new_relative(self, img_type: str, user_id: int) -> Path:
        """
        Vytvoří relativní cestu od media adresáře pro nový obrázek uživatele.

        Args:
            img_type (str): Typ obrázku ('master' nebo 'thumbnail').
            user_id (int): ID uživatele.

        Returns:
            Path: Relativní cesta k novému obrázku uživatele.

        Raises:
            KeyError: Pokud je zadán neznámý typ obrázku.
            ValueError: Pokud je zadáno neplatné ID uživatele.
        """
        if self.debug_mode:
            if img_type not in self.image_types_list:
                raise UnknownImageTypeError(img_type, self.image_types_str)
            if not isinstance(user_id, int) or user_id <= 0:
                raise InvalidUserIDError(user_id)

        try:
            image_name = self.get_new_image_name(img_type, user_id)
            return self.paths.PATH_FROM_MEDIA / img_type / image_name

        except ImageProcessingError as e:
            raise ImagePathError(img_type) from e

    @log_method
    def get_absolute_media(self, relative_path: Path) -> Path:
        """
        Převede relativní cestu na absolutní cestu v media adresáři.

        Args:
            relative_path (Path): Relativní cesta k souboru.

        Returns:
            Path: Absolutní cesta k souboru v media adresáři.
        """
        return Path(default_storage.path(str(relative_path)))

    @log_method
    def get_new_image_name(self, img_type: str, user_id: int) -> str:
        """
        Vygeneruje nové jméno pro obrázek uživatele.

        Args:
            img_type (str): Typ obrázku ('master' nebo 'thumbnail').
            user_id (int): ID uživatele.

        Returns:
            str: Nové jméno obrázku.

        Raises:
            KeyError: Pokud je zadán neznámý typ obrázku.
            ValueError: Pokud je zadáno neplatné ID uživatele.
        """
        if user_id <= 0:
            raise ...

        try:
            app_id = self.config.APP_ID
            type_id = self.config.get_type_id(img_type)
            return generate_image_name(app_id, type_id, user_id)
        except ... as e:
            raise ...