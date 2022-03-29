from django.contrib.auth import authenticate
from django.db import IntegrityError
from datetime import date, datetime, time, timedelta

from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import authenticate

from .models import Patient, Professional, User, Admin
from .serializers import AdminSerializer, LoginUserSerializer, PatientIdSerializer, PatientSerializer, ProfessionalSerializer
from .permissions import IsAdmin, ProfessionalsPermissions

# import ipdb
import pywhatkit


class LoginUserView(APIView):
    def post(self, request):
        serializer = LoginUserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(email=serializer.validated_data['email'], password=serializer.validated_data['password'])

        if user is not None:
            token = Token.objects.get_or_create(user=user)[0]
            return Response({'token': token.key})
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)



class PatientsView(ListCreateAPIView):

    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdmin]


class PatientByIdView(RetrieveUpdateDestroyAPIView):

    queryset = Patient.objects.all()
    serializer_class = PatientIdSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdmin]

    lookup_url_kwarg = "patient_id"


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
                specialty=request.data['specialty']
                )

            # whats_msg = "Professional criado com sucesso"

            # time_to_send = datetime.now() + timedelta(minutes=1)

            # pywhatkit.sendwhatmsg("+5519997416761", whats_msg, time_to_send.hour,time_to_send.minute)
            # pywhatkit.sendwhatmsg_instantly("+5519997416761", whats_msg)

            serializer = ProfessionalSerializer(professional)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({"message": "This professional already exists"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def get(self, request):

        professionals = Professional.objects.all()

        serialized = ProfessionalSerializer(professionals, many=True)

        return Response(serialized.data, status=status.HTTP_200_OK)

class ProfessionalsByIdView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [ProfessionalsPermissions]

    def get(self, request, council_number=''):

        try:
            professional = Professional.objects.get(council_number=council_number)
            user = User.objects.get(professional=professional)

            if request.user.is_admin == False:
                if user != request.user:
                    return Response(
                        {
                            "detail": "You do not have permission to perform this action."
                        },  
                        status=status.HTTP_401_UNAUTHORIZED
                    )

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

            if request.user.is_admin == False:
                if user != request.user:
                    return Response(
                        {
                            "detail": "You do not have permission to perform this action."
                        },  
                        status=status.HTTP_401_UNAUTHORIZED
                    )

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

            professional = Professional.objects.get(council_number=council_number)
            serialized = ProfessionalSerializer(professional)

            return Response(serialized.data)        

        except Professional.DoesNotExist:
            return Response({'message': 'Professional does not exist'}, status=status.HTTP_404_NOT_FOUND)
    

    def delete(self, request, council_number=''):

        try:
            professional = Professional.objects.get(council_number=council_number)
            user = User.objects.get(professional=professional)

            if request.user.is_admin == False:
                if user != request.user:
                    return Response(
                        {
                            "detail": "You do not have permission to perform this action."
                        },  
                        status=status.HTTP_401_UNAUTHORIZED
                    )
                
            professional.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        except Professional.DoesNotExist:
            return Response({"message": "Professional does not exist"}, status=status.HTTP_404_NOT_FOUND)


class AdminView(APIView):

    def post(self, request):
        try:
            serializer = AdminSerializer(data=request.data)
            data = request.data

            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.create_user(data['email'], data['password'], is_admin=True)

            admin = Admin.objects.create(user=user, name=request.data['name'])

            # fazer try/except KeyError

            serializer = AdminSerializer(admin)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({"message": "This admin already exists"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def get(self, request):

        admin = Admin.objects.all()

        serialized = AdminSerializer(admin, many=True)

        return Response(serialized.data, status=status.HTTP_200_OK)
