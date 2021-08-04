from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models

def sample_user(email='test@dario.com', password='dario123'):
    """Create a sample user model"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):
    def setUp(self):
        self.email = 'test@CORNERSHOP.mx'
        self.password = 'test123'

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email successful"""
        user = get_user_model().objects.create_user(
            email=self.email,
            password=self.password
        )

        self.assertEqual(user.email,self.email.lower())
        self.assertTrue(user.check_password(self.password))

    def test_new_user_email_normalized(self):
        """The Email for a new user is normalized"""
        user = get_user_model().objects.create_user(
            email=self.email,
            password=self.password
        )
        self.assertEqual(user.email, self.email.lower())

    def test_new_user_invalid_email(self):
        """When create user no email rises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_super_user_created(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@cornershop.mx',
            'test123'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """Test tag string rep"""
        tag = models.Tag.objects.create(
            user= sample_user(),
            name= 'Vegan'
        )

        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        """Test ingredient create representation"""
        ingredient = models.Ingredient.objects.create(
            user = sample_user(),
            name = 'Cucumber'
        )

        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        """Test that the recipe string reps """
        recipe = models.Recipe.objects.create(
            user= sample_user(),
            title= "Steak and mushroom sauce",
            time_minutes=5,
            price=5.00
        )

        self.assertEqual(str(recipe), recipe.title)