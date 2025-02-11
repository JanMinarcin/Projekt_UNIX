from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Profile

# Create your views here.
@login_required(login_url='signin')
def index(request):
    return render(request, 'index.html')

@login_required(login_url='signin')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':

        if request.FILES.get('image') == None:
            image = user_profile.profileimg
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        if request.FILES.get('image') != None:
            image  = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        return redirect('settings')


    return render(request, 'setting.html', {'user_profile': user_profile})

def signup(request):
    if request.method == 'POST':
       Meno = request.POST['Meno']
       email = request.POST['email']
       Heslo = request.POST['Heslo']
       Heslo2 = request.POST['Heslo2']

       if Heslo == Heslo2:
           if User.objects.filter(email=email).exists():
                messages.info(request, 'Email je už použitý')
                return redirect('signup')
           elif User.objects.filter(username=Meno).exists():
                messages.info(request, 'Meno je už použité')
                return redirect('signup')
           else:
                user = User.objects.create_user(username=Meno, email=email, password=Heslo)
                user.save()
                
                user_login = auth.authenticate(username=Meno, password=Heslo)
                auth.login(request, user_login)

                user_model = User.objects.get(username=Meno)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('settings')
       else:
              messages.info(request, 'Heslá sa nezhodujú')
              return redirect('signup')
           
       
    else:
        return render(request, 'signup.html')
    
def signin(request):
    if request.method == 'POST':
        Meno = request.POST['Meno']
        Heslo = request.POST['Heslo']

        user = auth.authenticate(username=Meno, password=Heslo)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Nesprávne meno alebo heslo')
            return redirect('signin')
    else:
        return render(request, 'signin.html')
    
@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')