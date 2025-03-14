from django.shortcuts import render
from .models import *
from .forms import *
from carts.models import *

app_name = 'orders'
# Create your views here.
def CreateOrderView(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = cart.cart_items.all()
    address = Address.objects.get(user=request.user)
    user = request.user
    profile = Profile.objects.get(user=request.user)
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
            OrderItem.objects.create(order=order, crop=item.crop, price=item.price, quantity=item.quantity)
            
        cart.cart_items.all().delete()
        return render(request, 'Orders/created.html', {'order': order})
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
    