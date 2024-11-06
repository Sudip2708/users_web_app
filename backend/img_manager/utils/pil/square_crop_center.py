import PIL
def square_crop_center(self, image: Image.Image) -> Image.Image:
    """
    Metoda ořeže obrázek na střed a poměr stran 1:1.

    Args:
        image: Obrázek otevřený v PIL.

    Returns:
        Vystředěný a čtvercově oříznutý obrázek.
    """
    width, height = image.size
    new_size = min(width, height)
    left = (width - new_size) // 2
    top = (height - new_size) // 2
    right = left + new_size
    bottom = top + new_size
    return image.crop((left, top, right, bottom))