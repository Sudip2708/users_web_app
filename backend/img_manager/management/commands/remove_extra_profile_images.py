from django.core.management.base import BaseCommand
from users.models.services.profile_image_integrity_checker import ProfileImageIntegrityChecker
from users.models.services.extra_profile_image_processor import ExtraProfileImageProcessor
"""
Tyto soubory implementují požadovanou funkcionalitu a odpovídají modernímu přístupu k programování a pravidlům Google Style Guide. Rozdělení do samostatných souborů zajišťuje přehlednost a modulárnost kódu.

Pro použití těchto příkazů v terminálu:

1. Pro zpracování uživatelů s chybějícími profilovými obrázky:
   ```
   python manage.py process_missing_profile_images
   ```

2. Pro odstranění nadbytečných profilových obrázků:
   ```
   python manage.py remove_extra_profile_images all
   ```
   nebo
   ```
   python manage.py remove_extra_profile_images some file1.jpg file2.jpg
   ```
   nebo
   ```
   python manage.py remove_extra_profile_images one file1.jpg
   ```

Tyto příkazy budou vypisovat informace do terminálu a nabízet možnosti další akce po dokončení operace.
"""
class Command(BaseCommand):
    help = 'Remove extra profile images'

    def add_arguments(self, parser):
        parser.add_argument('option', type=str, help="Choose 'all', 'some', or 'one'")
        parser.add_argument('file_names', nargs='*', type=str, help="File names to remove (for 'some' or 'one' option)")

    def handle(self, *args, **options):
        option = options['option']
        file_names = options['file_names']

        if option in ['some', 'one'] and not file_names:
            # If no file names provided, load from the temporary file
            results = ProfileImageIntegrityChecker.load_results()
            if results:
                file_names = results['unassigned_masters'] + results['unassigned_thumbnails']
            else:
                self.stdout.write(self.style.WARNING("No file names provided and no saved results found. Running a new check."))
                checker = ProfileImageIntegrityChecker()
                file_names = checker.unassigned_masters + checker.unassigned_thumbnails

        if not file_names and option != 'all':
            self.stdout.write(self.style.SUCCESS("No extra profile images found."))
            return

        checker = ProfileImageIntegrityChecker()
        unassigned_masters = checker.unassigned_masters
        unassigned_thumbnails = checker.unassigned_thumbnails

        report = ExtraProfileImageProcessor.process_and_report(
            unassigned_masters, unassigned_thumbnails, option, file_names
        )
        self.stdout.write(report)