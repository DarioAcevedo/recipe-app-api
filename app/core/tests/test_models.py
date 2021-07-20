from django.test import TestCase
from django.contrib.auth import get_user_model

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