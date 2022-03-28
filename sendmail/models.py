from django.db import models

# Create your models here.
class MailModel(models.Model):
    subject=models.CharField(255)
    message=models.TextField()
    sender=models.CharField(255)
    receiver=models.CharField(255)
    fail_silently=models.BooleanField(default=False)