from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication

from .models import AppointmentsModel
from .serializers import AppointmentsSerializer, AppointmentsToUpdateSerializer
from .permissions import AppointmentPermission, PatientSelfOrAdminPermissions, ProfessionalSelfOrAdminPermissions

from user.models import Patient, Professional, User

from utils.email_functions import send_appointment_cancel_email, send_appointment_confirmation_email, send_appointment_edition_email, send_appointment_finished_email
from utils.whatsapp_functions import send_appointment_confirmation_whatsapp, send_appointment_edition_whatsapp, send_appointment_cancel_whatsapp
from utils.functions import is_this_data_schedulable
from utils.variables import date_format_regex, date_format, now

from kenziedoc_project.exceptions import PatientNotFoundError, UserNotFoundError, ProfessionalNotFoundError

import math
import re
import ipdb


class CreateAppointment(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [AppointmentPermission]

    def post(self, request):
        try:
            professional = Professional.objects.get(council_number=request.data['council_number'])
        except Professional.DoesNotExist:
            raise ProfessionalNotFoundError()

        try:
            patient = Patient.objects.get(register_number=request.data['patient_register_number'])
        except Patient.DoesNotExist:
            raise PatientNotFoundError()

        try:
            user = User.objects.get(patient=patient)
        except User.DoesNotExist:
            raise UserNotFoundError()

        try:
            data=request.data
            data['professional'] = professional.pk
            data['patient'] = patient.pk

            date = data['date']
            appointment_date_naive = datetime.strptime(date, date_format)
            # Make it timezone-aware (assuming the default timezone)
            appointment_date = timezone.make_aware(appointment_date_naive)

            # Is data['date'] in the right format?:
            if not re.match(date_format_regex, date):
                return Response({"error": "Date not in format 'dd/mm/yyyy - hh:mm'. Check date typed!"}, status=status.HTTP_400_BAD_REQUEST)

            # No appointments in the past...:
            if not is_this_data_schedulable(str(date)):
                return Response({"error": "A appointment cannot be scheduled in the past. Check date typed!"}, status=status.HTTP_400_BAD_REQUEST)

            # Do we already have an appointment for this doctor at this period?:
            date_appointments_for_prof = AppointmentsModel.objects.filter(professional=professional, date=appointment_date).exists()

            if date_appointments_for_prof:
                return Response({"error": "This professional already has an appointment for this period!"}, status=status.HTTP_409_CONFLICT)

            # Is the patient already scheduled for another professional at this period?:
            date_appointments_for_pat = AppointmentsModel.objects.filter(patient=patient, date=appointment_date).exists()
            # ipdb.set_trace()
            if date_appointments_for_pat:
                return Response({"error": "This patient already has an appointment for this period!"}, status=status.HTTP_409_CONFLICT)


            serializer = AppointmentsSerializer(
                data=data
            )
            
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            with transaction.atomic():
                appointment = AppointmentsModel.objects.create(**serializer.validated_data)
                
                send_appointment_confirmation_email(appointment, professional, patient)
                send_appointment_confirmation_whatsapp(appointment, professional, patient)

                serializer = AppointmentsSerializer(appointment)

                return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)


class SpecificPatientView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [PatientSelfOrAdminPermissions]

    def get(self, request, register_number=''):
        try:
            patient = Patient.objects.get(register_number=register_number)
            user = User.objects.get(patient=patient)

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

            if appointment:

                professional = appointment.professional
                patient = appointment.patient

                serialized = AppointmentsToUpdateSerializer(data=request.data, partial=True)

                if serialized.is_valid():
                    data = {**serialized.validated_data}

                    # If 'finished' in data return error:
                    if 'finished' in data:
                        return Response({"error": "Field 'finished' cannot be updated here. Consider 'appointment_finish/' endpoint."}, status=status.HTTP_406_NOT_ACCEPTABLE)

                    if 'date' in data:
                        # Do we already have an appointment for this doctor at this period?:
                        date_appointments_for_prof = AppointmentsModel.objects.filter(professional=professional, date=data['date']).exists()

                        if date_appointments_for_prof:
                            return Response({"error": "This professional already has an appointment for this period!"}, status=status.HTTP_409_CONFLICT)

                        # Is the patient already scheduled for another professional at this period?:
                        date_appointments_for_pat = AppointmentsModel.objects.filter(patient=patient, date=data['date']).exists()
                        # ipdb.set_trace()
                        if date_appointments_for_pat:
                            return Response({"error": "This patient already has an appointment for this period!"}, status=status.HTTP_409_CONFLICT)
                        
                    updated_fields = {}
                    for key, value in data.items():

                        current_value = getattr(appointment, key)

                        if current_value != value:
                            updated_fields[key] = {'before': current_value, 'after': value}
                            setattr(appointment, key, value)
                    
                    with transaction.atomic():

                        appointment.save()

                        updated_appointment = AppointmentsModel.objects.get(uuid=appointment_id)
                        update_serialized = AppointmentsSerializer(updated_appointment)

                        professional = updated_appointment.professional
                        patient = updated_appointment.patient

                        send_appointment_edition_email(appointment, professional, patient, updated_fields)
                        send_appointment_edition_whatsapp(appointment, professional, patient, updated_fields)

                        return Response(update_serialized.data, status=status.HTTP_200_OK)

        except AppointmentsModel.DoesNotExist:
            return Response({'message': 'Appointment does not exist'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, appointment_id=''):
        try:
            appointment = AppointmentsModel.objects.get(uuid=appointment_id)

            if appointment:

                with transaction.atomic():

                    appointment.delete()

                    professional = appointment.professional
                    patient = appointment.patient

                    send_appointment_cancel_email(appointment, professional, patient)
                    send_appointment_cancel_whatsapp(appointment, professional, patient)

                    return Response(status=status.HTTP_204_NO_CONTENT)

        except AppointmentsModel.DoesNotExist:
            return Response({'message': 'Appointment does not exist'}, status=status.HTTP_404_NOT_FOUND)


class ProfessionalAppointmentsTodayView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [AppointmentPermission]

    def get(self, request, council_number=''):
        try:
            professional = Professional.objects.get(council_number=council_number)

            if professional:
                appointments = AppointmentsModel.objects.filter(professional=professional, date__date=now.date())
                # ipdb.set_trace()
                self.check_object_permissions(request, professional)

                # not_finished = []

                # for appointment in appointments:
                #     if appointment.date < now and not appointment.finished and (appointment.date.date() == now.date()):
                #         not_finished.append(appointment)

                # # ipdb.set_trace()
                # average_time = len(not_finished) * 60 # assuming an appointment of ca 1h.

                # hours = math.floor(average_time / 60)
                # minutes = average_time % 6                

                serializer = AppointmentsSerializer(appointments, many=True)

                # not_finished_appointments = AppointmentsModel.objects.filter(finished=False)

                # serializer = AppointmentsSerializer(not_finished_appointments, many=True)

                return Response(
                    serializer.data, 
                    status=status.HTTP_200_OK
                )

        except ObjectDoesNotExist:
            return Response(
                {"message": "Professional not registered"},
                status=status.HTTP_404_NOT_FOUND,
            )


class NotFinishedAppointmentsView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [AppointmentPermission]

    def get(self, request, council_number=''):
        try:
            professional = Professional.objects.get(council_number=council_number)

            if professional:
                appointments = AppointmentsModel.objects.filter(professional=professional)
                self.check_object_permissions(request, professional)

                not_finished = []

                for appointment in appointments:
                    if appointment.date < now and not appointment.finished and (appointment.date.date() == now.date()):
                        not_finished.append(appointment)

                # ipdb.set_trace()
                average_time = len(not_finished) * 60 # assuming an appointment of ca 1h.

                hours = math.floor(average_time / 60)
                minutes = average_time % 6                

                # serializer = AppointmentsSerializer(appointments, many=True)

                # not_finished_appointments = AppointmentsModel.objects.filter(finished=False)

                # serializer = AppointmentsSerializer(not_finished_appointments, many=True)

                return Response(
                    {'msg': f'There are {len(not_finished)} patients waiting for being attended by Dr. {professional.user.name} today. The avegare waiting time is ca {hours} hours and {minutes} minutes'}, 
                    status=status.HTTP_200_OK
                )

        except ObjectDoesNotExist:
            return Response(
                {"message": "Professional not registered"},
                status=status.HTTP_404_NOT_FOUND,
            )


class FinishAppointmentView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [AppointmentPermission]

    def patch(self, request, appointment_id=''):
        try:
            appointment = AppointmentsModel.objects.get(uuid=appointment_id)

            if appointment:
                if appointment.finished == True:
                    return Response({'message': 'This appointment is already finished!'}, status=status.HTTP_400_BAD_REQUEST)

                appointment.finished = True
                appointment.save()

                professional = appointment.professional
                patient = appointment.patient

                send_appointment_finished_email(appointment, professional, patient)
                send_appointment_cancel_whatsapp(appointment, professional, patient)

                return Response(status=status.HTTP_204_NO_CONTENT)

        except AppointmentsModel.DoesNotExist:
            return Response({'message': 'Appointment does not exist'}, status=status.HTTP_404_NOT_FOUND)
