from django.shortcuts import render, get_object_or_404
from .cart import Cart
from core.models import Products
from django.http import HttpResponse

# Create your views here.


def cart_summary(request):
    # Get the cart
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()
    return render (request, 'cart/cart_summary.html', {
        'cart_products': cart_products,
        'quantities' : quantities,
        'totals': totals
    })


