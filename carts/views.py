from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, Order
from products.models import *
# from django.views.decorators.http import require_POST
# from .cart import Cart

# Create your views here.
# @require_POST
def CartAddView(request, crop_id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    crop = get_object_or_404(Crop, id=crop_id)
    cart_item, Created = Cart.objects.get_or_create(user=request.user, crop=crop)
    
    if not Created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart_view')

def CartView(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.total_price() for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'Orders/cart.html', context)

def RemoveFromCart(request, cart_id):
    cart_item = get_object_or_404(Cart, user=request.user, id=cart_id)
    cart_item.delete()
    return redirect('cart_view')

def UpdateCart(request, cart_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
        new_quantity = int(request.POST.get('quantity', 1))
        cart_item.quantity = new_quantity
        cart_item.save()

    return redirect('cart_view')

def CheckOut(request):
    if not request.user.is_authenticated:
        return redirect('login')
    cart_items = Cart.objects.filter(user=request.user)
    if not cart_items:
        return redirect('cart_view')
    total_price = sum(item.total_price() for item in cart_items)

    #create orders from cart
    for item in cart_items:
        Order.objects.create(user=request.user, crop=item.crop, quantity=item.quantity, total_price=item.total_price(), status="pending")

    # clear Cart
    cart_items.delete()
    return render(request, 'Orders/checkout.html', {'total_price': total_price})

