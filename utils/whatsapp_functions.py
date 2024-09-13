import pywhatkit as wpp

from user.models import Patient, Professional
from appointments.models import AppointmentsModel

from utils.functions import appointment_date_convertion
from utils.variables import now

import ipdb


now_converted = appointment_date_convertion(now)


def send_appointment_confirmation_whatsapp(appointment: AppointmentsModel, professional: Professional, patient: Patient) -> None:
    date = appointment_date_convertion(appointment.date)
    
    message = (
        f"Dear {patient.user.name},\n\n"
        f"Your appointment with Dr. {professional.user.name} has been scheduled for {date}.\n\n"
        "Best regards,\n"
        "KenzieDoc"
    )

    # Assuming you have the phone numbers in international format
    professional_phone = professional.user.phone
    patient_phone = patient.user.phone

    # Send message to both professional and patient
    wpp.sendwhatmsg_instantly(phone_no=patient_phone, message=message, wait_time=10)
    wpp.sendwhatmsg_instantly(phone_no=professional_phone, message=message, wait_time=10)


def send_appointment_edition_whatsapp(appointment: AppointmentsModel, professional: Professional, patient: Patient, data: dict) -> None:

    # Discriminating what was updated:
    updates = ""
    for field, values in data.items():
        if field == "date":
            # ipdb.set_trace()
            before = appointment_date_convertion(values['before'])
            after = appointment_date_convertion(values['after'])
        else:
            before = values['before']
            after = values['after']
        updates += f"- {field.replace('_', ' ').capitalize()}: from '{before}' to '{after}'\n"

    message = (
        f"Dear {patient.user.name},\n\n"
        f"Your appointment data with Dr. {professional.user.name} has been updated in {now_converted}. The updates were:\n\n"
        f"{updates},\n\n"
        "Best regards,\n"
        "KenzieDoc"
    )

    # Assuming you have the phone numbers in international format
    professional_phone = professional.user.phone
    patient_phone = patient.user.phone

    # Send message to both professional and patient
    wpp.sendwhatmsg_instantly(phone_no=patient_phone, message=message, wait_time=10)
    wpp.sendwhatmsg_instantly(phone_no=professional_phone, message=message, wait_time=10)


def send_appointment_finished_whatsapp(appointment: AppointmentsModel, professional: Professional, patient: Patient) -> None:
    # Define message content
    message = (
        f"Dear {patient.user.name},\n\n"
        f"Your appointment with Dr. {professional.user.name} was finished in {now_converted}.\n\n"
        
        "Best regards,\n"

        "KenzieDoc"
    )

    # Assuming you have the phone numbers in international format
    professional_phone = professional.user.phone
    patient_phone = patient.user.phone

    # Send message to both professional and patient
    wpp.sendwhatmsg_instantly(phone_no=patient_phone, message=message, wait_time=10)
    wpp.sendwhatmsg_instantly(phone_no=professional_phone, message=message, wait_time=10)


def send_appointment_cancel_whatsapp(appointment: AppointmentsModel, professional: Professional, patient: Patient) -> None:
    # Define message content
    message = (
        f"Dear {patient.user.name},\n\n"
        f"Your appointment with Dr. {professional.user.name} was canceled in {now_converted}.\n\n"
        f"Contact support to re-schedule.\n\n"
        "Best regards,\n"
        "KenzieDoc"
    )

    # Assuming you have the phone numbers in international format
    professional_phone = professional.user.phone
    patient_phone = patient.user.phone

    # Send message to both professional and patient
    wpp.sendwhatmsg_instantly(phone_no=patient_phone, message=message, wait_time=10)
    wpp.sendwhatmsg_instantly(phone_no=professional_phone, message=message, wait_time=10)
