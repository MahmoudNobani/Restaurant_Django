from django.contrib import admin
from .models import Meal, Delivery, Order

admin.site.register(Meal)
admin.site.register(Delivery)
admin.site.register(Order)