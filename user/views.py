from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Professional
from .serializers import ProfessionalSerializer

# Create your views here.

class ProfessionalsView(APIView): 

  # authentication_classes = [TokenAuthentication]
  # permission_classes = [IsAdmin]

  # def post(self, request):

    # serializer = ProfessionalSerializer(data=request.data)
    
    # print("=====Professional=======")
    # print(Professional.objects.all())
    # # print(request.data.email)

    # print("============")
    # print(serializer.is_valid())
    # print(serializer)

    # if not serializer.is_valid():
    #   return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # if Professional.objects.filter(email=request.data['email']).exists() == True:
    #   response = {"message": "Professional already exists"}
    #   return Response(response, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    # try:
    #   professional = Professional.objects.create_user(
    #     name = request.data['first_name'],
    #     is_prof = request.data['is_prof'],
    #     email = request.data['email'],
    #     password = request.data['password'],
    #     council_number = request.data['council_number'],
    #     specialty = request.data['specialty'] 
    #     # address:?
    #   )
    # except KeyError:
    #   # return Response("instructor_id is a required field.", status=status.HTTP_400_BAD_REQUEST)
    #   return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    # serializer = ProfessionalSerializer(professional)

    # return Response(serializer.data, status=status.HTTP_201_CREATED)

  def post(self, request):
    try:
      serializer = ProfessionalSerializer(data=request.data)

      print("============")
      print(serializer.is_valid())
      print(serializer)

      if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      
      if Professional.objects.filter(council_number=serializer.validated_data['council_number']).exists() == True:
        return Response({"message": "This professional already exists"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

      new_professional = Professional.objects.create(**serializer.validated_data)

      serialized_new_professional = ProfessionalSerializer(new_professional)

      return Response(serialized_new_professional.data, status=status.HTTP_201_CREATED)

    except:
      return Response(status=status.HTTP_400_BAD_REQUEST)



  def get(self, request):

    professionals = Professional.objects.all()

    serialized = ProfessionalSerializer(professionals, many=True)

    return Response(serialized.data, status=status.HTTP_200_OK)
