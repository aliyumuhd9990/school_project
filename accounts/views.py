from django.shortcuts import render, redirect
from .models import CustomUser, Profile, Address
from django.contrib.auth import authenticate
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
# from django.urls import reverse


# from .authentications import authenticate
# Create your views here.
#pyhton manage.py migrate --run-syncdb
def SignupViews(request):
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
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_address = Address.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                new_address.save()

                if user.role == 'user':
                    return redirect('login')
                else:
                    return redirect('farmer-login')
        
    return render(request, 'accounts/sign-up.html')

def FarmerLoginViews(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('farmer-dash')
        else:
            messages.error(request, 'Invalid Creadentials!!')
            return redirect('farmer-login')
    else:
        return render(request, 'farmers_page/farmer-login.html')

def LoginViews(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Invalid Creadentials!!')
            return redirect('login')
    else:
        return render(request, 'accounts/sign-in.html')


@login_required
def AccountView(request):
     user = request.user
     profile = Profile.objects.get(user=user)
     address = Address.objects.get(user=user)
     context = {
          'user' : user,
          'profile': profile,
          'address' : address
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
          return redirect('account')
     return render(request, 'accounts/edit-address.html', {'address': address})

@login_required
def FarmerDashView(request):
     return render(request, 'farmers_page/farmer-dashboard.html')


@login_required
def logoutView(request):
    auth.logout(request)
    return redirect('login')



