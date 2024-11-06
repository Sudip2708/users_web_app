class NewImageProcessor:
    MIN_IMG_SIZE_IN_MB = 0.1
    MAX_IMG_SIZE_IN_MB = 5
    IMG_OUTPUT_DPI = (72, 72)
    IMG_OUTPUT_FORMAT = 'JPEG'
    SIZE = {
        'master': (400, 400),
        'thumbnail': (64, 64),
    }

    @staticmethod
    def process_new_image(user):
        try:
            uploaded_image_path = user.profile_image.path
            NewImageProcessor._validate_image(uploaded_image_path)
            NewImageProcessor._create_and_save_new_profile_images(user, uploaded_image_path)
            NewImageProcessor._cleanup_files(user, uploaded_image_path)
        except Exception as e:
            print(f"Error processing new profile image: {e}")

    @staticmethod
    def _validate_image(uploaded_image_path):
        validate_image_format(uploaded_image_path)
        validate_file_size(uploaded_image_path, NewImageProcessor.MIN_IMG_SIZE_IN_MB, NewImageProcessor.MAX_IMG_SIZE_IN_MB)

    @staticmethod
    def _create_and_save_new_profile_images(user, uploaded_image_path):
        with Image.open(uploaded_image_path) as img:
            img.info['dpi'] = NewImageProcessor.IMG_OUTPUT_DPI
            img = square_crop_center(img)
            user.profile_image = NewImageProcessor._create_image(img, 'master')
            user.profile_image_thumbnail = NewImageProcessor._create_image(img, 'thumbnail')

    @staticmethod
    def _create_image(img, img_type):
        resized_img = NewImageProcessor._resize_image(img, img_type)
        relative_path = PathHandler.create_relative_path_from_media(img_type)
        absolute_path = PathHandler.get_absolute_path_for_media(relative_path)
        save_image(resized_img, absolute_path, NewImageProcessor.IMG_OUTPUT_FORMAT)
        return relative_path

    @staticmethod
    def _resize_image(img, img_type):
        return resize_image(img, NewImageProcessor.SIZE[img_type])

    @staticmethod
    def _cleanup_files(user, uploaded_image_path):
        delete_file(uploaded_image_path)
        for img_type in ['master', 'thumbnail']:
            old_path = user.backup_data.get(img_type)
            if old_path:
                absolute_path = os.path.join(settings.MEDIA_ROOT, old_path)
                delete_file(absolute_path)