from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from doctors.models import Doctor
from mappings.models import PatientDoctorMapping
from patients.models import Patient


class Command(BaseCommand):
    help = 'Seeds fake sample data (Users, Patients, Doctors, Mappings) for testing'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding database with sample data...')

        # 1. Create Sample Users
        user1, created1 = User.objects.get_or_create(
            username='john@example.com',
            defaults={
                'email': 'john@example.com',
                'first_name': 'John Doe',
            },
        )
        if created1:
            user1.set_password('Password123!')
            user1.save()

        user2, created2 = User.objects.get_or_create(
            username='sarah@example.com',
            defaults={
                'email': 'sarah@example.com',
                'first_name': 'Sarah Smith',
            },
        )
        if created2:
            user2.set_password('Password123!')
            user2.save()

        # 2. Create Doctors
        doctor1, _ = Doctor.objects.get_or_create(
            email='alice.johnson@hospital.org',
            defaults={
                'name': 'Alice Johnson',
                'phone': '+1-555-0199',
                'specialization': 'Cardiology',
                'experience_years': 12,
                'created_by': user1,
            },
        )

        doctor2, _ = Doctor.objects.get_or_create(
            email='robert.chen@hospital.org',
            defaults={
                'name': 'Robert Chen',
                'phone': '+1-555-0288',
                'specialization': 'Neurology',
                'experience_years': 8,
                'created_by': user1,
            },
        )

        doctor3, _ = Doctor.objects.get_or_create(
            email='emily.davis@hospital.org',
            defaults={
                'name': 'Emily Davis',
                'phone': '+1-555-0377',
                'specialization': 'Pediatrics',
                'experience_years': 15,
                'created_by': user2,
            },
        )

        # 3. Create Patients
        patient1, _ = Patient.objects.get_or_create(
            phone='+1-555-0101',
            created_by=user1,
            defaults={
                'name': 'Arthur Dent',
                'age': 42,
                'gender': Patient.Gender.MALE,
                'address': '42 Country Lane, Cottington',
                'medical_history': 'Mild hypertension, routine checkups.',
            },
        )

        patient2, _ = Patient.objects.get_or_create(
            phone='+1-555-0102',
            created_by=user1,
            defaults={
                'name': 'Ford Prefect',
                'age': 35,
                'gender': Patient.Gender.MALE,
                'address': '12 Hitchhiker Way, London',
                'medical_history': 'No prior illnesses.',
            },
        )

        patient3, _ = Patient.objects.get_or_create(
            phone='+1-555-0103',
            created_by=user2,
            defaults={
                'name': 'Tricia McMillan',
                'age': 30,
                'gender': Patient.Gender.FEMALE,
                'address': '88 Astronomy Ave, Islington',
                'medical_history': 'Asthma, managed with inhaler.',
            },
        )

        # 4. Create Mappings
        PatientDoctorMapping.objects.get_or_create(patient=patient1, doctor=doctor1)
        PatientDoctorMapping.objects.get_or_create(patient=patient1, doctor=doctor2)
        PatientDoctorMapping.objects.get_or_create(patient=patient3, doctor=doctor3)

        self.stdout.write(self.style.SUCCESS('Successfully seeded sample data!\n'))
        self.stdout.write('Sample Accounts (Password: Password123!):')
        self.stdout.write(' - john@example.com')
        self.stdout.write(' - sarah@example.com')
