from django.shortcuts import render
from django.views.generic.base import View
from .models import Movie


class HomeView(View):
    def get(self, request):
        movies = Movie.objects.all()

        context = {
            'movies': movies,
        }

        return render(request, "index.html", context)
