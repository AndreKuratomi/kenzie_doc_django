from django.contrib.auth import authenticate
from django.db import IntegrityError, transaction
from datetime import date, datetime, time, timedelta

from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import authenticate

from .models import Address, Patient, Professional, User, Admin
from .serializers import AdminSerializer, LoginUserSerializer, PatientIdSerializer, PatientSerializer, ProfessionalSerializer, UserSerializer
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
                return Response({"Login error": "Please check login data."}, status=status.HTTP_401_UNAUTHORIZED)
        
        except Exception as e:
            return Response({"error": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)


class PatientsView(APIView):

    authentication_classes = [TokenAuthentication]
    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [IsAdmin]

        return super().get_permissions()

    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data.get('user', {}))

            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            data = serializer.validated_data

            if User.objects.filter(cpf=data['cpf']).exists():
                return Response({"message": "This user already exists!"}, status=status.HTTP_409_CONFLICT)

            with transaction.atomic():
                address_data = data.get('address', {})
                address = Address.objects.create(
                    post_code=address_data['post_code'],
                    house_number=address_data['house_number'],
                    street=address_data.get('street', ''),
                    city=address_data.get('city', ''),
                    state=address_data.get('state', '')
                )

                user = User.objects.create_user(
                    email=data['email'], 
                    password=data['password'],
                    name=data['name'],
                    surname=data['surname'],
                    cpf=data['cpf'],
                    phone=data['phone'],
                    age=data['age'],
                    sex=data['sex'],
                    address=address,
                )

                if user:

                    patient = Patient.objects.create(
                        user=user, 
                    )

                    if patient:

                        serializer = PatientSerializer(patient)

                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                    
                    else:
                        return Response("Patient not created! Verify data.", status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response("User not created! Verify data.", status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({f"message": {e}}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

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
        
        return super().get_permissions()

    lookup_url_kwarg = "patient_id"

    def get(self, request, patient_id=''):
        try:
            patient = Patient.objects.get(cpf=patient_id)
            
            # grant has_object_permission is going to be read because patient was manually called:            
            self.check_object_permissions(request, patient)

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
            # grant has_object_permission is going to be read because patient was manually called:
            self.check_object_permissions(request, patient)

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

            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            data = serializer.validated_data
            user_data = data['user']

            if User.objects.filter(cpf=user_data['cpf']).exists():
                return Response({"message": "This user already exists!"}, status=status.HTTP_409_CONFLICT)

            with transaction.atomic():
                address_data = user_data.get('address', {})
                address = Address.objects.create(
                    post_code=address_data['post_code'],
                    house_number=address_data['house_number'],
                    street=address_data.get('street', ''),
                    city=address_data.get('city', ''),
                    state=address_data.get('state', '')
                )

                user = User.objects.create_user(
                    email=user_data['email'], 
                    password=user_data['password'],
                    name=user_data['name'],
                    surname=user_data['surname'],
                    cpf=user_data['cpf'],
                    phone=user_data['phone'],
                    age=user_data['age'],
                    sex=user_data['sex'],
                    address=address,
                    is_prof=True
                )

                if user:
                    # ipdb.set_trace()
                    if Professional.objects.filter(council_number=data['council_number']).exists():
                        return Response({"message": "This professional already exists!"}, status=status.HTTP_409_CONFLICT)

                    professional = Professional.objects.create(
                        user=user, 
                        council_number=data['council_number'], 
                        specialty=data['specialty'].capitalize()
                    )
                
                    serializer = ProfessionalSerializer(professional)

                    return Response(serializer.data, status=status.HTTP_201_CREATED)

                else:
                    return Response("User not created! Verify data.", status=status.HTTP_400_BAD_REQUEST)
                
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

    authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAdmin]

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [IsAdmin]
        
        return super().get_permissions()


    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data.get('user', {}))

            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            data = serializer.validated_data

            if User.objects.filter(cpf=data['cpf']).exists():
                return Response({"message": "This user already exists!"}, status=status.HTTP_409_CONFLICT)

            with transaction.atomic():
                address_data = data.get('address', {})

                address = Address.objects.create(
                    post_code=address_data['post_code'],
                    house_number=address_data['house_number'],
                    street=address_data.get('street', ''),
                    city=address_data.get('city', ''),
                    state=address_data.get('state', '')
                )
                user = User.objects.create_user(
                    email=data['email'], 
                    password=data['password'],
                    name=data['name'],
                    surname=data['surname'],
                    cpf=data['cpf'],
                    phone=data['phone'],
                    age=data['age'],
                    sex=data['sex'],
                    address=address,
                    is_admin=True
                )

                if user:

                    admin = Admin.objects.create(
                        user=user, 
                    )

                    if admin:

                        serializer = AdminSerializer(admin)

                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                    
                    else:
                        return Response("Admin not created! Verify data.", status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response("User not created! Verify data.", status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({f"error": {e}}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


    def get(self, request):
        try:
            admins = Admin.objects.all()
            serialized = AdminSerializer(admins, many=True)

            return Response(serialized.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": f"Something went wrong: {e}"})
