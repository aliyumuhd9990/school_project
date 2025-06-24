from django.shortcuts import render, redirect
from .models import *
from .forms import *
from carts.models import *
# from .tasks import order_created
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponse
from .models import Order
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from xhtml2pdf import pisa
from django.template.loader import render_to_string, get_template

#email
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, send_mail

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

app_name = 'orders'

# Create your views here.
# def approve_payment_view(request, order_id):
#     if request.user.is_superuser:  # Ensure only admins can approve
#         order = get_object_or_404(Order, id=order_id, status="Pending")
#         order.status = "Paid"
#         order.farmer.balance += order.amount  # Update farmer balance
#         order.farmer.save()
#         order.save()
#         return JsonResponse({"message": "Payment approved successfully", "new_balance": order.farmer.balance})
#     return JsonResponse({"error": "Unauthorized"}, status=403)

def CreateOrderView(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = cart.cart_items.all()
    order = None
    address = Address.objects.get(user=request.user)
    user = request.user
    profile = Profile.objects.get(user=request.user)
    # total_price = sum(item.total_price() for item in cart_items)
    total_price = sum(item.total_price() for item in cart_items)
    
    if not cart:
        cart, created = Cart.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        # form = OrderCreateForm(request.POST)
        fname = request.POST.get('fname')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        city = request.POST.get('city')
        location = request.POST.get('location')

        order = Order.objects.create(
            full_name = fname,
            email = email,
            city = city,
            contact = contact,
            location = location,
            user = request.user,
        )
        print("Created Order:", order.id)
        

        for item in cart_items:
            OrderItem.objects.create(
                order=order, 
                crop=item.crop, 
                price=item.total_price, 
                quantity=item.quantity
                )
        
        if contact == "080xxxxxx":
            messages.error(request, 'Update Your Account')
            return redirect(reverse('orders:create_order'))
        else:
            cart.cart_items.all().delete()

            #order mail
            mail_subject = 'Thank you for your order'
            context = {
                    'user': request.user,
                    'order': order,
                }
            
            message = render_to_string('Orders/order_recieve_email.html', context)
            to_email = request.user.email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            return redirect('payment:initialize_payment', order_id=order.id)
            # return redirect('payment:initialize_payment', order_id=order.id)
            # order_id = 123  # Example order ID
            # task = order_created.delay(order_id)
            # return JsonResponse({"task_id": task.id, "message": "Order processing started!"})
    else:
        form = OrderCreateForm()
    context = {
        'cart': cart,
        'cart_items' : cart_items,
        'form' : form,
        'address' : address,
        'user' : user,
        'profile' : profile,
        'total_price' : total_price,
    }
    return render(request, 'Orders/create.html', context)


@login_required
def order_history(request):
    # Get orders for the logged-in user
    orders = Order.objects.filter(email=request.user.email)
    for order in orders:
        order.price = sum(item.price for item in order.items.all())
        
    paginator = Paginator(orders, 5)
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
        'orders': posts, 
        'page' : page,
        }
    
    return render(request, 'Orders/order_list.html', context)

@login_required
def transaction_history(request):
    # Get orders for the logged-in user
    orders = Order.objects.filter(email=request.user.email).order_by('-created')
    cart = Cart.objects.get(user=request.user)
    cart_items = cart.cart_items.all()
    total_price = sum(item.total_price() for item in cart_items)

    context = {
        'orders': orders, 
        'total_price' : orders.get_total_cost(),
        }
    
    return render(request, 'Orders/transactions.html', context)


@login_required
def generate_invoice(request, order_id):
    order = get_object_or_404(Order, id=order_id, email=request.user.email)
    cart = Cart.objects.get(user=request.user)
    cart_items = cart.cart_items.all()
    total_price = sum(item.price for item in order.items.all())


    # Determine status
    if order.paid:
        status = "Paid"
    elif order.braintree_id:
        status = "Cancelled"
    else:
        status = "Pending"

    template_path = 'Orders/order_pdf.html'
    context = {
        'order': order, 
        'status': status, 
        'total_price' : total_price,
        }

    # Render HTML
    template = get_template(template_path)
    html = template.render(context)

    # Generate PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=invoice_order_{order.id}.pdf'
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('We had some errors with PDF generation <pre>' + html + '</pre>')
    return response