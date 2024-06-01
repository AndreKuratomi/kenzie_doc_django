from rest_framework.exceptions import APIException


class UserAlreadyExistsError(APIException):
    status_code = '422'
    default_detail = {"message": ["This user already exists"]}


class PatientAlreadyExistsError(APIException):
    status_code = '422'
    default_detail = {"message": ["This patient already exists"]}
