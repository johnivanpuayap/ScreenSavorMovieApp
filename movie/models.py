from django.db import models


# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']  # Change the ordering to last name and then first name


class Director(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return self.first_name + " " + self.last_name

    class Meta:
        unique_together = ('first_name', 'last_name')  # Make sure that there are no duplicate directors


class Cast(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return self.first_name + " " + self.last_name

    class Meta:
        unique_together = ('first_name', 'last_name')  # Make sure that there are no duplicate actors


class Movie(models.Model):
    title = models.CharField(max_length=100)
    year_released = models.IntegerField()
    duration = models.IntegerField()
    description = models.TextField()
    genre = models.ManyToManyField(Genre)
    # The project assumes that a movie can only have one director
    director = models.ForeignKey(Director, on_delete=models.CASCADE)
    actors = models.ManyToManyField(Cast, through='Role')
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


class Role(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    cast = models.ForeignKey(Cast, on_delete=models.CASCADE)
    role = models.CharField(max_length=100)

    def __str__(self):
        return self.movie.__str__() + " as " + self.role

    class Meta:
        unique_together = ('movie', 'cast')