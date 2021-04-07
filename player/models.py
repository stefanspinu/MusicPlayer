from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Album(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Song(models.Model):

    LANGUAGE_CHOICE = (
        ('EN', 'EN'),
        ('RU', 'RU'),
        ('RO', 'RO'),
        ('ES', 'ES')
    )

    name = models.CharField(max_length=100)
    album = models.ForeignKey(
        Album, on_delete=models.PROTECT, null=True, blank=True)
    language = models.CharField(
        max_length=25, choices=LANGUAGE_CHOICE, default='EN')
    song_img = models.FileField()
    year = models.IntegerField()
    singer = models.CharField(max_length=100)
    song_file = models.FileField()

    def __str__(self):
        return self.name


class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    song = models.ManyToManyField(Song, default=None, null=True)

    def __str__(self):
        return self.name


class Favourite(models.Model):
    #id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    is_fav = models.BooleanField(default=False)

    def __str__(self):
        return self.song.name


class Recent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)

    def __str__(self):
        return self.song.name
