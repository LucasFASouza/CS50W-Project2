from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listing(models.Model):
    CATEGORIES_CHOICES = [
        ('Fashion', 'Fashion'),
        ('Home', 'Home'),
        ('Electronics', 'Electronics'),
        ('Toys', 'Toys'),
        ('Other', 'Other'),
    ]

    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    initial_bid = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    photo_url = models.URLField(blank=True)
    category = models.CharField(choices=CATEGORIES_CHOICES, max_length=24, blank=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    price = models.DecimalField(max_digits=6, decimal_places=2, blank=True)
    isActive = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title}: {self.description}"


class Biding(models.Model):
    value = models.DecimalField(max_digits=6, decimal_places=2)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidings")
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bidings")

    def __str__(self):
        return f"{self.buyer} bids ${self.value} in {self.item.title}"
