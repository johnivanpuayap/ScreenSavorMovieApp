from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import View
from django.db.models import Q
from .models import Movie, Genre
from .forms import MovieForm


class HomeView(View):
    def get(self, request):
        # returns all the movies
        movies = Movie.objects.all()
        form = MovieForm()

        # # returns all the movies that contains with g
        # movies = Movie.objects.filter(
        #     Q(title__icontains='g')
        # )
        #
        # # returns all the movies that starts with g
        # # this is case-sensitive
        # movies = Movie.objects.filter(
        #     Q(title__startswith='G') |
        #     Q(title__startswith='T')
        # )

        context = {
            'movies': movies,
            'form': form,
        }

        return render(request, "index.html", context)


class AddMovieView(View):
    def get(self, request):
        form = MovieForm()
        return render(request, 'add_movie.html', {'form': form})

    def post(self, request):
        entry = MovieForm(request.POST)
        if entry.is_valid():
            entry.save()
            return redirect('home')


def movie(request, movie_title):
    try:
        movie_details = get_object_or_404(Movie, title=movie_title)
        context = {
            "movie": movie_details,
        }

        return render(request, "movie.html", context)
    except Movie.DoesNotExist:
        return render(request, "error.html", {"error_message": "Movie not found"})
