from django.shortcuts import render
from django.http import HttpResponse
from .models import *
# Create your views here.

def IndexViews(request):
    return render(request, 'products/index.html')
def FarmerDashViews(request):
    crop = Crop.objects.all()
    return render(request, 'farmers_page/farmer-dashboard.html', {'crop': crop})
