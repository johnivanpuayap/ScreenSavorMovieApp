from django.db import models


# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=100)


class Director(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)


class Cast(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)


class Movie(models.Model):
    title = models.CharField(max_length=100, primary_key=True)
    year_released = models.IntegerField()
    duration = models.IntegerField()
    description = models.TextField()
    genre = models.ManyToManyField(Genre)
    # The project assumes that a movie can only have one director
    director = models.ForeignKey(Director, on_delete=models.CASCADE)


class MovieCast(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    cast = models.ForeignKey(Cast, on_delete=models.CASCADE)
    role = models.CharField(max_length=100)

    class Meta:
        unique_together = ('movie', 'cast')
