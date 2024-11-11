from django.shortcuts import render, get_object_or_404, redirect
from .models import (User, Profile, Categories, Suppliers
                     , Products, Orders, OrderItems, ShippingAddress)

from django.http import Http404
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login
# Create your views here.


def index(request):
    products = Products.objects.filter(status='in_stock')
    categories = Categories.objects.all()

    context = {
        'products':products,
        'categories':categories
    }

    return render(request,'core/index.html', context)


def about(request):
    return render(request, 'core/about.html', {})



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
        return render(request, '404.html', status=404)\
        


def suggestions_proudcts(request):
    products = Products.objects.filter(is_suggestion=True)
    return render(request, 'core/suggestions.html', {
        'products':products
    })


# Registration section


def signup(request):
    if request.method == 'POST':
        phone_number = request.POST['phone_number']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['<PASSWORD>']

        if password == password2:
            if User.objects.filter(phone_number=phone_number).exists():
                messages.error(request,'Phone number already exist')
                return redirect('core:signup')
            
            elif User.objects.filter(email=email).exists():
                messages.error(request,'email already exist')
                return redirect('core:signup')
            
            else:
                user= User.objects.create(
                    phone_number=phone_number,
                    email=email,
                    password = make_password(password)
                )

                user.save()
                messages.success(request, 'Account created')
                login(request,user)
                return redirect('core:index')
        

        else:
            messages.error(request,'password must be match')
            return redirect('core:signup'
            )
        
    
    return render(request,'register/signup.html',{})