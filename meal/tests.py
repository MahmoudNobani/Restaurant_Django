from django.test import TestCase
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .serializer import MealSerializer, OrderSerializer, DeliverySerializer
from .models import Meal, Order, Delivery
from employee.models import Employee, PhoneNumber
from employee.serializer1 import EmployeeSerializer  
from .serializer import MealSerializer

#DB tests
@pytest.mark.django_db
def test_meal_str(create_test_data):
    meal1 = create_test_data['meal1']
    assert str(meal1) == 'Burger'

@pytest.mark.django_db
def test_order_str(create_test_data):
    order = create_test_data['order']
    assert order.pk == 1
 
@pytest.mark.django_db
def test_delivery_str(create_test_data):
    delivery = create_test_data['delivery']
    order = create_test_data['order']
    assert delivery.pk == 1


#view test
@pytest.mark.django_db
def test_meal_list_create_view(admin_user, create_test_data):
    client = APIClient()
    url = reverse('meal-create')
    data = {'name': 'New Meal', 'price': 9.99, 'capacity': 30, 'sales': 5}

    client.force_authenticate(admin_user)
    # Create a new meal
    response = client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED

    url = reverse('meal-list')
    # Check if the meal is listed
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 4  # Assuming there are already 3 meals from the fixture

@pytest.mark.django_db
def test_update_meal(admin_user, create_test_data):
    client = APIClient()
    client.force_authenticate(admin_user)
    meal_id = create_test_data['meal1'].id
    url = reverse('meal-update', kwargs={'pk': meal_id})

    # New data to update the meal
    #updated_data = {"name": "qer","price": 9.0,"capacity": 13,"sales": 10}
    updated_data = {
        "name": "pizza",
        "price": 12.0,
        "capacity": 20,
        "sales": 12
    }

    # Update the meal
    response = client.patch(url, data=updated_data)
    print("NEXT LVL")
    print(response.data)
    assert response.status_code == status.HTTP_200_OK

    url = reverse('meal-Retrieve', kwargs={'pk': meal_id})
    # Ensure the meal is updated
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['name'] == updated_data['name']
    assert response.data['price'] == updated_data['price']
    assert response.data['capacity'] == updated_data['capacity']
    assert response.data['sales'] == updated_data['sales']


@pytest.mark.django_db
def test_order_delete_view(client, create_test_data):
    order_id = create_test_data['order'].id
    url = reverse('order-detail', kwargs={'pk': order_id})

    # Delete an order
    response = client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Ensure the order is deleted
    response = client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.django_db
def test_add_order(client, create_test_data):
    employee = create_test_data['employee']
    url = reverse('order-list-create')

    employee_data = EmployeeSerializer(employee).data
    meal1 = MealSerializer(create_test_data['meal1']).data
    meal2 = MealSerializer(create_test_data['meal2']).data
    new_order_data = {
        'empID': employee_data['id'],
        'price': 20.0,
        'delFlag': False,
        "completed": False,
        'meal': [meal1, meal2]
    }

    response = client.post(url, data=new_order_data, content_type='application/json')
    assert response.status_code == status.HTTP_201_CREATED

@pytest.mark.django_db
def test_list_orders(client, create_test_data):
    url = reverse('order-list-create')

    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1  # One order should be in the list

@pytest.mark.django_db
def test_patial_update_order(client, create_test_data):
    order = create_test_data['order']
    url = reverse('order-detail', kwargs={'pk': order.pk})

    updated_order_data = {
        'completed': True,
    }

    response = client.patch(url, data=updated_order_data, content_type='application/json')
    assert response.status_code == status.HTTP_204_NO_CONTENT
