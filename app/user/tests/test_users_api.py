from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')

def create_user(**params):
    return get_user_model().objects.create_user(**params)

class PublicUserApiTest(TestCase):
    """Test user api public"""
    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test to create a user with valid payload"""

        payload = {
            'email': 'dario@arcus.mx',
            'password': 'testpass',
            'name': 'Test name'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Tying to create a user duplicate"""
        payload = {
            'email': 'dario@arcus.mx',
            'password': 'testpass',
            'name': 'dario'
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that the usr create a secure pssword"""
        payload = {
            'email': 'dario@arcus.mx',
            'password': 'tes',
            'name': 'dario'
        }
        res = self.client.post(CREATE_USER_URL,payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
        user_exists = get_user_model().objects.filter(
            email=payload['email']
            ).exists()
        
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        payload = {
            'email': 'dario@arcus.mx',
            'password': 'test2456587'
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


    def test_create_token_invalid_credentials(self):

        create_user(email= 'dario@ardcus.mx', 
                    password='testpass')
        payload = {
            'email': 'dario@ardcus.mx', 
            'password': 'wrong'
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        payload = {
            'email': 'dario@ardcus.mx',
            'password': 'dsadasd'
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_missing_field(self):
        """User and password are required on the endpoint"""
        res = self.client.post(TOKEN_URL, {'email' : 'one', 'password': ''})

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


class UserManagementApiTest(TestCase):
    """Testing the user management endpoint"""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            email= 'dario@test.com',
            password= '1233455543',
            name= 'darius_1'
        )

        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Retreiving profile for logged user"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'email': self.user.email,
            'name': self.user.name
        })

    def test_post_not_allowed(self):

        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_user_update_test(self):
        payload = {
            'name': 'newname',
            'email': 'dario@onion.com',
            'password': 'newPassword123'
        }
        print(self.user.password)
        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        print(self.user.password)
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)