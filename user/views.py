from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import *
from django.views.generic.base import View
from django.db import connection
from django.contrib.auth.decorators import login_required

class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'user/login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            print(form.errors)
        return render(request, 'user/login.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('login')


class RegistrationView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'user/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data['username'].lower()
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('login')
        else:
            print(form.errors)
        return render(request, 'user/register.html', {'form': form})

class AdminRegistrationView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'user/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data['username']
            user.set_password(form.cleaned_data['password'])
            user.is_staff = True
            user.save()
            login(request, user)
            return redirect('login')
        else:
            print(form.errors)
        return render(request, 'user/register.html', {'form': form})
    

@login_required(login_url='/login/')
def toggle_like_movie(request, movie_id):
    if request.user.is_authenticated:
        with connection.cursor() as cursor:
            cursor.execute("CALL ToggleLikeMovie(%s, %s)", [request.user.username, movie_id])
        return redirect('movie', movie_id=movie_id)
    else:
        return render(request, "error.html", {"error_message": "You must be logged in to like or unlike a movie."})