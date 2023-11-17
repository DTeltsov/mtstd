from drf_spectacular.utils import extend_schema_view
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView

from .models import Author, Album, Genre, Song
from .serializers import AuthorSerializer, AlbumSerializer, GenreSerializer, SongSerializer


@extend_schema_view()
class RetrieveAuthorsView(ListAPIView):
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()


@extend_schema_view()
class AuthorView(RetrieveUpdateDestroyAPIView):
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()


@extend_schema_view()
class AlbumView(RetrieveUpdateDestroyAPIView):
    serializer_class = AlbumSerializer
    queryset = Album.objects.prefetch_related('songs', 'authors', 'songs__genres').all()


@extend_schema_view()
class RetrieveAlbumsView(ListAPIView):
    serializer_class = AlbumSerializer
    queryset = Album.objects.prefetch_related('songs', 'authors', 'songs__genres').all()


@extend_schema_view()
class SongView(RetrieveUpdateDestroyAPIView):
    serializer_class = SongSerializer
    queryset = Song.objects.prefetch_related('genres').all()


@extend_schema_view()
class RetrieveSongsView(ListAPIView):
    serializer_class = SongSerializer
    queryset = Song.objects.prefetch_related('genres').all()


@extend_schema_view()
class GenreView(RetrieveUpdateDestroyAPIView):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()


@extend_schema_view()
class RetrieveGenresView(ListAPIView):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()