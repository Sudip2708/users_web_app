import os
from typing import List, Dict, Tuple
from django.conf import settings
from django.db.models import Q
from pathlib import Path
import json

from users.models.custom_user import CustomUser
from users.models.services._processor_data._default_data.constants.image_paths import ImagePaths
from .img_name_decoder import ImageNameDecoder
from .generate_report import ProfileImageReportGenerator
from ..list_files_in_directory import list_files_in_directory



class ProfileImageIntegrityChecker:
    """
    A class for checking the integrity of profile images in the system.

    This class performs the following tasks:
    1. Retrieves all users and their profile image information from the database.
    2. Scans the profile image directories for existing files.
    3. Compares database records with actual files to identify discrepancies.
    4. Generates a detailed report of the findings.

    The class is designed for use by developers for system maintenance and
    troubleshooting purposes.

    Example:
        report = ProfileImageIntegrityChecker.check()
        print(report)
    """

    @staticmethod
    def check() -> str:
        """
        Perform a full integrity check on profile images and generate a report.

        Returns:
            str: A formatted string containing the full integrity report.
        """
        checker = ProfileImageIntegrityChecker()
        return checker._generate_report()

    def __init__(self):
        self.users = self._get_users_data()
        self.paths = ImagePaths()
        self.users_missing_images = set()
        self.users_assigned_images  = {'master': set(), 'thumbnail': set()}
        self.unassigned_files  = {'master': set(), 'thumbnail': set()}
        self.missing_files  = {'master': set(), 'thumbnail': set()}
        self._analyze_users_data()
        self._analyze_paths_data()


    def _get_users_data(self) -> List[Dict]:
        """Retrieve user data from the database."""
        try:
            fields = (
                'id', 'username', 'last_login',
                'profile_image', 'profile_image_thumbnail'
            )
            return list(CustomUser.objects.values(*fields))

        except:
            pass

    def _get_img_type(self, field_name: str):
        if field_name not in {'profile_image', 'profile_image_thumbnail'}:
            raise ValueError(f"Unknown field name: {field_name}")
        return 'master' if field_name == 'profile_image' else 'thumbnail'

    def _analyze_users_data(self):
        try:
            for user in self.users:
                for field_name in ('profile_image', 'profile_image_thumbnail'):
                    if not user[field_name]:
                        self.users_missing_images.add(user)
                    else:
                        img_name = user[field_name].split('/')[-1]
                        img_type = self._get_img_type(field_name)
                        self.users_assigned_images[img_type].add(image_name)
        except:
            pass

    def _analyze_paths_data(self, img_type: str) -> List[str]:
        """Return a list of unassigned master image files."""
        try:
            # Příprava dat
            files_from_folder = self._get_files_in_directory(img_type)
            files_from_databases = self.users_assigned_images[img_type]
            # vytvoření dat
            self._get_missing_files(files_from_databases, files_from_folder)
            self._get_unassigned_files(files_from_databases, files_from_folder)

        except:
            pass

    def _get_files_in_directory(self, img_type: str) -> List[str]:
        """Get a list of files in the specified directory."""
        try:
            absolute_path = self.paths.get_profile_images_abs_path(img_type)
            return set(list_files_in_directory(absolute_path))
        except ListFileError as e:
            self.error = f"Error getting files in directory: {e}"

    def _get_missing_files(self, files_from_databases, files_from_folder):
        # Porovnání, zda jsou všechny soubory
        try:
            missing_files = files_from_databases - files_from_folder
            if missing_files:
                self.missing_files[img_type] = missing_files
        except:
            pass

    def _get_unassigned_files(self, files_from_databases, files_from_folder):
        # Path Navrácení seznamu souborů které jsou navíc
        try:
            unassigned_files = files_from_folder - files_from_databases
            if unassigned_files:
                self.unassigned_files[img_type] = unassigned_files
        except:
            pass

    def _generate_report(self) -> str:
        """Generate a full report of the integrity check and save results."""
        report_generator = ProfileImageReportGenerator(
            self.users, self.users_missing_images,
            self.unassigned_masters, self.unassigned_thumbnails
        )

        # Save results to a temporary file
        results = {
            'users_missing_images': [user['id'] for user in
                                     self.users_missing_images],
            'unassigned_masters': self.unassigned_masters,
            'unassigned_thumbnails': self.unassigned_thumbnails
        }
        temp_file_path = Path(
            settings.BASE_DIR) / 'temp_profile_image_results.json'
        with open(temp_file_path, 'w') as f:
            json.dump(results, f)

        return report_generator.generate_report()

    @staticmethod
    def load_results():
        """Load results from the temporary file."""
        temp_file_path = Path(
            settings.BASE_DIR) / 'temp_profile_image_results.json'
        if temp_file_path.exists():
            with open(temp_file_path, 'r') as f:
                return json.load(f)
        return None