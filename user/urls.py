from django.urls import path
from .views import ProfessionalsView

urlpatterns = [
    # path('user/' ),
    # path('login/'),
    # path('address/'),
    # path('patient/'),
    path('professional/', ProfessionalsView.as_view()),
]