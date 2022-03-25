from email.headerregistry import Address
from rest_framework import serializers

from user.models import Patient, User
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

    users = UserSerializer(many=True)


class PatientSerializer(serializers.ModelSerializer):
    user = UserForPatientSerializer()

    class Meta:
        model = Patient
        fields = "__all__"

        extra_kwargs = {
            'cpf': {'read_only': False}
        }

    # def validate(self, validated_data):
    #     does_patient_already_exists = Patient.objects.filter(cpf=serializer.validated_data['cpf']).exists()
    #     if does_patient_already_exists is True:
    #         return Response({"message": "This patient already exists"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def create(self, validated_data):
        user = User.objects.create_user(email=validated_data['user']['email'], password=validated_data['user']['password'])
        new_patient = Patient.objects.create(user=user, cpf=validated_data['cpf'], age=validated_data['age'], sex=validated_data['sex'])

        return new_patient

# class PatientSerializer(serializers.Serializer):
#     user= UserSerializer(read_only=True)
#     cpf = serializers.CharField()
#     age = serializers.CharField()
#     sex = serializers.CharField()


class PatientToUpdateSerializer(serializers.Serializer):
    user= UserSerializer(read_only=True)
    cpf = serializers.CharField(required=False)
    age = serializers.CharField(required=False)
    sex = serializers.CharField(required=False)

    # users = UserSerializer(many=True)

class AdminSerializer(serializers.Serializer):
    name = serializers.CharField()
    password = serializers.CharField(write_only=True)