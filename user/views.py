from django.db import IntegrityError
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import PatientUser
from .serializers import PatientSerializer, PatientToUpdateSerializer
from .permissions import IsAdmin

from .services import is_valid_uuid


class PatientsView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdmin]

    def post(self, request):
        try:
            serializer = PatientSerializer(data=request.data)

            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            does_patient_already_exists = PatientUser.objects.filter(cpf=serializer.validated_data['cpf']).exists()
            if does_patient_already_exists is True:
                return Response({"message": "This patient already exists"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

            new_patient = PatientUser.objects.create(**serializer.validated_data)

            serialized_new_patient = PatientSerializer(new_patient)

            return Response(serialized_new_patient.data, status=status.HTTP_201_CREATED)

        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        
        all_patients = Patients.objects.all()
        serialized_all_patients = PatientSerializer(all_patients, many=True)

        return Response(serialized_all_patients.data, status=status.HTTP_200_OK)


class PatientByIdView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdmin]

    def get(self, request, user_id=''):
        try:
            valid_uuid = is_valid_uuid(user_id)
            if valid_uuid:
                patient = PatientUser.objects.filter(uuid=user_id)
                serialized = PatientSerializer(patient)

                return Response(serialized.data, status=status.HTTP_200_OK)

        except PatientUser.DoesNotExist:
            return Response({"message": "No patient found"}, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response({"message": "No valid UUID"}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, user_id=''):

        serializer = PatientToUpdateSerializer

        try:
            valid_uuid = is_valid_uuid(user_id)
            if valid_uuid:
                patient = PatientUser.objects.filter(uuid=user_id)
                serialized = PatientSerializer(patient)

                return Response(serialized.data, status=status.HTTP_200_OK)

        except PatientUser.DoesNotExist:
            return Response({"message": "No patient found"}, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response({"message": "No valid UUID"}, status=status.HTTP_404_NOT_FOUND)

        try:
            to_update = PatientUser.objects.filter(uuid=user_id).update(**serializer.validated_data)
        except IntegrityError:
            return Response({"message": "This user email already exists"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


        updated = PatientUser.objects.get(uuid=user_id)

        serialized = PatientUser(updated)

        return Response(serialized.data, status=status.HTTP_200_OK)

    def delete(self, request, user_id=''):
        try:
            valid_uuid = is_valid_uuid(user_id)
            if valid_uuid:
                patient = PatientUser.objects.filter(uuid=user_id)
                PatientUser.delete(patient)

                return Response(status=status.HTTP_204_NO_CONTENT)

        except PatientUser.DoesNotExist:
            return Response({"message": "No patient found"}, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response({"message": "No valid UUID"}, status=status.HTTP_404_NOT_FOUND)
