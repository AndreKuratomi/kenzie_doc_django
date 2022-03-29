from rest_framework import serializers
from user.serializers import PatientSerializer, ProfessionalSerializer


class AppointmentsSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    date = serializers.DateTimeField()
    complaint = serializers.CharField()
    finished = serializers.BooleanField()
    patient = PatientSerializer()
    professional = ProfessionalSerializer()
