from django.shortcuts import render, redirect
from core.models import ShippingAddress, Orders, OrderItems
import datetime
from django.contrib import messages
from cart.cart import Cart
from django.contrib.auth.decorators import login_required
# Create your views here.



def orders(request, id):
    if request.user.is_authenticated and request.user.is_superuser:
        # Get the order
        order = Orders.objects.get(id=id)

        # Get the order items
        items = OrderItems.objects.filter(order=id)

        if request.POST:
            status = request.POST['shipping_status']
            # Check if true or false
            if status == 'true':
                # Get the order
                order = Orders.objects.filter(id=id)
                # Update the status
                now = datetime.datetime.now()
                order.update(shipped=True, date_shipped=now, status='delivered')

            else:
                # Get the order
                order = Orders.objects.filter(id=id)
                # Update the status
                order.update(shipped=False, status='canceled')
            
            messages.success(request, "shipping status updated")

            return redirect('core:home')
        
        return render(request, 'payment/orders.html',{
            'order':order,
            'items':items
        })
    
    else:
        messages.error(request, 'Access Denied')
        return redirect('core:home')
    

def dashboard(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Orders.objects.all()
        return render(request, 'payment/orders_list.html', {
            'orders':orders
        })
    
    else:
        messages.error(request, 'Access Denied')
        return redirect('core:home')
    


def dash_not_shipped_list(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Orders.objects.filter(shipped=False)
        return render(request, 'payment/orders_not_shipped.html', {
            'orders': orders
        })
    
    else:
        messages.error(request, 'Access Denied')
        return redirect('core:home')



# Process orders
@login_required
def process_order(request):
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()

    if request.method == 'POST':
        # Check if the user has a shipping address
        try:
            shipping_address = ShippingAddress.objects.get(user=request.user)
        
        except shipping_address.DoesNotExist:
            shipping_address = None

        # If no shipping address , get it from POST data
        if not shipping_address:
            shipping_address_data = {
                'city': request.POST['city'],
                'shipping_address_1': request.POST['shipping_address_1'],
                'postal_code_1': request.POST['postal_code_1']
            }
            # Check if all required fields are present
            # missing_fields = [ key for key,value in shipping_address.items() if not value and key != 'shipping_address_2' and key != 'postal_code_2']

            # Save the new shipping address
            shipping_address = ShippingAddress.objects.create(
                user = request.user,
                city = shipping_address_data['city'],
                shipping_address_1 = shipping_address_data['shipping_address_1'],
                postal_code_1 = shipping_address_data['postal_code_1']
            )

        # Gather Order Info
        full_name = request.POST['full_name']
        # shipping_address_str = f"{shipping_address.city}\n{shipping_address.shipping_address_1}\n{shipping_address.postal_code_1}"
        city = shipping_address.city
        shipping_address_1 = shipping_address.shipping_address_1
        postal_code = shipping_address.postal_code_1
        amount_paid = totals

        # Create an Order
        user = request.user
        create_order = Orders(user=user, full_name=full_name,
                              city=city, shipping_address=shipping_address_1,
                              postal_code=postal_code, amount_paid=amount_paid)
        
        create_order.save()


        # Add order items
        order_id = create_order.id
        for product in cart_products():
            product_id = product.id
            price = product.sale_price if product.is_sale else product.price

            for key, value in quantities().items():
                if int(key) == product.id:
                    create_order_item = OrderItems(order_id=order_id, product_id=product_id, user=user, quantity= value, price=price)
                    create_order_item.save()
        

        # Todo: create delete our cart


        
