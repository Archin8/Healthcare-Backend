from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from patients.models import Patient
from .models import PatientDoctorMapping
from .serializers import MappingSerializer, PatientDoctorSerializer


class MappingListCreateView(ListCreateAPIView):
    serializer_class = MappingSerializer

    def get_queryset(self):
        return (
            PatientDoctorMapping.objects
            .filter(patient__created_by=self.request.user)
            .select_related('patient', 'doctor')
        )


class MappingDetailView(APIView):
    """
    GET    /api/mappings/<patient_id>/ -> doctors assigned to that patient
    DELETE /api/mappings/<id>/         -> remove that mapping
    Same URL shape, different meaning of <pk> per HTTP method (per the spec).
    """

    def get(self, request, pk):
        patient = get_object_or_404(Patient, pk=pk, created_by=request.user)
        mappings = patient.mappings.select_related('doctor')
        return Response(PatientDoctorSerializer(mappings, many=True).data)

    def delete(self, request, pk):
        mapping = get_object_or_404(
            PatientDoctorMapping, pk=pk, patient__created_by=request.user
        )
        mapping.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
