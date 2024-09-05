from email.headerregistry import Address
from rest_framework import serializers
from kenziedoc_project.exceptions import AddressNotFoundError, PatientAlreadyExistsError, UserAlreadyExistsError, UserNotFoundError

from user.models import Address, Admin, Patient, Professional, User
# from .services import is_valid_uuid

import ipdb


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    
    class Meta:
        model = User
        fields = [
            "uuid",
            "address",
            "age",
            "cpf",
            "email",
            "is_admin",
            "is_prof",
            "name",
            "password",
            "phone",
            "surname",
            "sex",
        ]

        extra_kwargs = {
            'password': {'write_only': True},
            'cpf': {'write_only': True}
        }


class LoginUserSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)


class PatientSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    
    class Meta:
        model = Patient
        fields = "__all__"


class PatientIdSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Patient
        fields = "__all__"


class ProfessionalSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Professional
        fields = [
            "user",
            "council_number",
            "specialty",
        ]


class AdminSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Admin
        fields = "__all__"



#For clinics:
# class AddressSerializer(serializers.Serializer):
#     uuid = serializers.UUIDField(read_only=True)
#     street = serializers.CharField()
#     house_number = serializers.IntegerField()
#     state = serializers.CharField()

#     users = UserSerializer(many=True)
