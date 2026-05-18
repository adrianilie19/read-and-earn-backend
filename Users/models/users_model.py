from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email=None, password=None, **extra_fields):
        if not email:
            raise ValueError('El usuario debe tener un email válido')
        if "@" not in email:
            raise ValueError('El formato del email no es válido')
        if not password:
            raise ValueError('La contraseña no puede estar vacía')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=100, unique=True, null=False, blank=False)
    nombre = models.CharField(max_length=50, null=False, blank=False)
    nivel = models.PositiveIntegerField(default=1, verbose_name="Nivel")
    exp = models.PositiveIntegerField(default=0, verbose_name="Experiencia")
    is_active = models.BooleanField(default=True, verbose_name="¿Está activo?")
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de registro")

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'users'
        ordering = ['email']
        verbose_name = '1. Usuario'
        verbose_name_plural = '1. Usuarios'

    def __str__(self):
        return f"{self.nombre} ({self.email})"
