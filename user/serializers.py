from rest_framework import serializers
# from appointments.serializers import AppointmentsSerializer
# import uuid


class AddressSerializer(serializers.Serializer):
    uuid = serializers.UUIDField()
    street = serializers.CharField()
    house_number = serializers.IntegerField()
    state = serializers.CharField()


class ProfessionalSerializer(serializers.Serializer):
    council_number = serializers.CharField()
    specialty = serializers.CharField()


class PatientSerializer(serializers.Serializer):
    cpf = serializers.CharField()
    age = serializers.CharField()
    sex = serializers.CharField()


class UserSerializer(serializers.Serializer):
    uuid = serializers.UUIDField()
    is_prof = serializers.BooleanField()
    is_admin = serializers.BooleanField()
    email = serializers.EmailField()
    username = serializers.CharField()

    address = AddressSerializer(many=True)
    patient = PatientSerializer(many=True)
    professional = ProfessionalSerializer(many=True)

    # address = serializers.ForeignKey()
    # patient = serializers.ForeignKey()
    # professional = serializers.ForeignKey()


# class PatientSerializer(serializers.Serializer):
#     uuid = serializers.UUIDField(read_only=True)

#     cpf = serializers.CharField()
#     name = serializers.CharField()
#     age = serializers.CharField()
#     gender = serializers.CharField()
#     email = serializers.CharField()
#     phone = serializers.CharField()
#     health_insurance = serializers.CharField()
#     # password_hash = serializers.CharField() ?
#     active = serializers.BooleanField()

#     # appointments = AppointmentsSerializer(many=True)


# class PatientToUpdateSerializer(serializers.Serializer):
#     name = serializers.CharField(required=False)
#     age = serializers.CharField(required=False)
#     gender = serializers.CharField(required=False)
#     email = serializers.CharField(required=False)
#     phone = serializers.CharField(required=False)
#     health_insurance = serializers.CharField(required=False)
#     # password_hash = serializers.CharField(required=False) ?
#     active = serializers.BooleanField(required=False) # bom, aqui só o administrator pode, né
