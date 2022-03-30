from email.headerregistry import Address
from rest_framework import serializers
from kenziedoc.exceptions import PatientAlreadyExistsError, UserAlreadyExistsError

from user.models import Patient, User
from .services import is_valid_uuid

# import ipdb


class UserSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    is_prof = serializers.BooleanField(write_only=True)
    is_admin = serializers.BooleanField(write_only=True)
    email = serializers.EmailField()
    # name = serializers.CharField()
    # phone = serializers.CharField()


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
    address = AddressSerializer(many=True, read_only=True) 
    name = serializers.CharField()
    phone = serializers.CharField()  


class NewPatientSerializer(serializers.Serializer):
    user = UserSerializer(read_only=True)
    cpf = serializers.CharField()
    age = serializers.CharField()
    sex = serializers.CharField()


class PatientSerializer(serializers.ModelSerializer):
    user = UserForPatientSerializer()

    class Meta:
        model = Patient
        fields = "__all__"

        extra_kwargs = {
            'cpf': {'read_only': False}
        }

    def validate(self, attrs):
        email = attrs['user']['email']

        does_user_already_exists = User.objects.filter(email=email).exists()
        if does_user_already_exists is True:
            raise UserAlreadyExistsError()

        cpf = attrs['cpf']

        does_patient_already_exists = Patient.objects.filter(cpf=cpf).exists()
        if does_patient_already_exists is True:
            raise PatientAlreadyExistsError()

        return super().validate(attrs)

    def create(self, validated_data):
        user = User.objects.create_user(email=validated_data['user']['email'], password=validated_data['user']['password'])
        new_patient = Patient.objects.create(user=user, cpf=validated_data['cpf'], age=validated_data['age'], sex=validated_data['sex'])

        return new_patient


class PatientIdSerializer(serializers.ModelSerializer):
    user = UserForPatientSerializer()

    class Meta:
        model = Patient
        fields = "__all__"

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.filter(uuid=instance.user.uuid).update(**user_data)
        patient = Patient.objects.filter(cpf=instance.cpf).update(**validated_data)

        updated_patient = Patient.objects.get(cpf=instance.cpf)

        return updated_patient

    # def delete(self, request):
    #     ipdb.set_trace()
    #     user = User.objects.filter(uuid=user.uuid)
    #     user.delete()

    #     patient = Patient.objects.filter(cpf=cpf)
    #     patient.delete()

# class PatientToDeleteSerializer(serializers.ModelSerializer):
#     def delete(self, request):
#         ipdb.set_trace()
#         user = User.objects.filter(uuid=user.uuid)
#         user.delete()

#         patient = Patient.objects.filter(cpf=cpf)
#         patient.delete()


class AdminSerializer(serializers.Serializer):
    user = UserSerializer(read_only=True)
    name = serializers.CharField()
    password = serializers.CharField(write_only=True)
