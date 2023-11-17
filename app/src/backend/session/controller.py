from PyQt5.QtCore import QObject, pyqtProperty, pyqtSignal
from qasync import asyncSlot

from app.logger import logger
from app.src.backend.database import Database
from app.src.backend.integration import PropertyMeta
from app.src.backend.player import Player
from app.src.backend.user import User


class Session(QObject, metaclass=PropertyMeta):
    signalError = pyqtSignal(str)
    user = pyqtProperty(QObject, fget=lambda self: self._user, constant=True)

    def __init__(self):
        super().__init__()
        self._user = User()
        self.player = Player()
        self.database = Database()

    def _connect_signals(self):
        self._user.signalSuccessLogin.connect(self.load_songs_info)
        self._user.signalError.connect(self.signalError)

    @asyncSlot(str, str)
    async def login(self, login, password):
        await self.user.login(login, password, self.database.login)

    @asyncSlot()
    async def logout(self):
        self.user.logout()
        self.database.reset()

    async def load_songs_info(self):
        pass

