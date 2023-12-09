from django.db import models
from user.models import User
from movie.models import Movie


# Create your models here.
class Collection(models.Model):
    name = models.CharField(max_length=250, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movies = models.ManyToManyField(Movie)