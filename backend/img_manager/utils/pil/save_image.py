import os
from PIL import Image

def save_image(self, img, path, format):
    try:
        saved_image = img.save(path, format=format)
        os.path.exists(saved_image)
    except shutil.Error as e:
        print(f"Při ukládání souboru došlo k chybě: {e}")