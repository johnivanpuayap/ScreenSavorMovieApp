from django.db import models
from movie.models import Movie
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(max_length=128, null=False)
    firstname = models.CharField(max_length=128, null=False)
    lastname = models.CharField(max_length=128, null=False)


class Follows(models.Model):
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
    watchHistory_id = models.IntegerField(primary_key=True, null=False)
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, null=False, on_delete=models.CASCADE)
    date = models.DateField(null=False)
