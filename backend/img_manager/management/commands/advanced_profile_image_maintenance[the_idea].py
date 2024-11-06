"""
Vaše současné řešení pokrývá hlavní aspekty údržby úložišť pro profilové obrázky a kontroly polí u uživatelů. Nicméně, existuje několik dalších oblastí, které by mohly být užitečné pro vývojáře při správě systému. Zde jsou některá doporučení pro rozšíření funkcionalit:

1. Kontrola integrity souborů:
   - Ověřte, zda jsou soubory obrázků skutečně validní obrázky (nejsou poškozené).
   - Zkontrolujte, zda mají obrázky správný formát a rozlišení.

2. Optimalizace obrázků:
   - Přidejte možnost komprese velkých obrázků pro úsporu místa.
   - Vytvořte funkci pro převod obrázků do jednotného formátu.

3. Čištění starých/nepoužívaných obrázků:
   - Identifikujte a odstraňte obrázky, které nebyly použity delší dobu.

4. Záloha před změnami:
   - Přidejte možnost vytvoření zálohy před provedením hromadných změn.

5. Statistiky využití úložiště:
   - Vytvořte report o využití místa profilovými obrázky.

6. Kontrola konzistence mezi master a thumbnail verzemi:
   - Ověřte, zda pro každý master obrázek existuje odpovídající thumbnail a naopak.

7. Hromadná aktualizace miniatur:
   - Přidejte možnost přegenerovat všechny miniatury podle aktuálních master obrázků.

8. Kontrola oprávnění souborů:
   - Ověřte, zda mají soubory správná oprávnění pro čtení/zápis.

9. Detekce duplicitních obrázků:
   - Identifikujte a nabídněte odstranění duplicitních obrázků pro úsporu místa.

10. Automatické doplnění chybějících obrázků:
    - Vytvořte funkci pro automatické generování výchozích profilových obrázků pro uživatele bez obrázku.

Zde je návrh nového Django management příkazu, který by mohl pokrýt některé z těchto dodatečných funkcí:

Tento nový příkaz `advanced_profile_image_maintenance` přidává několik užitečných funkcí pro vývojáře:

1. Optimalizace obrázků pro snížení velikosti souborů.
2. Čištění nepoužívaných obrázků.
3. Kontrola integrity souborů obrázků.
4. Přegenerování všech miniatur.

Můžete ho použít následovně:

```
python manage.py advanced_profile_image_maintenance --optimize --clean-unused --check-integrity --regenerate-thumbnails
```

Můžete použít libovolnou kombinaci těchto přepínačů podle potřeby.

Toto rozšíření pokrývá další aspekty údržby profilových obrázků, které mohou být užitečné pro vývojáře. Nicméně, vždy je důležité pečlivě zvážit specifické potřeby vašeho projektu a případně přidat další funkce nebo upravit stávající podle konkrétních požadavků.
"""

import os
from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.files.storage import default_storage
from django.db.models import Q
from users.models.custom_user import CustomUser
from users.models.services._processor_data._default_data.constants.image_paths import \
    ImagePaths
from PIL import Image
import hashlib


class Command(BaseCommand):
    help = 'Perform advanced maintenance on profile images'

    def add_arguments(self, parser):
        parser.add_argument(
            '--optimize',
            action='store_true',
            help='Optimize images to reduce file size',
        )
        parser.add_argument(
            '--clean-unused',
            action='store_true',
            help='Remove unused images',
        )
        parser.add_argument(
            '--check-integrity',
            action='store_true',
            help='Check integrity of image files',
        )
        parser.add_argument(
            '--regenerate-thumbnails',
            action='store_true',
            help='Regenerate all thumbnail images',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS(
            "Starting advanced profile image maintenance..."))

        paths = ImagePaths()
        master_path = os.path.join(settings.MEDIA_ROOT, paths.PATH_FROM_MEDIA,
                                   'master')
        thumbnail_path = os.path.join(settings.MEDIA_ROOT,
                                      paths.PATH_FROM_MEDIA, 'thumbnail')

        if options['optimize']:
            self.optimize_images(master_path)
            self.optimize_images(thumbnail_path)

        if options['clean_unused']:
            self.clean_unused_images(master_path, thumbnail_path)

        if options['check_integrity']:
            self.check_image_integrity(master_path)
            self.check_image_integrity(thumbnail_path)

        if options['regenerate_thumbnails']:
            self.regenerate_thumbnails(master_path, thumbnail_path)

        self.stdout.write(
            self.style.SUCCESS("Advanced profile image maintenance completed."))

    def optimize_images(self, directory):
        self.stdout.write(f"Optimizing images in {directory}...")
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            try:
                with Image.open(file_path) as img:
                    img.save(file_path, optimize=True, quality=85)
            except Exception as e:
                self.stdout.write(self.style.WARNING(
                    f"Failed to optimize {filename}: {str(e)}"))

    def clean_unused_images(self, master_path, thumbnail_path):
        self.stdout.write("Cleaning unused images...")
        used_images = set(
            CustomUser.objects.values_list('profile_image_master', flat=True)) | \
                      set(CustomUser.objects.values_list(
                          'profile_image_thumbnail', flat=True))

        for directory in [master_path, thumbnail_path]:
            for filename in os.listdir(directory):
                if filename not in used_images:
                    os.remove(os.path.join(directory, filename))
                    self.stdout.write(f"Removed unused image: {filename}")

    def check_image_integrity(self, directory):
        self.stdout.write(f"Checking image integrity in {directory}...")
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            try:
                with Image.open(file_path) as img:
                    img.verify()
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"Corrupt image found: {filename}"))

    def regenerate_thumbnails(self, master_path, thumbnail_path):
        self.stdout.write("Regenerating thumbnails...")
        for filename in os.listdir(master_path):
            master_file_path = os.path.join(master_path, filename)
            thumbnail_file_path = os.path.join(thumbnail_path, filename)
            try:
                with Image.open(master_file_path) as img:
                    img.thumbnail((100, 100))  # Adjust size as needed
                    img.save(thumbnail_file_path)
            except Exception as e:
                self.stdout.write(self.style.WARNING(
                    f"Failed to regenerate thumbnail for {filename}: {str(e)}"))