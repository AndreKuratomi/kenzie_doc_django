from email.headerregistry import Address
from rest_framework import serializers


class AddressSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    street = serializers.CharField()
    house_number = serializers.IntegerField()
    state = serializers.CharField()


class ProfessionalSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    # username = serializers.CharField()
    # keila editing
    name = serializers.CharField()
    email = serializers.CharField()
     # keila editing
    council_number = serializers.CharField()
    specialty = serializers.CharField()
    address = AddressSerializer(many=True, read_only=True)
