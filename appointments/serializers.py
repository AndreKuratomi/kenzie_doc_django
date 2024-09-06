from rest_framework import serializers
from user.models import Patient, Professional
from user.serializers import PatientSerializer, ProfessionalSerializer


class AppPatientSerializer(serializers.Serializer):
    cpf = serializers.CharField()


class AppProfessonalSerializer(serializers.Serializer):
    council_number = serializers.CharField()


class AppointmentsSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    date = serializers.DateTimeField()
    complaint = serializers.CharField()
    finished = serializers.BooleanField(default=False)
    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all())
    professional = serializers.PrimaryKeyRelatedField(queryset=Professional.objects.all())


class AllAppointmentsSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    date = serializers.DateTimeField()
    complaint = serializers.CharField()
    finished = serializers.BooleanField()
    patient = PatientSerializer()
    professional = ProfessionalSerializer()


class AppointmentsToUpdateSerializer(serializers.Serializer):
    date = serializers.DateTimeField(required=False)
    complaint = serializers.CharField(required=False)
    finished = serializers.BooleanField(required=False)
    patient = serializers.CharField()
    professional = serializers.CharField()