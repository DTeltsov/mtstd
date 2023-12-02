from rest_framework import serializers
from .models import Author, Album, Genre, Song


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"


class SongAlbumSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True)

    class Meta:
        model = Album
        fields = ('title', 'authors')


class SongSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True)
    albums = SongAlbumSerializer(many=True)

    class Meta:
        model = Song
        fields = "__all__"


class AlbumSerializer(serializers.ModelSerializer):
    songs = SongSerializer(many=True)
    authors = AuthorSerializer(many=True)

    class Meta:
        model = Album
        fields = "__all__"
