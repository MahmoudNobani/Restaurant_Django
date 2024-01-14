from django.urls import path, include

from .views import (
    MealListView, MealRetrieveView, MealCreateView, MealUpdateView,
    OrderListCreateView, OrderDetailView,
    DeliveryListCreateView, DeliveryDetailView,
)

urlpatterns = [
    path('', MealCreateView.as_view(), name='meal-create'),
    path('list/', MealListView.as_view(), name='meal-list'),
    path('<int:pk>/', MealUpdateView.as_view(), name='meal-update'),
    path('list/<int:pk>/', MealRetrieveView.as_view(), name='meal-Retrieve'),

    path('ord/', OrderListCreateView.as_view(), name='order-list-create'),
    path('ord/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),

    path('deli/', DeliveryListCreateView.as_view(), name='delivery-list-create'),
    path('deli/<int:pk>/', DeliveryDetailView.as_view(), name='delivery-detail'),
]