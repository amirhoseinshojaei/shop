from django.urls import path
from . import views


app_name = 'payment'

urlpatterns = [
    path('orders/', views.orders_list, name='orders_list'),
    path('orders/<uuid:id>/', views.orders, name='orders'),
]