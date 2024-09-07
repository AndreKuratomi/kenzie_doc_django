from .variables import brazilian_time_parsed, date_format

from datetime import datetime

def is_this_data_schedulable(date: str) -> bool:
    parsed_date = datetime.strptime(date, date_format)

    return parsed_date > brazilian_time_parsed