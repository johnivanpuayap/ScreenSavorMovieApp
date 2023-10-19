from django.shortcuts import render, get_object_or_404
from django.views.generic.base import View
from django.db.models import Q
from .models import Movie, Genre


class HomeView(View):
    def get(self, request):
        # returns all the movies
        movies = Movie.objects.all()

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
        }

        return render(request, "index.html", context)


def movie(request, movie_title):
    try:
        movie_details = get_object_or_404(Movie, title=movie_title)

        context = {
            "movie": movie_details,
        }

        return render(request, "movie.html", context)
    except Movie.DoesNotExist:
        # Handle the case where the movie doesn't exist, e.g., redirect to an error page or display an error message.
        return render(request, "error.html", {"error_message": "Movie not found"})