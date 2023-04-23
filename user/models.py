import uuid

from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.utils import timezone


# Create your models here.
class CustomerProfile(models.Model):
    customerID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customerName = models.CharField(default="New User", max_length=50)
    customerEmail = models.EmailField(blank=True)
    customerAddress = models.CharField(blank=True, max_length=200)
    customerMobile = models.CharField(blank=True, max_length=11)
    customerImage = models.ImageField(blank=True)
    customerAccountCreationDate = models.DateField(default=timezone.now)

    def __str__(self):
        return f"Profile of {self.customerName}"
