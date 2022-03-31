from email.headerregistry import Address
from rest_framework import serializers
from kenziedoc.exceptions import PatientAlreadyExistsError, UserAlreadyExistsError

from user.models import Patient, User
from .services import is_valid_uuid



class UserSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    is_prof = serializers.BooleanField(write_only=True)
    is_admin = serializers.BooleanField(write_only=True)
    email = serializers.EmailField()


class UserForPatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["password", "email"]

        extra_kwargs = {
            'password': {'write_only': True}
        }


class LoginUserSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)


class AddressSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    street = serializers.CharField()
    house_number = serializers.IntegerField()
    state = serializers.CharField()

    users = UserSerializer(many=True)


class ProfessionalSerializer(serializers.Serializer):
    user = UserSerializer(read_only=True)
    council_number = serializers.CharField()
    specialty = serializers.CharField()
    name = serializers.CharField()
    phone = serializers.CharField()  


class NewPatientSerializer(serializers.Serializer):
    user = UserSerializer(read_only=True)
    cpf = serializers.CharField()
    age = serializers.CharField()
    sex = serializers.CharField()


class PatientSerializer(serializers.Serializer):
    user = UserSerializer(read_only=True)
    cpf = serializers.CharField()
    age = serializers.CharField()
    sex = serializers.CharField()
    name = serializers.CharField()
    phone = serializers.CharField()


    def validate(self, attrs):
        email = attrs['user']['email']


class PatientIdSerializer(serializers.ModelSerializer):
    user = UserForPatientSerializer()

    class Meta:
        model = Patient
        fields = "__all__"



class AdminSerializer(serializers.Serializer):
    user = UserSerializer(read_only=True)
    name = serializers.CharField()
    password = serializers.CharField(write_only=True)
