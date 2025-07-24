from django.contrib.auth.models import (
    AbstractBaseUser,
    Permission,
    BaseUserManager,
)
from app.core.models import AbstractModel
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user

class User(AbstractBaseUser, AbstractModel):
    email = models.EmailField(null=True, unique=True, blank=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    otp = models.BigIntegerField(null=True, blank=True)
    is_verify = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "auth_user_user"


class UserProfile(AbstractModel):
    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name="user_profile", null=True, blank=True)
    email = models.EmailField(null=True, unique=True, blank=True)
    first_name = models.CharField(max_length=150, null=True, blank=True)
    last_name = models.CharField(max_length=150, null=True, blank=True)
    username = models.CharField(max_length=150, unique=True,null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=150, null=True, blank=True)
    language = models.CharField(default="en", null=True, blank=True)
    status = models.BooleanField(default=True)

    class Meta:
        db_table = "user_profile"