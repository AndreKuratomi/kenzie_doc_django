from rest_framework.exceptions import APIException


class UserAlreadyExistsError(APIException):
    status_code = '409'
    default_detail = {"message": ["This user already exists!"]}


class PatientAlreadyExistsError(APIException):
    status_code = '409'
    default_detail = {"message": ["This patient already exists!"]}


class AddressNotFoundError(APIException):
    status_code = '404'
    default_detail = {"message": ["Address not found!"]}


class UserNotFoundError(APIException):
    status_code = '404'
    default_detail = {"message": ["User not found!"]}
    default_code = "not_found"


class PatientNotFoundError(APIException):
    status_code = '404'
    default_detail = {"message": ["No user found for this register_number!"]}
    default_code = "not_found"


class ProfessionalNotFoundError(APIException):
    status_code = '404'
    default_detail = {"message": ["No professional found for this council_number!"]}
    default_code = "not_found"


class NotPatientError(APIException):
    status_code = '403'
    default_detail = {"message": ["This user is not patient!"]}
    default_code = "forbitten"
