from django.db import models
from employee.models import Employee
# Create your models here.
class Meal(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    capacity = models.IntegerField()
    sales = models.IntegerField()

    def __str__(self) -> str:
        return self.name

class Order(models.Model):
    empID = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="orders")
    price = models.FloatField()
    delFlag = models.BooleanField(default=False)
    meal = models.ManyToManyField(Meal)
    completed = models.BooleanField(default=False)

    def __str__(self) -> str:
        return str(self.pk)

class Delivery(models.Model):
    name = models.CharField(max_length=100)
    orderID = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="delivery")
    address = models.TextField()

    def __str__(self) -> str:
        return str(self.pk)