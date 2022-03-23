from rest_framework import serializers
from appointments.serializers import AppointmentsSerializer


class PatientSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)

    cpf = serializers.CharField()
    name = serializers.CharField()
    age = serializers.CharField()
    gender = serializers.CharField()
    email = serializers.CharField()
    phone = serializers.CharField()
    health_insurance = serializers.CharField()
    # password_hash = serializers.CharField() ?
    active = serializers.Booleanfield()

    appointments = AppointmentsSerializer(many=True)


class PatientToUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    age = serializers.CharField(required=False)
    gender = serializers.CharField(required=False)
    email = serializers.CharField(required=False)
    phone = serializers.CharField(required=False)
    health_insurance = serializers.CharField(required=False)
    # password_hash = serializers.CharField(required=False) ?
    active = serializers.BooleanField(required=False) # bom, aqui só o administrator pode, né
