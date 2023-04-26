from django.contrib import admin
from .models import CustomerProfile, Item, Cart

# Register your models here.
admin.site.register(CustomerProfile)
admin.site.register(Item)
admin.site.register(Cart)
