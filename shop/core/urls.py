from django.urls import path
from . import views


app_name = 'core'


urlpatterns = [
    path('', views.index, name='home'),
    path('<str:slug>/', views.product_detail, name='product_detail'),
]