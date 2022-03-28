from rest_framework import serializers
from user.serializers import PatientSerializer, ProfessionalSerializer


class AppointmentsSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    date = serializers.DateTimeField(read_only=True)
    complaint = serializers.CharField()
    finished = serializers.BooleanField()
    patient = PatientSerializer(read_only=True)
    professional = ProfessionalSerializer(read_only=True)
