class ProfileImagesConstantsError(Exception):
    """Výjimky týkající se konstant pro profilové obrázky uživatele."""
    pass












class MissingAttributeError(AppsMapError):
    """Výjimka pro chybějící atribut v třídě."""
    def __init__(self, class_name: str, attribute_name: str, allowed_attributes: str):
        self.class_name = class_name
        self.attribute_name = attribute_name
        self.allowed_attributes = allowed_attributes
        super().__init__(
            f"Chyba vyvolaná třídou {class_name}. "
            f"Atribut {attribute_name} není v třídě definován. "
            f"Možné hodnoty: {allowed_attributes}."
        )

class UnknownAppsMapKeyError(AppsMapError):
    """Výjimka pro neznámý klíč pro získání textové reprezentace aplikace."""
    def __init__(self, class_name: str, image_app_id: int, allowed_keys: str):
        self.class_name = class_name
        self.image_app_id = image_app_id
        self.allowed_keys = allowed_keys
        super().__init__(
            f"Chyba vyvolaná třídou {class_name}. "
            f"Není definovaná aplikace pro ID: {image_app_id}. "
            f"Možné hodnoty: {allowed_keys}."
        )

class AttributeIsNotDirectoryError(AppsMapError):
    """Výjimka pro neznámý klíč pro získání textové reprezentace aplikace."""
    def __init__(self, class_name: str, attribute_name: str, attribute_type: str):
        self.class_name = class_name
        self.attribute_name = attribute_name
        self.attribute_type = attribute_type
        super().__init__(
            f"Chyba vyvolaná třídou {class_name}. "
            f"Atribut {attribute_name} není slovník. "
            f"Typ atributu: {attribute_type}."
        )

class NoAttributeError(AppsMapError):
    """Výjimka pro případ že v třídě není žádný atribut."""
    def __init__(self, class_name: str):
        self.class_name = class_name
        super().__init__(
            f"Třída {class_name} nemá definované žádné atributy."
        )