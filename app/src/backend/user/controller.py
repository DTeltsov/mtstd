from PyQt5.QtCore import QObject, pyqtProperty, pyqtSignal
from app.src.backend.integration import PropertyMeta
from app.src.localization import translate
from .model import UserModel


class User(QObject, metaclass=PropertyMeta):
    """
    Class representing a user.

    Attributes:
    - model (UserModel): Model associated with the user.
    - signalSuccessLogin (pyqtSignal): Signal emitted upon successful user login.
    - signalError (pyqtSignal): Signal emitted upon login error.

    Methods:
    - __init__(): Initializes a new User instance.
    - login(login, password, login_coro, token): Attempts to log in the user with the provided credentials.
    - logout(): Logs out the user.

    Note: This class should be used with the PropertyMeta metaclass for automatic creation of Property attributes.
    """
    model = pyqtProperty(UserModel, fget=lambda self: self._model)
    signalSuccessLogin = pyqtSignal(list)
    signalError = pyqtSignal(str)

    def __init__(self):
        """
        Initializes a new User instance.

        Returns:
        None
        """
        super().__init__()
        self._model = UserModel()

    async def login(self, login, password, login_coro, token):
        """
        Attempts to log in the user with the provided credentials.

        Parameters:
        - login (str): User login.
        - password (str): User password.
        - login_coro (coroutine): Coroutine function for user login.
        - token (str): User token.

        Returns:
        None
        """
        if (not login or not password) and not token:
            self.signalError.emit(translate('login_errors', 'no_login_or_pass'))
            return

        if not (data := await login_coro({'username': login, 'password': password, 'token': token})):
            self.signalError.emit(translate('login_errors', 'invalid_login_or_pass'))
            return

        self.model.setup(data.get('user_data'))
        self.signalSuccessLogin.emit(data.get('user_data', {}).get('songs', []))

    async def logout(self):
        """
        Logs out the user.

        Returns:
        None
        """
        self.model.reset()
