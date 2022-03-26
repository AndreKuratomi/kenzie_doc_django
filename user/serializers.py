from email.headerregistry import Address
from rest_framework import serializers
from kenziedoc.exceptions import PatientAlreadyExistsError, UserAlreadyExistsError

from user.models import Patient, User
from .services import is_valid_uuid

import ipdb

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


class PatientToUpdateSerializer(serializers.Serializer):
    user = UserSerializer(read_only=True)
    cpf = serializers.CharField(required=False)
    age = serializers.CharField(required=False)
    sex = serializers.CharField(required=False)

    # users = UserSerializer(many=True)


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
    address = AddressSerializer(many=True, read_only=True)

    users = UserSerializer(many=True)


class PatientSerializer(serializers.ModelSerializer):
    user = UserForPatientSerializer()

    class Meta:
        model = Patient
        fields = "__all__"

        extra_kwargs = {
            'cpf': {'read_only': False}
        }

    def validate(self, attrs, request):
        # if request.method != "PATCH":
        email = attrs['user']['email']

        does_user_already_exists = User.objects.filter(email=email).exists()
        if does_user_already_exists is True:
            raise UserAlreadyExistsError()

        cpf = attrs['cpf']

        does_patient_already_exists = Patient.objects.filter(cpf=cpf).exists()
        if does_patient_already_exists is True:
            raise PatientAlreadyExistsError()

        return super().validate(attrs, request)

    def create(self, validated_data):
        user = User.objects.create_user(email=validated_data['user']['email'], password=validated_data['user']['password'])
        new_patient = Patient.objects.create(user=user, cpf=validated_data['cpf'], age=validated_data['age'], sex=validated_data['sex'])

        return new_patient

    def update(self, validated_data):
        #   ESTÁ CONFUNDINDO COM O CREATE. NÃO PASSA DO VALIDATE
        ipdb.set_trace()
        user_to_update = User.objects.update(**validated_data)
        user_updated = Patient.objects.get(user_to_update)

        return user_updated

class AdminSerializer(serializers.Serializer):
    name = serializers.CharField()
    password = serializers.CharField(write_only=True)