from rest_framework import status
from rest_framework.test import APITestCase


class AuthTests(APITestCase):
    payload = {'name': 'Jane', 'email': 'jane@example.com', 'password': 'StrongPass123'}

    def test_register_then_login(self):
        r = self.client.post('/api/auth/register/', self.payload, format='json')
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.assertNotIn('password', r.data)

        r = self.client.post('/api/auth/login/',
                             {'email': self.payload['email'], 'password': self.payload['password']},
                             format='json')
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertIn('access', r.data)

    def test_duplicate_email_rejected(self):
        self.client.post('/api/auth/register/', self.payload, format='json')
        r = self.client.post('/api/auth/register/', self.payload, format='json')
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_wrong_password(self):
        self.client.post('/api/auth/register/', self.payload, format='json')
        r = self.client.post('/api/auth/login/',
                             {'email': self.payload['email'], 'password': 'wrong'}, format='json')
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)
