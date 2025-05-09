from .models import *

def cart_items_count(request):
    if request.user.is_authenticated:
        cart_count = CartItem.objects.filter(user=request.user).count()
    else:
        cart_count = 0
    return {'cart_count': cart_count}