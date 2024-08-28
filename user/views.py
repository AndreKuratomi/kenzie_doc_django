from django.contrib.auth import authenticate
from django.db import IntegrityError
from datetime import date, datetime, time, timedelta

from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import authenticate

from utils.functions import is_this_user_admin_or_the_user_himself, is_this_user_admin

from .models import Patient, Professional, User, Admin
from .serializers import AdminSerializer, LoginUserSerializer, PatientIdSerializer, PatientSerializer, ProfessionalSerializer
from .permissions import IsAdmin, IsJustLogged, PatientSelfOrAdminPermissions, ProfessionalSelfOrAdminPermissions

import ipdb


class LoginUserView(APIView):
    def post(self, request):
        try:
            serializer = LoginUserSerializer(data=request.data)

            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            user = authenticate(email=serializer.validated_data['email'], password=serializer.validated_data['password'])

            if user is not None:
                token = Token.objects.get_or_create(user=user)[0]
                return Response({'token': token.key})
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        except Exception as e:
            return Response({"error": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)


class PatientsView(APIView):

    authentication_classes = [TokenAuthentication]
    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [IsAdmin]

    def post(self, request):
        try:
            serializer = PatientSerializer(data=request.data)
            data = request.data

            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            if Patient.objects.filter(cpf=serializer.validated_data['cpf']).exists() == True:
                return Response({"message": "This patient already exists"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

            user = User.objects.create_user(data['user']['email'], data['user']['password'])
            patient = Patient.objects.create(
                user=user, 
                name=request.data['name'],
                cpf=request.data['cpf'],
                phone=request.data['phone'],
                age = request.data['age'],
                sex = request.data['sex']
            )

            if user and patient:
                serializer = PatientSerializer(patient)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response("User or patient not created! Verify data.", status=status.HTTP_400_BAD_REQUEST)
        
        except IntegrityError:
            return Response({"message": "This patient already exists"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def get(self, request):
        try:
            patients = Patient.objects.all()
            serialized = PatientSerializer(patients, many=True)

            return Response(serialized.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)


class PatientByIdView(RetrieveUpdateDestroyAPIView):

    authentication_classes = [TokenAuthentication]
    def get_permissions(self):
        if self.request.method == 'DELETE':
            self.permission_classes = [IsAdmin]
        else:
            self.permission_classes = [PatientSelfOrAdminPermissions]

    lookup_url_kwarg = "patient_id"

    def get(self, request, patient_id=''):
        try:
            patient = Patient.objects.get(cpf=patient_id)
            user = User.objects.get(patient=patient)

            serializer = PatientSerializer(patient)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Patient.DoesNotExist:
            return Response(
                {'message': 'Patient does not exist'}, status=status.HTTP_404_NOT_FOUND,
            )        

    def patch(self, request, patient_id=''):
        try:
            patient = Patient.objects.get(cpf=patient_id)
            user = User.objects.get(patient=patient)

            serialized = PatientIdSerializer(data=request.data, partial=True)

            if not serialized.is_valid():
                return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
            
            data = {**serialized.validated_data}

            # CPF update not allowed:
            if 'patient_id' in data:
                if Patient.objects.filter(patient_id=request.data['patient_id']).exists() == True:
                    response = {"message": "This patient_id already exists and it is not updatable!"}
                    return Response(response, status=status.HTTP_422_UNPROCESSABLE_ENTITY)                   
                
            # User data update if provided:
            user_data = request.data.get("user", {})
            if user_data:
                for key, value in user_data.items():
                    setattr(user, key, value)
                user.save()

            # Patient update if provided:
            patient_data = {key: value for key, value in serialized.validated_data.items() if key != 'user'}
            for key, value in patient_data.items():
                setattr(patient, key, value)
            patient.save()

            patient = Patient.objects.get(cpf=patient_id)
            serialized = PatientSerializer(patient)

            return Response(serialized.data, status=status.HTTP_200_OK)        

        except User.DoesNotExist:
            return Response({'message': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

        except Patient.DoesNotExist:
            return Response({'message': 'Patient does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, patient_id=''):
        try:
            patient = Patient.objects.get(cpf=patient_id)
            user = User.objects.get(patient=patient)

            patient.delete()
            user.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except Patient.DoesNotExist:
            return Response({'message': 'Patient does not exist'}, status=status.HTTP_404_NOT_FOUND)


class ProfessionalsView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdmin]

    def post(self, request):
        try:
            serializer = ProfessionalSerializer(data=request.data)
            data = request.data

            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            if Professional.objects.filter(council_number=serializer.validated_data['council_number']).exists() == True:
                return Response({"message": "This professional already exists"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

            user = User.objects.create_user(data['email'], data['password'], is_prof=True)
            professional = Professional.objects.create(
                user=user, 
                council_number=request.data['council_number'], 
                name=request.data['name'],
                phone=request.data['phone'],
                specialty=request.data['specialty'].capitalize()
                )
          
            serializer = ProfessionalSerializer(professional)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except IntegrityError:
            return Response({"message": "This professional already exists"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def get(self, request):
        try:
            professionals = Professional.objects.all()
            serialized = ProfessionalSerializer(professionals, many=True)

            return Response(serialized.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": f"Something went wrong: {e}"})


class ProfessionalsByIdView(APIView):

    authentication_classes = [TokenAuthentication]

    def get_permissions(self):
        if self.request.method == 'DELETE':
            self.permission_classes = [IsAdmin]
        elif self.request.method == 'GET':
            self.permission_classes = [IsJustLogged]
        else:
            self.permission_classes = [ProfessionalSelfOrAdminPermissions]
        
        return super().get_permissions()

    def get(self, request, council_number=''):
        try:
            professional = Professional.objects.get(council_number=council_number)
            serializer = ProfessionalSerializer(professional)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Professional.DoesNotExist:
            return Response(
                {'message': 'Professional does not exist'}, status=status.HTTP_404_NOT_FOUND,
            )        
        

    def patch(self, request, council_number=''):
        try:
            professional = Professional.objects.get(council_number=council_number)
            user = User.objects.get(professional=professional)

            serialized = ProfessionalSerializer(data=request.data, partial=True)
            serialized.is_valid()
            
            data = {**serialized.validated_data}
            
            # Council_number update not allowed:
            if 'council_number' in data:
                if Professional.objects.filter(council_number=request.data['council_number']).exists() == True:
                    response = {"message": "Council_number can't be updated!"}
                    return Response(response, status=status.HTTP_422_UNPROCESSABLE_ENTITY)                   
                
            # User data update if provided:
            user_data = request.data.get("user", {})
            if user_data:
                for key, value in user_data.items():
                    setattr(user, key, value)
                user.save()

            # Professional update if provided:
            professional_data = {key: value for key, value in serialized.validated_data.items() if key != 'user'}
            for key, value in professional_data.items():
                setattr(professional, key, value)
            professional.save()

            professional = Professional.objects.get(council_number=council_number)
            serialized = ProfessionalSerializer(professional)

            return Response(serialized.data, status=status.HTTP_200_OK)        

        except Professional.DoesNotExist:
            return Response({'message': 'Professional does not exist'}, status=status.HTTP_404_NOT_FOUND)
    

    def delete(self, request, council_number=''):
        try:
            professional = Professional.objects.get(council_number=council_number)
            user = User.objects.get(professional=professional)
                
            user.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except Professional.DoesNotExist:
            return Response({"message": "Professional does not exist"}, status=status.HTTP_404_NOT_FOUND)


class ProfessionalsBySpecialtyView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsJustLogged]

    def get(self, request, specialty=''):
        try:
            professionals_by_specialty = Professional.objects.filter(specialty=specialty.capitalize())
            serialized = ProfessionalSerializer(professionals_by_specialty, many=True)

            return Response(serialized.data, status=status.HTTP_200_OK)

        except Professional.DoesNotExist:
            return Response(
                {'message': 'No professionals for this specialty!'}, status=status.HTTP_404_NOT_FOUND,
            )        


class AdminView(APIView):

    def post(self, request):
        try:
            serializer = AdminSerializer(data=request.data)
            data = request.data

            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.create_user(data['email'], data['password'], is_admin=True)
            admin = Admin.objects.create(user=user, name=request.data['name'])
            serializer = AdminSerializer(admin)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except IntegrityError:
            return Response({"message": "This admin already exists"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def get(self, request):
        try:
            admin = Admin.objects.all()
            serialized = AdminSerializer(admin, many=True)

            return Response(serialized.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": f"Something went wrong: {e}"})
