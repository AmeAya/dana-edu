from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import MinLengthValidator
from phonenumber_field.modelfields import PhoneNumberField
from .managers import CustomUserManager
from .functions import getNumberChoices, getLiteralChoices


class Answer(models.Model):
    text = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='answers/', null=True, blank=True)
    is_correct = models.BooleanField(default=False, null=False, blank=False)


class Area(models.Model):
    name = models.CharField(null=False, blank=False)
    head = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    Region = models.ForeignKey('Region', on_delete=models.CASCADE)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    iin = models.CharField(max_length=12, validators=[MinLengthValidator(12)], null=False, blank=False, unique=True)
    surname = models.CharField(max_length=150, null=True, blank=True)
    name = models.CharField(max_length=150, null=True, blank=True)
    patronymic = models.CharField(max_length=150, null=True, blank=True)
    photo = models.ImageField(upload_to='users/', null=True, blank=True)
    phone = PhoneNumberField(null=False, blank=False, unique=True)
    birth_date = models.DateField(null=False, blank=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    group = models.ForeignKey('Group', on_delete=models.CASCADE, null=True, blank=True)

    USERNAME_FIELD = 'iin'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return str(self.surname) + ' ' + str(self.name) + ' ' + str(self.iin)


class Group(models.Model):
    number = models.SmallIntegerField(null=False, blank=False, choices=getNumberChoices())
    literal = models.CharField(null=False, blank=False, choices=getLiteralChoices(), max_length=1)
    school = models.ForeignKey('School', on_delete=models.CASCADE)


class Ministry(models.Model):
    name = models.CharField(null=False, blank=False)
    head = models.ForeignKey('CustomUser', on_delete=models.CASCADE)


class Question(models.Model):
    text = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='questions/', null=True, blank=True)
    answers = models.ManyToManyField('Answer')


class Region(models.Model):
    name = models.CharField(null=False, blank=False)
    head = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    ministry = models.ForeignKey('Ministry', on_delete=models.CASCADE)


class School(models.Model):
    name = models.CharField(null=False, blank=False, max_length=100)
    address = models.TextField(null=False, blank=False)
    staff = models.ManyToManyField('CustomUser', related_name='staff')
    director = models.OneToOneField('CustomUser', on_delete=models.CASCADE, related_name='director')
