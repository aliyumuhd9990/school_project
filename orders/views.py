from django.shortcuts import render, redirect
from .models import *
from .forms import *
from carts.models import *
# from .tasks import order_created
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Order
from django.urls import reverse

app_name = 'orders'

# Create your views here.
def approve_payment_view(request, order_id):
    if request.user.is_superuser:  # Ensure only admins can approve
        order = get_object_or_404(Order, id=order_id, status="Pending")
        order.status = "Paid"
        order.farmer.balance += order.amount  # Update farmer balance
        order.farmer.save()
        order.save()
        return JsonResponse({"message": "Payment approved successfully", "new_balance": order.farmer.balance})
    return JsonResponse({"error": "Unauthorized"}, status=403)

def CreateOrderView(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = cart.cart_items.all()
    order = None
    address = Address.objects.get(user=request.user)
    user = request.user
    profile = Profile.objects.get(user=request.user)
    # total_price = sum(item.total_price() for item in cart_items)
    total_price = sum(item.total_price() for item in cart_items)
    
    if not cart:
        cart, created = Cart.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        # form = OrderCreateForm(request.POST)
        fname = request.POST.get('fname')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        city = request.POST.get('city')
        location = request.POST.get('location')

        order = Order.objects.create(
            full_name = fname,
            email = email,
            city = city,
            contact = contact,
            location = location
        )
        

        for item in cart_items:
            OrderItem.objects.create(
                order=order, 
                crop=item.crop, 
                price=item.total_price, 
                quantity=item.quantity
                )
            
        cart.cart_items.all().delete()
        request.session['order_id'] = order.id
        return redirect(reverse('payment:process'))
        # order_id = 123  # Example order ID
        # task = order_created.delay(order_id)
        # return JsonResponse({"task_id": task.id, "message": "Order processing started!"})
    else:
        form = OrderCreateForm()
    context = {
        'cart': cart,
        'cart_items' : cart_items,
        'form' : form,
        'address' : address,
        'user' : user,
        'profile' : profile,
        'total_price' : total_price,
    }
    return render(request, 'Orders/create.html', context)
    