from email.headerregistry import Address
from rest_framework import serializers
from kenziedoc.exceptions import PatientAlreadyExistsError, UserAlreadyExistsError

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


    # def update(self, validated_data):
    #     user = User.objects.create_user(email=validated_data['user']['email'], password=validated_data['user']['password'])
    #     new_patient = Patient.objects.create(user=user, cpf=validated_data['cpf'], age=validated_data['age'], sex=validated_data['sex'])

    #     return new_patient


    # def get(self, request, user_id=''):
    #     try:
    #         valid_uuid = is_valid_uuid(user_id)
    #         if valid_uuid:
    #             patient = Patient.objects.filter(uuid=user_id)
    #             serialized = PatientSerializer(patient)

    #             return Response(serialized.data, status=status.HTTP_200_OK)

    #     except Patient.DoesNotExist:
    #         return Response({"message": "No patient found"}, status=status.HTTP_404_NOT_FOUND)
    #     except ValueError:
    #         return Response({"message": "No valid UUID"}, status=status.HTTP_404_NOT_FOUND)

    # def patch(self, request, user_id=''):

    #     serializer = PatientToUpdateSerializer

    #     try:
    #         valid_uuid = is_valid_uuid(user_id)
    #         if valid_uuid:
    #             patient = Patient.objects.filter(uuid=user_id)
    #             serialized = PatientSerializer(patient)

    #             return Response(serialized.data, status=status.HTTP_200_OK)

    #     except Patient.DoesNotExist:
    #         return Response({"message": "No patient found"}, status=status.HTTP_404_NOT_FOUND)
    #     except ValueError:
    #         return Response({"message": "No valid UUID"}, status=status.HTTP_404_NOT_FOUND)

    #     try:
    #         to_update = Patient.objects.filter(uuid=user_id).update(**serializer.validated_data)
    #     except IntegrityError:
    #         return Response({"message": "This user email already exists"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


    #     updated = Patient.objects.get(uuid=user_id)

    #     serialized = Patient(updated)

    #     return Response(serialized.data, status=status.HTTP_200_OK)

    # def delete(self, request, user_id=''):
    #     try:
    #         valid_uuid = is_valid_uuid(user_id)
    #         if valid_uuid:
    #             patient = Patient.objects.filter(uuid=user_id)
    #             Patient.delete(patient)

    #             return Response(status=status.HTTP_204_NO_CONTENT)

    #     except Patient.DoesNotExist:
    #         return Response({"message": "No patient found"}, status=status.HTTP_404_NOT_FOUND)
    #     except ValueError:
    #         return Response({"message": "No valid UUID"}, status=status.HTTP_404_NOT_FOUND)


class PatientToUpdateSerializer(serializers.Serializer):
    user = UserSerializer(read_only=True)
    cpf = serializers.CharField(required=False)
    age = serializers.CharField(required=False)
    sex = serializers.CharField(required=False)

    # users = UserSerializer(many=True)

class AdminSerializer(serializers.Serializer):
    name = serializers.CharField()
    password = serializers.CharField(write_only=True)