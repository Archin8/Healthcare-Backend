from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from .models import Patient


class PatientTests(APITestCase):
    def setUp(self):
        self.a = User.objects.create_user('a@x.com', 'a@x.com', 'StrongPass123')
        self.b = User.objects.create_user('b@x.com', 'b@x.com', 'StrongPass123')
        self.patient = Patient.objects.create(
            created_by=self.a, name='Pat', age=30, gender='M', phone='9876543210')

    def test_requires_auth(self):
        self.assertEqual(self.client.get('/api/patients/').status_code, 401)

    def test_user_cannot_access_others_patient(self):
        self.client.force_authenticate(self.b)
        self.assertEqual(self.client.get(f'/api/patients/{self.patient.id}/').status_code, 404)
        self.assertEqual(self.client.get('/api/patients/').data, [])

    def test_owner_can_delete(self):
        self.client.force_authenticate(self.a)
        self.assertEqual(self.client.delete(f'/api/patients/{self.patient.id}/').status_code, 204)
