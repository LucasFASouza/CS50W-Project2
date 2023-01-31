from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listing(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")

    def __str__(self):
        return f"{self.name}, {self.description}"
