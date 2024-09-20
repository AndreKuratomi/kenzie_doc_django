from django.urls import path
from .views import AdminView, LoginUserView, PatientsView, PatientByIdView, ProfessionalsBySpecialtyView, ProfessionalsView, ProfessionalsByIdView


urlpatterns = [
    # path('user/'),
    path('login/', LoginUserView.as_view()),
    path('admin/', AdminView.as_view()),
    path('patient/', PatientsView.as_view()),
    path('patient/<str:register_number>/', PatientByIdView.as_view()),
    path('professional/', ProfessionalsView.as_view()),
    path('professional/<str:council_number>/', ProfessionalsByIdView.as_view()),
    path('professional/specialty/<str:specialty>/', ProfessionalsBySpecialtyView.as_view())
]