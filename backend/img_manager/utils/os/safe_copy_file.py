import os
import shutil
import logging
from typing import Optional

# Nastavení základní konfigurace loggeru
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(module)s - %(message)s'
)
logger = logging.getLogger(__name__)

def copy_file(source_path: str, destination_path: str) -> Optional[str]:
    """
    Kopíruje soubor z jednoho umístění do druhého.

    Tato funkce kopíruje soubor ze zdrojové cesty do cílové cesty pomocí
    shutil.copyfile(). Ověřuje existenci zdrojového souboru před kopírováním
    a existenci cílového souboru po kopírování. Používá logging pro zaznamenávání
    průběhu a chyb.

    Args:
        source_path (str): Cesta ke zdrojovému souboru.
        destination_path (str): Cesta, kam má být soubor zkopírován.

    Returns:
        Optional[str]: Cesta k zkopírovanému souboru, pokud byla operace úspěšná.
                       None, pokud kopírování selhalo.

    Raises:
        FileNotFoundError: Pokud zdrojový soubor neexistuje.
        PermissionError: Pokud nemáme oprávnění ke čtení zdrojového souboru
                         nebo zápisu do cílového umístění.
        shutil.SameFileError: Pokud jsou zdrojová a cílová cesta stejné.
        OSError: Pro jiné chyby operačního systému.

    Example:
        >>> source = "/path/to/source/file.txt"
        >>> destination = "/path/to/destination/file_copy.txt"
        >>> result = copy_file(source, destination)
        >>> if result:
        ...     logger.info(f"Soubor byl úspěšně zkopírován do: {result}")
        ... else:
        ...     logger.error("Kopírování souboru selhalo.")
    """
    try:
        if not os.path.exists(source_path):
            logger.error(f"Zdrojový soubor neexistuje: {source_path}")
            raise FileNotFoundError(f"Zdrojový soubor neexistuje: {source_path}")

        logger.info(f"Začínám kopírování souboru z {source_path} do {destination_path}")
        copied_file = shutil.copyfile(source_path, destination_path)

        if os.path.exists(copied_file):
            logger.info(f"Soubor byl úspěšně zkopírován do: {copied_file}")
            return copied_file
        else:
            logger.warning(f"Kopírování proběhlo, ale cílový soubor nebyl nalezen: {copied_file}")
            return None
    except (PermissionError, shutil.SameFileError, OSError) as e:
        logger.error(f"Chyba při kopírování souboru: {e}")
        return None