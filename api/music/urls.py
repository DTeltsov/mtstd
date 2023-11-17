from django.urls import path

from . import views

urlpatterns = [
    path('song/', views.SongView.as_view(), name='song'),
    path('songs/', views.RetrieveSongsView.as_view(), name='songs'),
    path('album/', views.AlbumView.as_view(), name='album'),
    path('albums/', views.RetrieveAlbumsView.as_view(), name='albums'),
    path('author/', views.AuthorView.as_view(), name='author'),
    path('authors/', views.RetrieveAuthorsView.as_view(), name='authors'),
    path('genre/', views.GenreView.as_view(), name='genres'),
    path('genres/', views.RetrieveGenresView.as_view(), name='genres'),
]