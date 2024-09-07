from datetime import datetime
import pytz

brazilian_timezone = pytz.timezone('America/Sao_Paulo')

date_format = '%d/%m/%Y - %H:%M'

brazilian_time = datetime.now(brazilian_timezone).strftime(date_format)

brazilian_time_parsed = datetime.strptime(brazilian_time, date_format)

date_format_regex = r'^\d{2}/\d{2}/\d{4} - \d{2}:\d{2}$'

