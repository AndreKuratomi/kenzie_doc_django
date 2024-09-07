from django.core.mail import send_mail
from django.conf import settings

from user.models import Patient, Professional
from appointments.models import AppointmentsModel


def send_appointment_confirmation_email(appointment: AppointmentsModel, professional: Professional, patient: Patient) -> None:
    subject = "Appointment Confirmation"
    message = (
        f"Dear {patient.user.name},\n\n"
        f"Your appointment with Dr. {professional.name} has been scheduled for {appointment.date}.\n\n"
        "Best regards,\n"
        "KenzieDoc"
    )
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [patient.user.email, professional.email]
    )


def send_appointment_edition_email(appointment: AppointmentsModel, professional: Professional, patient: Patient) -> None:
    subject = "Appointment Confirmation"
    message = (
        f"Dear {patient.user.name},\n\n"
        f"Your appointment data with Dr. {professional.name} has been updated in (date_modified). The updates were:\n\n"
        f"{appointment.date},\n\n"
        f"{appointment.complaint},\n\n"
        "Best regards,\n"
        "KenzieDoc"
    )
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [patient.user.email, professional.email]
    )


def send_appointment_cancel_email(appointment: AppointmentsModel, professional: Professional, patient: Patient) -> None:
    subject = "Appointment Confirmation"
    message = (
        f"Dear {patient.user.name},\n\n"
        f"Your appointment with Dr. {professional.name} has been canceled in ().\n\n"
        f"Contact support to re-schedule.\n\n"
        "Best regards,\n"
        "KenzieDoc"
    )
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [patient.user.email, professional.email]
    )
