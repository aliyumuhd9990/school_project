from django.shortcuts import render
from django.http import HttpResponse
from .models import *
# Create your views here.

def IndexView(request):
    return render(request, 'products/index.html')
def FarmerDashView(request):
    crop = Crop.objects.all()
    return render(request, 'farmers_page/farmer-dashboard.html', {'crop': crop})

def FarmerProductView(request, id):
    crop = Crop.objects.get(id=id)
    return render(request, 'farmers_page/farmers-product.html', {'crop': crop})
def ProductView(request):
    # crop = Crop.objects.all()
    return render(request, 'products/products.html')

def AboutView(request):
    return render(request, 'products/about.html')
