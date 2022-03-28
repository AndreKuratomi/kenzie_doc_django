from django.db import models
import uuid


class AppointmentsModel(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateTimeField(auto_now_add=True)
    complaint = models.CharField(max_length=255, default="")
    finished = models.BooleanField(default=False)
    patient = models.OneToOneField(
        "user.Patient", related_name="appointment", on_delete=models.CASCADE
    )
    professional = models.OneToOneField(
        "user.Professional", related_name="appointments", on_delete=models.CASCADE
    )
