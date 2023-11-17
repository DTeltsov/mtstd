from PyQt5.QtCore import QObject, pyqtProperty, pyqtSignal

from app.src.backend.integration import PropertyMeta
from app.src.localization import translate
from .model import UserModel


class User(QObject, metaclass=PropertyMeta):
    model = pyqtProperty(UserModel, fget=lambda self: self._model)
    signalSuccessLogin = pyqtSignal(int)
    signalError = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._model = UserModel()

    async def login(self, login, password, login_coro):
        if not login or not password:
            self.signalError.emit(translate('login_errors', 'no_login_or_pass'))
            return

        if not (data := await login_coro({'login': login, 'password': password})):
            self.signalError.emit(translate('login_errors', 'invalid_login_or_pass'))
            return

        self.model.setup(data)
        self.signalSuccessLogin.emit()

    async def logout(self):
        self.model.reset()
