from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Doctor


class DoctorTests(APITestCase):
    def setUp(self):
        self.a = User.objects.create_user('a@x.com', 'a@x.com', 'StrongPass123')
        self.b = User.objects.create_user('b@x.com', 'b@x.com', 'StrongPass123')
        self.doctor = Doctor.objects.create(
            created_by=self.a, name='Dr Smith', email='smith@hospital.com',
            phone='1234567890', specialization='Cardiology', experience_years=10)

    def test_requires_auth(self):
        self.assertEqual(self.client.get('/api/doctors/').status_code, 401)

    def test_any_user_can_list(self):
        self.client.force_authenticate(self.b)
        r = self.client.get('/api/doctors/')
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data), 1)

    def test_any_user_can_retrieve(self):
        self.client.force_authenticate(self.b)
        r = self.client.get(f'/api/doctors/{self.doctor.id}/')
        self.assertEqual(r.status_code, status.HTTP_200_OK)

    def test_non_creator_cannot_update(self):
        self.client.force_authenticate(self.b)
        r = self.client.put(f'/api/doctors/{self.doctor.id}/', {
            'name': 'Dr Jones', 'email': 'smith@hospital.com',
            'phone': '1234567890', 'specialization': 'Cardiology',
            'experience_years': 10}, format='json')
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)

    def test_non_creator_cannot_delete(self):
        self.client.force_authenticate(self.b)
        r = self.client.delete(f'/api/doctors/{self.doctor.id}/')
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)

    def test_creator_can_update(self):
        self.client.force_authenticate(self.a)
        r = self.client.put(f'/api/doctors/{self.doctor.id}/', {
            'name': 'Dr Jones', 'email': 'smith@hospital.com',
            'phone': '1234567890', 'specialization': 'Neurology',
            'experience_years': 12}, format='json')
        self.assertEqual(r.status_code, status.HTTP_200_OK)

    def test_creator_can_delete(self):
        self.client.force_authenticate(self.a)
        r = self.client.delete(f'/api/doctors/{self.doctor.id}/')
        self.assertEqual(r.status_code, status.HTTP_204_NO_CONTENT)

    def test_duplicate_email_rejected(self):
        self.client.force_authenticate(self.a)
        r = self.client.post('/api/doctors/', {
            'name': 'Dr Clone', 'email': 'smith@hospital.com',
            'phone': '1234567890', 'specialization': 'Dermatology',
            'experience_years': 5}, format='json')
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
