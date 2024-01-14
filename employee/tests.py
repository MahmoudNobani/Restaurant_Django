from django.test import TestCase
import pytest
from meal.models import Meal, Order, Delivery
from .models import Employee, PhoneNumber
from .serializer1 import EmpSerWithPhone, EmployeeSerializer, PhoneNumberSerializer, PhoneNumberSerializer1
import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

#DB tests
@pytest.mark.django_db
def test_employee_str(create_test_data):
    """
    Test the __str__ method of the Employee model after creating one

    Args:
        create_test_data: Fixture that creates test data in the database.
    """
    employee = create_test_data['employee']
    assert str(employee) == 'John'

@pytest.mark.django_db
def test_phone_number(create_test_data):
    """
    Test PhoneNumber model attributes after creating one

    Args:
        create_test_data: Fixture that creates test data in the database.

    """
    phone_number = create_test_data['phone_number']
    assert phone_number.PhoneNumber == 1234567890

#View test
@pytest.mark.django_db
class TestEmployeeViews:
    """
    Test cases for Employee views.
    """
    def test_create_employee(self,admin_user):
        """
        Test creating an Employee instance through the API.

        Args:
            admin_user: Fixture that creates an admin user for authentication.

        """
        client = APIClient()
        client.force_authenticate(admin_user)
        url = reverse('employee-list-create')
        data = {
            "username": "k",
            "salary": 1324,
            "position": "casher",
            "address": "ramallah",
            "password": "m",
            "phone_numbers": [
                {"PhoneNumber": "07"},
                {"PhoneNumber": "1"}
            ]
        }

        response = client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED

    def test_list_employees(self,admin_user):
        """
        Test listing Employee instances through the API.

        Args:
            admin_user: Fixture that creates an admin user for authentication.
        """
        client = APIClient()
        client.force_authenticate(admin_user)
        url = reverse('employee-list-create')
        
        # Create a sample employee for testing
        Employee.objects.create(name="Test Employee", salary=40000.0, position="Casher", address="456 Side St")
        
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == Employee.objects.count()

    def test_update_employee(self):
        """
        Test updating an Employee instance through the API.
        """
        client = APIClient()
        employee = Employee.objects.create_user(username="Employee", password="m", email="user@gmail.com",salary=40000.0, position="Casher", address="456 Side St")
        client.force_authenticate(employee)
        url = reverse('employee-detail', kwargs={'pk': employee.pk})
        data = {"address": "nablus"}

        response = client.patch(url, data, format='json')
        print(response.data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['address'] == "nablus"

    def test_delete_employee(self,admin_user):
        """
        Test deleting an Employee instance through the API.

        Args:
            admin_user: Fixture that creates an admin user for authentication.

        """
        client = APIClient()
        client.force_authenticate(admin_user)
        employee = Employee.objects.create_user(username="Test Employee", password="m", email="user@gmail.com",salary=40000.0, position="Casher", address="456 Side St")
        url = reverse('employee-detail', kwargs={'pk': employee.pk})

        response = client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Employee.objects.filter(pk=employee.pk).exists()


@pytest.mark.django_db
class TestPhoneNumberViews:
    """
    Test cases for PhoneNumber views.
    """
    def test_list_phone_numbers(self):
        """
        Test listing PhoneNumber instances through the API.
        """
        client = APIClient()
        url = reverse('phone-number-list')
        
        # Create a sample phone number for testing
        employee = Employee.objects.create(name="Test Employee", salary=40000.0, position="Casher", address="456 Side St")
        PhoneNumber.objects.create(empID=employee, PhoneNumber="1234567890")
        
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == PhoneNumber.objects.count()

    def test_update_phone_number(self):
        """
        Test updating a PhoneNumber instance through the API.
        """
        client = APIClient()
        employee = Employee.objects.create(name="Test Employee", salary=40000.0, position="Casher", address="456 Side St")
        phone_number = PhoneNumber.objects.create(empID=employee, PhoneNumber="1234567890")
        url = reverse('phone-number-detail', kwargs={'pk': phone_number.pk})
        data = {"PhoneNumber": "9876543210"}

        response = client.patch(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['PhoneNumber'] == 9876543210

    def test_delete_phone_number(self):
        """
        Test deleting a PhoneNumber instance through the API.
        """
        client = APIClient()
        employee = Employee.objects.create(name="Test Employee", salary=40000.0, position="Casher", address="456 Side St")
        phone_number = PhoneNumber.objects.create(empID=employee, PhoneNumber="1234567890")
        url = reverse('phone-number-detail', kwargs={'pk': phone_number.pk})
        url12 = reverse('phone-number-list')
        response12 = client.get(url12)
        print(response12.data)
        response = client.delete(url)
        print(response)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not PhoneNumber.objects.filter(pk=phone_number.pk).exists()


@pytest.mark.django_db
class TestOrderViews:
    """
    Test cases for Order views.
    """
    def test_list_orders_by_employee(self):
        """
        Test listing orders associated with a specific employee through the API.
        """
        client = APIClient()
        employee = Employee.objects.create(name="Test Employee", salary=40000.0, position="Casher", address="456 Side St")
        url = reverse('Orders-By-Emp', kwargs={'employee_id': employee.pk})

        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == Order.objects.filter(empID=employee.pk).count()
