from django.shortcuts import render, redirect, get_object_or_404
# from django.http import HttpResponse
from .models import *
from django.contrib.auth.decorators import login_required
# Create your views here.


def IndexView(request):
    crop = Crop.objects.all()
    return render(request, 'products/index.html', {'crop': crop})

def FarmerDashView(request):
    crop = Crop.objects.filter(farmer=request.user)
    return render(request, 'farmers_page/farmer-dashboard.html', {'crop': crop})

@login_required
def AddProductView(request):
    if request.method == 'POST':
        cname = request.POST['cname']
        cdesc = request.POST['cdesc']
        cprice = request.POST['cprice']
        cimg = request.POST['cimg']

        crop = Crop.objects.create(farmer=request.user, crop_name=cname, crop_desc=cdesc, crop_price=cprice, crop_img=cimg)
        crop.farmer = request.user
        crop.save()
        return redirect('farmer-dash')
    else:
        return render(request, 'farmers_page/add-crops.html')
    
    # crop = Crop.objects.get(id=id)
    # return render(request, 'farmers_page/farmers-product.html', {'crop': crop})
def ProductDetailView(request,id):
    crop = get_object_or_404(Crop, id=id)
    return render(request, 'products/products-details.html', {'crop' : crop})

def ProductView(request):
    crop = Crop.objects.all()
    return render(request, 'products/products.html', {'crop' : crop})

def AboutView(request):
    return render(request, 'products/about.html')
