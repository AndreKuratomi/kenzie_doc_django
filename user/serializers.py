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
            "is_prof",
            "is_admin",
            "cpf",
            "name",
            "surname",
            "age",
            "sex",
            "email",
            "password",
            "phone",
            "address",
        ]

        extra_kwargs = {
            'password': {'write_only': True},
            'cpf': {'write_only': True},
            'is_admin': {'write_only': True},
            'is_prof': {'write_only': True}
        }


class LoginUserSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)


class PatientSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Patient
        fields = "__all__"


# class PatientIdSerializer(serializers.ModelSerializer):
#     user = UserSerializer()

#     class Meta:
#         model = Patient
#         fields = "__all__"


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
    user = UserSerializer(read_only=True)
    # ipdb.set_trace()
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


# class UserForPatientSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = "__all__"

#         extra_kwargs = {
#             'password': {'write_only': True},
#             'cpf': {'read_only': True}
#         }


# class NewPatientSerializer(serializers.Serializer):
#     user = UserSerializer(read_only=True)
#     cpf = serializers.CharField()
#     age = serializers.CharField()
#     sex = serializers.CharField()


    # ipdb.set_trace()
    # class Meta:
    #     model = Patient
    #     fields = "__all__"

        # extra_kwargs = {
        #     'cpf': {'read_only': False}
        # }

    # def validate(self, attrs):
    #     # ipdb.set_trace()
    #     email = attrs['user']['email']

    #     does_user_already_exist = User.objects.filter(email=email).exists()
    #     if does_user_already_exist is True:
    #         raise UserAlreadyExistsError()

    #     cpf = attrs['user']['cpf']

    #     does_patient_already_exist = User.objects.filter(cpf=cpf).exists()
    #     if does_patient_already_exist is True:
    #         raise PatientAlreadyExistsError()

    #     return super().validate(attrs)

    # def create(self, validated_data):

    #     user_data = validated_data.pop('user')
    #     address_data = user_data.pop('address')

    #     if not user_data:
    #         raise UserNotFoundError()
    #     elif not address_data:
    #         raise AddressNotFoundError()

    #     address = Address.objects.create(
    #         post_code=address_data['post_code'],
    #         house_number=address_data['house_number'],
    #         street=address_data['street'],
    #         city=address_data['city'],
    #         state=address_data['state'],
    #     )

    #     user = User.objects.create_user(
    #         email=user_data['email'], 
    #         password=user_data['password'], 
    #         cpf=user_data['cpf'], 
    #         name=user_data['name'], 
    #         surname=user_data['surname'], 
    #         phone=user_data['phone'], 
    #         age=user_data['age'], 
    #         sex=user_data['sex'],
    #         address=address
    #     )
        
    #     new_patient = Patient.objects.create(user=user)

    #     return new_patient


class PatientIdSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Patient
        fields = "__all__"

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.filter(uuid=instance.user.uuid).update(**user_data)
        patient = Patient.objects.filter(cpf=instance.cpf).update(**validated_data)
        # ipdb.set_trace()

        updated_patient = Patient.objects.get(cpf=instance.cpf)

        return updated_patient



    # name = serializers.CharField()
    # password = serializers.CharField(write_only=True)

