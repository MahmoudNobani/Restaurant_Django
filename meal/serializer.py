from rest_framework import serializers

from .models import Meal, Order, Delivery, OrderMeal
from employee.models import Employee, PhoneNumber

class MealSerializer(serializers.ModelSerializer):
    """
    Serializer for the Meal model.

    Attributes:
        Meta:
            model (Meal): The model associated with the serializer.
            fields (list): The fields to be included in the serialized representation ('__all__' for all fields).
    """
    class Meta:
        model = Meal
        fields = '__all__'

class OrderMealSerializer(serializers.ModelSerializer):
    """
    Serializer for the OrderMeal model.

    Attributes:
        Meta:
            model (OrderMeal): The model associated with the serializer.
            fields (list): The fields to be included in the serialized representation ('quantity' and 'meal').
    """
    class Meta:
        model = OrderMeal
        fields = ['quantity', 'meal']

class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for the Order model.

    Attributes:
        meal_ordered (list): A serialized representation of meals associated with the order.
        price (float): The total price of the order (read-only).

        Methods:
            get_meals(obj): Helper method to retrieve and serialize meals associated with the order.
            
        Meta:
            model (Order): The model associated with the serializer.
            fields (list): The fields to be included in the serialized representation.
    """
    meal_orderd = serializers.SerializerMethodField('get_meals')
    price = serializers.FloatField(read_only=True)  

    def get_meals(self, obj) -> list:
        z = Order.meal.through.objects.filter(order=obj.pk)
        #print(z)
        x = []
        for i in z:
            x.append(OrderMealSerializer(i).data)
        return x

    class Meta:
        model = Order
        fields = ['pk','empID', 'price', 'delFlag', 'meal_orderd', 'completed']

class OrderSerializerReadOnly(serializers.ModelSerializer):
    """
    Read-only Serializer for the Order model.

    Attributes:
        meal_ordered (list): A serialized representation of meals associated with the order (read-only).
        price (float): The total price of the order (read-only).

        Methods:
            get_meals(obj): Helper method to retrieve and serialize meals associated with the order (read-only).

        Meta:
            model (Order): The model associated with the serializer.
            fields (list): The fields to be included in the serialized representation (excluding 'meal').
            read_only_fields (list): Fields that are read-only in the serialized representation.
    """
    #meal = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    price = serializers.FloatField(read_only=True)  
    meal_orderd = serializers.SerializerMethodField('get_meals')


    def get_meals(self, obj) -> list:
        z = Order.meal.through.objects.filter(order=obj.pk)
        #print(z)
        x = []
        for i in z:
            x.append(OrderMealSerializer(i).data)
        return x

    class Meta:
        model = Order
        fields = ['empID', 'price', 'delFlag', 'meal_orderd', 'completed']
        read_only_fields = ['empID', 'price', 'meal_orderd', 'meal', ]

class DeliverySerializer(serializers.ModelSerializer):
    """
    Serializer for the Delivery model.

    Attributes:
        Meta:
            model (Delivery): The model associated with the serializer.
            fields (list): The fields to be included in the serialized representation ('name', 'address', 'orderID').
    """
    #orderID = OrderSerializer()
    class Meta:
        model = Delivery
        fields = ['name','address','orderID']

# class OrderSerializer(serializers.ModelSerializer):
#     meal = MealSerializer(many=True)
#     price = serializers.FloatField(read_only=True)  

#     class Meta:
#         model = Order
#         fields = '__all__'
