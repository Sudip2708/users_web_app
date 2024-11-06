class ImgManagerConfigError(Exception):
    """Výjimky týkajícíse definice aplikací."""
    pass

class MissingAttributeError(ImgManagerConfigError):
    """Výjimka pro chybějící atribut v třídě."""
    def __init__(self, method_name: str, class_name: str, attribute_name: str, allowed_attributes: str):
        self.method_name = method_name
        self.class_name = class_name
        self.attribute_name = attribute_name
        self.allowed_attributes = allowed_attributes
        super().__init__(
            f"Chyba vyvolaná metodou {method_name} třídy {class_name}. "
            f"Atribut {attribute_name} není v třídě definován. "
            f"Možné hodnoty: {allowed_attributes}."
        )

class UnknownAppsMapKeyError(ImgManagerConfigError):
    """Výjimka pro neznámý klíč pro získání textové reprezentace aplikace."""
    def __init__(self, method_name: str, class_name: str, image_app_id: int, allowed_keys: str):
        self.method_name = method_name
        self.class_name = class_name
        self.image_app_id = image_app_id
        self.allowed_keys = allowed_keys
        super().__init__(
            f"Chyba vyvolaná metodou {method_name} třídy {class_name}. "
            f"Není definovaný klíč s ID: {image_app_id}. "
            f"Možné hodnoty: {allowed_keys}."
        )

class AppsMapConfigError(ImgManagerConfigError):
    """Výjimka pro případ že v třídě není žádný atribut."""
    def __init__(self, class_name: str, method_name: str):
        self.class_name = class_name
        self.method_name = method_name
        super().__init__(
            f"Chyba vyvolaná metodou {method_name} třídy {class_name}."
        )