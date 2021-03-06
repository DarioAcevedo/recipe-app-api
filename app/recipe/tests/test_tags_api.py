from django.contrib.auth import get_user_model
from django.test.utils import tag
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Tag, Recipe

from ..serializers import TagSerializer

TAGS_URL = reverse('recipe:tag-list')


class PublicTagsApiTests(TestCase):
    """ Test the publicly available tags api"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Login is required for retreiving tags"""
        res = self.client.get(TAGS_URL)


        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateTagsApiTests(TestCase):
    """Test the authorized user tags API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@test.com',
            'password213'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retreiving_tag(self):
        """Test retreiving tags"""
        Tag.objects.create(user=self.user, name='Vegan')
        Tag.objects.create(user=self.user, name='Dessert')

        res = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
    
    def test_tags_limited_to_user(self):
        """Test that tags return just the tags for authenticated user"""
        user2 = get_user_model().objects.create_user(
            'other@test.com',
            'password867867'
        )

        Tag.objects.create(user=user2, name='Fruity')
        tag = Tag.objects.create(user=self.user, name='Comfort food')

        res = self.client.get(TAGS_URL)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)

    def test_create_tag_successful(self):
        """Test creating a new tag"""
        payload = {'name': 'Test tag'}
        self.client.post(TAGS_URL, payload)

        exists = Tag.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()
        self.assertTrue(exists)

    def test_create_tag_without_name(self):
        """Test creating a tag with invalid payload"""
        payload = {'name' : ''}
        res = self.client.post(TAGS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)     

    def test_retrive_tags_assigned_to_recipes(self):

        tag1 = Tag.objects.create(user=self.user, name='Breakfast')
        tag2 = Tag.objects.create(user=self.user, name='Lunch')
        recipe = Recipe.objects.create(
            title='Coriander eggs on toast',
            time_minutes=3,
            price=5.00,
            user=self.user
        )

        recipe.tags.add(tag1)

        res = self.client.get(TAGS_URL, {'assigned_only': 1})

        serializer1 = TagSerializer(tag1)
        serializer2 = TagSerializer(tag2)

        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)


    def test_retrieve_tags_assigned_unique(self):
        """Test that returns unique items"""
        tag = Tag.objects.create(user=self.user, name='Breakfast')
        Tag.objects.create(user=self.user, name='Lunch')

        recipe1 = Recipe.objects.create(
            title='Pancakes',
            user=self.user,
            time_minutes=5,
            price=10.00
        )
        recipe2 = Recipe.objects.create(
            title='Eggs',
            user=self.user,
            time_minutes=2,
            price=20.00
        )

        recipe1.tags.add(tag)
        recipe2.tags.add(tag)

        res = self.client.get(TAGS_URL, {'assigned_only': 1})

        self.assertEqual(len(res.data), 1)