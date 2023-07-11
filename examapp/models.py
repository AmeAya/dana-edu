from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import MinLengthValidator
from phonenumber_field.modelfields import PhoneNumberField
from .managers import CustomUserManager
from .functions import getNumberChoices, getLiteralChoices, getExamTypesChoices, getUserTypeChoices
from datetime import timedelta


class Answer(models.Model):
    text = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='answers/', null=True, blank=True)
    is_correct = models.BooleanField(default=False)


class Area(models.Model):
    name = models.CharField(max_length=100)
    head = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    Region = models.ForeignKey('Region', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class CurrentExam(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    variant = models.ForeignKey('Variant', on_delete=models.CASCADE)
    subjects = models.ManyToManyField('Subject')


class CustomUser(AbstractBaseUser, PermissionsMixin):
    iin = models.CharField(max_length=12, validators=[MinLengthValidator(12)], unique=True)
    surname = models.CharField(max_length=150, null=True, blank=True)
    name = models.CharField(max_length=150, null=True, blank=True)
    patronymic = models.CharField(max_length=150, null=True, blank=True)
    photo = models.ImageField(upload_to='users/', null=True, blank=True)
    phone = PhoneNumberField(unique=True)
    group = models.ForeignKey('Group', on_delete=models.CASCADE, null=True, blank=True)
    type = models.CharField(max_length=20, choices=getUserTypeChoices())
    birth_date = models.DateField()
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'iin'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return str(self.surname) + ' ' + str(self.name) + ' ' + str(self.iin)


class ExamForGroup(models.Model):
    group = models.ForeignKey('Group', on_delete=models.CASCADE)
    variants = models.ManyToManyField('Variant')
    duration = models.FloatField(default=240)
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # noinspection PyTypeChecker
        self.ends_at = self.starts_at + timedelta(minutes=self.duration)
        super().save(*args, **kwargs)


class Group(models.Model):
    number = models.SmallIntegerField(choices=getNumberChoices())
    literal = models.CharField(choices=getLiteralChoices(), max_length=1)
    school = models.ForeignKey('School', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.number) + str(self.literal)


class Ministry(models.Model):
    name = models.CharField(max_length=100)
    head = models.ForeignKey('CustomUser', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class PupilAnswer(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    answers = models.ManyToManyField('Answer')


class Question(models.Model):
    number = models.PositiveSmallIntegerField()
    text = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='questions/', null=True, blank=True)
    points = models.PositiveSmallIntegerField(choices=[(1, '1'), (2, '2')])
    answers = models.ManyToManyField('Answer')
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)
    variant = models.ForeignKey('Variant', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.number) + '.' + str(self.text) + ' ' + str(self.subject.name)


class Region(models.Model):
    name = models.CharField(max_length=100)
    head = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    ministry = models.ForeignKey('Ministry', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Result(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    variant = models.ForeignKey('Variant', on_delete=models.CASCADE)
    subjects = models.ForeignKey('SubjectCombination', on_delete=models.CASCADE)
    starts_at = models.DateTimeField(auto_now=True)
    ends_at = models.DateTimeField(null=True, blank=True)
    points = models.PositiveSmallIntegerField(default=0)
    answers = models.ManyToManyField('PupilAnswer')

    def __str__(self):
        return self.user.surname + ' ' + self.user.name + ' ' + str(self.points)


class School(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    staff = models.ManyToManyField('CustomUser', related_name='staff')
    director = models.OneToOneField('CustomUser', on_delete=models.CASCADE, related_name='director')

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=100)
    is_required = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class SubjectCombination(models.Model):
    first_subject = models.ForeignKey('Subject', on_delete=models.CASCADE, related_name='first')
    second_subject = models.ForeignKey('Subject', on_delete=models.CASCADE, related_name='second')

    def __str__(self):
        return self.first_subject.name + '-' + self.second_subject.name


class Variant(models.Model):
    name = models.CharField(max_length=100)
    exam_type = models.CharField(max_length=10, choices=getExamTypesChoices())

    def __str__(self):
        return self.name
