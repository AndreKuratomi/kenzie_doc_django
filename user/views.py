from django.db import IntegrityError
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Patient, Professional
from .serializers import PatientSerializer, PatientToUpdateSerializer, ProfessionalSerializer
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
            
            does_patient_already_exists = Patient.objects.filter(cpf=serializer.validated_data['cpf']).exists()
            if does_patient_already_exists is True:
                return Response({"message": "This patient already exists"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

            new_patient = Patient.objects.create(**serializer.validated_data)

            serialized_new_patient = PatientSerializer(new_patient)

            return Response(serialized_new_patient.data, status=status.HTTP_201_CREATED)

        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        
        all_patients = Patient.objects.all()
        serialized_all_patients = PatientSerializer(all_patients, many=True)

        return Response(serialized_all_patients.data, status=status.HTTP_200_OK)


class PatientByIdView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdmin]

    def get(self, request, user_id=''):
        try:
            valid_uuid = is_valid_uuid(user_id)
            if valid_uuid:
                patient = Patient.objects.filter(uuid=user_id)
                serialized = PatientSerializer(patient)

                return Response(serialized.data, status=status.HTTP_200_OK)

        except Patient.DoesNotExist:
            return Response({"message": "No patient found"}, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response({"message": "No valid UUID"}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, user_id=''):

        serializer = PatientToUpdateSerializer

        try:
            valid_uuid = is_valid_uuid(user_id)
            if valid_uuid:
                patient = Patient.objects.filter(uuid=user_id)
                serialized = PatientSerializer(patient)

                return Response(serialized.data, status=status.HTTP_200_OK)

        except Patient.DoesNotExist:
            return Response({"message": "No patient found"}, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response({"message": "No valid UUID"}, status=status.HTTP_404_NOT_FOUND)

        try:
            to_update = Patient.objects.filter(uuid=user_id).update(**serializer.validated_data)
        except IntegrityError:
            return Response({"message": "This user email already exists"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


        updated = Patient.objects.get(uuid=user_id)

        serialized = Patient(updated)

        return Response(serialized.data, status=status.HTTP_200_OK)

    def delete(self, request, user_id=''):
        try:
            valid_uuid = is_valid_uuid(user_id)
            if valid_uuid:
                patient = Patient.objects.filter(uuid=user_id)
                Patient.delete(patient)

                return Response(status=status.HTTP_204_NO_CONTENT)

        except Patient.DoesNotExist:
            return Response({"message": "No patient found"}, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response({"message": "No valid UUID"}, status=status.HTTP_404_NOT_FOUND)


class ProfessionalsView(APIView):

    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAdmin]

    def post(self, request):

        serializer = ProfessionalSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if Professional.objects.filter(council_number=serializer.validated_data['council_number']).exists() == True:
            return Response({"message": "This professional already exists"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        # professional = Professional.objects.create_user(**serializer.validated_data)
        professional = Professional.objects.create(**serializer.validated_data)

        # users.set([]) ?

        serializer = ProfessionalSerializer(professional)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):

        professionals = Professional.objects.all()

        serialized = ProfessionalSerializer(professionals, many=True)

        return Response(serialized.data, status=status.HTTP_200_OK)

class ProfessionalsByIdView(APIView):

    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAdmin]

    def get(self, request, council_number=''):

        try:
            professional = Professional.objects.get(council_number=council_number)

        except Professional.DoesNotExist:
            return Response(
                {'message': 'Professional does not exist'}, status=status.HTTP_404_NOT_FOUND,
            )

        serializer = ProfessionalSerializer(professional)

        return Response(serializer.data, status=status.HTTP_200_OK)
        

    def patch(self, request, council_number=''):

        try:
            professional = Professional.objects.get(council_number=council_number)

            serialized = ProfessionalSerializer(data=request.data, partial=True)
            serialized.is_valid()
            
            data = {**serialized.validated_data}

            if 'council_number' in data:
                if Professional.objects.filter(council_number=request.data['council_number']).exists() == True:
                    response = {"message": "This council_number already exists"}
                    return Response(response, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

            for key, value in data.items():
                professional.__dict__[key] = value
            
            professional.save()

            professional = Professional.objects.get(uuid=council_number)
            serialized = ProfessionalSerializer(professional)

            return Response(serialized.data)        

        except Professional.DoesNotExist:
            return Response(
                {'message': 'Professional does not exist'}, status=status.HTTP_404_NOT_FOUND,
            )
    

    def delete(self, request, council_number=''):

        try:
            professional = Professional.objects.get(council_number=council_number).delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        except Professional.DoesNotExist:
            return Response({"message": "Professional does not exist"}, status=status.HTTP_404_NOT_FOUND)
