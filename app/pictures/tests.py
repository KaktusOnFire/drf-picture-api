from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, override_settings
from PIL import Image

from pictures.models import Picture

import tempfile
import io
import random

TEMPDIR = tempfile.gettempdir()

def generate_photo_file():
    """
        Helper method to create an image
    """
    file = io.BytesIO()
    image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
    image.save(file, 'png')
    file.name = 'test.png'
    file.seek(0)
    return file

class PermissionTests(APITestCase):
    user = 'test_user'
    password = '4EGePjndgFCi'
    
    def test_crud_unauthorized(self):
        """
        Try to use CRUD without auth token
        """
        url = reverse('picture-list')
        response = self.client.get(url, None)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_crud_authorized(self):
        """
        Try to use CRUD with auth token
        """
        url = reverse('register')
        data = {
            'username': self.user,
            'password': self.password,
            'password2': self.password,
            'email': 'iamcool@gmail.ya',
            'first_name': 'Super',
            'last_name': 'User',
        }
        self.client.post(url, data, format='json')
        login_response = self.client.post(reverse('login'), data, format='json')
        token = login_response.json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION=f'TOKEN {token}')
        url = reverse('picture-list')
        response = self.client.get(url, None)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class CrudTests(APITestCase):
    user = 'test_user'
    password = '4EGePjndgFCi'

    def setUp(self):
        """
        Preparing test user and picture object
        """
        self.user_object = User.objects.create(
            username=self.user,
            email='iamcool@gmail.ya',
            first_name='Super',
            last_name='User',
        )
        self.user_object.set_password(self.password)
        self.user_object.save()
        self.token, created = Token.objects.get_or_create(user=self.user_object)

        self.client.credentials(HTTP_AUTHORIZATION=f'TOKEN {self.token.key}')

        self.test_pic = Picture.objects.create(
            user=self.user_object,
            image=SimpleUploadedFile(
                name='test.png', 
                content=generate_photo_file().read(), 
                content_type='image/png'
            )
        )
    
    def tearDown(self):
        """
        Cleanup =)
        """
        for el in Picture.objects.all():
            el.delete()
    
    def test_get_all(self):
        """
        Get all pictures for specific user
        """
        url = reverse('picture-list')
        response = self.client.get(url, None)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Picture.objects.all().count(), 1)

    def test_get_by_id(self):
        """
        Get picture by id
        """
        url = reverse('picture-detail',args=[self.test_pic.id])
        response = self.client.get(url, None)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["id"], self.test_pic.id)

    def test_create(self):
        """
        Create a new picture object
        """
        data = {
            'image': generate_photo_file()
        }
        url = reverse('picture-list')
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update(self):
        """
        Update an existing picture object
        """
        data = {
            'image': generate_photo_file()
        }
        url = reverse('picture-detail', args=[self.test_pic.id])
        response = self.client.put(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete(self):
        """
        Delete an existing picture object
        """
        url = reverse('picture-detail', args=[self.test_pic.id])
        response = self.client.delete(url, None)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class AdminDeleteTest(APITestCase):
    admin_username = 'admin'
    admin_password = '12345'
    test_username = 'test_user'
    test_password = '4EGePjndgFCi'
    
    def setUp(self):
        """
        Preparing test users and picture objects
        """

        #Creating regular user
        self.user = User.objects.create(
            username=self.test_username,
            email='iamcool@gmail.ya',
            first_name='Super',
            last_name='User',
        )
        self.user.set_password(self.test_password)
        self.user.save()
        self.user_token, created = Token.objects.get_or_create(user=self.user)
        
        #Creating admin
        self.admin = User.objects.create(
            username=self.admin_username,
            email='admin@gmail.ya',
            first_name='Admin',
            last_name='Adminov',
            is_staff=True
        )
        self.admin.set_password(self.admin_password)
        self.admin.save()
        self.admin_token, created = Token.objects.get_or_create(user=self.admin)

        for el in range(0,10):
            Picture.objects.create(
                user=random.choice((self.user, self.admin)),
                image=SimpleUploadedFile(
                    name='test.png', 
                    content=generate_photo_file().read(), 
                    content_type='image/png'
                )
            )

    def tearDown(self):
        """
        Cleanup =)
        """
        for el in Picture.objects.all():
            el.delete()

    def test_bulk_delete_nonadmin(self):
        """
        Try to delete all pictures with non-admin user
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'TOKEN {self.user_token.key}')
        url = reverse('picture-bulk')
        response = self.client.delete(url, None)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_bulk_delete_admin(self):
        """
        Try to delete all pictures with admin user
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'TOKEN {self.admin_token.key}')
        url = reverse('picture-bulk')
        response = self.client.delete(url, None)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
