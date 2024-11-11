from django.urls import path
from . import views


app_name = 'core'


urlpatterns = [
    path('', views.index, name='home'),
    path('product/<str:slug>/', views.product_detail, name='product_detail'),
    path('categories/', views.categories, name='categories'),
    path('category/<str:slug>/', views.category_detail, name='category_detail'),
]