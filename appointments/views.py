from datetime import datetime
from urllib import response
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import authentication_classes, permission_classes
from .models import AppointmentsModel
from .serializers import AllAppointmentsSerializer, AppPatientSerializer, AppProfessonalSerializer, AppointmentsSerializer
from .permissions import AppointmentPermission
from user.models import Patient, Professional, User
from user.serializers import PatientSerializer, ProfessionalSerializer, NewPatientSerializer

import ipdb


class SpecificPatientView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [AppointmentPermission]

    def get(self, request, cpf):
        try:
            patient = Patient.objects.get(cpf=cpf)

            appointment = AppointmentsModel.objects.filter(patient=patient)

            for appointments in appointment:
                serializer = AppointmentsSerializer(appointments)

            return response(serializer.data, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return response(
                {"message": "Patient does not exist"}, status=status.HTTP_404_NOT_FOUND
            )


class SpecificProfessionalView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [AppointmentPermission]

    def get(self, request, council_number):
        try:
            professional = Professional.objects.get(council_number=council_number)

            appointment = AppointmentsModel.objects.filter(professional=professional)

            for appointments in appointment:
                serializer = AppointmentsSerializer(appointments)

            return response(serializer.data, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return response(
                {"message": "Professional not registered"},
                status=status.HTTP_404_NOT_FOUND,
            )


class NotFinishedAppointmentView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [AppointmentPermission]

    def get(self, request):
        try:

            not_finished_appointment = AppointmentsModel.objects.filter(finished=False)

            for unfinished in not_finished_appointment:
                serializer = AppointmentsSerializer(unfinished)

            return response(serializer.data, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return response(
                {"message": "Professional not registered"},
                status=status.HTTP_404_NOT_FOUND,
            )


class CreateAppointment(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [AppointmentPermission]

    def post(self, request):

        professional = Professional.objects.get(council_number=request.data['council_number'])
        
        patient = Patient.objects.get(cpf=request.data['cpf']) 

        data=request.data

        prof = ProfessionalSerializer(professional)
        pat = NewPatientSerializer(patient)

        data['professional'] = prof.data["council_number"]
        data['patient'] = pat.data["cpf"]

        serializer = AppointmentsSerializer(
            data=data
        )
        
        print(serializer.validated_data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.validated_data['professional'] = professional
        serializer.validated_data['patient'] = patient
        appointment = AppointmentsModel.objects.create(**serializer.validated_data)
        serializer = AppointmentsSerializer(appointment)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

        # except Professional.ObjectDoesNotExist:
        #     return Response(
        #         {"message": "Professional not registered"},
        #         status=status.HTTP_404_NOT_FOUND,
        #     )

        except Patient.DoesNotExist:
            return Response(
                {"message": "Patient not registered"}, status=status.HTTP_404_NOT_FOUND
            )
