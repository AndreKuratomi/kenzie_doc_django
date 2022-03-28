from django.shortcuts import render
from django.core.mail import send_mail
from rest_framework.views import APIView

class EmailView(APIView):
    def send(request):

        send_mail(request['subject'],request["message"], request["sender"], request["receiver"])

        return {"message": "email successfully sent!"}

