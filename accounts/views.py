from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.contrib.auth import authenticate
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from orders.models import *

#activation
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode 
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, send_mail
from django.conf import settings
from .utils import *
import uuid


# from .authentications import authenticate
# Create your views here.
#pyhton manage.py migrate --run-syncdb
def SignupView(request):
    if request.method == "POST":
        fname = request.POST['fname']
        email = request.POST['email']
        role = request.POST['role']
        password1 = request.POST['password']
        password2 = request.POST['confirm_password']
 
        if password1 != password2:
            messages.error(request, 'Password Don\'t Match!!')
            return redirect('signup')
        elif CustomUser.objects.filter(email=email).exists():
                messages.error(request, 'Email Already Exist!!')
                return redirect('signup')
        else:
                user = CustomUser.objects.create_user(full_name=fname, email=email, password=password1, role=role)
                user.save()

                #create a profile page for the new user
                user_model = CustomUser.objects.get(email=email)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id, balance=0.00, total_earned=0.00,)
                new_address = Address.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                new_address.save()
                #user activation
                current_site = get_current_site(request)
                mail_subject = 'Your account needs to be verify'
                context = {
                     'user': user,
                     'domain': current_site,
                     'uid' : urlsafe_base64_encode(force_bytes(user.id)),
                     'token' : default_token_generator.make_token(user),

                }
                message = render_to_string('accounts/email_verified.html', context)
                to_email = email
                send_email = EmailMessage(mail_subject, message, to=[to_email])
                
                send_email.send()
               #  messages.success(request, 'Thank you for registaring with us, we have sent you an email verification to your email address!')
                return redirect('/accounts/login/?command=verification&email='+email)
        
    return render(request, 'accounts/sign-up.html')

def ActivateEmailView(request, token, uidb64):
        try:
             uid = urlsafe_base64_decode(uidb64).decode()
             user = CustomUser._default_manager.get(id=uid) 
        except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
             user = None

        if user is not None and default_token_generator.check_token(user, token):
             user.is_active = True
             user.save()
             messages.success(request, 'Congratulations! Your account is activated!')
             return redirect('login')
        else:
             messages.error(request, 'Invalid Activation Link!')
             return redirect('signup')
             
             
        # return HttpResponse("Account Activated!")
def SentEmailView(request):
     return render(request, 'accounts/email_sent.html')

def FarmerLoginViews(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(email=email, password=password)
        if user is not None:
            if user.role != 'user':
                auth.login(request, user)
                return redirect(reverse('products:farmer_dash'))
            else:
                messages.error(request, 'Users cannot log in here!!')
                return redirect('farmer-login')
        else:
            messages.error(request, 'Invalid Credentials!!')
            return redirect('farmer-login')
    else:
        return render(request, 'farmers_page/farmer-login.html')

def LoginView(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(email=email, password=password)
        if user is not None:
            if user.role != 'farmer':
                auth.login(request, user)
                return redirect(reverse('products:index'))
            else:
                messages.error(request, 'Farmers cannot log in here!!')
                return redirect('login')
        else:
            messages.error(request, 'Invalid Credentials!!')
            return redirect('login')
    else:
        return render(request, 'accounts/sign-in.html')


@login_required
def AccountView(request):
     user = request.user
     profile = Profile.objects.get(user=user)
     address = Address.objects.get(user=user)
    #  order = Order.objects.get()
     context = {
          'user' : user,
          'profile': profile,
          'address' : address,
        #   'order' : order,
     }
     return render(request, 'accounts/account.html', context)


@login_required
def EditProfileView(request):
     user = request.user
     profile = Profile.objects.get(user=request.user)
     address = Address.objects.get(user=request.user)

     context = {
        'user': user,
        'profile': profile, 
        'address': address,
     }
     

     if not profile.profile_img:
          profile.profile_img = 'img/profile_images/du.png'

     if request.method == "POST":
          #this is for the CustomUser table
          user.full_name = request.POST.get('fname', user.full_name)#updating new name
          user.email = request.POST.get('email', user.email)#updating new email

          #this is for profile table
          profile.contact = request.POST.get('contact', profile.contact)
        #   img = request.FILES.get('file')
          

          if 'file' in request.FILES:
               profile.profile_img = request.FILES['file']



          user.save()
          profile.save()
          messages.success(request, 'Profile Updated!!')
        
          return redirect('account')
     return render(request, 'accounts/edit-profile.html', context)

@login_required
def EditAddressView(request):
     address = Address.objects.get(user=request.user)
     

     if request.method == 'POST':
          address.state = request.POST.get('state', address.state)
          address.city = request.POST.get('city', address.city)
          address.street = request.POST.get('str', address.street)
          address.location = request.POST.get('lct', address.location)

          address.save()
          messages.success(request, 'Address Updated!!')
          return redirect('edit-address')
     return render(request, 'accounts/edit-address.html', {'address': address})

# @login_required
# def FarmerDashView(request):
#      return render(request, 'farmers_page/farmer-dashboard.html')

def VerifyView(request):
    return render(request, 'accounts/email_verification.html')


@login_required
def logoutView(request):
    auth.logout(request)
    return redirect('login')

