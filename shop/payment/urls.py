from django.urls import path
from . import views

urlpatterns = [
    path('orders/<uuid:id>/', views.orders, name='orders'),
]