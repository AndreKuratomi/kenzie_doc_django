from email.headerregistry import Address
from rest_framework import serializers


class AddressSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    street = serializers.CharField()
    house_number = serializers.IntegerField()
    state = serializers.CharField()


class ProfessionalSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    username = serializers.CharField()
    council_number = serializers.CharField(read_only=True)
    specialty = serializers.CharField()
    address = AddressSerializer(many=True, read_only=True)
