from django.db import models
from movie.models import Movie
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(max_length=32, null=False, primary_key=True)
    first_name = models.CharField(max_length=128, null=False)
    last_name = models.CharField(max_length=128, null=False)

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    date_liked = models.DateField(auto_now_add=True)

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following_set')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers_set')
    follow_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f"{self.follower} follows {self.following}"


class WatchList(models.Model):
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, null=False, on_delete=models.CASCADE)


class WatchHistory(models.Model):
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, null=False, on_delete=models.CASCADE)
    date = models.DateField(null=False)
