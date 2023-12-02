from django.urls import path

from . import views

urlpatterns = [
    path('song/', views.SongView.as_view(), name='song'),
    path('album/', views.AlbumView.as_view(), name='album'),
    path('author/', views.AuthorView.as_view(), name='author'),
    path('genre/', views.GenreView.as_view(), name='genres'),
]