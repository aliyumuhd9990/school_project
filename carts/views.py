from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from products.models import *
# from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# from .cart import Cart

# Create your views here.
# @require_POST
@login_required
def CartAddView(request, crop_id):  
    crop = get_object_or_404(Crop, id=crop_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        quantity = request.POST.get('quantity')
    # Check if item is already in cart
        cart_item, created = CartItem.objects.get_or_create(cart=cart, crop=crop, quantity=quantity)

        if not created:
            cart_item.quantity += int(quantity)  # Increment quantity if item exists
            cart_item.save()

        messages.success(request, 'Cart Successfully Updated!!')
        return redirect('cart_view')  # Redirect to cart view after adding

@login_required
def CartView(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    total_price = sum(item.total_price() for item in cart_items)
    context = {
        'cart_items': cart_items, 
        'total_price': total_price
        }

    return render(request, 'Orders/cart.html', context)

@login_required
def RemoveFromCart(request, cart_id):
    cart_items = get_object_or_404(CartItem, id=cart_id)
    cart_items.delete()

    messages.success(request, 'Item Removed Successfully!!')
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

