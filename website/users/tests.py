from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIRequestFactory

from .serializers import UserSerializer

User = get_user_model()


class TestUser(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create(username='testman', email='test.man@example.com', password='MegaPassword1234')
        self.user.set_password('MegaPassword1234')
        self.user.is_superuser = True
        self.user.first_name = 'Test'
        self.user.last_name = 'Man'
        self.user.save()
        self.token = Token.objects.create(user=self.user)
        self.token.save()
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.token.key))

    def test_user_registration_logout_login(self):
        """
        This tests registration, logout, and login
        """
        register_url = reverse('rest_register')
        logout_url = reverse('rest_logout')
        login_url = reverse('rest_login')
        register_data = {
            'username': 'testman2',
            'email': 'test.man2@example.com',
            'password1': 'MegaPassword1234',
            'password2': 'MegaPassword1234',
            'preferred_language': 'en'
        }
        login_data = {
            'username': 'testman2',
            'password': 'MegaPassword1234'
        }
        register_response = self.client.post(register_url, register_data, format='json')
        self.assertEqual(register_response.status_code, status.HTTP_201_CREATED)
        logout_response = self.client.post(logout_url, {}, format='json')
        self.assertEqual(logout_response.status_code, status.HTTP_200_OK)
        login_response = self.client.post(login_url, login_data, format='json')
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)

    def test_user_obtain_auth_token(self):
        url = reverse('obtain-auth-token')
        data = {
            'username': 'testman',
            'password': 'MegaPassword1234'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_token = response.data.get('token')
        self.assertEqual(self.token.key, response_token)

    def test_user_create(self):
        url = reverse('api:user-list')
        data = {
            'username': 'testingwoman',
            'first_name': 'Testing',
            'last_name': 'Woman',
            'email': 'testingwoman@testing.com',
            'password': 'Password1234',
            'preferred_language': 'en'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(username='testingwoman')
        self.assertEqual(user.email, 'testingwoman@testing.com')
        self.assertEqual(user.first_name, 'Testing')
        self.assertEqual(user.last_name, 'Woman')

    def test_user_get(self):
        response = self.client.get('/api/users/testman/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data,
                         {'username': 'testman', 'email': 'test.man@example.com', 'first_name': 'Test',
                          'last_name': 'Man', 'full_name': 'Test Man', 'preferred_language': 'en',
                          'url': 'http://testserver/api/users/testman/'})

    def test_user_list(self):
        users = User.objects.all()
        request = self.factory.get('/')
        serializer = UserSerializer(users, context={'request': request}, many=True)
        response = self.client.get(reverse('api:user-list'))
        self.assertEqual(response.data, serializer.data)
