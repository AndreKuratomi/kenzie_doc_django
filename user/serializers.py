from email.headerregistry import Address
from rest_framework import serializers
# import uuid

class UserSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    is_prof = serializers.BooleanField(write_only=True)
    is_admin = serializers.BooleanField(write_only=True)
    email = serializers.EmailField()

class AddressSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    street = serializers.CharField()
    house_number = serializers.IntegerField()
    state = serializers.CharField()

    users = UserSerializer(many=True)


class ProfessionalSerializer(serializers.Serializer):
    user= UserSerializer(read_only=True)
    council_number = serializers.CharField()
    specialty = serializers.CharField()
    address = AddressSerializer(many=True, read_only=True)

class PatientSerializer(serializers.Serializer):
    cpf = serializers.CharField()
    age = serializers.CharField()
    sex = serializers.CharField()

    # users = UserSerializer(many=True)

class PatientToUpdateSerializer(serializers.Serializer):
    user= UserSerializer(read_only=True)
    cpf = serializers.CharField(required=False)
    age = serializers.CharField(required=False)
    sex = serializers.CharField(required=False)

    # users = UserSerializer(many=True)

class AdminSerializer(serializers.Serializer):
    name = serializers.CharField()
    password = serializers.CharField(write_only=True)