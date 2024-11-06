from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify

from .managers.custom_user_managers import CustomUserManager
# from .utils.username_utils import unique_username_from_email
# from .utils.profile_image_validation import validate_image_and_size

class CustomUser(AbstractUser):

    email = models.EmailField(
        verbose_name='Email',
        unique=True,
    )

    username = models.CharField(
        verbose_name='User Name',
        unique=True,
        max_length=50,
    )

    slug = models.SlugField(
        verbose_name='Username Slug',
        unique=True,
    )

    # Nastavení cesty pro uložení obrázků do složky media
    PROFILE_IMAGE_PATH = 'users/profile_images/masters/'
    THUMBNAIL_PATH = 'users/profile_images/thumbnails/'

    profile_image = models.ImageField(
        verbose_name='Profile Image',
        upload_to=PROFILE_IMAGE_PATH,
        default='new_user',
    )

    profile_image_thumbnail = models.ImageField(
        verbose_name='Profile Image Thumbnail',
        upload_to=THUMBNAIL_PATH,
        default='new_user',
    )

    backup_data = models.JSONField(
        verbose_name='Profile Image Backup',
        default=dict,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def save(self, *args, **kwargs):

        # Automatické vytvoření unikátního username (Pokud není nastaveno)
        if not self.username:
            self.username = unique_username_from_email(self.email)

        # Automatické vytvoření slugu (Pokud neodpovídá slugu)
        if self.slug != slugify(self.username):
            self.slug = slugify(self.username)

        # # Zpracování profilového obrázku
        # if self.pk:
        #     if self.backup_data['profile_image'] != self.profile_image.name:
        #         validate_image_and_size(self.profile_image)
        #         self.profile_image_processing()
        # else:
        #     self.set_default_profile_images()

        super().save(*args, **kwargs)




    def __str__(self):
        return self.slug







