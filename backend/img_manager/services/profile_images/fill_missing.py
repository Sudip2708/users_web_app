from typing import List, Dict
from django.db.models import Q
from users.models.custom_user import CustomUser
from users.models.services._processor_data._default_data.constants.image_paths import \
    ImagePaths
from .img_name_decoder import ImageNameDecoder


class MissingProfileImageProcessor:
    def __init__(self, users_missing_images: List[Dict],
                 unassigned_masters: List[str]):
        self.users_missing_images = users_missing_images
        self.unassigned_masters = unassigned_masters
        self.paths = ImagePaths()

    def process_users(self) -> str:
        """Process users with missing profile images and return a report."""
        report = []
        for user in self.users_missing_images:
            if not user['profile_image_master'] and user[
                'profile_image_thumbnail']:
                report.append(self._process_missing_master(user))
            elif user['profile_image_master'] and not user[
                'profile_image_thumbnail']:
                report.append(self._process_missing_thumbnail(user))
            else:
                report.append(self._process_missing_both(user))

        return "\n".join(report)

    def _process_missing_master(self, user: Dict) -> str:
        potential_masters = self._find_potential_masters(user['id'])
        if potential_masters:
            newest_master = max(potential_masters,
                                key=lambda x: ImageNameDecoder(x).data[
                                    'timestamp'])
            self._initialize_image(user['id'], newest_master)
            return f"User {user['username']} (ID: {user['id']}): Master image initialized from {newest_master}"
        else:
            self._set_default_images(user['id'])
            return f"User {user['username']} (ID: {user['id']}): Default images set"

    def _process_missing_thumbnail(self, user: Dict) -> str:
        self._initialize_image(user['id'], user['profile_image_master'])
        return f"User {user['username']} (ID: {user['id']}): Thumbnail generated from existing master"

    def _process_missing_both(self, user: Dict) -> str:
        return self._process_missing_master(user)

    def _find_potential_masters(self, user_id: int) -> List[str]:
        return [
            img for img in self.unassigned_masters
            if ImageNameDecoder(img).data['user_id'] == user_id
        ]

    def _initialize_image(self, user_id: int, image_name: str) -> None:
        user = CustomUser.objects.get(id=user_id)
        user.profile_image_processing(image_name)

    def _set_default_images(self, user_id: int) -> None:
        user = CustomUser.objects.get(id=user_id)
        user.set_default_profile_images()

    @classmethod
    def process_and_report(cls, users_missing_images: List[Dict],
                           unassigned_masters: List[str]) -> str:
        processor = cls(users_missing_images, unassigned_masters)
        report = processor.process_users()
        return (
            f"Processing report:\n{'-' * 20}\n{report}\n{'-' * 20}\n"
            "To perform a new check, use: python manage.py check_profile_images\n"
            "To remove extra files, use: python manage.py remove_extra_profile_images"
        )

