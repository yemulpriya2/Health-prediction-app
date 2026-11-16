from rest_framework import viewsets
from .models import Patient
from .serializers import PatientSerializer
from .services import generate_health_remarks

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

    def perform_create(self, serializer):
        patient = serializer.save()
        patient.remarks = generate_health_remarks(patient)
        patient.save(update_fields=["remarks", "updated_at"])

    def perform_update(self, serializer):
        patient = serializer.save()
        patient.remarks = generate_health_remarks(patient)
        patient.save(update_fields=["remarks", "updated_at"])
