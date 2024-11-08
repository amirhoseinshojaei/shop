from .cart import Cart

# Create context processors so our cart work all pages

def cart(request):
    return {
        'cart': Cart(request)
    }