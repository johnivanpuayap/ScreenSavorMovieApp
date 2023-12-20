from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import *
from django.views.generic.base import View
from django.db import connection
from django.contrib.auth.decorators import login_required
from django.contrib import messages

class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'user/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
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
            return redirect('home')
        else:
            error_message = form.errors.as_text()
            messages.error(request, error_message)
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
            cursor.execute("CALL LikeUnlikeMovie(%s, %s)", [request.user.username, movie_id])
        return redirect('movie', movie_id=movie_id)
    else:
        return render(request, "error.html", {"error_message": "You must be logged in to like or unlike a movie."})
    
def get_user_profile(request, username):
    user = User.objects.get(username=username)

    # Execute the stored procedure
    with connection.cursor() as cursor:
        cursor.callproc('TopGenresForUser', [username])
        top_genres = [
            {'name': row[0]}
            for row in cursor.fetchall()
        ]

    with connection.cursor() as cursor:
        cursor.callproc('GetLikedMovies', [username])
        liked_movies = [
            {'id': row[0], 'title': row[1]}
            for row in cursor.fetchall()
        ]

    return render(request, 'user/user.html', {'user': user, 'top_genres': top_genres, 'liked_movies': liked_movies})