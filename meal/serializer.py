from rest_framework import serializers

from .models import Meal, Order, Delivery
from employee.models import Employee, PhoneNumber

class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    meal = MealSerializer(many=True)
    price = serializers.FloatField(read_only=True)  

    class Meta:
        model = Order
        fields = '__all__'

class DeliverySerializer(serializers.ModelSerializer):
    #orderID = OrderSerializer()
    class Meta:
        model = Delivery
        fields = ['name','address','orderID']