from django.urls import path
from .views import (
    CreateAppointment,
    SpecificPatientView,
    SpecificProfessionalView,
    NotFinishedAppointmentView,
)

urlpatterns = [
    path("appointments/", CreateAppointment.as_view()),
    path("appointments/<str:cpf>/", SpecificPatientView.as_view()),
    path("appointments/<str:council_number/", SpecificProfessionalView.as_view()),
    path("appointments/open/", NotFinishedAppointmentView.as_view()),
]
