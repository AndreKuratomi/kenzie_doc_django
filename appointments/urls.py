from django.urls import path
from .views import (
    CreateAppointment,
    FinishAppointmentView,
    NotFinishedAppointmentsView,
    ProfessionalAppointmentsTodayView,
    SpecificPatientView,
    SpecificAppointmentView,
    SpecificProfessionalView,
)

urlpatterns = [
    path('appointments/', CreateAppointment.as_view()),
    path('appointments/professional/<str:council_number>/', SpecificProfessionalView.as_view()),
    path('appointments/<str:appointment_id>/', SpecificAppointmentView.as_view()),
    path('appointment_finish/<str:appointment_id>/', FinishAppointmentView.as_view()),
    path('appointments/patient/<str:register_number>/', SpecificPatientView.as_view()),
    path('appointments/open_24/<str:council_number>/', ProfessionalAppointmentsTodayView.as_view()),
    path('appointments/open/<str:council_number>/', NotFinishedAppointmentsView.as_view()),
]
