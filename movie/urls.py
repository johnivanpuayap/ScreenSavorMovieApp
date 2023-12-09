from django.urls import path
from .views import HomeView, AddMovieView
from . import views

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('<str:movie_id>', views.movie, name='movie'),
    path('add/', AddMovieView.as_view(), name='add_movie'),
    path('search/', views.search, name='search'),
]