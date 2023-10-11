from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.shortcuts import render, redirect
from .models import User


# Create your views here.
def login_page(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)

        except():
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')

    context = {'page': page}
    return render(request, 'login_register.html', context)


def logout_user(request):
    logout(request)
    return redirect('home')


def register_page(request):
    page = 'register'
    form = UserCreationForm()
    context = {
        'page': page,
        'form': form,
    }

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration. Please try again!')

    return render(request, 'login_register.html', context)


def home(request):

    return render(request, 'home.html')
