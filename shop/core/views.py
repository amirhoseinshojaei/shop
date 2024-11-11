from django.shortcuts import render, get_object_or_404
from .models import (User, Profile, Categories, Suppliers
                     , Products, Orders, OrderItems, ShippingAddress)

from django.http import Http404
from django.contrib import messages
# Create your views here.


def index(request):
    products = Products.objects.filter(status='in_stock')
    categories = Categories.objects.all()

    context = {
        'products':products,
        'categories':categories
    }

    return render(request,'core/index.html', context)



def product_detail(request, slug):
    try:
        product = get_object_or_404(Products, slug=slug)
        return render(request, 'core/product_detail.html',{
            'product':product
        })
    
    except Http404:
        messages.error(request, 'Product does not exist')
        return render(request, '404.html', status=404)
    


def categories(request):
    categories = Categories.objects.all()
    return render(request, 'core/categories.html', context={
        'categories':categories
    })


def category_detail(request, slug):
    try:
        category = get_object_or_404(Categories, slug=slug)
        product = Products.objects.filter(category=category)
        return render(request, 'category_detail.html',{
            'category':category,
            'product':product
        })
    
    except Http404:
        messages.error(request, 'Category does not exist')
        return render(request, '404.html', status=404)