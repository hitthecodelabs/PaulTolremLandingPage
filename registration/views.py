from .forms import UserRegisterForm
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, HttpResponseRedirect
from .forms import UserRegistrationForm
from .models import UserProfile, ActivityLog

from django.views import View
from registration.models import User

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            # Crear perfil de usuario y guardar el número de teléfono
            user_profile = UserProfile(user=new_user, phone_number=user_form.cleaned_data['phone_number'])
            user_profile.save()
    
            # Registrar la actividad de registro
            activity_log = ActivityLog(user=new_user, action="Sign in")
            activity_log.save()

            # Iniciar sesión automáticamente después del registro
            login(request, new_user)

            return HttpResponseRedirect(reverse('home'))
    else:
        user_form = UserRegistrationForm()
    
    return render(request, 'registration/register.html', {'form': user_form})

class MakeSuperuserView(View):
    def get(self, request, username):
        try:
            user = User.objects.get(username=username)  # Query your custom user model
            user.is_superuser = True
            user.is_staff = True
            user.save()
            return HttpResponse(f"User {username} is now a superuser.")
        except User.DoesNotExist:
            return HttpResponse("User not found.")

'''
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse("Incorrect username or password.")
    else:
        form = AuthenticationForm()
        return render(request, 'registration/login.html', {'form': form})
'''

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Registrar la actividad de inicio de sesión
            activity_log = ActivityLog(user=user, action="Log in")
            activity_log.save()

            return HttpResponseRedirect(reverse('home'))
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})

def home(request):
    return render(request, 'registration/home.html')

'''
@login_required
def home(request):
    return render(request, 'registration/home.html')

def user_logout(request):
    logout(request)
    return redirect('login')
'''

def user_logout(request):
    # Registrar la actividad de cierre de sesión
    activity_log = ActivityLog(user=request.user, action="Logout")
    activity_log.save()

    logout(request)
    return redirect('login')