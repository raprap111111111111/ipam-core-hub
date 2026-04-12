import uuid
import hashlib
import secrets
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)

    first_name = models.CharField(max_length=150, blank=True, null=True)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)

    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True)
    is_hr_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    @property
    def full_name(self):
        parts = [self.first_name, self.middle_name, self.last_name]
        return " ".join(part for part in parts if part).strip()

    def __str__(self):
        return self.email


