from rest_framework import serializers
from user.serializers import PatientSerializer, ProfessionalSerializer

class AppPatientSerializer(serializers.Serializer):
    cpf = serializers.CharField()

class AppProfessonalSerializer(serializers.Serializer):
    council_number = serializers.CharField()

# class 

class AppointmentsSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    date = serializers.DateTimeField()
    complaint = serializers.CharField()
    finished = serializers.BooleanField()
    patient = AppPatientSerializer()
    professional = AppProfessonalSerializer()

class AllAppointmentsSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    date = serializers.DateTimeField()
    complaint = serializers.CharField()
    finished = serializers.BooleanField()
    patient = serializers.RelatedField()
    professional = serializers.RelatedField()

