from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
import uuid

# Create your models here.
class UsersModel(BaseUserManager):
    def create_user(self, email, password, is_prof=False, is_admin=False, **extra_fields):
        if not email:
            raise ValueError("Email needed to creation")

        email = self.normalize_email(email)
        user = self.model(email=email, is_prof=is_prof, is_admin=is_admin,  **extra_fields)
        user.set_password(password)

        user.save(using=self.db)
        return user

    def create_user_patient(self, email, password, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_user_prof(self, email, password, **extra_fields):
        return self._create_user(email, password, True, False, **extra_fields)

    def create_user_adm(self, email, password, **extra_fields):
        return self._create_user(email, password, False, True, **extra_fields)

class User(AbstractUser):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_prof = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(unique=False, null=True, max_length=255)
    address = models.ForeignKey("Address", on_delete=models.CASCADE, related_name='users', null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UsersModel()

class Address(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    street = models.CharField(max_length=255)
    house_number = models.IntegerField()
    state = models.CharField(max_length=255)

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cpf = models.CharField(primary_key=True, max_length=11, editable=False)
    age = models.CharField(max_length=255)
    sex = models.CharField(max_length=255)

class Professional(models.Model):
    council_number = models.CharField(primary_key=True, max_length=8, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialty = models.CharField(max_length=255)
    patients = models.ManyToManyField(Patient)

class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

