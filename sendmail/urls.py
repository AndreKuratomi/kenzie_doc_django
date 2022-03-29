from django.urls import path
from .views import EmailView

urlpatterns = [
    path("send_email/", EmailView.as_view()),
]
