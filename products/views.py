from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import *
from orders.models import *
from accounts.models import *
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from decimal import Decimal
from django.db.models import Q
from xhtml2pdf import pisa

# Create your views here.
app_name = 'products'

def IndexView(request):
    crop = Crop.objects.all().order_by('crop_name')[:6]
    categories = Category.objects.all()
    crops = Crop.objects.filter(available = True)
    
        
    context = {
        'crop': crop,
        'categories': categories,
    }
    return render(request, 'products/index.html', context)

@login_required
def FarmerDashView(request):
    crop = Crop.objects.filter(farmer=request.user)[:6]
    order_items = OrderItem.objects.filter(crop__in=crop)
    recent_orders = order_items.order_by('order')[:5]
    pending_orders = order_items.filter(order__paid=False)[:5]
    farmer_profile, created = Profile.objects.get_or_create(user=request.user)

    if farmer_profile.total_earned == 0.00:
        total_earned = 0
        for item in order_items:
            if item.order.paid == True:
                total_earned += item.price

        farmer_profile.total_earned = total_earned
        farmer_profile.balance = total_earned
        farmer_profile.save()


    context = {
        'crop': crop,
        'total_earnings': farmer_profile.balance,
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
        return redirect(reverse('products:add-crop'))
    else:
        return render(request, 'farmers_page/add-crops.html')
    
    # crop = Crop.objects.get(id=id)
    # return render(request, 'farmers_page/farmers-product.html', {'crop': crop})
def ProductDetailView(request,id):
    crop = get_object_or_404(Crop, id=id, available=True)
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

    #handling search query
    query = request.GET.get('q')
    if query:
        crop = Crop.objects.filter(
    Q(crop_name__icontains=query) |
    Q(crop_desc__icontains=query)
)
        
    paginator = Paginator(crop, 6)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        #if page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        #if page is out of range deliver last page of result
        posts = paginator.page(paginator.num_pages)
   
    context = {
        'crop': posts,
        'page': page,
        'category': category,
        'categories': categories,
        'query': query,
    }
    return render(request, 'products/list.html', context)

def product_search(request):
    query = request.GET.get('q')
    if query:
        products = Crop.objects.filter(
    Q(name__icontains=query) |
    Q(description__icontains=query)
)
    else:
        products = Crop.objects.all()
    return render(request, 'products/product_search.html', {'products': products})

def AboutView(request):
    return render(request, 'products/about.html')

@login_required
def EditProductView(request, id):
    crop = get_object_or_404(Crop,id=id)

    if request.method == 'POST':
        crop_name = request.POST.get('cname')
        crop_desc = request.POST.get('cdesc')
        crop_price = request.POST.get('cprice')
        crop_img = request.FILES.get('cimg')
        cat = request.POST.get('cat')
        is_available = request.POST.get('available')=='on'
        # slug = request.POST.get('slug')

        category, created = Category.objects.get_or_create(name = cat)

        crop.crop_name = crop_name
        crop.crop_desc = crop_desc
        crop.crop_price = crop_price
        if crop_img:
            crop.crop_img = crop_img
        crop.category = category
        crop.available = is_available
        crop.farmer = request.user

        new_slug = slugify(crop_name)
        if crop.slug != new_slug:
            original_slug = new_slug
            counter = 1

            while Crop.objects.filter(slug=new_slug).exclude(id=crop.id).exists():
                new_slug = f"{original_slug}-{counter}"
                counter += 1
            crop.slug = new_slug

        crop.save()
        messages.success(request, 'Crop Edited Successfully!!')
        return redirect(reverse('products:edit-crop', args=[crop.id]))
    return render(request, 'farmers_page/edit-crops.html', {'crop': crop})

@login_required
def ViewCrops(request):
    # crop = Crop.objects.filter(farmer=request.user)
    object_list = Crop.objects.filter(farmer=request.user)
    #6 post in each page
    paginator = Paginator(object_list, 6)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        #if page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        #if page is out of range deliver last page of result
        posts = paginator.page(paginator.num_pages)

    context = {
        'crop' : posts,
        'page' : page,
    }
    return render(request, 'farmers_page/view-crops.html', context)

@login_required
def OrderListView(request):
     crop = Crop.objects.filter(farmer=request.user)
     order_items = OrderItem.objects.filter(crop__in=crop)
     recent_orders = order_items.order_by('order')
    #6 post in each page
     paginator = Paginator(recent_orders, 5)
     page = request.GET.get('page')
     try:
        posts = paginator.page(page)
     except PageNotAnInteger:
        #if page is not an integer deliver the first page
        posts = paginator.page(1)
     except EmptyPage:
        #if page is out of range deliver last page of result
        posts = paginator.page(paginator.num_pages)

     context = {
         'recent_orders': posts,
         'page': page,
         
     }
     return render(request, 'farmers_page/order-page.html', context)
@login_required
def PendingListView(request):
     crop = Crop.objects.filter(farmer=request.user)
     order_items = OrderItem.objects.filter(crop__in=crop)
     pending_orders = order_items.filter(order__paid=False)
    
    #6 post in each page
     paginator = Paginator(pending_orders, 5)
     page = request.GET.get('page')
     try:
        posts = paginator.page(page)
     except PageNotAnInteger:
        #if page is not an integer deliver the first page
        posts = paginator.page(1)
     except EmptyPage:
        #if page is out of range deliver last page of result
        posts = paginator.page(paginator.num_pages)

     context = {
         'pending_orders': posts,
         'page': page,
         
     }
     return render(request, 'farmers_page/pending-page.html', context)

@login_required
def withdrawView(request):
    if request.method == "POST":
        bank_name = request.POST.get('bank_name')
        account_name = request.POST.get('account_name')
        account_num = request.POST.get('account_num')
        withdrawal_amount = request.POST.get('amount')
        withdrawal_amount = Decimal(withdrawal_amount)
        farmer_profile, created = Profile.objects.get_or_create(user=request.user)



        if withdrawal_amount >= farmer_profile.balance:
            messages.error(request, 'Insufficient Balance!!')
            return redirect(reverse('products:withdraw_page'))
        else:
            withdraw = withdrawalRequest.objects.create(farmer=request.user, bank_name=bank_name,   account_name=account_name, account_num=account_num, withdrawal_amount=withdrawal_amount)
            withdraw.save()
            farmer_profile.balance -= withdraw.withdrawal_amount
            farmer_profile.save()

            messages.success(request, 'Withdrawal Request Sent Successfully!!')
            return redirect(reverse('products:farmer_dash'))
    else:
        pass
        
    return render(request, 'farmers_page/withdraw.html')

def removeCrop(request, id):
    crop = Crop.objects.get(id=id)
    crop.delete()
    messages.success(request, "Crop Removed Successfull!!")
    return redirect(reverse('products:farmer_dash'))

def historyView(request):
    history = withdrawalRequest.objects.filter(farmer=request.user)

    paginator = Paginator(history, 5)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        #if page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        #if page is out of range deliver last page of result
        posts = paginator.page(paginator.num_pages)

    context = {
        'history' : posts,
        'page': page,
    }
    return render(request, 'farmers_page/history.html', context)

def invoice_detail(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    return render(request, 'products/invoice_detail.html', {'invoice': invoice})

def invoice_pdf(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    template_path = 'products/invoice_detail.html'
    context = {'invoice': invoice}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename="invoice_{invoice.id}.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa.CreatePDF(html, dest=response)
    return response