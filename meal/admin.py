from django.contrib import admin

# Register your models here.
from .models import Meal, Delivery, Order
admin.site.register(Meal)
admin.site.register(Delivery)
admin.site.register(Order)