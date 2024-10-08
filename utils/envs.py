import os
import ipdb

from dotenv import load_dotenv

load_dotenv()

django_secret = os.getenv("DJANGO_SECRET_KEY").replace('*', '=')

# Keys for login:
user_email = os.getenv("EMAIL_HOST_USER")
password = os.getenv("EMAIL_HOST_PASSWORD")
# nfe_email = os.getenv("EMAIL_NFE")
