from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import User

class TokenTests(APITestCase):
    "Test token authentication with logs"

    def setUp(self):
        self.user = User.objects.create_user(username='john',
                                        password='banana')
        self.token = Token.objects.get(user=self.user)

    def test_get_token(self):
        "Test getting a token from username and password through the API"
        url = '/api-token-auth/'
        client = APIClient()
        auth = {'username':'john', 'password':'banana'}
        token_request = client.post(url, data = auth, format='json')
        self.assertEqual(token_request.status_code, status.HTTP_200_OK)
        self.assertEqual(token_request.json()['token'], self.token.key)


    def test_token_auth(self):        
        "Test simple get http request with and without Token credential"
        client = APIClient()
        users_request = client.get('/api/users/', format='json')
        self.assertEqual(users_request.status_code, status.HTTP_401_UNAUTHORIZED)
        client.credentials(HTTP_AUTHORIZATION = 'Token ' + self.token.key)
        users_request_auth = client.get('/api/users/', format = 'json')
        self.assertEqual(users_request_auth.status_code, status.HTTP_200_OK)
        data = users_request_auth.json()
        usernames = []
        for user in data:
            usernames.append(user['username'])
        self.assertIn(self.user.username, usernames)
