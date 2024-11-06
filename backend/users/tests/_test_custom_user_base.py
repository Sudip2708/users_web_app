from django.test import TestCase
from django.utils.text import slugify
from django.db.utils import IntegrityError

from users.models.custom_user import CustomUser

class CustomUserBaseTests(TestCase):

    def setUp(self):
        # Inicializace před každým testem
        self.user = CustomUser.objects.create_user(
            email="testuser@example.com",
            password="password123",
        )

    def test_unique_email(self):
        # Test vyvolání výjimky při založení účtu s již použitým emailem
        with self.assertRaises(IntegrityError):
            CustomUser.objects.create_user(
                email="testuser@example.com",
                password="password123",
            )

    def test_username_generating(self):
        # Test zda se správně generuje uživatelské jméno z emailu
        base_username = self.user.email.split('@')[0].lower()
        self.assertEqual(self.user.username, base_username)

    def test_username_lowercase(self):
        # Test, že username je převedeno na malá písmena
        user = CustomUser.objects.create_user(
            email="John.Doe@example.com",
            password="password123",
        )
        self.assertEqual(user.username, "john.doe")

    def test_username_uniqueness(self):
        # Test zda je generování uživatelského jména vždy jedinečné
        user1 = CustomUser.objects.create_user(
            email="testuser@different_provider1.com",
            password="password123",
        )
        user2 = CustomUser.objects.create_user(
            email="testuser@different_provider2.com",
            password="password123",
        )
        user3 = CustomUser.objects.create_user(
            email="testuser@different_provider3.com",
            password="password123",
        )
        self.assertEqual(user1.username, "testuser1")
        self.assertEqual(user2.username, "testuser2")
        self.assertEqual(user3.username, "testuser3")

    def test_username_change_and_slug_change(self):
        # Test zda je možné změnit uživatelské jméno
        user = CustomUser.objects.create_user(
            email="testuser1@example.com",
            password="password123",
        )
        old_username = user.username
        new_username = "new_username"
        user.username = new_username
        user.save()
        self.assertEqual(user.username, new_username)
        self.assertEqual(user.slug, slugify(new_username))

        user.username = old_username
        user.save()
        self.assertEqual(user.username, old_username)
        self.assertEqual(user.slug, slugify(old_username))

    def test_slug_generating(self):
        # Test zda se správně generuje slug z uživatelského jména
        generate_slug = slugify(self.user.username)
        self.assertEqual(self.user.slug, generate_slug)

    def test_slug_reset_after_change(self):
        # Test zda pole slug se při změně nastavý na původní hodnotu
        generate_slug = slugify(self.user.username)
        self.user.slug = "new_slug"
        self.user.save()
        self.assertEqual(self.user.slug, generate_slug)

    def test_user_str_method(self):
        # Test správnosti __str__ metody
        self.assertEqual(str(self.user), self.user.slug)

    def test_profile_image_default(self):
        # Test zda má profilový obrázek správně nastavenou výchozí hodnotu
        self.assertEqual(self.user.profile_image, 'users/profile_pics/default_400x400.png')

    def test_profile_image_thumbnail_default(self):
        # Test zda má miniatura profilového obrázku správně nastavenou výchozí hodnotu
        self.assertEqual(self.user.profile_image_thumbnail, 'users/profile_pics/default_64x64.png')


