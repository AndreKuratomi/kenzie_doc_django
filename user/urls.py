from django.urls import path
from .views import ProfessionalsView, ProfessionalsByIdView, AdminView, LoginView

from user.views import PatientByIdView, PatientsView

urlpatterns = [
    # path('user/'),
    path('login/', LoginView.as_view()),
    # path('address/'),
    path('admin/', AdminView.as_view()),
    path('patient/', PatientsView.as_view()),
    path('patient/<patient_id>/', PatientByIdView.as_view()),
    path('professional/', ProfessionalsView.as_view()),
    path('professional/<str:council_number>', ProfessionalsByIdView.as_view())
]