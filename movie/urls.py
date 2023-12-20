from django.urls import path
from .views import HomeView, AddMovieView, GetMovieView, SearchMovieView
from . import views

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('alltime/', views.getTopLiked, name='alltime'),
    path('<str:movie_id>', GetMovieView.as_view(), name='movie'),
    path('add/', AddMovieView.as_view(), name='add_movie'),
    path('search/', SearchMovieView.as_view(), name='search'),
    path('all/', views.MovieListView.as_view(), name='movies'),
    path('genre/<str:genre_name>', views.getMoviesByGenre, name='genre'),
    path('director/<str:director_name>', views.getMoviesByDirector, name='director'),
    path('cast/<str:cast_name>', views.getCastByDirector, name='cast')
]