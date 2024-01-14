from rest_framework import generics
from .models import Meal, Order, Delivery
from employee.models import Employee
from .serializer import MealSerializer, OrderSerializer, DeliverySerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly, IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.authentication import TokenAuthentication, BasicAuthentication

class MealCreateView(generics.CreateAPIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [BasicAuthentication]
    queryset = Meal.objects.all()
    serializer_class = MealSerializer

class MealListView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    queryset = Meal.objects.all()
    serializer_class = MealSerializer

class MealRetrieveView(generics.RetrieveAPIView):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer

class MealUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [BasicAuthentication]
    queryset = Meal.objects.all()
    serializer_class = MealSerializer

class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        data=request.data
        meals_data = self.request.data.get('meal', [])
        sum = 0
        meal_obj = []

        try: 
            emp = Employee.objects.get(pk=data['empID'])
        except:
            return Response("invalid employee ID", status=status.HTTP_404_NOT_FOUND)
        print(emp)
        for i in meals_data:
            for j in i:
                if j == 'price':
                    sum += i[j]
                if j == 'id':
                    x = Meal.objects.get(pk=i[j])
                    meal_obj.append(x)

        for i in meal_obj:
            print(i)
            if i.capacity > 0:
                i.capacity-=1
            i.sales+=1
            i.save()
        
        ord_data = {
            "empID": emp,
            "price": sum,
            "delFlag": data['delFlag'],
            "meal":meal_obj,
            "completed": data['completed'],
        }

        ord_obj = Order(empID= emp,
            price=sum,
            delFlag=data['delFlag'],
            completed= data['completed'])
        ord_obj.save()
        ord_obj.meal.set(meal_obj)
        
        ord_obj.save()
        data['price'] = sum
        return Response(data, status=status.HTTP_201_CREATED)

class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    http_method_names = ["patch","get","delete"]

    def destroy(self, request, pk, *args, **kwargs):
        o = Order.objects.get(pk=pk)
        m = o.meal.through.objects.filter(order_id=pk)
        if o.completed == False:
            for i in m:
                x = Meal.objects.get(pk=1)
                x.capacity+=1
                if x.sales > 0:
                    x.sales-=1
                x.save()
        o.delete()
        return Response({'message': 'Order deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    
    def partial_update(self, request, pk, *args, **kwargs):
        o = Order.objects.get(pk=pk)
        if str(request.data['completed']) == 'False':
            o.completed = 'False'
        else:
            o.completed = 'True'
        o.save()
        return Response({'message': 'Order deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    
    def update(self, request, *args, **kwargs):
        return Response({'message': 'error u can only update completed field'}, status=status.HTTP_400_BAD_REQUEST)


class DeliveryListCreateView(generics.ListCreateAPIView):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer

    def create(self, request, *args, **kwargs):
        print(request.data)
        #return Response("fine")
        return super().create(request, *args, **kwargs)

class DeliveryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer
