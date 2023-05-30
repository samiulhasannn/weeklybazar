from django.contrib import admin
from .models import CustomerProfile, Item, Cart, Order, QuantifiedItem

# Register your models here.
admin.site.register(CustomerProfile)
admin.site.register(Item)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(QuantifiedItem)
