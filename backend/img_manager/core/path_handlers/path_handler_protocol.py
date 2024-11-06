from typing import Protocol
from pathlib import Path
from .default_images_constants_image_paths import ImagePaths, ImageConfig

class PathHandlerProtocol(Protocol):
    """
    Protokol definující rozhraní pro správu cest k profilovým obrázkům uživatelů.

    Tento handler je použit k nastavení cest potřebných pro třídu DefaultImageHandler,
    která se stará o vytvoření kopie defaultního obrázku při založení instance uživatele.
    """

    paths: ImagePaths
    config: ImageConfig

    def __init__(self) -> None:
        """
        Inicializuje PathHandler s cestami a konfigurací.

        Atributy paths a config by měly být nastaveny v konstruktoru konkrétní implementace.
        """

    def get_absolute_path_for_default(self, img_type: str) -> Path:
        """
        Vrátí absolutní cestu k výchozímu obrázku daného typu.

        Args:
            img_type (str): Typ obrázku ('master' nebo 'thumbnail').

        Returns:
            Path: Absolutní cesta k výchozímu obrázku.

        Raises:
            KeyError: Pokud je zadán neznámý typ obrázku.
        """
        ...

    def create_relative_path_from_media(self, img_type: str, user_id: int) -> Path:
        """
        Vytvoří relativní cestu od media adresáře pro obrázek uživatele.

        Args:
            img_type (str): Typ obrázku ('master' nebo 'thumbnail').
            user_id (int): ID uživatele.

        Returns:
            Path: Relativní cesta k obrázku uživatele.

        Raises:
            KeyError: Pokud je zadán neznámý typ obrázku.
            ValueError: Pokud je zadáno neplatné ID uživatele.
        """
        ...

    def get_absolute_path_for_media(self, relative_path: Path) -> Path:
        """
        Převede relativní cestu na absolutní cestu v media adresáři.

        Args:
            relative_path (Path): Relativní cesta k souboru.

        Returns:
            Path: Absolutní cesta k souboru v media adresáři.
        """
        ...

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
        ...