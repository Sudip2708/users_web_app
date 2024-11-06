from typing import List, Dict
from .img_name_decoder import ImageNameDecoder


class ProfileImageReportGenerator:
    """Generates reports for profile image integrity checks."""

    def __init__(
            self,
            users: List[Dict],
            users_missing_images: List[Dict],
            unassigned_masters: List[str],
            unassigned_thumbnails: List[str]
    ):
        self.users = users
        self.users_missing_images = users_missing_images
        self.unassigned_masters = unassigned_masters
        self.unassigned_thumbnails = unassigned_thumbnails

    def generate_report(self) -> str:
        """Generate a full report of the integrity check."""
        report = []
        report.append(self._generate_summary())
        report.append(self._generate_missing_images_report())
        report.append(self._generate_unassigned_files_report('master'))
        report.append(self._generate_unassigned_files_report('thumbnail'))
        report.append(self._generate_conclusion())
        return "\n".join(report)

    def _generate_summary(self) -> str:
        """Generate a summary of the integrity check."""
        return (
            f"\n{'=' * 50}\n"
            f"Výsledek kontroly úložišť pro profilové obrázky\n"
            f"{'-' * 50}\n"
            f"Celkový počet uživatelů: {len(self.users)}\n"
            f"Počet uživatelů s chybějícím profilovým obrázkem: {len(self.users_missing_images)}\n"
            f"Počet nepřiřazených profilových obrázků master: {len(self.unassigned_masters)}\n"
            f"Počet nepřiřazených profilových obrázků thumbnail: {len(self.unassigned_thumbnails)}\n"
        )

    def _generate_missing_images_report(self) -> str:
        """Generate a report of users with missing profile images."""
        report = [
            f"\n{'=' * 50}",
            "Výpis uživatelů s chybějícím obrázkem",
            f"{'-' * 50}"
        ]
        for i, user in enumerate(self.users_missing_images, 1):
            report.append(
                f"Záznam {i}/{len(self.users_missing_images)}:\n"
                f"- Uživatel ID: {user['id']}\n"
                f"- Uživatel Username: {user['username']}\n"
                f"- Profile Img Master: {user['profile_image_master'] or 'Chybí'}\n"
                f"- Profile Img Thumbnail: {user['profile_image_thumbnail'] or 'Chybí'}\n"
                f"- Last Login Date: {user['last_login']}\n"
                f"{'-' * 50}"
            )
        return "\n".join(report)

    def _generate_unassigned_files_report(self, image_type: str) -> str:
        """Generate a report of unassigned files for the specified image type."""
        files = self.unassigned_masters if image_type == 'master' else self.unassigned_thumbnails
        report = [
            f"\n{'=' * 50}",
            f"Výpis souborů z úložiště {image_type}",
            f"{'-' * 50}"
        ]
        for i, file_name in enumerate(files, 1):
            report.append(
                f"Výpis {i}/{len(files)}:\n"
                f"- Jméno souboru: {file_name}\n"
                f"{ImageNameDecoder.decode(file_name)}\n"
                f"{'-' * 50}"
            )
        return "\n".join(report)

    def _generate_conclusion_old(self) -> str:
        """Generate a conclusion with advice on how to proceed."""
        return (
            f"\n{'=' * 50}\n"
            "Co dál? Máte k dispozici tyto příkazy:\n"
            "1. Pro odstranění nepřiřazených souborů použijte: python manage.py remove_unassigned_images\n"
            "2. Pro aktualizaci chybějících profilových obrázků: python manage.py update_missing_profile_images\n"
            "3. Pro detailní analýzu konkrétního souboru: python manage.py analyze_image_file <název_souboru>\n"
            "Před provedením jakýchkoli změn důrazně doporučujeme vytvořit zálohu databáze a souborů.\n"
            f"{'=' * 50}\n"
        )

    def _generate_conclusion(self) -> str:
        """Generate a conclusion with advice on how to proceed."""
        conclusion = (
            f"\n{'=' * 50}\n"
            "Co dál? Máte k dispozici tyto příkazy:\n"
        )

        if self.users_missing_images:
            user_ids = ' '.join(
                str(user['id']) for user in self.users_missing_images)
            conclusion += f"1. Pro aktualizaci chybějících profilových obrázků:\n   python manage.py process_missing_profile_images {user_ids}\n\n"

        if self.unassigned_masters or self.unassigned_thumbnails:
            files = ' '.join(
                self.unassigned_masters + self.unassigned_thumbnails)
            conclusion += f"2. Pro odstranění nepřiřazených souborů:\n   python manage.py remove_extra_profile_images some {files}\n\n"

        conclusion += (
            "3. Pro detailní analýzu konkrétního souboru:\n   python manage.py analyze_image_file <název_souboru>\n\n"
            "Před provedením jakýchkoli změn důrazně doporučujeme vytvořit zálohu databáze a souborů.\n"
            f"{'=' * 50}\n"
        )
        return conclusion