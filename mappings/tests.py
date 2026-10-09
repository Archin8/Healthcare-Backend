from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from doctors.models import Doctor
from patients.models import Patient
from .models import PatientDoctorMapping


class MappingTests(APITestCase):
    def setUp(self):
        self.a = User.objects.create_user('a@x.com', 'a@x.com', 'StrongPass123')
        self.b = User.objects.create_user('b@x.com', 'b@x.com', 'StrongPass123')
        self.patient = Patient.objects.create(
            created_by=self.a, name='Pat', age=30, gender='M', phone='9876543210')
        self.doctor = Doctor.objects.create(
            created_by=self.a, name='Dr Smith', email='smith@hospital.com',
            phone='1234567890', specialization='Cardiology', experience_years=10)

    def test_requires_auth(self):
        self.assertEqual(self.client.get('/api/mappings/').status_code, 401)

    def test_create_mapping(self):
        self.client.force_authenticate(self.a)
        r = self.client.post('/api/mappings/',
                             {'patient': self.patient.id, 'doctor': self.doctor.id},
                             format='json')
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

    def test_duplicate_mapping_rejected(self):
        self.client.force_authenticate(self.a)
        self.client.post('/api/mappings/',
                         {'patient': self.patient.id, 'doctor': self.doctor.id},
                         format='json')
        r = self.client.post('/api/mappings/',
                             {'patient': self.patient.id, 'doctor': self.doctor.id},
                             format='json')
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cannot_map_others_patient(self):
        self.client.force_authenticate(self.b)
        r = self.client.post('/api/mappings/',
                             {'patient': self.patient.id, 'doctor': self.doctor.id},
                             format='json')
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_shows_only_own(self):
        PatientDoctorMapping.objects.create(patient=self.patient, doctor=self.doctor)
        self.client.force_authenticate(self.b)
        r = self.client.get('/api/mappings/')
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data), 0)

    def test_get_doctors_for_patient(self):
        PatientDoctorMapping.objects.create(patient=self.patient, doctor=self.doctor)
        self.client.force_authenticate(self.a)
        r = self.client.get(f'/api/mappings/{self.patient.id}/')
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data), 1)

    def test_delete_mapping(self):
        mapping = PatientDoctorMapping.objects.create(
            patient=self.patient, doctor=self.doctor)
        self.client.force_authenticate(self.a)
        r = self.client.delete(f'/api/mappings/{mapping.id}/')
        self.assertEqual(r.status_code, status.HTTP_204_NO_CONTENT)
        r = self.client.delete(f'/api/mappings/{mapping.id}/')
        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)
