import os
from typing import List, Tuple
from django.conf import settings
from users.models.services._processor_data._default_data.constants.image_paths import \
    ImagePaths


class ExtraProfileImageProcessor:
    def __init__(self, unassigned_masters: List[str],
                 unassigned_thumbnails: List[str]):
        self.unassigned_masters = unassigned_masters
        self.unassigned_thumbnails = unassigned_thumbnails
        self.paths = ImagePaths()

    def remove_files(self, option: str, file_names: List[str] = None) -> str:
        """Remove extra files based on the given option."""
        if option == 'all':
            return self._remove_all_files()
        elif option in ['some', 'one']:
            return self._remove_specific_files(file_names)
        else:
            return "Invalid option. Please choose 'all', 'some', or 'one'."

    def _remove_all_files(self) -> str:
        master_report = self._remove_files_from_directory('master',
                                                          self.unassigned_masters)
        thumbnail_report = self._remove_files_from_directory('thumbnail',
                                                             self.unassigned_thumbnails)
        return f"{master_report}\n{thumbnail_report}"

    def _remove_specific_files(self, file_names: List[str]) -> str:
        if not file_names:
            return "No file names provided. Please specify the files to remove."

        master_files, thumbnail_files = self._separate_files(file_names)
        master_report = self._remove_files_from_directory('master',
                                                          master_files)
        thumbnail_report = self._remove_files_from_directory('thumbnail',
                                                             thumbnail_files)
        return f"{master_report}\n{thumbnail_report}"

    def _remove_files_from_directory(self, directory: str,
                                     files: List[str]) -> str:
        removed = []
        not_found = []
        base_path = os.path.join(settings.MEDIA_ROOT,
                                 self.paths.PATH_FROM_MEDIA, directory)

        for file in files:
            file_path = os.path.join(base_path, file)
            if os.path.exists(file_path):
                os.remove(file_path)
                removed.append(file)
            else:
                not_found.append(file)

        return (f"{directory.capitalize()} directory:\n"
                f"Removed: {', '.join(removed) if removed else 'None'}\n"
                f"Not found: {', '.join(not_found) if not_found else 'None'}")

    def _separate_files(self, file_names: List[str]) -> Tuple[
        List[str], List[str]]:
        master_files = [f for f in file_names if f in self.unassigned_masters]
        thumbnail_files = [f for f in file_names if
                           f in self.unassigned_thumbnails]
        return master_files, thumbnail_files

    @classmethod
    def process_and_report(cls, unassigned_masters: List[str],
                           unassigned_thumbnails: List[str], option: str,
                           file_names: List[str] = None) -> str:
        processor = cls(unassigned_masters, unassigned_thumbnails)
        report = processor.remove_files(option, file_names)
        return (
            f"File removal report:\n{'-' * 20}\n{report}\n{'-' * 20}\n"
            "To perform a new check, use: python manage.py check_profile_images\n"
            "To process users with missing images, use: python manage.py process_missing_profile_images"
        )