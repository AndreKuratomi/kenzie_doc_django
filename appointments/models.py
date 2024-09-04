from django.db import models
import uuid


class AppointmentsModel(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    date = models.DateTimeField()
    complaint = models.CharField(max_length=255, default="")
    finished = models.BooleanField(default=False)

    patient = models.ManyToManyField("user.Patient", related_name="appointment")
    professional = models.ManyToManyField("user.Professional", related_name="appointment")
