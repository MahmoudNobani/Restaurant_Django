from rest_framework import generics
from collections import Counter
from .models import Meal, Order, Delivery
from employee.models import Employee
from .serializer import MealSerializer, OrderSerializer, DeliverySerializer, OrderSerializerReadOnly
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from rest_framework.permissions import IsAdminUser
from rest_framework.authentication import TokenAuthentication, BasicAuthentication


class MealCreateView(generics.CreateAPIView):
    """
    General ViewSet Description:
    
    API view for creating a Meal.
    Supports POST method.

    post: allow the addition of a new meal

    only accessible to admin user with basic authentication
    """

    permission_classes = [IsAdminUser]
    authentication_classes = [BasicAuthentication]
    queryset = Meal.objects.all()
    serializer_class = MealSerializer

class MealListView(generics.ListAPIView):
    """
    General ViewSet Description:

    API view for listing Meals.

    get: list all the meals in the system

    allows access only with the help of token authentication
    """
    authentication_classes = [TokenAuthentication]
    queryset = Meal.objects.all()
    serializer_class = MealSerializer

class MealRetrieveView(generics.RetrieveAPIView):
    """
    General ViewSet Description:

    API view for retrieving a Meal.
    get: allows one meal to be retirved
    """
    queryset = Meal.objects.all()
    serializer_class = MealSerializer

class MealUpdateView(generics.UpdateAPIView):
    """
    General ViewSet Description:

    API view for updating a Meal.
    
    patch: update attribute of a meal

    only accessible to admin user with basic authentication
    """
    permission_classes = [IsAdminUser]
    authentication_classes = [BasicAuthentication]
    queryset = Meal.objects.all()
    serializer_class = MealSerializer

class OrderListCreateView(generics.ListCreateAPIView):
    """
    General ViewSet Description:

    API view for creating a new Order or listing all orders

    get: list all orders in system
    post: add a new order
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        """
        create: Creates a new Order.

        Method:
            - POST

        Parameters:
            - data: Request data containing order details, including the list of meals.

        Response:
            - Status code: 201 if successful, 404 if invalid employee or meal IDs.
        """
        data=request.data
        meals_data = self.request.data.get('meal', [])
        sum = 0
        meal_obj = []

        try: 
            emp = Employee.objects.get(pk=data['empID'])
        except:
            return Response("invalid employee ID", status=status.HTTP_404_NOT_FOUND)
        
        for i in meals_data:
            try: 
                meal_temp = Meal.objects.get(pk=i)
                meal_obj.append(meal_temp)
                sum += meal_temp.price
            except:
                return Response("invalid Meal ID", status=status.HTTP_404_NOT_FOUND)
               
        for i in meal_obj:
            try: 
                if i.capacity > 0:
                    i.capacity-=1
                if i.capacity <= 0:
                    raise ValueError("Meal is not available atm, please order something else")
                i.sales+=1
            except ValueError as e:
                return Response(str(e), status=status.HTTP_404_NOT_FOUND)    
        for i in meal_obj:
            i.save()           



        ord_obj = Order(empID= emp,
            price=sum,
            delFlag=data['delFlag'],
            completed= data['completed'])
        ord_obj.save()
        ord_obj.meal.set(meal_obj)
        
        ord_obj.save()
        
        for k, v in Counter(meal_obj).items():
            Order.meal.through.objects.filter(order=ord_obj, meal=k).update(quantity=v)

        data['price'] = sum
        return Response(data, status=status.HTTP_201_CREATED)
    
class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    General ViewSet Description:

    API view for retrieving, updating, and deleting an Order.
    Supports GET, PATCH, and DELETE methods.

    retrieve: Retrieve data for the order with details on the meals.
    partial update: Partially update order data (completed or delFlag).
    delete: Delete order data.

    Only accessible to the original author or admin users with basic authentication.
    """

    queryset = Order.objects.all()
    serializer_class = OrderSerializerReadOnly
    http_method_names = ["patch","get","delete"]

    def destroy(self, request, pk, *args, **kwargs):
        """
        destroy: Deletes an Order.

        Method:
            - DELETE

        Parameters:
            - pk: Primary key of the Order.
            - request: the request and its data

        Response:
            - Status code: 204 if successful, 404 if the Order is not found.
        """
        order_obj = Order.objects.get(pk=pk)
        meals_ids = order_obj.meal.through.objects.filter(order_id=pk)
        if order_obj.completed == False:
            for i in meals_ids:
                meal_obj = Meal.objects.get(pk=i.meal.pk)
                meal_obj.capacity+=1
                if meal_obj.sales > 0:
                    meal_obj.sales-=1
                meal_obj.save()
        
        order_obj.delete()
        return Response({'message': 'Order deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    
    def partial_update(self, request, pk, *args, **kwargs):
        """
        partial_update: Partially updates an Order's data (completed or delFlag).

        Method:
            - PATCH

        Parameters:
            - pk: Primary key of the Order.
            - request: Request data containing fields to be updated.

        Response:
            - Status code: 204 if successful, 404 if the Order is not found.
        """
        order_obj = Order.objects.get(pk=pk)
        if "completed" in request.data:
            if str(request.data['completed']) == 'False' or str(request.data['completed']) == 'false':
                order_obj.completed = 'False'
            else:
                order_obj.completed = 'True'

        if "delFlag" in request.data:
            if str(request.data['delFlag']) == 'False' or str(request.data['delFlag']) == 'false':
                order_obj.delFlag = 'False'
            else:
                order_obj.delFlag = 'True'
        order_obj.save()
        return Response({'message': 'Order edited successfully'}, status=status.HTTP_204_NO_CONTENT)
    
class DeliveryListCreateView(generics.ListCreateAPIView):
    """
    General ViewSet Description:

    API view for creating a new Delivery associated with an Order.
    
    post: creates a delibery request with the needed data for an order
    """
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer

    def create(self, request, *args, **kwargs):
        """
        create: Creates a new Delivery associated with an Order.

        Method:
            - POST

        Parameters:
            - data: Request data containing delivery details and associated order ID.
        Response:
            - Status code: 201 if successful, 404 if the order is not found or delivery is not allowed.
        """
        try:
            order_instance = Order.objects.get(pk=request.data["orderID"])
            # order_serializer = OrderSerializer(order_instance)
            # serialized_order_data = order_serializer.data
            if order_instance.delFlag is True:
                if order_instance.completed is False:
                    return super().create(request, *args, **kwargs)
                else:
                    return Response({'error': "the order cant have a delivery as the completed flag is True"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            else:
                return Response({'error': "the order cant have a delivery as the delivery flag is false"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

class DeliveryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    General ViewSet Description:

    API view for retrieving, updating, and deleting a Delivery.
    
    get: get a delivery details
    patch: update a delivery
    delete: delete a delivery
    """
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer



#old create if meal were objects:
# class OrderListCreateView(generics.ListCreateAPIView):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer

#     def create(self, request, *args, **kwargs):
#         data=request.data
#         meals_data = self.request.data.get('meal', [])
#         sum = 0
#         meal_obj = []

#         try: 
#             emp = Employee.objects.get(pk=data['empID'])
#         except:
#             return Response("invalid employee ID", status=status.HTTP_404_NOT_FOUND)
#         print(emp)
#         for i in meals_data:
#             for j in i:
#                 if j == 'price':
#                     sum += i[j]
#                 if j == 'id':
#                     x = Meal.objects.get(pk=i[j])
#                     meal_obj.append(x)

#         for i in meal_obj:
#             print(i)
#             if i.capacity > 0:
#                 i.capacity-=1
#             i.sales+=1
#             i.save()
        
#         ord_data = {
#             "empID": emp,
#             "price": sum,
#             "delFlag": data['delFlag'],
#             "meal":meal_obj,
#             "completed": data['completed'],
#         }

#         ord_obj = Order(empID= emp,
#             price=sum,
#             delFlag=data['delFlag'],
#             completed= data['completed'])
#         ord_obj.save()
#         ord_obj.meal.set(meal_obj)
        
#         ord_obj.save()
#         data['price'] = sum
#         return Response(data, status=status.HTTP_201_CREATED)