from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager

class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=False)
    nombres = models.CharField(max_length=50,blank=True)
    apellidos = models.CharField(max_length=30, blank=True)
    is_staff=models.BooleanField(default=False)


    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS= ['email',]

    objects = UserManager()

    def get_full_name(self):
        return self.nombres + ' ' + self.apellidos