from django.urls import path
from .views import LoginUserView, PatientsView, PatientByIdView, ProfessionalsView, ProfessionalsByIdView

urlpatterns = [
    # path('user/'),
    path('login/', LoginUserView.as_view()),
    # path('address/'),
    path('patient/', PatientsView.as_view()),
    path('patient/<str:patient_id>/', PatientByIdView.as_view()),
    path('professional/', ProfessionalsView.as_view()),
    path('professional/<str:council_number>', ProfessionalsByIdView.as_view())
]