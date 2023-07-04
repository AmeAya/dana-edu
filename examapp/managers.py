from django.contrib.auth.models import BaseUserManager
from django.utils import timezone
from datetime import datetime


class CustomUserManager(BaseUserManager):
    def _create_user(self, iin, password, is_staff, is_superuser, **extra_fields):
        if not iin:
            raise ValueError('Users must have an iin')
        user = self.model(
            iin=iin,
            birth_date=datetime.strptime(iin[:6], "%y%m%d").date(),
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            last_login=timezone.now(),
            date_joined=timezone.now(),
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, iin, password, **extra_fields):
        return self._create_user(iin, password, False, False, **extra_fields)

    def create_superuser(self, iin, password, **extra_fields):
        user = self._create_user(iin, password, True, True, **extra_fields)
        return user
