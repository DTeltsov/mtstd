from PyQt5.QtCore import QObject
from app.src.backend.integration import PropertyMeta, Property


class UserModel(QObject, metaclass=PropertyMeta):
    """
    Class representing the model associated with a user.

    Attributes:
    - first_name (str): First name of the user.
    - last_name (str): Last name of the user.
    - login (str): Login of the user.
    - subscription_active (bool): Indicates whether the user has an active subscription.

    Methods:
    - setup(data): Sets up the user model with the provided data.
    - reset(): Resets the user model attributes to their default values.

    Note: This class should be used with the PropertyMeta metaclass for automatic creation of Property attributes.
    """
    first_name = Property('')
    last_name = Property('')
    login = Property('')
    subscription_active = Property(False)

    def setup(self, data):
        """
        Sets up the user model with the provided data.

        Parameters:
        - data (dict): Data containing information about the user.

        Returns:
        None
        """
        self.login = data.get('login', '')
        self.first_name = data.get('first_name', '')
        self.last_name = data.get('last_name', '')
        if sub_model := data.get('subscription_model', {}):
            self.subscription_active = sub_model.get('active', False)
        else:
            self.subscription_active = False

    def reset(self):
        """
        Resets the user model attributes to their default values.

        Returns:
        None
        """
        self.first_name = ''
        self.last_name = ''
        self.login = ''
        self.subscription_active = False
