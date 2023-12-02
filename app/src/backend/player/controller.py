from itertools import cycle

from PyQt5.QtCore import QObject, pyqtSignal, pyqtProperty, QDateTime
from PyQt5.QtMultimedia import QMediaPlayer, QMediaPlaylist
from qasync import asyncSlot

from app.logger import logger
from app.src.backend.integration import Property, PropertyMeta
from app.src.backend.library import Song


class Player(QObject, metaclass=PropertyMeta):
    """
    Class representing a music player.

    Attributes:
    - song (Song): Current song being played.
    - player (QMediaPlayer): Media player instance for playing audio.
    - playlist (QMediaPlaylist): Media playlist instance for managing the playlist.

    Methods:
    - set_song(song): Sets the current song and adds it to the playlist.
    - play(): Plays the current song.
    - stop(): Stops the currently playing song.

    Note: This class should be used with the PropertyMeta metaclass for automatic creation of Property attributes.
    """
    songChanged = pyqtSignal()
    song = pyqtProperty(QObject, fget=lambda self: self._song, notify=songChanged)
    player_state = Property(QMediaPlayer.PausedState)
    current_time = Property('0.00')
    remaining_time = Property('0.00')
    repeat_mode = Property(QMediaPlaylist.Sequential)
    position = Property(0)
    start = Property(0)
    end = Property(0)

    def __init__(self):
        super().__init__()
        self._song = Song({'title': 'this_song_is_empty'}, '', '')
        self.player = QMediaPlayer()
        self.playlist = QMediaPlaylist()
        self.player.setPlaylist(self.playlist)
        self.repeat_modes = (
            x for x in cycle([QMediaPlaylist.Sequential, QMediaPlaylist.Loop, QMediaPlaylist.CurrentItemInLoop])
        )
        self.connect_signals()
        self.change_repeat_mode()

    def connect_signals(self):
        self.player.positionChanged.connect(self.update_current_time)
        self.player.durationChanged.connect(self.update_remaining_time)
        self.player.stateChanged.connect(self.update_player_state)
        self.player.error.connect(self.handle_error)

    @song.setter
    def song(self, song):
        self._song = song
        self.songChanged.emit()

    def handle_error(self):
        logger.error(
            f'Current song: {self.song.title}, player state: {self.player.state()}, '
            f'error: {self.player.errorString()}'
        )

    def update_remaining_time(self, duration):
        self.remaining_time = QDateTime.fromMSecsSinceEpoch(duration).toString("mm:ss")
        self.end = duration

    def update_current_time(self, position):
        self.current_time = QDateTime.fromMSecsSinceEpoch(position).toString("mm:ss")
        self.position = position

    def update_player_state(self, state):
        self.player_state = state

    def clear_playlist_and_add_song(self, media_content):
        self.playlist.clear()
        self.playlist.addMedia(media_content)

    @asyncSlot(name='play')
    async def play(self):
        """
        Plays the current song.

        Returns:
        None
        """
        self.player.play()

    @asyncSlot(name='next')
    async def next(self):
        self.playlist.next()

    @asyncSlot(name='previous')
    async def previous(self):
        self.playlist.previous()

    @asyncSlot(name='pause')
    async def pause(self):
        """
        Stops the currently playing song.

        Returns:
        None
        """
        self.player.pause()

    @asyncSlot(int, name='move')
    async def move(self, value):
        self.player.setPosition(value)

    @asyncSlot(name='changeRepeatMode')
    async def change_repeat_mode(self):
        self.playlist.setPlaybackMode(next(self.repeat_modes))
        self.repeat_mode = self.playlist.playbackMode()

    def playlist_append_song(self, media_content):
        self.playlist.insertMedia(-1, media_content)

    def playlist_insert_song(self, media_content):
        self.playlist.insertMedia(0, media_content)
