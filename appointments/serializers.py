from rest_framework import serializers
from .models import AppointmentsModel
from user.models import Patient, Professional
from user.serializers import PatientSerializer, ProfessionalSerializer

from datetime import datetime


date = serializers.DateTimeField( # brazilian format
    input_formats=['%d/%m/%Y - %H:%M'],
    format='%d/%m/%Y - %H:%M'
)


class AppointmentsSerializer(serializers.ModelSerializer):
    
    uuid = serializers.UUIDField(read_only=True)
    complaint = serializers.CharField()
    date = date
    finished = serializers.BooleanField(default=False)
    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all())
    professional = serializers.PrimaryKeyRelatedField(queryset=Professional.objects.all())

    class Meta:
        model = AppointmentsModel
        fields = '__all__'


class AppointmentsToUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppointmentsModel
        fields = '__all__'
