from ._processor_data.default_images_handler import DefaultImageHandler
from ._processor_data.new_image_processor import NewImageProcessor
from ._processor_data._default_data.path_handler_local import PathHandlerLocal

class ProfileImageProcessor:
    def __init__(self, user):
        self.user = user

    def set_default_profile_images(self):
        path_handler = PathHandlerLocal()
        DefaultImageHandler.set_default_images(path_handler, self.user)
        self._backup_and_save()

    def process_new_profile_img(self):
        NewImageProcessor.process_new_image(self.user)
        self._backup_and_save()

    def _backup_and_save(self):
        master = self.user.profile_image.name
        thumbnail = self.user.profile_image_thumbnail.name
        self.user.backup_data['profile_image'] = master
        self.user.backup_data['profile_image_thumbnail'] = thumbnail
        self.user.save()