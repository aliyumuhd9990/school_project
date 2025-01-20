from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def IndexViews(request):
    return render(request, 'products/index.html')
