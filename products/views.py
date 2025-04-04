from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import *
from orders.models import *
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.contrib import messages
# Create your views here.
app_name = 'products'

def IndexView(request):
    crop = Crop.objects.all()
    return render(request, 'products/index.html', {'crop': crop})

@login_required
def FarmerDashView(request):
    crop = Crop.objects.filter(farmer=request.user)
    order_items = OrderItem.objects.filter(crop__in=crop)
    total_earnings = sum(item.price for item in order_items if item.order.paid)
    recent_orders = order_items.order_by('order')[:5]
    pending_orders = order_items.filter(order__paid=False)[:5]

    context = {
        'crop': crop,
        'total_earnings': total_earnings,
        'recent_orders': recent_orders,
        'pending_orders': pending_orders,
    }
    return render(request, 'farmers_page/farmer-dashboard.html', context)

@login_required
def AddProductView(request):
    if request.method == 'POST':
        cname = request.POST.get('cname')
        cdesc = request.POST.get('cdesc')
        cprice = request.POST.get('cprice')
        cimg = request.FILES.get('cimg')
        cat = request.POST.get('cat')
        is_available = request.POST['available']
        # slug = request.POST.get('slug')

        is_available = True if is_available == 'on' else False
        category, created = Category.objects.get_or_create(name = cat)
        slug = slugify(cname)

        counter = 1
        original_slug = slug
        while Crop.objects.filter(slug=slug).exists():
            slug = f"{original_slug}-{counter}"
            counter += 1

        crop = Crop.objects.create(farmer=request.user, crop_name=cname, crop_desc=cdesc, crop_price=cprice, crop_img=cimg, category=category, available=is_available, slug=slug)
    
        crop.farmer = request.user
        crop.crop_name
        crop.save()
        messages.success(request, 'Crops Added Successfully!!')
        return redirect(reverse('products:farmer_dash'))
    else:
        return render(request, 'farmers_page/add-crops.html')
    
    # crop = Crop.objects.get(id=id)
    # return render(request, 'farmers_page/farmers-product.html', {'crop': crop})
def ProductDetailView(request,id,slug):
    crop = get_object_or_404(Crop, id=id, slug=slug, available=True)
    crops = Crop.objects.filter(available = True)
    recommend_crop = Crop.objects.filter(category=crop.category).exclude(id=crop.id)[:4]
    
    context = {
        'crop' : crop,
        'crops' : crops,
        'recommend_crop' : recommend_crop,
    }
    return render(request, 'products/products-details.html', context)

def ProductView(request):
    crop = Crop.objects.all()
    return render(request, 'products/products.html', {'crop' : crop})

def ProductListView(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    crop = Crop.objects.filter(available = True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        crop = crop.filter(category=category)

    context = {
        'crop': crop,
        'category': category,
        'categories': categories,
    }
    return render(request, 'products/list.html', context)

def AboutView(request):
    return render(request, 'products/about.html')

@login_required
def EditProductView(request, id):
    crop = Crop.objects.get(id=id)
    return render(request, 'farmers_page/edit-crops.html', {'crop': crop})

@login_required
def ViewCrops(request):
    crop = Crop.objects.filter(farmer=request.user)

    context = {
        'crop' : crop
    }
    return render(request, 'farmers_page/view-crops.html', context)

@login_required
def OrderListView(request):
     crop = Crop.objects.filter(farmer=request.user)
     order_items = OrderItem.objects.filter(crop__in=crop)
     recent_orders = order_items.order_by('order')
     context = {
         'recent_orders': recent_orders,
     }
     return render(request, 'farmers_page/order-page.html', context)
