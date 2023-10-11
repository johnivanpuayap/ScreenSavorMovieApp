from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import *


# Create your views here.

def index(request):
    return render(request, 'user/home.html')


def loginPage(request):
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


def registerPage(request):
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




def homePage(request):
    return render(request, 'user/home.html')

