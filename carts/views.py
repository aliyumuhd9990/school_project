from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from products.models import *
from .cart import Cart

# Create your views here.
@require_POST
def CartAddView(request, crop_id):
    cart = Cart(request)
    crop = get_object_or_404(Crop, id=crop_id)
    quantity = request.POST.get('quantity')
