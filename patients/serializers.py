from django.core.validators import RegexValidator
from rest_framework import serializers
from .models import Patient

phone_regex = RegexValidator(
    regex=r'^\+?\d{7,15}$',
    message='Enter a valid phone number (digits, optional leading +, 7–15 chars).'
)


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ('id', 'name', 'age', 'gender', 'phone', 'address',
                  'medical_history', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')
        extra_kwargs = {
            'name': {'min_length': 2},
            'phone': {'validators': [phone_regex]},
        }

    def validate_age(self, value):
        if value > 130:
            raise serializers.ValidationError('Enter a realistic age.')
        return value
