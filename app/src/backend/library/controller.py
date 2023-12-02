from PyQt5.QtCore import QObject, pyqtProperty, pyqtSignal

from app.src.backend.integration import PropertyMeta, Property
from .album import Album
from .song import Song


class Library(QObject, metaclass=PropertyMeta):
    """
    Class representing a music library.

    Attributes:
    - albums (list): List of albums in the library.
    - artists (list): List of artists in the library.

    Methods:
    - setup(songs): Sets up the library by processing a list of songs and organizing them into albums.

    Note: This class should be used with the PropertyMeta metaclass for automatic creation of Property attributes.
    """
    albums = Property([])
    artists = Property([])
    signalDisplayAlbumChanged = pyqtSignal()
    displayAlbum = pyqtProperty(QObject, fget=lambda self: self._display_album, notify=signalDisplayAlbumChanged)

    def __init__(self):
        super().__init__()
        self._display_album = Album({})

    def set_display_album(self, album_name):
        if album := self.get_album_by_name(album_name):
            self._display_album = album
            self.signalDisplayAlbumChanged.emit()

    @property
    def songs(self):
        return [song for album in self.albums for song in album.songs]

    def setup(self, songs):
        """
        Sets up the library by processing a list of songs and organizing them into albums.

        Parameters:
        - songs (list): List of songs to be added to the library.

        Returns:
        None
        """
        for song in songs:
            album_data = next((album for album in song.get('albums', [])), {})
            artist = next((author for author in album_data.get('authors', [])), {})
            song = Song(song, album_data.get('title'), artist.get('name'))
            if album := next((album for album in self.albums if album.title == album_data.get('title')), None):
                album.songs.append(song)
            else:
                album = Album(album_data)
                album.songs.append(song)
                self.albums.append(album)
        for album in self.albums:
            album.choose_cover_and_artist()

    def get_song_by_name(self, song_name):
        return next((song for song in self.songs if song.title == song_name), None)

    def get_album_by_name(self, album_name):
        return next((album for album in self.albums if album.title == album_name), None)