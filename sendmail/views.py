from django.shortcuts import render
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from sendmail.serializers import EmailSerializer

class EmailView(APIView):
    def post(self, request):

        serializer = EmailSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        send_mail(
            request.data['subject'],
            request.data["message"], 
            request.data["sender"], 
            request.data["receiver"]
        )

        return Response({"message": "Email successfully sent"}, status=status.HTTP_200_OK)
    