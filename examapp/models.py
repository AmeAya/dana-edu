from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import MinLengthValidator
from phonenumber_field.modelfields import PhoneNumberField
from .CustomUserManager import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    iin = models.CharField(max_length=12, validators=[MinLengthValidator(12)], null=False, blank=False, unique=True)
    surname = models.CharField(max_length=150, null=True, blank=True)
    name = models.CharField(max_length=150, null=True, blank=True)
    patronymic = models.CharField(max_length=150, null=True, blank=True)
    phone = PhoneNumberField(null=False, blank=False, unique=True)
    birth_date = models.DateField(null=False, blank=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'iin'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return str(self.surname) + ' ' + str(self.name) + ' ' + str(self.iin)
