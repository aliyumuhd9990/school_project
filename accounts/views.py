from django.shortcuts import render, redirect
from .models import CustomUser, Profile
from django.contrib.auth import authenticate
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
# from .authentications import authenticate
# Create your views here.
#pyhton manage.py migrate --run-syncdb
def SignupViews(request):
    if request.method == "POST":
        fname = request.POST['fname']
        email = request.POST['email']
        password1 = request.POST['password']
        password2 = request.POST['confirm_password']

        if password1 != password2:
            messages.error(request, 'Password Don\'t Match!!')
            return redirect('signup')
        elif CustomUser.objects.filter(email=email).exists():
                messages.error(request, 'Email Already Exist!!')
                return redirect('signup')
        else:
                user = CustomUser.objects.create_user(full_name=fname, email=email, password=password1)
                user.save()

                #create a profile page for the new user
                user_model = CustomUser.objects.get(email=email)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('login')
        
    return render(request, 'accounts/sign-up.html')

def FarmerSignupViews(request):
     if request.method == "POST":
        fname = request.POST['fname']
        email = request.POST['email']
        contact = request.POST['contact']
        state = request.POST['state']
        city = request.POST['city']
        file = request.POST['file']
        password1 = request.POST['password']
        password2 = request.POST['confirm_password']

        if password1 != password2:
            messages.error(request, 'Password Don\'t Match!!')
            return redirect('farmer-signup')
        elif CustomUser.objects.filter(email=email).exists():
                messages.error(request, 'Email Already Exist!!')
                return redirect('farmer-signup')
        else:
                user = CustomUser.objects.create_user(full_name=fname, email=email, password=password1)
                user.save()

                #create a profile page for the new user
                user_model = CustomUser.objects.get(email=email)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id, contact=contact, state=state, city=city, profile_img=file)
                new_profile.save()
                return redirect('farmer-login')
     return render(request, 'farmers_page/farmer-signup.html')

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
        return render(request, 'farmers_page/farmer-signin.html')

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
def logoutView(request):
    auth.logout(request)
    return redirect('login')


@login_required
def FarmerLogoutView(request):
    auth.logout(request)
    return redirect('farmer-login')
