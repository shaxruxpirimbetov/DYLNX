from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        USER = "USER"
        EMPLOYEE = "EMPLOYEE"
        ADMIN = "ADMIN"

    role = models.CharField(
        max_length=20,
        choices=Role,
        default=Role.USER
    )
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    stack = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"User {self.username}"

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["-date_joined"]