import uuid

from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.utils import timezone
from PIL import Image
import math


# Create your models here.
class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    customerID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customerName = models.CharField(default="New User", max_length=50)
    customerEmail = models.EmailField(blank=True)
    customerAddress = models.CharField(blank=True, max_length=200)
    # customerMobile = models.CharField(default=user.username, editable=False)
    customerImage = models.ImageField(blank=True, default='profile_pics/default.jpg', upload_to='profile_pics')
    customerAccountCreationDate = models.DateField(default=timezone.now)

    def __str__(self):
        return f"Profile of {self.customerName}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        image = Image.open(self.customerImage.path)

        if image.height > 300 or image.width > 300:
            output_size = (300, 300)
            image.thumbnail(output_size)
            image.save(self.customerImage.path)


class Item(models.Model):
    itemID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    itemName = models.CharField(max_length=100)
    itemType = models.CharField(default="", max_length=50)
    itemPrice = models.DecimalField(max_digits=10, decimal_places=2)
    itemQuantity = models.PositiveIntegerField(default=0)
    itemDescription = models.TextField()
    itemImage = models.ImageField(blank=True, default='item_pics/default_item.jpg', upload_to='item_pics')

    def __str__(self):
        return f"{self.itemName}"


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item, blank=True)
    deliveryCharge = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    totalPrice = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def setTotalPrice(self):
        total = self.totalPrice
        for item in self.items.all():
            total += item.itemPrice
        self.totalPrice = total

    def setDeliveryCharge(self):
        self.deliveryCharge = math.floor(float(self.totalPrice) * 0.02)

    def __str__(self):
        return f"{self.user.customerprofile.customerName}'s Cart"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        self.setTotalPrice()
        self.setDeliveryCharge()
