from django.db import models
import uuid


class AppointmentsModel(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    date = models.DateTimeField()
    complaint = models.CharField(max_length=255, default="")
    finished = models.BooleanField(default=False)

    # Multiple appointments over time for multiple patients and professionals, 
    # but each appointment has one professional and one patient.

    patient = models.ForeignKey("user.Patient", on_delete=models.CASCADE, related_name="appointments")
    professional = models.ForeignKey("user.Professional", on_delete=models.CASCADE, related_name="appointments")
