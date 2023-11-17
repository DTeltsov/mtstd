from PyQt5.QtCore import QObject

from app.src.backend.integration import PropertyMeta, Property


class UserModel(QObject, metaclass=PropertyMeta):
    first_name = Property('')
    last_name = Property('')
    login = Property('')
    subscription_active = Property(False)

    def setup(self, data):
        self.login = data.get('login')
        self.first_name = data.get('first_name')
        self.last_name = data.get('last_name')
        self.subscription_active = data.get('subscription_active')

    def reset(self):
        self.first_name = ''
        self.last_name = ''
        self.login = ''
        self.subscription_active = False
