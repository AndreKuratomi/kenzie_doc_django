from typing import List
from django.core.mail import send_mail
from django.conf import settings

from user.models import Patient, Professional
from appointments.models import AppointmentsModel

from utils.functions import appointment_date_convertion
from utils.variables import now


import ipdb

now_converted = appointment_date_convertion(now)


def send_appointment_confirmation_email(appointment: AppointmentsModel, professional: Professional, patient: Patient) -> None:
    
    date = appointment_date_convertion(appointment.date)

    subject = "Appointment confirmation"

    message = (
        f"Dear {patient.user.name},\n\n"
        f"Your appointment with Dr. {professional.user.name} has been scheduled for {date}.\n\n"
        "Best regards,\n"
        "KenzieDoc"
    )

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [patient.user.email, professional.user.email]
    )


def send_appointment_edition_email(appointment: AppointmentsModel, professional: Professional, patient: Patient, data: dict) -> None:

    # Discriminating what was updated:
    updates = ""
    for field, values in data.items():
        if field == "date":
            before = appointment_date_convertion(values['before'])
            after = appointment_date_convertion(values['after'])
        else:
            before = values['before']
            after = values['after']
        updates += f"- {field.replace('_', ' ').capitalize()}: from '{before}' to '{after}'\n"

    subject = "Appointment edition"

    message = (
        f"Dear {patient.user.name},\n\n"
        f"Your appointment data with Dr. {professional.user.name} has been updated in {now_converted}. The updates were:\n\n"
        f"{updates},\n\n"
        "Best regards,\n"
        "KenzieDoc"
    )

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [patient.user.email, professional.user.email]
    )


def send_appointment_finished_email(appointment: AppointmentsModel, professional: Professional, patient: Patient) -> None:

    subject = "Appointment edition"

    message = (
        f"Dear {patient.user.name},\n\n"
        f"Your appointment with Dr. {professional.user.name} was finished in {now_converted}.\n\n"
        
        "Best regards,\n"

        "KenzieDoc"
    )

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [patient.user.email, professional.user.email]
    )


def send_appointment_cancel_email(appointment: AppointmentsModel, professional: Professional, patient: Patient) -> None:
    
    subject = "Appointment cancellation"
    
    message = (
        f"Dear {patient.user.name},\n\n"
        f"Your appointment with Dr. {professional.user.name} has been canceled in {now_converted}.\n\n"
        f"Contact support to re-schedule.\n\n"
        "Best regards,\n"
        "KenzieDoc"
    )
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [patient.user.email, professional.user.email]
    )
