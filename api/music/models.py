import os
from django.db import models
from storages.backends.s3boto3 import S3Boto3Storage
from django.core.validators import FileExtensionValidator


class Author(models.Model):
    name = models.CharField(max_length=254, unique=True)

    class Meta:
        db_table = 'author'

    def __str__(self):
        return self.name


def song_upload_path(instance, filename):
    return os.path.join('song_file', filename)


def pic_upload_path(instance, filename):
    return os.path.join('song_cover', filename)


class Genre(models.Model):
    name = models.CharField(max_length=254, unique=True)

    class Meta:
        db_table = 'genre'

    def __str__(self):
        return self.name


class Song(models.Model):
    title = models.CharField(max_length=254)
    length = models.FloatField()
    cover = models.FileField(
        storage=S3Boto3Storage, upload_to=song_upload_path,
        blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg'])]
    )
    file = models.FileField(
        storage=S3Boto3Storage, upload_to=song_upload_path,
        blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=['mp3', 'flac', 'wav'])]
    )
    genres = models.ManyToManyField(Genre, related_name='songs', related_query_name='song')

    class Meta:
        db_table = 'song'

    def __str__(self):
        return f'{self.title} - {self.length}'


class Album(models.Model):
    title = models.CharField(max_length=254)
    songs = models.ManyToManyField(Song, related_name='albums', related_query_name='album')
    authors = models.ManyToManyField(Author, related_name='albums', related_query_name='album')

    class Meta:
        db_table = 'album'

    def __str__(self):
        return f'{self.title}'
