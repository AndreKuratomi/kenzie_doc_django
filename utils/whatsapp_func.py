import pywhatkit as wpp

from user.models import Patient, Professional
from appointments.models import AppointmentsModel


def send_appointment_confirmation_whatsapp(appointment: AppointmentsModel, professional: Professional, patient: Patient) -> None:
    # Define message content
    message = (
        f"Dear {patient.user.name},\n\n"
        f"Your appointment with Dr. {professional.name} has been scheduled for {appointment.date}.\n\n"
        "Best regards,\n"
        "Your Health Service"
    )

    # Assuming you have the phone numbers in international format
    professional_phone = professional.phone_number
    patient_phone = patient.user.phone_number

    # Send message to both professional and patient
    wpp.sendwhatmsg_instantly(phone_no=patient_phone, message=message, wait_time=10)
    wpp.sendwhatmsg_instantly(phone_no=professional_phone, message=message, wait_time=10)


def send_appointment_edition_whatsapp(appointment: AppointmentsModel, professional: Professional, patient: Patient) -> None:
    # Define message content
    message = (
        f"Dear {patient.user.name},\n\n"
        f"Your appointment with Dr. {professional.name} has been scheduled for {appointment.date}.\n\n"
        "Best regards,\n"
        "Your Health Service"
    )

    # Assuming you have the phone numbers in international format
    professional_phone = professional.phone_number
    patient_phone = patient.user.phone_number

    # Send message to both professional and patient
    wpp.sendwhatmsg_instantly(phone_no=patient_phone, message=message, wait_time=10)
    wpp.sendwhatmsg_instantly(phone_no=professional_phone, message=message, wait_time=10)


def send_appointment_cancel_whatsapp(appointment: AppointmentsModel, professional: Professional, patient: Patient) -> None:
    # Define message content
    message = (
        f"Dear {patient.user.name},\n\n"
        f"Your appointment with Dr. {professional.name} has been scheduled for {appointment.date}.\n\n"
        "Best regards,\n"
        "Your Health Service"
    )

    # Assuming you have the phone numbers in international format
    professional_phone = professional.phone_number
    patient_phone = patient.user.phone_number

    # Send message to both professional and patient
    wpp.sendwhatmsg_instantly(phone_no=patient_phone, message=message, wait_time=10)
    wpp.sendwhatmsg_instantly(phone_no=professional_phone, message=message, wait_time=10)
