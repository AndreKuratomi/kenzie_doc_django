import random
import string

from datetime import datetime
from django.utils import timezone

from .variables import brazilian_timezone, brazilian_time_parsed, date_format

import ipdb


def is_this_data_schedulable(date: str) -> bool:
    """Function to avoid past dates for appointments."""

    parsed_date = datetime.strptime(date, date_format)

    return parsed_date > brazilian_time_parsed


def generate_register_number() -> str:
    """Public Id for patients after registration in substitution to CPF."""

    first_part = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    second_part = random.choice(string.ascii_letters + string.digits)
    register_number = f'{first_part}-{second_part}'

    return register_number


def appointment_date_convertion(date: datetime) -> datetime:
    """Converts appointment date to brazilian format '%d/%m/%Y - %H:%M' and timezone."""

    date_converted = date.astimezone(brazilian_timezone)
    appointment_date = date_converted.strftime(date_format)

    return appointment_date
