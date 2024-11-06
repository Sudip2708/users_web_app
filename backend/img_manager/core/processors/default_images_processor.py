from ._default_data.protocols.path_handler_protocol import PathHandlerProtocol
from users.models.services.utils.os_copy_file import copy_file

class DefaultImageProcessor:
    def __init__(self, path_handler: PathHandlerProtocol, user):
        self.paths = path_handler
        self.user = user

    def set_default_images(self):
        try:
            relative_path_master = self._copy_default('master')
            relative_path_thumbnail = self._copy_default('thumbnail')
            self.user.profile_image = relative_path_master
            self.user.profile_image_thumbnail = relative_path_thumbnail
        except Exception as e:
            print(f"Error setting default images: {e}")

    def _copy_default(self, img_type):
        default_image_path = self.paths.get_absolute_default(img_type)
        relative_path = self.paths.create_new_relative(img_type, self.user.id)
        absolute_path = self.paths.get_absolute_media(relative_path)
        copy_file(default_image_path, absolute_path)
        return relative_path
