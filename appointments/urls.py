from django.urls import path
from .views import (
    CreateAppointment,
    SpecificPatientView,
    SpecificAppointmentView,
    SpecificProfessionalView,
    NotFinishedAppointmentView,
)

urlpatterns = [
    path('appointments/', CreateAppointment.as_view()),
    path('appointments/professional/<str:council_number>/', SpecificProfessionalView.as_view()),
    path('appointments/<str:appointment_id>/', SpecificAppointmentView.as_view()),
    path('appointments/patient/<str:cpf>/', SpecificPatientView.as_view()),
    path('appointments/open/', NotFinishedAppointmentView.as_view()),
]
