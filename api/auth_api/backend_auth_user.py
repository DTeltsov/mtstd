from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

UserModel = get_user_model()


class BackendAuth(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)

        user = UserModel._default_manager.get_by_natural_key(username)
        if user.check_password(password) and self.user_can_authenticate(user):
            return user