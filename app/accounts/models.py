from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        PLAYER = "PLAYER", "Player"
        OWNER = "OWNER", "Owner"

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.PLAYER,
    )

    def __str__(self) -> str:
        return self.username

