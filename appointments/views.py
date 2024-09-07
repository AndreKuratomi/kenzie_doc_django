from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import authentication_classes, permission_classes

from .models import AppointmentsModel
from .serializers import AllAppointmentsSerializer, AppPatientSerializer, AppProfessonalSerializer, AppointmentsSerializer, AppointmentsToUpdateSerializer
from .permissions import AppointmentPermission, PatientSelfOrAdminPermissions, ProfessionalSelfOrAdminPermissions

from user.models import Patient, Professional, User
from user.serializers import PatientSerializer, ProfessionalSerializer, UserSerializer
from user.views import ProfessionalsByIdView

from kenziedoc_project.exceptions import PatientNotFoundError, UserNotFoundError, ProfessionalNotFoundError

import ipdb


class SpecificPatientView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [PatientSelfOrAdminPermissions]

    def get(self, request, cpf=''):
        try:
            user = User.objects.get(cpf=cpf)
            patient = Patient.objects.get(user=user)

            if patient:
                appointments = AppointmentsModel.objects.filter(patient=patient)
                self.check_object_permissions(request, patient)

                serializer = AppointmentsSerializer(appointments, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

        except Patient.DoesNotExist:
            return Response(
                {"message": "Patient does not exist"}, status=status.HTTP_404_NOT_FOUND
            )


class SpecificProfessionalView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [ProfessionalSelfOrAdminPermissions]

    def get(self, request, council_number=''):
        try:
            professional = Professional.objects.get(council_number=council_number)

            if professional:
                appointments = AppointmentsModel.objects.filter(professional=professional)
                self.check_object_permissions(request, professional)

                serializer = AppointmentsSerializer(appointments, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

        except Professional.DoesNotExist:
            return Response(
                {"message": "Professional not registered"}, status=status.HTTP_404_NOT_FOUND,
            )


class SpecificAppointmentView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [AppointmentPermission]

    def get(self, request, appointment_id=''):
        try:
            appointment = AppointmentsModel.objects.get(uuid=appointment_id)

            if appointment:

                serializer = AppointmentsSerializer(appointment)

                return Response(serializer.data, status=status.HTTP_200_OK)

        except AppointmentsModel.DoesNotExist:
            return Response(
                {"message": "Appointment not registered"}, status=status.HTTP_404_NOT_FOUND,
            )

    def patch(self, request, appointment_id=''):
        try:
            appointment = AppointmentsModel.objects.get(uuid=appointment_id)
            # user = User.objects.get(professional=professional)
            if appointment:
                serialized = AppointmentsToUpdateSerializer(data=request.data, partial=True)

                if serialized.is_valid():
                    data = {**serialized.validated_data}

                    for key, value in data.items():
                        appointment.__dict__[key] = value

                    appointment.save()

                    updated_appointment = AppointmentsModel.objects.get(uuid=appointment_id)
                    serialized = AppointmentsSerializer(updated_appointment)

                    return Response(serialized.data, status=status.HTTP_200_OK)

        except AppointmentsModel.DoesNotExist:
            return Response({'message': 'Appointment does not exist'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, appointment_id=''):
        try:
            appointment = AppointmentsModel.objects.get(uuid=appointment_id)

            if appointment:

                appointment.delete()

                return Response(status=status.HTTP_204_NO_CONTENT)

        except AppointmentsModel.DoesNotExist:
            return Response({'message': 'Appointment does not exist'}, status=status.HTTP_404_NOT_FOUND)


class NotFinishedAppointmentView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [AppointmentPermission]

    def get(self, request):
        try:

            not_finished_appointment = AppointmentsModel.objects.filter(finished=False)

            for unfinished in not_finished_appointment:
                serializer = AppointmentsSerializer(unfinished)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response(
                {"message": "Professional not registered"},
                status=status.HTTP_404_NOT_FOUND,
            )


class CreateAppointment(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [AppointmentPermission]

    def post(self, request):
        try:
            professional = Professional.objects.get(council_number=request.data['council_number'])
        except Professional.DoesNotExist:
            raise ProfessionalNotFoundError()

        try:
            user = User.objects.get(cpf=request.data['cpf']) 
        except User.DoesNotExist:
            raise UserNotFoundError()
        
        try:
            patient = Patient.objects.get(user=user)
        except Patient.DoesNotExist:
            raise PatientNotFoundError()

        try:
            data=request.data
            data['professional'] = professional.pk
            data['patient'] = patient.pk

            serializer = AppointmentsSerializer(
                data=data
            )
            
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            appointment = AppointmentsModel.objects.create(**serializer.validated_data)
            serializer = AppointmentsSerializer(appointment)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)
