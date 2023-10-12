from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import *


# Views for Login
def home(request):
    return render(request, 'home.html')


def login_page(request):
    alert_message = None
    if request.method == 'GET':
        form = LoginForm()
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('../home')
            else:
                alert_message = 'Invalid username or password.'

    context = {"form": form, "alert_message": alert_message}
    return render(request, 'user/login.html', context)


def logout_user(request):
    logout(request)
    return redirect('home')


def register_page(request):
    if request.method == 'GET':
        form = RegisterForm()
        alert_message = None
    else:
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            alert_message = 'Registration successful!'
        else:
            alert_message = 'Username already taken.'

    form = RegisterForm()
    context = {"form": form, "alert_message": alert_message}
    return render(request, 'user/register.html', context)
