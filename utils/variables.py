from datetime import datetime
from django.utils import timezone

import pytz


date_format = '%d/%m/%Y - %H:%M'

brazilian_timezone = pytz.timezone('America/Sao_Paulo')
brazilian_time = datetime.now(brazilian_timezone).strftime(date_format)
brazilian_time_parsed = datetime.strptime(brazilian_time, date_format)

date_format_regex = r'^\d{2}/\d{2}/\d{4} - \d{2}:\d{2}$'

now = timezone.now()

