from rest_framework import serializers
from doctors.serializers import DoctorSerializer
from .models import PatientDoctorMapping


class MappingSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.name', read_only=True)

    class Meta:
        model = PatientDoctorMapping
        fields = ('id', 'patient', 'doctor', 'patient_name', 'doctor_name', 'assigned_at')
        read_only_fields = ('id', 'assigned_at')

    def validate_patient(self, patient):
        if patient.created_by_id != self.context['request'].user.id:
            raise serializers.ValidationError(
                'You can only assign doctors to your own patients.'
            )
        return patient


class PatientDoctorSerializer(serializers.ModelSerializer):
    """Used for GET /api/mappings/<patient_id>/ — doctors for one patient."""
    mapping_id = serializers.IntegerField(source='id', read_only=True)
    doctor = DoctorSerializer(read_only=True)

    class Meta:
        model = PatientDoctorMapping
        fields = ('mapping_id', 'doctor', 'assigned_at')
