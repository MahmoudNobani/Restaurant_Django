import json
from rest_framework import generics
from rest_framework.views import APIView
from .models import PhoneNumber, Employee
from rest_framework.response import Response
from .serializer1 import EmployeeSerializer,PhoneNumberSerializer,EmpSerWithPhone
from meal.models import Order
from meal.serializer import OrderSerializer
from rest_framework import status 
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly, IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.authentication import TokenAuthentication, BasicAuthentication, SessionAuthentication
from .permissions import IsAuthorOrReadOnly

class EmployeeListCreateView(generics.ListCreateAPIView):
    """
    general viewset description
    View for listing and creating Employee instances.

    List: list all employees
    create: create all employees, this api also accepts phone numbers with it

    Only accessible to admin users with basic authentication.
    """
    permission_classes = [IsAdminUser]
    authentication_classes = [BasicAuthentication]
    queryset = Employee.objects.all()
    serializer_class = EmpSerWithPhone

class EmployeeDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    general viewset description:
    View for retrieving, updating, and deleting an Employee instance.
    Supports PATCH, GET, and DELETE methods.

    retrieve: retive data for employee with the associated phone number
    partial update: partially updates employee data
    delete: delete employee data

    Only accessible to the original author or admin users with basic authentication.
    """
    permission_classes = [IsAuthorOrReadOnly]
    authentication_classes = [BasicAuthentication]
    queryset = Employee.objects.all()
    serializer_class = EmpSerWithPhone
    http_method_names = ["patch","get","delete"]

class PhoneNumberListCreateView(generics.ListCreateAPIView):
    """
    general viewset description:
    View for listing and creating PhoneNumber instances.

    List: list all phone numbers
    create: create phone for an existing employee

    No specific permissions are set.
    """
    #permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = PhoneNumber.objects.all()
    serializer_class = PhoneNumberSerializer

class PhoneNumberDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    general viewset description:
    View for retrieving, updating, and deleting a PhoneNumber instance.

    retrieve: Retrieve a specifc phone number

    update: Update a specifc phone number

    delete: delete a specifc phone number

    No specific permissions are set.
    """
    #permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = PhoneNumber.objects.all()
    serializer_class = PhoneNumberSerializer

class ListOrdersByEmp(generics.ListAPIView):
    """
    general viewset description:
    View for listing orders associated with a specific employee.

    list: get the order associated with a specifc employee
    """
    serializer_class = OrderSerializer

    def get_queryset(self):
        employee_id = self.kwargs['employee_id']
        return Order.objects.filter(empID=employee_id)

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({'error': 'resource not found'}, status=status.HTTP_404_NOT_FOUND)

# class EmployeeListView(generics.ListCreateAPIView):
#     permission_classes = [IsAuthenticated]
#     queryset = Employee.objects.all()
#     serializer_class = EmpSerWithPhone

# class EmployeeCreateView(generics.ListCreateAPIView):
#     permission_classes = [IsAdminUser]
#     queryset = Employee.objects.all()
#     serializer_class = EmpSerWithPhone

# class ListOrdersByEmp(APIView):
#     def get(self, request, employee_id):
#         try:
#             order = Order.objects.filter(empID=employee_id)
#             x = []
#             for i in order:
#                 s = OrderSerializer(i)
#                 x.append(s.data)
#             return Response(x, status=status.HTTP_200_OK)
#         except:
#             return Response({'error': 'resource not found'}, status=status.HTTP_404_NOT_FOUND)

