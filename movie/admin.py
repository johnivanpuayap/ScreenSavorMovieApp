from django.contrib import admin
from .models import Genre, Cast, Director, Movie, MovieCast

admin.site.register(Genre)
admin.site.register(Cast)
admin.site.register(Director)
admin.site.register(Movie)
admin.site.register(MovieCast)
