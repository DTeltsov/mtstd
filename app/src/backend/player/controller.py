from PyQt5.QtCore import QObject
from app.src.backend.integration import Property, PropertyMeta
from qasync import asyncSlot
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent


class Player(QObject, metaclass=PropertyMeta):
    song = Property('')
    player = QMediaPlayer()

    @asyncSlot(name='setSong')
    def set_song(self):
        pass
        # file_dialog = QFileDialog()
        # song_path, _ = file_dialog.getOpenFileName(self, 'Open Song', '', 'Audio Files (*.mp3 *.ogg *.wav)')
        # if song_path:
        #     song_content = QMediaContent.fromUrl(song_path)
        #     self.media_player.setMedia(song_content)
        #     self.song_label.setText(f'Now playing: {song_path}')
