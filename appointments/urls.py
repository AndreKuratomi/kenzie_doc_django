from django.urls import path
from .views import (
    CreateAppointment,
    SpecificPatientView,
    SpecificAppointmentView,
    SpecificProfessionalView,
    NotFinishedAppointmentsView,
)

urlpatterns = [
    path('appointments/', CreateAppointment.as_view()),
    path('appointments/professional/<str:council_number>/', SpecificProfessionalView.as_view()),
    path('appointments/<str:appointment_id>/', SpecificAppointmentView.as_view()),
    path('appointments/patient/<str:register_number>/', SpecificPatientView.as_view()),
    path('appointments_open/', NotFinishedAppointmentsView.as_view()),
]
