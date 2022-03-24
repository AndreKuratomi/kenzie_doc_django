from django.urls import path
from .views import ProfessionalsView, ProfessionalsByIdView

from user.views import PatientByIdView, PatientsView

urlpatterns = [
    # path('user/'),
    # path('login/'),
    # path('address/'),
    path('patient/', PatientsView.as_view()),
    path('patient/<patient_id>/', PatientByIdView.as_view()),
    path('professional/', ProfessionalsView.as_view()),
    path('professional/<str:council_number>', ProfessionalsByIdView.as_view())
]