import os
from io import BytesIO

from PyQt5.QtCore import QObject, QUrl
from PyQt5.QtMultimedia import QMediaContent
from pydub import AudioSegment

from app.src.backend.integration import Property, PropertyMeta


class Song(QObject, metaclass=PropertyMeta):
    """
    Class representing a music song.

    Attributes:
    - file (str): File path of the song.
    - cover (str): Cover image path of the song.
    - length (float): Length of the song in seconds.
    - title (str): Title of the song.
    - album (str): Album to which the song belongs.
    - artist (str): Artist of the song.

    Methods:
    - __init__(song_data, album, artist): Initializes a new Song instance with the provided song data, album, and artist.

    Note: This class should be used with the PropertyMeta metaclass for automatic creation of Property attributes.
    """
    file_url = Property('')
    cover = Property('')
    length = Property(0.0)
    title = Property('')
    album = Property('')
    artist = Property('')

    def __init__(self, song_data, album, artist):
        """
        Initializes a new Song instance with the provided song data, album, and artist.

        Parameters:
        - song_data (dict): Data containing information about the song.
        - album (str): Album to which the song belongs.
        - artist (str): Artist of the song.

        Returns:
        None
        """
        super().__init__()
        self.file_url = song_data.get('file', '').replace('localstack', 'localhost')
        self.cover = song_data.get('cover', '').replace('localstack', 'localhost')
        self.length = song_data.get('length', 0.0)
        self.title = song_data.get('title', '')
        self.album = album or ''
        self.artist = artist or ''
        self.media_content = ''

    def set_media_content(self, song_bytes_file):
        audio_segment = AudioSegment.from_file(BytesIO(song_bytes_file))
        dir_path = f"{os.getcwd()}/files"
        os.makedirs(dir_path, exist_ok=True)
        file_path = os.path.join(dir_path, f"{self.title.replace(' ', '_')}.wav")
        audio_segment.export(file_path, "wav")
        self.media_content = QMediaContent(QUrl.fromLocalFile(file_path))

