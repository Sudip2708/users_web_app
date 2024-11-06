"""
Tento nový Django management command `auto_profile_image_maintenance` provede automaticky všechny kroky údržby profilových obrázků. Můžete ho použít následovně:

1. Pro plné automatické provedení všech kroků:
   ```
   python manage.py auto_profile_image_maintenance
   ```

2. Pro "suchý běh" (dry run), který ukáže, co by se stalo, ale neprovede žádné změny:
   ```
   python manage.py auto_profile_image_maintenance --dry-run
   ```

Tento příkaz provede následující:

1. Spustí kontrolu integrity profilových obrázků (`check_profile_images`).
2. Zpracuje chybějící profilové obrázky (`process_missing_profile_images`).
3. Odstraní nadbytečné soubory profilových obrázků (`remove_extra_profile_images`).

Každý krok je jasně označen v výstupu a poskytuje informace o tom, co se děje. Pokud je použit přepínač `--dry-run`, příkaz ukáže, co by se stalo, ale neprovede žádné skutečné změny.

Tento přístup má několik výhod:

1. Automatizuje celý proces údržby profilových obrázků.
2. Poskytuje jasný a strukturovaný výstup o tom, co se děje v každém kroku.
3. Umožňuje "suchý běh" pro bezpečné testování před provedením skutečných změn.
4. Využívá existující příkazy a třídy, což zachovává modularitu a znovupoužitelnost kódu.

Tento nový příkaz je ideální pro pravidelnou údržbu nebo pro situace, kdy potřebujete rychle provést kompletní kontrolu a opravu profilových obrázků v systému.
"""

from django.core.management.base import BaseCommand
from django.core.management import call_command
from io import StringIO
from users.models.services.profile_image_integrity_checker import ProfileImageIntegrityChecker
from users.models.services.missing_profile_image_processor import MissingProfileImageProcessor
from users.models.services.extra_profile_image_processor import ExtraProfileImageProcessor

class Command(BaseCommand):
    help = 'Automatically perform full profile image maintenance'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Perform a dry run without making any changes',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting automatic profile image maintenance..."))

        # Step 1: Check profile images
        self.stdout.write(self.style.NOTICE("\nStep 1: Checking profile images"))
        check_output = self._call_command('check_profile_images')
        self.stdout.write(check_output)

        # Load results from the temporary file
        results = ProfileImageIntegrityChecker.load_results()
        if not results:
            self.stdout.write(self.style.ERROR("Failed to load integrity check results."))
            return

        # Step 2: Process missing profile images
        self.stdout.write(self.style.NOTICE("\nStep 2: Processing missing profile images"))
        if results['users_missing_images']:
            if not options['dry_run']:
                process_output = self._call_command('process_missing_profile_images', *map(str, results['users_missing_images']))
            else:
                process_output = f"Would process {len(results['users_missing_images'])} users with missing images."
            self.stdout.write(process_output)
        else:
            self.stdout.write("No missing profile images to process.")

        # Step 3: Remove extra profile images
        self.stdout.write(self.style.NOTICE("\nStep 3: Removing extra profile images"))
        if results['unassigned_masters'] or results['unassigned_thumbnails']:
            if not options['dry_run']:
                remove_output = self._call_command('remove_extra_profile_images', 'all')
            else:
                remove_output = f"Would remove {len(results['unassigned_masters'])} master images and {len(results['unassigned_thumbnails'])} thumbnail images."
            self.stdout.write(remove_output)
        else:
            self.stdout.write("No extra profile images to remove.")

        self.stdout.write(self.style.SUCCESS("\nAutomatic profile image maintenance completed."))
        if options['dry_run']:
            self.stdout.write(self.style.WARNING("This was a dry run. No actual changes were made."))

    def _call_command(self, command, *args):
        """Call a management command and return its output as a string."""
        out = StringIO()
        call_command(command, *args, stdout=out)
        return out.getvalue()