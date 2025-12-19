from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    email = models.EmailField(
        unique=True,
        blank=False,
        null=False,
        verbose_name="Correo electrónico"
    )

    def __str__(self):
        return self.username
