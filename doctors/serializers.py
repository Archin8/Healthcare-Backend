from django.core.validators import RegexValidator
from rest_framework import serializers
from .models import Doctor

phone_regex = RegexValidator(
    regex=r'^\+?\d{7,15}$',
    message='Enter a valid phone number (digits, optional leading +, 7–15 chars).'
)


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ('id', 'name', 'email', 'phone', 'specialization',
                  'experience_years', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')
        extra_kwargs = {
            'name': {'min_length': 2},
            'phone': {'validators': [phone_regex]},
        }
