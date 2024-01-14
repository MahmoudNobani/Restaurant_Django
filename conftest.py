from django.test import TestCase
import pytest
from meal.models import Meal, Order, Delivery
from employee.models import Employee, PhoneNumber


#DB TESTS
@pytest.fixture
def create_test_data():
    meal1 = Meal.objects.create(name='Burger', price=10.99, capacity=50, sales=0)
    meal2 = Meal.objects.create(name='Pizza', price=15.99, capacity=40, sales=0)
    meal3 = Meal.objects.create(name='Salad', price=8.99, capacity=30, sales=0)

    employee = Employee.objects.create(username='John',name='John Doe', password="m", salary=50000.0, position='Manager', address='123 Main St')
    phone_number = PhoneNumber.objects.create(empID=employee, PhoneNumber=1234567890)

    order = Order.objects.create(empID=employee, price=35.97, delFlag=False)
    order.meal.add(meal1, meal2, meal3)

    delivery = Delivery.objects.create(name='John Doe', orderID=order, address='123 Main St')

    return {
        'meal1': meal1,
        'meal2': meal2,
        'meal3': meal3,
        'employee': employee,
        'phone_number': phone_number,
        'order': order,
        'delivery': delivery,
    }



@pytest.fixture
def admin_user():
    return Employee.objects.create_superuser(username='admin', email="admin@gmail.com",password='password', salary=4523)


