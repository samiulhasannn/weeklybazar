import uuid

from django.db import models
from django.contrib.auth.models import User
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
    itemUnitQuantity = models.CharField(max_length=100, default="Not Specified")
    itemDescription = models.TextField()
    itemImage = models.ImageField(blank=True, default='item_pics/default_item.jpg', upload_to='item_pics')

    def __str__(self):
        return f"{self.itemName}"


class QuantifiedItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(QuantifiedItem, blank=True)
    totalPrice = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deliveryCharge = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    netTotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def setTotalPrice(self):
        total = 0
        for quantified_item in self.items.all():
            total += (quantified_item.item.itemPrice * quantified_item.quantity)
        self.totalPrice = total

    def setDiscount(self):
        self.discount = math.ceil(float(self.totalPrice) * 0.1)

    def setDeliveryCharge(self):
        self.deliveryCharge = math.floor(float(self.totalPrice) * 0.02)

    def setNetTotal(self):
        self.netTotal = self.totalPrice + self.deliveryCharge - self.discount

    def __str__(self):
        return f"{self.user.customerprofile.customerName}'s Cart"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        self.setTotalPrice()
        self.setDiscount()
        self.setDeliveryCharge()
        self.setNetTotal()


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(QuantifiedItem, blank=True)
    date = models.DateTimeField(auto_now=True)
    totalPrice = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deliveryCharge = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    netTotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def setTotalPrice(self):
        total = self.totalPrice
        for item in self.items.all():
            total += (item.item.itemPrice * item.quantity)
        self.totalPrice = total

    def setDiscount(self):
        self.discount = math.ceil(float(self.totalPrice) * 0.1)

    def setDeliveryCharge(self):
        self.deliveryCharge = math.floor(float(self.totalPrice) * 0.02)

    def setNetTotal(self):
        self.netTotal = self.totalPrice + self.deliveryCharge - self.discount

    def __str__(self):
        return f"{self.user.customerprofile.customerName}'s Order for {self.date}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        self.setTotalPrice()
        self.setDiscount()
        self.setDeliveryCharge()
        self.setNetTotal()
