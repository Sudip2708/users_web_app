"""
Tento Django management command vytváří nový příkaz `check_profile_images`, který můžete spustit následujícím způsobem:

1. Pro základní kontrolu a stručný výpis:
   ```
   python manage.py check_profile_images
   ```

2. Pro detailní výpis celého reportu:
   ```
   python manage.py check_profile_images --verbose
   ```

Tento příkaz provede následující:

1. Zavolá statickou metodu `check()` třídy `ProfileImageIntegrityChecker`.
2. Vygeneruje kompletní report.
3. V závislosti na tom, zda je použit přepínač `--verbose`, buď vypíše celý report, nebo jen stručné shrnutí.
4. Informuje uživatele o dokončení kontroly a možnosti zobrazení detailního reportu.

Tento přístup poskytuje flexibilitu při používání - můžete rychle získat přehled o stavu profilových obrázků, nebo si zobrazit detailní informace, pokud je to potřeba.

Navíc, díky tomu, že jsme v předchozí úpravě implementovali ukládání výsledků do dočasného souboru, tento příkaz také připraví data pro další příkazy (`process_missing_profile_images` a `remove_extra_profile_images`), které mohou tyto výsledky následně použít.

To umožňuje efektivní workflow, kde můžete nejprve spustit kontrolu, prohlédnout si výsledky a pak snadno navázat dalšími akcemi bez nutnosti opakovat analýzu.
"""
from django.core.management.base import BaseCommand
from users.models.services.profile_image_integrity_checker import \
    ProfileImageIntegrityChecker


class Command(BaseCommand):
    help = 'Check integrity of profile images and generate a report'

    def add_arguments(self, parser):
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Increase output verbosity',
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS("Starting profile image integrity check..."))

        report = ProfileImageIntegrityChecker.check()

        if options['verbose']:
            self.stdout.write(report)
        else:
            # Print a summary if not in verbose mode
            summary = self._generate_summary(report)
            self.stdout.write(summary)

        self.stdout.write(
            self.style.SUCCESS("Profile image integrity check completed."))
        self.stdout.write(
            "For detailed results, check the generated report or run this command with --verbose flag.")

    def _generate_summary(self, report):
        # Extract key information from the report
        lines = report.split('\n')
        summary_lines = [line for line in lines if
                         line.startswith("Celkový počet") or line.startswith(
                             "Počet")]

        summary = "Summary:\n" + "\n".join(summary_lines)
        summary += "\n\nFor next steps, please refer to the 'Co dál?' section in the full report."

        return summary