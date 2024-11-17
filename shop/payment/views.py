from django.shortcuts import render, redirect
from core.models import ShippingAddress, Orders, OrderItems
import datetime
from django.contrib import messages
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
                order.update(shipped=True, date_shipped=now)

            else:
                # Get the order
                order = Orders.objects.filter(id=id)
                # Update the status
                order.update(shipped=False)
            
            messages.success(request, "shipping status updated")

            return redirect('core:home')
        
        return render(request, 'payment/orders.html',{
            'order':order,
            'items':items
        })
    
    else:
        messages.error(request, 'Access Denied')
        return redirect('core:home')
    


