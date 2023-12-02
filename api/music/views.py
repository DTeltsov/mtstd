from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter, OpenApiTypes
from rest_framework.generics import ListAPIView

from .models import Author, Album, Genre, Song
from .serializers import AuthorSerializer, AlbumSerializer, GenreSerializer, SongSerializer


@extend_schema_view(
    get=extend_schema(
        "Get list of artists or single artist",
        parameters=[
            OpenApiParameter(
                "name", OpenApiTypes.STR, OpenApiParameter.QUERY, description="Album title"
            )
        ]
    )
)
class AuthorView(ListAPIView):
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()

    def get(self, request, *args, **kwargs):
        if name := request.query_params.get('name', None):
            self.queryset = self.queryset.filter(name=name)
        return super().get(request, *args, **kwargs)


@extend_schema_view(
    get=extend_schema(
        "Get list of albums or single album",
        parameters=[
            OpenApiParameter(
                "title", OpenApiTypes.STR, OpenApiParameter.QUERY, description="Album title"
            ),
            OpenApiParameter(
                "song_title", OpenApiTypes.STR, OpenApiParameter.QUERY, description="Song title"
            ),
            OpenApiParameter(
                "artist_name", OpenApiTypes.STR, OpenApiParameter.QUERY, description="Artist name"
            ),
        ]
    )
)
class AlbumView(ListAPIView):
    serializer_class = AlbumSerializer
    queryset = Album.objects.prefetch_related('songs', 'authors', 'songs__genres').all()

    def get(self, request, *args, **kwargs):
        if title := request.query_params.get('title', None):
            self.queryset = self.queryset.filter(title=title)
        if song_title := request.query_params.get('song_title', None):
            self.queryset = self.queryset.filter(songs__title=song_title)
        if artist_name := request.query_params.get('artist_name', None):
            self.queryset = self.queryset.filter(authors__name=artist_name)
        return super().get(request, *args, **kwargs)


@extend_schema_view(
    get=extend_schema(
        "Get list of songs or single song",
        parameters=[
            OpenApiParameter(
                "title", OpenApiTypes.STR, OpenApiParameter.QUERY, description="Song title"
            ),
            OpenApiParameter(
                "genres", OpenApiTypes.STR, OpenApiParameter.QUERY, many=True, description="Song genres"
            ),
        ]
    )
)
class SongView(ListAPIView):
    serializer_class = SongSerializer
    queryset = Song.objects.prefetch_related('genres').all()

    def get(self, request, *args, **kwargs):
        if title := request.GET.get('title', None):
            self.queryset = self.queryset.filter(title=title)
        if genres := request.GET.get('genres', None):
            self.queryset = self.queryset.filter(genres__name__in=genres)
        return super().get(request, *args, **kwargs)


@extend_schema_view(
    get=extend_schema(
        "Get list of genres or single genre",
        parameters=[
            OpenApiParameter(
                "name", OpenApiTypes.STR, OpenApiParameter.QUERY, description="Genre name"
            )
        ]
    )
)
class GenreView(ListAPIView):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()