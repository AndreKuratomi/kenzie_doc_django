from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from django.core.validators import RegexValidator

from utils.functions import generate_register_number

import uuid


class UsersModel(BaseUserManager):
    def create_user(self, email, password, is_prof=False, is_admin=False, **extra_fields):
        if not email:
            raise ValueError("Email necessary for creation!")

        email = self.normalize_email(email)
        user = self.model(email=email, is_prof=is_prof, is_admin=is_admin, **extra_fields)
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
    SEX = (
        ('m', 'M'),
        ('f', 'F')
    )
    
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) # editable=False is processed as read_only
    cpf = models.CharField(max_length=11)

    is_prof = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    username = models.CharField(unique=False, null=True, max_length=255)
    age = models.IntegerField()
    sex = models.CharField(max_length=1, choices=SEX)
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=11)
    
    address = models.ForeignKey("Address", on_delete=models.CASCADE, related_name='users', null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UsersModel()


class UserLogin(models.Model):
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255, unique=False)


class Address(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    street = models.CharField(max_length=255, blank=True)
    house_number = models.CharField(max_length=255)
    post_code = models.CharField(max_length=255) # use a separate API for filling the blank ones
    city = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=2, blank=True)


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    register_number = models.CharField(
        max_length=8,
        unique=True,
        default=generate_register_number,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9]{6}-[a-zA-Z0-9]{1}$',
                message='Register number must be in the format dddddd-d where d is an alphanumeric character.'
            )
        ]
    )


class Professional(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    council_number = models.CharField(max_length=8, unique=True)
    specialty = models.CharField(max_length=255)


class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

