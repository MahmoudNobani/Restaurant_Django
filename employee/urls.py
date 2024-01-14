from django.urls import path
from .views import (
    EmployeeListCreateView, EmployeeDetailView,
    PhoneNumberListCreateView, PhoneNumberDetailView,
    ListOrdersByEmp,
)

urlpatterns = [
    path('', EmployeeListCreateView.as_view(), name='employee-list-create'),
    path('<int:pk>/', EmployeeDetailView.as_view(), name='employee-detail'),

    path('phone/', PhoneNumberListCreateView.as_view(), name='phone-number-list'),
    path('phone/<int:pk>/', PhoneNumberDetailView.as_view(), name='phone-number-detail'),
    
    path('ObE/<int:employee_id>', ListOrdersByEmp.as_view(), name='Orders-By-Emp')
]