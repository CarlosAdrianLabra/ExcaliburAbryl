from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db.models.fields import CharField
from .managers import UserManager

class User(AbstractBaseUser, PermissionsMixin):

    #Tipo de Usuarios

    ADMINISTRADOR ='0'
    INVENTARIO='1'
    PUNTODEVENTA='2'
    CODIGODEBARRAS='3'
    PROMOCIONES='4'
    COMPRADEZAPATO='5'
    
    ROLE_CHOICES=[
        (ADMINISTRADOR,'Administrador'),
        (INVENTARIO,'Inventario'),
        (PUNTODEVENTA,'Punto de venta',),
        (CODIGODEBARRAS,'Codigo de barras'),
        (PROMOCIONES, 'Promociones'),
        (COMPRADEZAPATO, 'Compra de zapato')
    ]

    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=False)
    nombres = models.CharField(max_length=50,blank=True)
    apellidos = models.CharField(max_length=30, blank=True)
    is_staff=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    role= models.CharField(max_length=1,
        choices=ROLE_CHOICES,
        blank=True,
        default=ADMINISTRADOR
        )


    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS= ['email',]

    objects = UserManager()

    def get_full_name(self):
        return self.nombres + ' ' + self.apellidos