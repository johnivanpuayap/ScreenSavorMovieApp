from django.shortcuts import render
from django.views.generic.base import View
from django.db.models import Q
from .models import Movie


class HomeView(View):
    def get(self, request):
        # returns all the movies
        movies = Movie.objects.all()

        # returns all the movies that start with G
        movies = Movie.objects.filter(
            Q(title__icontains='g')
        )

        context = {
            'movies': movies,
        }

        return render(request, "index.html", context)


def movie(request, movie_title):

    movie = Movie.objects.get(title=movie_title)

    context = {
        "movie": movie
    }

    return render(request, "movie.html", context)
