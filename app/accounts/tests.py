from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

class RegisterTests(APITestCase):
    def test_wrong_syntax(self):
        """
        Create account with wrong input data
        """
        url = reverse('register')
        data = {'name': 'SuperCoolUser'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_right_syntax(self):
        """
        Create account with right input data
        """
        url = reverse('register')
        data = {
            'username': 'test_user',
            'password': '4EGePjndgFCi',
            'password2': '4EGePjndgFCi',
            'email': 'iamcool@gmail.ya',
            'first_name': 'Super',
            'last_name': 'User',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class LoginTests(APITestCase):
    user = 'test_user'
    password = '4EGePjndgFCi'

    def setUp(self):
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

    def test_login_wrong_user(self):
        """
        Try to get token with wrong credentials
        """
        url = reverse('login')
        data = {
            'username': 'test_user',
            'password': '11111111',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login__right_user(self):
        """
        Try to get token with right credentials
        """
        url = reverse('login')
        data = {
            'username': self.user,
            'password': self.password,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class WhoamiTests(APITestCase):
    user = 'test_user'
    password = '4EGePjndgFCi'

    def setUp(self):
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
        self.token = login_response.json()["token"]

    def test_login_wrong_token(self):
        """
        Try to get user info with wrong token
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'TOKEN SUPER_TOKEN')
        url = reverse('whoami')
        response = self.client.get(url, None)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_right_token(self):
        """
        Try to get user info with right token
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'TOKEN {self.token}')
        url = reverse('whoami')
        response = self.client.get(url, None)
        self.assertEqual(response.status_code, status.HTTP_200_OK)