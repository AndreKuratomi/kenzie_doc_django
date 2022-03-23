from django.urls import path

from user.views import PatientByIdView, PatientsView

urlpatterns = [
    path('user/' ),
    path('login/'),
    path('address/'),
    path('patients/', PatientsView.as_view()),
    path('patients/<patient_id>/', PatientByIdView.as_view()),
    path('professional/')
]