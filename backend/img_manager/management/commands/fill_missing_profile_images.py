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

from django.core.management.base import BaseCommand
from users.models.services.profile_image_integrity_checker import \
    ProfileImageIntegrityChecker
from users.models.services.missing_profile_image_processor import \
    MissingProfileImageProcessor


class Command(BaseCommand):
    help = 'Process users with missing profile images'

    def add_arguments(self, parser):
        parser.add_argument('user_ids', nargs='*', type=int,
                            help="User IDs to process")

    def handle(self, *args, **options):
        user_ids = options['user_ids']

        if not user_ids:
            # If no user IDs provided, load from the temporary file
            results = ProfileImageIntegrityChecker.load_results()
            if results:
                user_ids = results['users_missing_images']
            else:
                self.stdout.write(self.style.WARNING(
                    "No user IDs provided and no saved results found. Running a new check."))
                checker = ProfileImageIntegrityChecker()
                user_ids = [user['id'] for user in checker.users_missing_images]

        if not user_ids:
            self.stdout.write(self.style.SUCCESS(
                "No users with missing profile images found."))
            return

        # Get the full user data and unassigned masters
        checker = ProfileImageIntegrityChecker()
        users_missing_images = [user for user in checker.users if
                                user['id'] in user_ids]
        unassigned_masters = checker.unassigned_masters

        report = MissingProfileImageProcessor.process_and_report(
            users_missing_images, unassigned_masters)
        self.stdout.write(report)