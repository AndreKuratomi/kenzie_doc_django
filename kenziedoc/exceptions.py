from rest_framework.exceptions import APIException


class UUIDNotValidError(APIException):
    status_code = '404'
    default_detail = {"message": "No valid UUID"}


class UserAlreadyExistsError(APIException):
    status_code = '422'
    default_detail = {"message": ["This user already exists"]}


class PatientAlreadyExistsError(APIException):
    status_code = '422'
    default_detail = {"message": ["This patient already exists"]}


class PatientNotFoundError(APIException):
    status_code = '404'
    default_detail = {"message": "No patient found"}
