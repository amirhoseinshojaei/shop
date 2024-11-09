from django.shortcuts import render, get_object_or_404
from .models import (User, Profile, Categories, Suppliers
                     , Products, Orders, OrderItems, ShippingAddress)
# Create your views here.


def index(request):
    products = Products.objects.filter(status='in_stock')
    categories = Categories.objects.all()

    context = {
        'products':products,
        'categories':categories
    }

    return render(request,'core/index.html', context)
