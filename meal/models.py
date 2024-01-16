from django.db import models
from employee.models import Employee
# Create your models here.
class Meal(models.Model):
    """
    Model representing a meal.

    Attributes:
        name (str): The name of the meal.
        price (float): The price of the meal.
        capacity (int): The available quantity of the meal.
        sales (int): The number of times this meal has been sold.
    """
    name = models.CharField(max_length=100)
    price = models.FloatField()
    capacity = models.IntegerField()
    sales = models.IntegerField()

    def __str__(self) -> str:
        """
        Return the name  of the meal.

        Returns:
        - str: the name of meal as a string.
        """
        return self.name

class Order(models.Model):
    """
    Model representing an order.

    Attributes:
        empID (Employee): The employee associated with the order.
        price (float): The total price of the order.
        delFlag (bool): A flag indicating whether the order has been delivered.
        meal (ManyToManyField): The meals included in the order through the 'OrderMeal' intermediary model.
        completed (bool): A flag indicating whether the order is completed.
    """
    empID = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="orders")
    price = models.FloatField()
    delFlag = models.BooleanField(default=False)
    meal = models.ManyToManyField(Meal, through='OrderMeal')
    completed = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        """
        Return the id of the Order.

        Returns:
        - str: the id of Order as a string.
        """
        return str(self.pk)

class OrderMeal(models.Model):
    """
    Intermediary model representing a meal included in an order.

    Attributes:
        order (Order): The order to which the meal belongs.
        meal (Meal): The meal associated with the order.
        quantity (int): The quantity of the meal in the order.

    Methods:
        __str__(): Returns a string representation of the order meal with quantity and meal name.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)  # You can change the default value as needed

    def __str__(self) -> str:
        """
       Returns a string representation of the order meal with quantity and meal name.

        Returns:
        - str: the qunatity * meal as a string.
        """
        return f"{self.quantity} x {self.meal}"

class Delivery(models.Model):
    name = models.CharField(max_length=100)
    orderID = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="delivery")
    address = models.TextField()
    """
    Model representing a delivery.

    Attributes:
        name (str): The name of the delivery.
        orderID (Order): The order associated with the delivery.
        address (str): The delivery address.

    Methods:
        __str__(): Returns a string representation of the delivery by its primary key.
    """

    def __str__(self) -> str:
        """
       Returns a string representation of the delivery by its primary key.

        Returns:
        - str: the id of delivery as a string.
        """
        return str(self.pk)