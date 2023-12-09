from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import View
from django.db.models import Q
from .models import Movie, Genre
from .forms import MovieForm
from django.db import connection
from django.shortcuts import render, get_object_or_404
class HomeView(View):
    def get(self, request):
        with connection.cursor() as cursor:
            cursor.callproc("GetAllMovies")
            movies = cursor.fetchall()

        # Convert tuples to dictionaries
        movies_list = []
        for movie_tuple in movies:
            movie_dict = {
                'id': movie_tuple[0],
                'title': movie_tuple[1],  # Change this to 'title'
                'year_released': movie_tuple[2],  # Optionally, change this to 'year_released'
                'description': movie_tuple[4],  # Change this to 'description'
                'average_rating': float(movie_tuple[6]),  # Change this to 'average_rating'
                'genres': movie_tuple[7].split(',') if movie_tuple[7] else [],  # Change this to 'genres'
            }
            movies_list.append(movie_dict)

        context = {
            'movies': movies_list,
        }

        return render(request, "index.html", context)

class AddMovieView(View):
    def get(self, request):
        form = MovieForm()
        return render(request, 'add_movie.html', {'form': form})

    def post(self, request):
        form = MovieForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')


def movie(request, movie_id):
    try:
        with connection.cursor() as cursor:
            cursor.execute("CALL GetMovieDetails(%s)", [movie_id])
            movie_details = cursor.fetchall()

            cursor.nextset()
            genres = cursor.fetchall()

            cursor.nextset()
            cast_details = cursor.fetchall()

            cursor.nextset()
            reviews = cursor.fetchall()

            cursor.nextset()
            average_rating = cursor.fetchall()

            cursor.nextset()
            collections = cursor.fetchall()

        print(average_rating)

        context = {
            "movie": {
                "title": movie_details[0][0],
                "year_released": movie_details[0][1],
                "duration": movie_details[0][2],
                "description": movie_details[0][3],
                "director": movie_details[0][4],
            } if movie_details else None,
            "genres": [genre[0] for genre in genres],
            "cast_details": [{"name": cast[0], "role": cast[1]} for cast in cast_details],
            "reviews": [{"username": review[0], "rating": review[1], "description": review[2]} for review in reviews] if reviews and reviews[0][0] != 'No reviews found.' else None,
            "average_rating": average_rating[0][0] if average_rating else 0,
            "collections": [{"name": collection[0], "user": collection[1]} for collection in collections] if collections and collections[0][0] != 'No collections found.' else None,
        }

        return render(request, "movie.html", context)
    except Movie.DoesNotExist:
        return render(request, "error.html", {"error_message": "Movie not found"})