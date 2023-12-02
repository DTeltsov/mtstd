from collections import Counter

from PyQt5.QtCore import QObject

from app.src.backend.integration import Property, PropertyMeta


class Album(QObject, metaclass=PropertyMeta):
    """
    Class representing an album.

    Attributes:
    - songs (list): List of songs associated with the album.
    - cover (str): Cover image path of the album.
    - title (str): Title of the album.
    - artist (str): Artist of the album.

    Methods:
    - __init__(data): Initializes a new Album instance with the provided data.
    - choose_cover_and_artist(): Chooses the most common cover and artist based on the associated songs.

    Note: This class should be used with the PropertyMeta metaclass for automatic creation of Property attributes.
    """
    songs = Property([])
    cover = Property('')
    title = Property('')
    artist = Property('')

    def __init__(self, data):
        """
        Initializes a new Album instance with the provided data.

        Parameters:
        - data (dict): Data containing information about the album.

        Returns:
        None
        """
        super().__init__()
        self.title = data.get('title')

    def choose_cover_and_artist(self):
        """
        Chooses the most common cover and artist based on the associated songs.

        Returns:
        None
        """
        self.cover = Counter([song.cover for song in self.songs]).most_common(1)[0][0]
        self.artist = Counter([song.artist for song in self.songs]).most_common(1)[0][0]
