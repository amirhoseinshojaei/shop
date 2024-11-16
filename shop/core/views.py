from django.shortcuts import render, get_object_or_404, redirect
from .models import (User, Profile, Categories, Suppliers
                     , Products, Orders, OrderItems, ShippingAddress)

from django.http import Http404
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
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
        return render(request, '404.html', status=404)
        


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



def login_user(request):
    if request.method == 'POST':
        phone_number = request.POST['phone_number']
        password = request.POST['password']
        user = authenticate(phone_number=phone_number, password=password)

        if user is not None:
            login(request, user)
            messages.success(request,'You are now Logged In')
            return redirect('core:index')
        
        else:
            messages.error(request,'Invalid phone number or password')
            return redirect('core:login')
        
    
    return render(request,'register/login.html',{})



def logout_user(request):
    logout(request)
    messages.success(request, 'You are logged out now')
    return redirect('core:why_logout')


def why_logout(request):
    return render(request, 'register/why_logout.html',{})


@login_required
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        new_password2 = request.POST['new_password2']

        if not request.user.check_password(current_password):
            messages.error('current password is Incorrect')
            return redirect('core:change_password')
        
        if new_password == new_password2:
            request.user.password = make_password(new_password)
            request.user.save()
            messages.success('password changed successfully')
            return redirect('core:index')
        
        else:
            messages.error(request,'new password must be match')
            return redirect('core:change_password')
        
    return render(request, 'register/change_password.html', {})


# Profile

@login_required
def profile_view(request):
    profile = request.user.profile
    return render(request, 'core/profile.html', {'profile':profile})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        profile = user.profile
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.save()
        profile.address = request.POST['address']
        profile.postal_code = request.POST['postal_code']
        profile.city = request.POST['city']
        profile.save()

        return redirect('core:profile')
    
    return render(request, 'core/edit_profile.html', {})