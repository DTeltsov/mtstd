from PyQt5.QtCore import QObject, pyqtProperty, pyqtSignal, QSettings, pyqtSlot
from qasync import asyncSlot

from app.src.backend.database import Database
from app.src.backend.integration import PropertyMeta
from app.src.backend.library import Library
from app.src.backend.player import Player
from app.src.backend.user import User


class Session(QObject, metaclass=PropertyMeta):
    """
    The `Session` class manages user sessions, login/logout, and library setup.

    Attributes:
    - signalError (pyqtSignal): Signal emitted in case of an error with the error message as the argument.
    - signalStartSession (pyqtSignal): Signal emitted when starting a new session.
    - user (pyqtProperty): Property representing the user, with read-only access.
    - library (pyqtProperty): Property representing the library, with read-only access.

    Methods:
    - __init__(): Constructor to initialize the `Session` object.
    - _connect_signals(): Connects signals between the user and the session.
    - login(login: str, password: str, token: str = '') -> None: Asynchronously logs in the user.
    - logout() -> None: Asynchronously logs out the user.
    - setup_library(songs: list) -> None: Asynchronously sets up the library with the given songs.
    - memorize_session() -> None: Memorizes the current session by storing the token in settings.
    - check_q_settings() -> None: Checks the settings for an existing token and logs in if found.
    """

    signalError = pyqtSignal(str)
    signalStartSession = pyqtSignal()
    user = pyqtProperty(QObject, fget=lambda self: self._user, constant=True)
    library = pyqtProperty(QObject, fget=lambda self: self._library, constant=True)
    player = pyqtProperty(QObject, fget=lambda self: self._player, constant=True)

    def __init__(self):
        """
        Initializes a new `Session` object.

        This constructor creates instances of the User, Player, Database, and Library classes.
        It also connects signals and performs the initial check for stored settings.
        """
        super().__init__()
        self._user = User()
        self._player = Player()
        self.database = Database()
        self._library = Library()
        self.q_settings = QSettings()
        self._connect_signals()
        self.check_q_settings()

    def _connect_signals(self):
        """
        Connects signals between the user and the session.

        Signals Connected:
        - signalSuccessLogin: Connected to the setup_library method.
        - signalError: Connected to the signalError signal of the session.
        """
        self._user.signalSuccessLogin.connect(self.setup_library)
        self._user.signalError.connect(self.signalError)
        self.player.player.currentMediaChanged.connect(self.change_current_song)

    @asyncSlot(str, str, str)
    async def login(self, login, password, token=''):
        """
        Asynchronously logs in the user.

        Parameters:
        - login (str): The user's login.
        - password (str): The user's password.
        - token (str): Optional token for authentication.

        Returns:
        None
        """
        await self.user.login(login, password, self.database.login, token)

    @asyncSlot()
    async def logout(self):
        """
        Asynchronously logs out the user.

        Returns:
        None
        """
        self.user.logout()
        self.database.reset()
        self.q_settings.remove('token')
        self.q_settings.sync()

    @asyncSlot(list)
    async def setup_library(self, songs):
        """
        Asynchronously sets up the library with the given songs.

        Parameters:
        - songs (list): List of songs to set up the library.

        Returns:
        None
        """
        self.memorize_session()
        self.library.setup(songs)
        self.signalStartSession.emit()

    def memorize_session(self):
        """
        Memorizes the current session by storing the token in settings.

        Returns:
        None
        """
        self.q_settings.setValue('token', self.database.token)
        self.q_settings.sync()

    def check_q_settings(self):
        """
        Checks the settings for an existing token and logs in if found.

        Returns:
        None
        """
        if self.q_settings.contains('token'):
            self.login('', '', self.q_settings.value('token', ''))

    async def load_song_media(self, song):
        song_bytes_file = await self.database.download_audio(song.file_url)
        song.set_media_content(song_bytes_file)

    @pyqtSlot(str, name='showAlbum')
    def show_album(self, album_name):
        self.library.set_display_album(album_name)

    @asyncSlot(str)
    async def play(self, song_name):
        if song := self.library.get_song_by_name(song_name):
            if not song.media_content:
                await self.load_song_media(song)
            self.player.clear_playlist_and_add_song(song.media_content)
            self.player.play()

    @asyncSlot(str, name='playNext')
    async def play_next(self, song_name):
        if song := self.library.get_song_by_name(song_name):
            if not song.media_content:
                await self.load_song_media(song)
            self.player.playlist_insert_song(song.media_content)

    @asyncSlot(str, name='playLater')
    async def play_later(self, song_name):
        if song := self.library.get_song_by_name(song_name):
            if not song.media_content:
                await self.load_song_media(song)
            self.player.playlist_append_song(song.media_content)

    def change_current_song(self, media_content):
        if song := next((song for song in self.library.songs if song.media_content == media_content), None):
            self.player.song = song
