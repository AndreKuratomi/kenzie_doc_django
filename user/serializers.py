from email.headerregistry import Address
from rest_framework import serializers
# import uuid


class UserSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    is_prof = serializers.BooleanField()
    is_admin = serializers.BooleanField()
    email = serializers.EmailField()
    username = serializers.CharField()


class AddressSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    street = serializers.CharField()
    house_number = serializers.IntegerField()
    state = serializers.CharField()

    users = UserSerializer(many=True)


class ProfessionalSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    # comentei o username
    # username = serializers.CharField()

    # pegar outros campos -> (is_prof, is_admin, email, username)?
    # name = serializers.CharField()
    # email = serializers.CharField()...
    council_number = serializers.CharField()
    specialty = serializers.CharField()
    address = AddressSerializer(many=True, read_only=True)

    users = UserSerializer(many=True)


class PatientSerializer(serializers.Serializer):
    cpf = serializers.CharField()
    age = serializers.CharField()
    sex = serializers.CharField()

    users = UserSerializer(many=True)


class PatientToUpdateSerializer(serializers.Serializer):
    cpf = serializers.CharField(required=False)
    age = serializers.CharField(required=False)
    sex = serializers.CharField(required=False)

    users = UserSerializer(many=True)

class AdminSerializer(serializers.Serializer):
    name = serializers.CharField()
    password = serializers.CharField(write_only=True)